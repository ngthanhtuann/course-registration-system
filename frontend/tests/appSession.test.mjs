import assert from "node:assert/strict"
import { readFile } from "node:fs/promises"
import { beforeEach, test } from "node:test"
import ts from "typescript"

// Exercise App's initial element tree and background effect with controlled
// hooks/API promises, without a browser, server or authentication credentials.
const fixture = {
  state: undefined, effect: undefined, stored: null, token: null,
  useState(initial) {
    fixture.state = typeof initial === "function" ? initial() : initial
    return [fixture.state, (next) => {
      fixture.state = typeof next === "function" ? next(fixture.state) : next
    }]
  },
  useEffect(effect) { fixture.effect = effect },
  getStoredUser() { return fixture.stored },
  clearAuth() { fixture.token = null; fixture.stored = null },
  saveAuth(token, user) { fixture.token = token; fixture.stored = user },
  ApiError: class extends Error {
    constructor(status) { super("API failure"); this.status = status }
  },
  api: { me: null, student: { profile: null }, lecturer: { profile: null } },
}
globalThis.__appSessionTest = fixture
globalThis.localStorage = { getItem: () => fixture.token }
let source = await readFile(new URL("../src/App.tsx", import.meta.url), "utf8")
source = source.replace(/^import (.+) from .+$/gm, (_line, names) => {
  if (names.startsWith("type ")) return ""
  if (names.startsWith("React,")) return `
    const React = { createElement: (type, props, ...children) => ({ type, props: { ...props, children } }) };
    const { useState, useEffect } = globalThis.__appSessionTest;
    const lazy = () => () => null;
    const Suspense = "Suspense";`
  if (names.includes("clearAuth")) return `const ${names} = globalThis.__appSessionTest;`
  if (names.startsWith("{")) return names.replace(/[{}]/g, "").split(",")
    .map((name) => `const ${name.trim()} = ${JSON.stringify(name.trim())};`).join("\n")
  return `const ${names} = () => null;`
})
const compiled = ts.transpileModule(source, {
  compilerOptions: { target: ts.ScriptTarget.ES2020, module: ts.ModuleKind.ESNext, jsx: ts.JsxEmit.React },
}).outputText
const { default: App } = await import(`data:text/javascript;base64,${Buffer.from(compiled).toString("base64")}`)
const deferred = () => {
  let resolve, reject
  const promise = new Promise((yes, no) => { resolve = yes; reject = no })
  return { promise, resolve, reject }
}
const flush = () => new Promise((resolve) => setImmediate(resolve))
const cached = (role = "admin") => ({
  id: "example", username: "example", fullName: "Cached name", email: "example@test.invalid",
  role, status: "Active", ...(role === "student" ? { studentId: "s1", major: "CS" } :
    role === "lecturer" ? { lecturerId: "l1", qualifications: ["CS101"] } : {}),
})
const base = (role = "admin") => ({ user_id: "example", username: "example",
  fullname: "Fresh name", email: "example@test.invalid", role, active_status: true })

test("logout clears the session even when the backend request fails", async () => {
  let sentToken
  fixture.api.logout = async () => {
    sentToken = fixture.token
    throw new Error("Network unavailable")
  }
  const tree = App()
  const routes = tree.props.children[0].props.children
  const adminRoute = routes.find((route) => route.props.path === "/admin/*")
  adminRoute.props.element.props.onLogout()
  await flush()
  assert.equal(sentToken, "session")
  assert.equal(fixture.token, null)
  assert.equal(fixture.state, null)
})
beforeEach(() => {
  fixture.token = "session"
  fixture.stored = cached()
  fixture.api.me = async () => base()
  fixture.api.student.profile = async () => ({ student_id: "s1", major_code: "NEW" })
  fixture.api.lecturer.profile = async () => ({ lecturer_id: "l1", qualifications: ["NEW"] })
})

test("initial router renders cached users for all roles before session validation starts", () => {
  let calls = 0
  fixture.api.me = () => { calls++; return new Promise(() => {}) }
  for (const role of ["admin", "student", "lecturer"]) {
    fixture.stored = cached(role)
    const tree = App()
    assert.equal(tree.type, "BrowserRouter")
    assert.equal(fixture.state, fixture.stored)
    assert.equal(calls, 0)
    const routes = tree.props.children[0].props.children
    assert.equal(routes[0].props.element.props.to, `/${role}/dashboard`)
  }
})

test("successful background validation publishes refreshed identity without clearing the UI", async () => {
  const response = deferred()
  fixture.api.me = () => response.promise
  App()
  fixture.effect()
  assert.equal(fixture.state.fullName, "Cached name")
  response.resolve(base())
  await flush()
  assert.equal(fixture.state.fullName, "Fresh name")
  assert.equal(fixture.token, "session")
})

test("student/lecturer profile refresh does not delay cached UI or validated identity", async () => {
  for (const role of ["student", "lecturer"]) {
    const profile = deferred()
    fixture.stored = cached(role)
    fixture.api.me = async () => base(role)
    fixture.api[role].profile = () => profile.promise
    App()
    const cleanup = fixture.effect()
    await flush()
    assert.equal(fixture.state.fullName, "Fresh name")
    assert.equal(fixture.state.role, role)
    if (role === "student") assert.equal(fixture.state.major, "CS")
    else assert.deepEqual(fixture.state.qualifications, ["CS101"])
    cleanup()
    profile.resolve({})
    await flush()
  }
})

test("401, 403 and invalid session responses clear auth", async () => {
  for (const result of [401, 403, null, { ...base(), role: "unknown" }, { ...base(), active_status: false }]) {
    fixture.token = "session"
    fixture.stored = cached()
    fixture.api.me = async () => {
      if (typeof result === "number") throw new fixture.ApiError(result)
      return result
    }
    App()
    fixture.effect()
    await flush()
    assert.equal(fixture.state, null)
    assert.equal(fixture.token, null)
    assert.equal(fixture.stored, null)
  }
})

test("network and server failures preserve cached UI", async () => {
  for (const status of [0, 500, 503]) {
    fixture.api.me = async () => { throw new fixture.ApiError(status) }
    App()
    fixture.effect()
    await flush()
    assert.equal(fixture.state.fullName, "Cached name")
    assert.equal(fixture.token, "session")
  }
})

test("late validation cannot restore a logged-out session or overwrite a newer login", async () => {
  for (const nextToken of [null, "new-session"]) {
    fixture.token = "session"
    fixture.stored = cached()
    const response = deferred()
    fixture.api.me = () => response.promise
    App()
    fixture.effect()
    fixture.token = nextToken
    fixture.stored = nextToken ? { ...cached(), id: "new-user" } : null
    fixture.state = fixture.stored
    response.resolve(base())
    await flush()
    assert.equal(fixture.token, nextToken)
    assert.equal(fixture.state?.id ?? null, nextToken ? "new-user" : null)
  }
})

test("missing token and malformed cached user render unauthenticated immediately", () => {
  fixture.token = null
  assert.equal(App().type, "BrowserRouter")
  assert.equal(fixture.state, null)
  fixture.token = "session"
  fixture.stored = { role: "unexpected" }
  App()
  assert.equal(fixture.state, null)
})

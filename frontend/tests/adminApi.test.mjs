import assert from "node:assert/strict"
import { readFile } from "node:fs/promises"
import { beforeEach, test } from "node:test"
import ts from "typescript"
import { clearAdminCache, getAdminSnapshot, loadAdminList } from "../src/services/adminCache.ts"

// Compile only the API module with the project's existing TypeScript compiler.
// Browser APIs and HTTP responses are fakes; no server or credentials are used.
globalThis.window = new EventTarget()
const storage = new Map()
globalThis.localStorage = {
  getItem: (key) => storage.get(key) ?? null,
  setItem: (key, value) => storage.set(key, value),
  removeItem: (key) => storage.delete(key),
}
const source = (await readFile(new URL("../src/services/api.ts", import.meta.url), "utf8"))
  .replace('"./adminCache"', JSON.stringify(new URL("../src/services/adminCache.ts", import.meta.url).href))
  .replaceAll("import.meta.env", "({})")
const compiled = ts.transpileModule(source, {
  compilerOptions: { target: ts.ScriptTarget.ES2020, module: ts.ModuleKind.ESNext },
}).outputText
const { api, saveAuth, clearAuth } = await import(`data:text/javascript;base64,${Buffer.from(compiled).toString("base64")}`)
const json = (body, status = 200) => new Response(JSON.stringify(body), { status })

beforeEach(() => {
  storage.clear()
  clearAdminCache()
  saveAuth("test-session", { role: "admin" })
})

test("all user, course, major and qualification mutations invalidate affected lists", async (t) => {
  t.mock.method(globalThis, "fetch", async () => json({ message: "success" }))
  const cases = [
    [() => api.admin.createUser({}), ["users"]],
    [() => api.admin.updateUser("id", {}), ["users"]],
    [() => api.admin.deactivateUser("id"), ["users"]],
    [() => api.admin.createCourse({}), ["courses"]],
    [() => api.admin.updateCourse("code", {}), ["courses"]],
    [() => api.admin.deleteCourse("code"), ["courses"]],
    [() => api.admin.createMajor({}), ["majors"]],
    [() => api.admin.updateMajor("code", {}), ["majors"]],
    [() => api.admin.deleteMajor("code"), ["majors"]],
    [() => api.admin.addQualification("id", "code"), ["users"]],
    [() => api.admin.removeQualification("id", "code"), ["users"]],
    [() => api.updateProfile("name", "email"), ["users"]],
  ]
  for (const [mutate, affected] of cases) {
    for (const key of ["users", "courses", "majors"]) await loadAdminList(key, async () => [key])
    await mutate()
    for (const key of ["users", "courses", "majors"]) {
      assert.deepEqual(getAdminSnapshot(key).data, affected.includes(key) ? undefined : [key])
    }
  }
})

test("failed CRUD preserves cached rows", async (t) => {
  await loadAdminList("courses", async () => ["existing"])
  t.mock.method(globalThis, "fetch", async () => json({ error: "conflict" }, 409))
  await assert.rejects(api.admin.deleteCourse("code"), /conflict/)
  assert.deepEqual(getAdminSnapshot("courses").data, ["existing"])
})

test("API list calls share HTTP requests and preserve authorization", async (t) => {
  const fetch = t.mock.method(globalThis, "fetch", async (_url, options) => {
    assert.equal(options.headers.get("Authorization"), "Bearer test-session")
    return json([{ user_id: "example" }])
  })
  await Promise.all([api.admin.users(), api.admin.users()])
  await api.admin.users()
  assert.equal(fetch.mock.callCount(), 1)
})

test("concurrent GETs across all roles are shared but later realtime reads are fresh", async (t) => {
  const fetch = t.mock.method(globalThis, "fetch", async () => json([]))
  for (const read of [api.me, api.admin.dashboard, api.student.periods,
    () => api.student.courses("p"), () => api.lecturer.students("c", "s")]) {
    const before = fetch.mock.callCount()
    await Promise.all([read(), read()])
    assert.equal(fetch.mock.callCount() - before, 1)
    await read()
    assert.equal(fetch.mock.callCount() - before, 2)
  }
})

test("semester CRUD invalidates all role-specific semester lists", async (t) => {
  t.mock.method(globalThis, "fetch", async () => json([]))
  for (const mutate of [() => api.admin.createSemester({}),
    () => api.admin.updateSemester("s", {}), () => api.admin.deleteSemester("s")]) {
    await Promise.all([api.admin.semesters(), api.student.semesters(), api.lecturer.semesters()])
    await mutate()
    for (const key of ["semesters", "student:semesters", "lecturer:semesters"]) {
      assert.equal(getAdminSnapshot(key).data, undefined)
    }
  }
})

test("writes are never deduplicated and failed GETs can retry", async (t) => {
  const fetch = t.mock.method(globalThis, "fetch", async () => json({}))
  await Promise.all([api.student.register("c", "p"), api.student.register("c", "p")])
  assert.equal(fetch.mock.callCount(), 2)
  fetch.mock.mockImplementation(async () => json({ error: "offline" }, 503))
  await assert.rejects(api.student.grades(), /offline/)
  fetch.mock.mockImplementation(async () => json([]))
  assert.deepEqual(await api.student.grades(), [])
})

test("logout and token changes clear memory; saving the same token preserves cache", async () => {
  await loadAdminList("users", async () => ["cached"])
  saveAuth("test-session", { role: "admin" })
  assert.deepEqual(getAdminSnapshot("users").data, ["cached"])
  clearAuth()
  assert.equal(getAdminSnapshot("users").data, undefined)
  assert.equal(storage.has("crs_token"), false)
  saveAuth("another-session", { role: "admin" })
  await loadAdminList("users", async () => ["another"])
  saveAuth("third-session", { role: "admin" })
  assert.equal(getAdminSnapshot("users").data, undefined)
  assert.deepEqual([...storage.keys()].sort(), ["crs_token", "crs_user"])
})

test("401 clears auth and cache; an old session's 401 cannot log out a new session", async (t) => {
  t.mock.method(globalThis, "fetch", async () => json({ error: "expired" }, 401))
  await loadAdminList("users", async () => ["cached"])
  await assert.rejects(api.me(), /expired/)
  assert.equal(getAdminSnapshot("users").data, undefined)
  assert.equal(storage.has("crs_token"), false)

  let resolve
  globalThis.fetch = () => new Promise((done) => { resolve = done })
  saveAuth("old-session", { role: "admin" })
  const pending = api.me()
  saveAuth("new-session", { role: "admin" })
  resolve(json({ error: "expired" }, 401))
  await assert.rejects(pending, /expired/)
  assert.equal(storage.get("crs_token"), "new-session")
})

import assert from "node:assert/strict"
import { beforeEach, test } from "node:test"
import {
  ADMIN_CACHE_TTL, clearAdminCache, getAdminSnapshot,
  invalidateAdminCache, loadAdminList, subscribeAdminCache,
} from "../src/services/adminCache.ts"

const deferred = () => {
  let resolve, reject
  const promise = new Promise((yes, no) => { resolve = yes; reject = no })
  return { promise, resolve, reject }
}
beforeEach(() => clearAdminCache())

test("prefetch and navigation share one request and expose data synchronously", async () => {
  const response = deferred()
  let calls = 0
  const loader = () => { calls++; return response.promise }
  const prefetch = loadAdminList("users", loader)
  const navigation = loadAdminList("users", loader)
  assert.equal(prefetch, navigation)
  const users = [{ user_id: "sample" }]
  response.resolve(users)
  await navigation
  assert.equal(getAdminSnapshot("users").data, users)
  assert.equal(await loadAdminList("users", loader), users)
  assert.equal(calls, 1)
})

test("stale rows stay visible during background refresh and refresh failure", async (t) => {
  const now = Date.now()
  t.mock.method(Date, "now", () => now)
  const old = [{ course_code: "old" }]
  await loadAdminList("courses", async () => old)
  Date.now.mock.mockImplementation(() => now + ADMIN_CACHE_TTL + 1)
  const response = deferred()
  const refresh = loadAdminList("courses", () => response.promise)
  assert.equal(getAdminSnapshot("courses").data, old)
  response.reject(new Error("offline"))
  await assert.rejects(refresh, /offline/)
  assert.equal(getAdminSnapshot("courses").data, old)
  assert.equal(getAdminSnapshot("courses").error.message, "offline")
  const fresh = [{ course_code: "new" }]
  await loadAdminList("courses", async () => fresh)
  assert.equal(getAdminSnapshot("courses").data, fresh)
})

test("CRUD invalidation clears old rows and preserves unrelated caches", async () => {
  await loadAdminList("users", async () => [1])
  await loadAdminList("majors", async () => [2])
  invalidateAdminCache("users")
  assert.equal(getAdminSnapshot("users").data, undefined)
  assert.deepEqual(getAdminSnapshot("majors").data, [2])
  await loadAdminList("users", async () => [3])
  assert.deepEqual(getAdminSnapshot("users").data, [3])
})

test("GET started before CRUD cannot overwrite refreshed data", async () => {
  const old = deferred()
  const pending = loadAdminList("users", () => old.promise)
  await Promise.resolve()
  invalidateAdminCache("users")
  await loadAdminList("users", async () => ["after CRUD"])
  old.resolve(["before CRUD"])
  assert.deepEqual(await pending, ["after CRUD"])
  assert.deepEqual(getAdminSnapshot("users").data, ["after CRUD"])
})

test("invalidation of an in-flight prefetch starts a fresh read", async () => {
  const old = deferred()
  let calls = 0
  const pending = loadAdminList("users", () => ++calls === 1 ? old.promise : Promise.resolve(["fresh"]))
  await Promise.resolve()
  invalidateAdminCache("users")
  old.resolve(["stale"])
  assert.deepEqual(await pending, ["fresh"])
  assert.equal(calls, 2)
})

test("late responses from a previous auth session never populate the next session", async () => {
  const old = deferred()
  const pending = loadAdminList("users", () => old.promise)
  const rejected = assert.rejects(pending, /session changed/)
  clearAdminCache()
  await loadAdminList("users", async () => ["new session"])
  old.resolve(["old session"])
  await rejected
  assert.deepEqual(getAdminSnapshot("users").data, ["new session"])
})

test("empty lists are cached and failed requests can retry", async () => {
  await assert.rejects(loadAdminList("users", async () => { throw new Error("offline") }))
  assert.equal(getAdminSnapshot("users").data, undefined)
  await loadAdminList("users", async () => [])
  const result = await loadAdminList("users", async () => { throw new Error("duplicate") })
  assert.deepEqual(result, [])
})

test("subscribers see stable snapshots and can unsubscribe", async () => {
  assert.equal(getAdminSnapshot("users"), getAdminSnapshot("users"))
  let updates = 0
  const unsubscribe = subscribeAdminCache(() => updates++)
  await loadAdminList("users", async () => [])
  invalidateAdminCache("users")
  clearAdminCache()
  assert.equal(updates, 3)
  unsubscribe()
  clearAdminCache()
  assert.equal(updates, 3)
})

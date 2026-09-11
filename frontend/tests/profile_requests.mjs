import { readFile, writeFile } from "node:fs/promises"
import ts from "typescript"
import { clearAdminCache } from "../src/services/adminCache.ts"
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

let calls = 0
globalThis.fetch = async () => {
  calls++
  await new Promise((resolve) => setTimeout(resolve, 20))
  return new Response("[]", { status: 200 })
}
const results = {}
for (const [name, read] of [
  ["session.me", api.me], ["admin.dashboard", api.admin.dashboard],
  ["admin.semesters", api.admin.semesters], ["student.semesters", api.student.semesters],
  ["lecturer.semesters", api.lecturer.semesters], ["student.periods", api.student.periods],
  ["student.courses", () => api.student.courses("example")],
  ["lecturer.courses", () => api.lecturer.teachingCourses("example")],
]) {
  clearAuth()
  saveAuth("synthetic-test-session", { role: "admin" })
  clearAdminCache()
  calls = 0
  const start = performance.now()
  await Promise.all([read(), read()])
  const concurrent = calls
  await read()
  results[name] = { concurrent_requests: concurrent, requests_after_revisit: calls,
    synthetic_total_ms: Math.round(performance.now() - start) }
}
console.log(JSON.stringify(results, null, 2))
await writeFile(process.argv[2], JSON.stringify({ note: "Synthetic 20ms fetch; API request counts, NOT browser/Neon latency", results }, null, 2))

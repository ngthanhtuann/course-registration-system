export type AdminList = "users" | "courses" | "majors" | "semesters"
export const ADMIN_CACHE_TTL = 30_000

type Snapshot = { data?: any[]; error?: Error }
type Entry = { snapshot: Snapshot; updatedAt: number; pending?: Promise<any[]> }
// Keep the existing store; role-prefixed keys also hold shared semester lists.
const entries = new Map<string, Entry>()
const listeners = new Set<() => void>()
let session = 0

function entryFor(key: string): Entry {
  let entry = entries.get(key)
  if (!entry) {
    entry = { snapshot: {}, updatedAt: 0 }
    entries.set(key, entry)
  }
  return entry
}

function emit() {
  listeners.forEach((listener) => listener())
}

export function subscribeAdminCache(listener: () => void) {
  listeners.add(listener)
  return () => { listeners.delete(listener) }
}

export function getAdminSnapshot(key: string) {
  return entryFor(key).snapshot
}

export function invalidateAdminCache(...keys: string[]) {
  keys.forEach((key) => entries.delete(key))
  emit()
}

export function clearAdminCache() {
  session += 1
  entries.clear()
  emit()
}

export function loadAdminList(key: string, loader: () => Promise<any[]>): Promise<any[]> {
  const entry = entryFor(key)
  if (entry.pending) return entry.pending
  if (entry.snapshot.data && Date.now() - entry.updatedAt < ADMIN_CACHE_TTL) {
    return Promise.resolve(entry.snapshot.data)
  }
  const startedSession = session
  const pending = Promise.resolve().then(loader).then(
    (data) => {
      if (session !== startedSession) throw new Error("Authentication session changed.")
      // Do not publish a GET started before a successful mutation.
      if (entries.get(key) !== entry) return loadAdminList(key, loader)
      entry.snapshot = { data }
      entry.updatedAt = Date.now()
      emit()
      return data
    },
    (error: Error) => {
      if (session === startedSession && entries.get(key) === entry) {
        entry.snapshot = { data: entry.snapshot.data, error }
        emit()
      }
      throw error
    },
  ).finally(() => { entry.pending = undefined })
  entry.pending = pending
  return pending
}

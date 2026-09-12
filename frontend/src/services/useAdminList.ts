import { useEffect, useSyncExternalStore } from "react"
import { api, getStoredUser } from "./api"
import { getAdminSnapshot, subscribeAdminCache } from "./adminCache"
import type { AdminList } from "./adminCache"

const empty: any[] = []

function refresh(key: AdminList) {
  if (getStoredUser<{ role: string }>()?.role === "admin") {
    void api.admin[key]().catch(() => { /* Cache exposes errors to the page. */ })
  }
}

export function useAdminList(key: AdminList) {
  const snapshot = useSyncExternalStore(subscribeAdminCache, () => getAdminSnapshot(key))
  const missing = snapshot.data === undefined && !snapshot.error
  useEffect(() => {
    // Mount refreshes stale data without hiding rows, or retries a failed prefetch.
    refresh(key)
  }, [key])
  useEffect(() => {
    // Observe the snapshot identity even if a mutation invalidates an empty list.
    if (!snapshot.data && !snapshot.error) refresh(key)
  }, [key, snapshot])
  return {
    data: snapshot.data ?? empty,
    error: snapshot.error?.message ?? "",
    loading: missing,
  }
}

export function prefetchAdminLists() {
  if (getStoredUser<{ role: string }>()?.role !== "admin") return
  void Promise.allSettled([api.admin.users(), api.admin.courses(), api.admin.majors(), api.admin.semesters()])
}

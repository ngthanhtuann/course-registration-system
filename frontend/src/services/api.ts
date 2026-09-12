import { clearAdminCache, invalidateAdminCache, loadAdminList } from "./adminCache"

export const API_URL = (import.meta.env.VITE_API_URL || "").replace(/\/$/, "")

// Share only in-flight GETs. Grades, seats and authorization are not TTL-cached.
const pendingReads = new Map<string, Promise<unknown>>()

export class ApiError extends Error {
  status: number

  constructor(message: string, status = 0) {
    super(message)

    this.name = "ApiError"

    this.status = status
  }
}

function getToken() {
  return localStorage.getItem("crs_token") || ""
}

export function saveAuth(token: string, user: unknown) {
  const changed = getToken() !== token
  localStorage.setItem("crs_token", token)

  localStorage.setItem("crs_user", JSON.stringify(user))
  if (changed) {
    pendingReads.clear()
    clearAdminCache()
  }
}

export function getStoredUser<T>() {
  const raw = localStorage.getItem("crs_user")

  if (!raw) return null as T | null

  try {
    return JSON.parse(raw) as T
  } catch {
    return null as T | null
  }
}

export function clearAuth() {
  pendingReads.clear()
  localStorage.removeItem("crs_token")

  localStorage.removeItem("crs_user")
  clearAdminCache()
}

// Other tabs can change the shared authentication token, but list data stays
// exclusively in this tab's memory.
window.addEventListener("storage", (event) => {
  if (event.key === "crs_token" || event.key === null) {
    pendingReads.clear()
    clearAdminCache()
  }
})

function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  if (options.method && options.method !== "GET") return sendRequest<T>(path, options)
  const existing = pendingReads.get(path)
  if (existing) return existing as Promise<T>
  const pending = sendRequest<T>(path, options).finally(() => {
    if (pendingReads.get(path) === pending) pendingReads.delete(path)
  })
  pendingReads.set(path, pending)
  return pending
}

async function sendRequest<T>(path: string, options: RequestInit = {}): Promise<T> {
  const headers = new Headers(options.headers)

  headers.set("Accept", "application/json")

  if (options.body && !headers.has("Content-Type"))
    headers.set("Content-Type", "application/json")

  const token = getToken()

  if (token) headers.set("Authorization", `Bearer ${token}`)

  let response: Response

  try {
    response = await fetch(`${API_URL}${path}`, { ...options, headers })
  } catch {
    throw new ApiError(
      `Cannot connect to backend at ${API_URL}. Make sure the Flask server is running.`,
      0,
    )
  }

  const text = await response.text()

  let data: any = null

  if (text) {
    try {
      data = JSON.parse(text)
    } catch {
      data = null
    }
  }

  if (!response.ok) {
    const message =
      data?.error || data?.message || `Request failed (${response.status})`

    if (response.status === 401 && token === getToken()) clearAuth()

    throw new ApiError(message, response.status)
  }

  if (token === getToken() && options.method && options.method !== "GET") {
    // The refresh after a write must not join an older GET.
    pendingReads.clear()
    if (
      /^\/api\/admin\/users(?:\/|$)/.test(path) ||
      /^\/api\/admin\/lecturer-qualifications(?:\/|$)/.test(path) ||
      path === "/api/account/profile"
    ) invalidateAdminCache("users")
    if (/^\/api\/admin\/courses(?:\/|$)/.test(path)) invalidateAdminCache("courses")
    if (/^\/api\/admin\/majors(?:\/|$)/.test(path)) invalidateAdminCache("majors")
    if (/^\/api\/admin\/semesters(?:\/|$)/.test(path)) {
      invalidateAdminCache("semesters", "student:semesters", "lecturer:semesters")
    }
  }
  return data as T
}

export const api = {
  logout: () => request<any>("/api/logout", { method: "POST" }),
  login: (username: string, password: string) =>
    request<{
      token: string
      user: any
    }>("/api/login", {
      method: "POST",
      body: JSON.stringify({ username, password }),
    }),

  me: () => request<any>("/api/me"),

  updateProfile: (fullname: string, email: string) =>
    request<any>("/api/account/profile", {
      method: "PUT",
      body: JSON.stringify({ fullname, email }),
    }),

  changePassword: (current_password: string, new_password: string) =>
    request<any>("/api/account/password", {
      method: "PUT",
      body: JSON.stringify({ current_password, new_password }),
    }),

  admin: {
    dashboard: () => request<any>("/api/admin/dashboard"),

    users: () => loadAdminList("users", () => request<any[]>("/api/admin/users")),

    createUser: (payload: any) =>
      request<any>("/api/admin/users", {
        method: "POST",
        body: JSON.stringify(payload),
      }),

    updateUser: (id: string, payload: any) =>
      request<any>(`/api/admin/users/${encodeURIComponent(id)}`, {
        method: "PUT",
        body: JSON.stringify(payload),
      }),

    deactivateUser: (id: string) =>
      request<any>(`/api/admin/users/${encodeURIComponent(id)}`, {
        method: "DELETE",
      }),

    majors: () => loadAdminList("majors", () => request<any[]>("/api/admin/majors")),

    createMajor: (payload: any) =>
      request<any>("/api/admin/majors", {
        method: "POST",
        body: JSON.stringify(payload),
      }),

    updateMajor: (code: string, payload: any) =>
      request<any>(`/api/admin/majors/${encodeURIComponent(code)}`, {
        method: "PUT",
        body: JSON.stringify(payload),
      }),

    deleteMajor: (code: string) =>
      request<any>(`/api/admin/majors/${encodeURIComponent(code)}`, {
        method: "DELETE",
      }),

    courses: () => loadAdminList("courses", () => request<any[]>("/api/admin/courses")),

    createCourse: (payload: any) =>
      request<any>("/api/admin/courses", {
        method: "POST",
        body: JSON.stringify(payload),
      }),

    updateCourse: (code: string, payload: any) =>
      request<any>(`/api/admin/courses/${encodeURIComponent(code)}`, {
        method: "PUT",
        body: JSON.stringify(payload),
      }),

    deleteCourse: (code: string) =>
      request<any>(`/api/admin/courses/${encodeURIComponent(code)}`, {
        method: "DELETE",
      }),

    curriculum: (major: string) =>
      request<any[]>(`/api/admin/curriculum/${encodeURIComponent(major)}`),

    addCurriculum: (payload: any) =>
      request<any>("/api/admin/curriculum", {
        method: "POST",
        body: JSON.stringify(payload),
      }),

    updateCurriculum: (id: string, payload: any) =>
      request<any>(`/api/admin/curriculum/${encodeURIComponent(id)}`, {
        method: "PUT",
        body: JSON.stringify(payload),
      }),

    deleteCurriculum: (id: string) =>
      request<any>(`/api/admin/curriculum/${encodeURIComponent(id)}`, {
        method: "DELETE",
      }),

    semesters: () => loadAdminList("semesters", () => request<any[]>("/api/admin/semesters")),

    createSemester: (payload: any) =>
      request<any>("/api/admin/semesters", {
        method: "POST",
        body: JSON.stringify(payload),
      }),

    updateSemester: (id: string, payload: any) =>
      request<any>(`/api/admin/semesters/${encodeURIComponent(id)}`, {
        method: "PUT",
        body: JSON.stringify(payload),
      }),

    deleteSemester: (id: string) =>
      request<any>(`/api/admin/semesters/${encodeURIComponent(id)}`, {
        method: "DELETE",
      }),

    periods: () => request<any[]>("/api/admin/registration-periods"),

    createPeriod: (payload: any) =>
      request<any>("/api/admin/registration-periods", {
        method: "POST",
        body: JSON.stringify(payload),
      }),

    updatePeriod: (id: string, payload: any) =>
      request<any>(
        `/api/admin/registration-periods/${encodeURIComponent(id)}`,
        { method: "PUT", body: JSON.stringify(payload) },
      ),

    deletePeriod: (id: string) =>
      request<any>(
        `/api/admin/registration-periods/${encodeURIComponent(id)}`,
        { method: "DELETE" },
      ),

    demand: (periodId: string, majorCode = "") =>
      request<any[]>(
        `/api/admin/registration-demand?period_id=${encodeURIComponent(periodId)}${
          majorCode ? `&major_code=${encodeURIComponent(majorCode)}` : ""
        }`,
      ),

    demandStudents: (courseCode: string, periodId: string, majorCode = "") =>
      request<any[]>(
        `/api/admin/registration-demand/${encodeURIComponent(courseCode)}/students?period_id=${encodeURIComponent(periodId)}${
          majorCode ? `&major_code=${encodeURIComponent(majorCode)}` : ""
        }`,
      ),

    assignments: (semesterId = "") =>
      request<any[]>(
        `/api/admin/teaching-assignments${
          semesterId ? `?semester_id=${encodeURIComponent(semesterId)}` : ""
        }`,
      ),

    createAssignment: (payload: any) =>
      request<any>("/api/admin/teaching-assignments", {
        method: "POST",
        body: JSON.stringify(payload),
      }),

    deleteAssignment: (id: string) =>
      request<any>(
        `/api/admin/teaching-assignments/${encodeURIComponent(id)}`,
        { method: "DELETE" },
      ),

    qualifiedLecturers: (courseCode: string) =>
      request<any[]>(
        `/api/admin/qualified-lecturers/${encodeURIComponent(courseCode)}`,
      ),

    addQualification: (lecturerId: string, courseCode: string) =>
      request<any>("/api/admin/lecturer-qualifications", {
        method: "POST",
        body: JSON.stringify({
          lecturer_id: lecturerId,
          course_code: courseCode,
        }),
      }),

    removeQualification: (lecturerId: string, courseCode: string) =>
      request<any>(
        `/api/admin/lecturer-qualifications/${encodeURIComponent(lecturerId)}/${encodeURIComponent(courseCode)}`,
        { method: "DELETE" },
      ),
  },

  lecturer: {
    profile: () => request<any>("/api/lecturer/profile"),

    semesters: () => loadAdminList("lecturer:semesters", () => request<any[]>("/api/lecturer/semesters")),

    teachingCourses: (semesterId: string) =>
      request<any[]>(
        `/api/lecturer/teaching-courses?semester_id=${encodeURIComponent(semesterId)}`,
      ),

    students: (courseCode: string, semesterId: string) =>
      request<any[]>(
        `/api/lecturer/courses/${encodeURIComponent(courseCode)}/students?semester_id=${encodeURIComponent(semesterId)}`,
      ),

    updateGrade: (registrationId: string, grade: number) =>
      request<any>(
        `/api/lecturer/registrations/${encodeURIComponent(registrationId)}/grade`,
        { method: "PUT", body: JSON.stringify({ grade }) },
      ),
  },

  student: {
    profile: () => request<any>("/api/student/profile"),

    semesters: () => loadAdminList("student:semesters", () => request<any[]>("/api/student/semesters")),

    periods: () => request<any[]>("/api/student/registration-periods"),

    curriculum: () => request<any[]>("/api/student/curriculum"),

    courses: (periodId = "", search = "") =>
      request<any[]>(
        `/api/student/courses?${
          periodId ? `period_id=${encodeURIComponent(periodId)}&` : ""
        }${search ? `search=${encodeURIComponent(search)}` : ""}`,
      ),

    registrations: (semesterId = "") =>
      request<any[]>(
        `/api/student/registrations${
          semesterId ? `?semester_id=${encodeURIComponent(semesterId)}` : ""
        }`,
      ),

    register: (courseCode: string, periodId: string) =>
      request<any>("/api/student/registrations", {
        method: "POST",
        body: JSON.stringify({ course_code: courseCode, period_id: periodId }),
      }),

    drop: (registrationId: string) =>
      request<any>(
        `/api/student/registrations/${encodeURIComponent(registrationId)}/drop`,
        { method: "PUT" },
      ),

    grades: (semesterId = "") =>
      request<any[]>(
        `/api/student/grades${
          semesterId ? `?semester_id=${encodeURIComponent(semesterId)}` : ""
        }`,
      ),
  },
}

export const API_URL = (import.meta.env.VITE_API_URL || "").replace(/\/$/, "")

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
  localStorage.setItem("crs_token", token)

  localStorage.setItem("crs_user", JSON.stringify(user))
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
  localStorage.removeItem("crs_token")

  localStorage.removeItem("crs_user")
}

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
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

    if (response.status === 401) clearAuth()

    throw new ApiError(message, response.status)
  }

  return data as T
}

export const api = {
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

    users: () => request<any[]>("/api/admin/users"),

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

    majors: () => request<any[]>("/api/admin/majors"),

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

    courses: () => request<any[]>("/api/admin/courses"),

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

    semesters: () => request<any[]>("/api/admin/semesters"),

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

    demandStudents: (courseCode: string, periodId: string) =>
      request<any[]>(
        `/api/admin/registration-demand/${encodeURIComponent(courseCode)}/students?period_id=${encodeURIComponent(periodId)}`,
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

    semesters: () => request<any[]>("/api/lecturer/semesters"),

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

    semesters: () => request<any[]>("/api/student/semesters"),

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

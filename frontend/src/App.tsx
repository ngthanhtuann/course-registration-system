import React, { lazy, Suspense, useEffect, useState } from "react"
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom"
import type { AuthUser, Student, Lecturer } from "./types"
import Layout from "./components/Layout"
import Login from "./pages/LoginPage"
import AdminDashboard from "./pages/admin/AdminDashboard"
import LecturerDashboard from "./pages/lecturer/LecturerDashboard"
import StudentDashboard from "./pages/student/StudentDashboard"
import { api, ApiError, clearAuth, getStoredUser, saveAuth } from "./services/api"

// Load secondary pages only when opened; keep the layout and dashboards ready.
const ManageAccount = lazy(() => import("./pages/ManageAccount"))
const ManageUser = lazy(() => import("./pages/admin/ManageUser"))
const ManageMajor = lazy(() => import("./pages/admin/ManageMajors"))
const ManageCurriculum = lazy(() => import("./pages/admin/ManageCurriculum"))
const ManageCourse = lazy(() => import("./pages/admin/ManageCourses"))
const ManageSemester = lazy(() => import("./pages/admin/ManageSemesters"))
const ManageRegistrationPeriod = lazy(() => import("./pages/admin/RegistrationPeriod"))
const ManageRegistrationDemand = lazy(() => import("./pages/admin/RegistrationDemand"))
const AssignLecturer = lazy(() => import("./pages/admin/AssignLecturer"))
const ManageTeachingCourse = lazy(() => import("./pages/lecturer/TeachingCourses"))
const ManageStudentGrades = lazy(() => import("./pages/lecturer/ManageGrades"))
const ViewCourses = lazy(() => import("./pages/student/ViewCourses"))
const CourseRegistration = lazy(() => import("./pages/student/CourseRegistration"))
const ViewRegistrationStatus = lazy(() => import("./pages/student/RegistrationStatus"))
const DropCourse = lazy(() => import("./pages/student/DropCourse"))
const ViewGrades = lazy(() => import("./pages/student/ViewGrades"))

function ProtectedLayout({
  user,
  onLogout,
  requiredRole,
  children,
}: {
  user: AuthUser
  onLogout: () => void
  requiredRole: string
  children: React.ReactNode
}) {
  if (!user) return <Navigate to="/login" replace />
  if (user.role !== requiredRole) {
    const redirect =
      user.role === "admin"
        ? "/admin/dashboard"
        : user.role === "lecturer"
          ? "/lecturer/dashboard"
          : "/student/dashboard"
    return <Navigate to={redirect} replace />
  }
  return (
    <Layout user={user} onLogout={onLogout}>
      <Suspense fallback={<div className="p-6 text-slate-500">Loading?</div>}>
        {children}
      </Suspense>
    </Layout>
  )
}

function readCachedUser(): AuthUser {
  if (!localStorage.getItem("crs_token")) return null
  const cached = getStoredUser<AuthUser>()
  if (
    !cached || !cached.id || typeof cached.fullName !== "string" ||
    !["admin", "student", "lecturer"].includes(cached.role) ||
    cached.status !== "Active"
  ) return null
  return cached
}

export default function App() {
  const [user, setUser] = useState<AuthUser>(readCachedUser)

  useEffect(() => {
    let alive = true
    const token = localStorage.getItem("crs_token")
    const currentSession = () => alive && localStorage.getItem("crs_token") === token
    const invalidate = () => {
      // request() may already have removed this token after a 401. Never clear
      // a newer login when a response from the previous session arrives late.
      if (alive && (!localStorage.getItem("crs_token") || currentSession())) {
        clearAuth()
        setUser(null)
      }
    }
    const publish = (next: Exclude<AuthUser, null>) => {
      if (!currentSession()) {
        if (alive && !localStorage.getItem("crs_token")) setUser(null)
        return false
      }
      saveAuth(token!, next)
      setUser((previous) => JSON.stringify(previous) === JSON.stringify(next) ? previous : next)
      return true
    }
    const restore = async () => {
      if (!user || !token) {
        invalidate()
        return
      }
      try {
        const base = await api.me()
        if (!currentSession()) {
          if (alive && !localStorage.getItem("crs_token")) setUser(null)
          return
        }
        if (!base?.user_id || !["admin", "student", "lecturer"].includes(base.role) ||
            base.active_status === false) {
          invalidate()
          return
        }
        // Publish validated identity before waiting for optional profile data.
        // Keep the cached role-specific fields only for the same identity/role.
        const cached = user.id === base.user_id && user.role === base.role ? user : null
        const common = {
          id: base.user_id,
          username: base.username,
          fullName: base.fullname,
          email: base.email,
          status: "Active" as const,
        }
        const normalized: Exclude<AuthUser, null> = base.role === "student"
          ? { ...common, role: "student", studentId: cached?.role === "student" ? cached.studentId : "",
              major: cached?.role === "student" ? cached.major : "" }
          : base.role === "lecturer"
            ? { ...common, role: "lecturer", lecturerId: cached?.role === "lecturer" ? cached.lecturerId : "",
                qualifications: cached?.role === "lecturer" ? cached.qualifications : [] }
            : { ...common, role: "admin" }
        if (!publish(normalized)) return
        if (normalized.role === "student") {
          const full = await api.student.profile()
          publish({ ...normalized, studentId: full.student_id, major: full.major_code })
        } else if (normalized.role === "lecturer") {
          const full = await api.lecturer.profile()
          publish({ ...normalized, lecturerId: full.lecturer_id, qualifications: full.qualifications || [] })
        }
      } catch (error) {
        if (error instanceof ApiError && (error.status === 401 || error.status === 403)) {
          invalidate()
        } else if (alive && !localStorage.getItem("crs_token")) {
          setUser(null)
        }
        // Network/5xx errors do not prove the session invalid. Keep the visible
        // cached user; all protected requests still require backend authorization.
      }
    }
    void restore()
    return () => {
      alive = false
    }
  }, [])

  const handleLogout = () => {
    clearAuth()
    setUser(null)
  }
  return (
    <BrowserRouter>
      <Routes>
        <Route
          path="/login"
          element={
            user ? (
              <Navigate
                to={
                  user.role === "admin"
                    ? "/admin/dashboard"
                    : user.role === "lecturer"
                      ? "/lecturer/dashboard"
                      : "/student/dashboard"
                }
                replace
              />
            ) : (
              <Login onLogin={setUser} />
            )
          }
        />
        <Route
          path="/admin/*"
          element={
            <ProtectedLayout
              user={user}
              onLogout={handleLogout}
              requiredRole="admin"
            >
              <Routes>
                <Route path="dashboard" element={<AdminDashboard />} />
                <Route path="users" element={<ManageUser />} />
                <Route path="majors" element={<ManageMajor />} />
                <Route path="curriculum" element={<ManageCurriculum />} />
                <Route path="courses" element={<ManageCourse />} />
                <Route path="semesters" element={<ManageSemester />} />
                <Route
                  path="registration-period"
                  element={<ManageRegistrationPeriod />}
                />
                <Route
                  path="registration-demand"
                  element={<ManageRegistrationDemand />}
                />
                <Route path="assign-lecturer" element={<AssignLecturer />} />
                <Route
                  path="account"
                  element={
                    <ManageAccount user={user} onLogout={handleLogout} />
                  }
                />
                <Route
                  path="*"
                  element={<Navigate to="/admin/dashboard" replace />}
                />
              </Routes>
            </ProtectedLayout>
          }
        />
        <Route
          path="/lecturer/*"
          element={
            <ProtectedLayout
              user={user}
              onLogout={handleLogout}
              requiredRole="lecturer"
            >
              <Routes>
                <Route
                  path="dashboard"
                  element={<LecturerDashboard user={user as Lecturer} />}
                />
                <Route
                  path="courses"
                  element={<ManageTeachingCourse user={user as Lecturer} />}
                />
                <Route
                  path="grades"
                  element={<ManageStudentGrades user={user as Lecturer} />}
                />
                <Route
                  path="account"
                  element={
                    <ManageAccount user={user} onLogout={handleLogout} />
                  }
                />
                <Route
                  path="*"
                  element={<Navigate to="/lecturer/dashboard" replace />}
                />
              </Routes>
            </ProtectedLayout>
          }
        />
        <Route
          path="/student/*"
          element={
            <ProtectedLayout
              user={user}
              onLogout={handleLogout}
              requiredRole="student"
            >
              <Routes>
                <Route
                  path="dashboard"
                  element={<StudentDashboard user={user as Student} />}
                />
                <Route
                  path="courses"
                  element={<ViewCourses user={user as Student} />}
                />
                <Route
                  path="register"
                  element={<CourseRegistration user={user as Student} />}
                />
                <Route
                  path="status"
                  element={<ViewRegistrationStatus user={user as Student} />}
                />
                <Route
                  path="drop"
                  element={<DropCourse user={user as Student} />}
                />
                <Route
                  path="grades"
                  element={<ViewGrades user={user as Student} />}
                />
                <Route
                  path="account"
                  element={
                    <ManageAccount user={user} onLogout={handleLogout} />
                  }
                />
                <Route
                  path="*"
                  element={<Navigate to="/student/dashboard" replace />}
                />
              </Routes>
            </ProtectedLayout>
          }
        />
        <Route path="*" element={<Navigate to="/login" replace />} />
      </Routes>
    </BrowserRouter>
  )
}

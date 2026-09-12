import React, { useState } from "react"
import { NavLink, useNavigate } from "react-router-dom"
import type { AuthUser } from "../types"

interface NavItem {
  label: string
  path: string
  icon: React.ReactNode
}

const ICONS = {
  dashboard: (
    <svg
      width="18"
      height="18"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      viewBox="0 0 24 24"
    >
      <rect x="3" y="3" width="7" height="7" rx="1" />
      <rect x="14" y="3" width="7" height="7" rx="1" />
      <rect x="3" y="14" width="7" height="7" rx="1" />
      <rect x="14" y="14" width="7" height="7" rx="1" />
    </svg>
  ),
  users: (
    <svg
      width="18"
      height="18"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      viewBox="0 0 24 24"
    >
      <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" />
      <circle cx="9" cy="7" r="4" />
      <path d="M23 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75" />
    </svg>
  ),
  major: (
    <svg
      width="18"
      height="18"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      viewBox="0 0 24 24"
    >
      <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5" />
    </svg>
  ),
  curriculum: (
    <svg
      width="18"
      height="18"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      viewBox="0 0 24 24"
    >
      <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20" />
      <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z" />
    </svg>
  ),
  course: (
    <svg
      width="18"
      height="18"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      viewBox="0 0 24 24"
    >
      <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z" />
      <path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z" />
    </svg>
  ),
  semester: (
    <svg
      width="18"
      height="18"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      viewBox="0 0 24 24"
    >
      <rect x="3" y="4" width="18" height="18" rx="2" />
      <path d="M16 2v4M8 2v4M3 10h18" />
    </svg>
  ),
  registration: (
    <svg
      width="18"
      height="18"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      viewBox="0 0 24 24"
    >
      <path d="M9 11l3 3L22 4" />
      <path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11" />
    </svg>
  ),
  demand: (
    <svg
      width="18"
      height="18"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      viewBox="0 0 24 24"
    >
      <line x1="18" y1="20" x2="18" y2="10" />
      <line x1="12" y1="20" x2="12" y2="4" />
      <line x1="6" y1="20" x2="6" y2="14" />
    </svg>
  ),
  assign: (
    <svg
      width="18"
      height="18"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      viewBox="0 0 24 24"
    >
      <circle cx="12" cy="8" r="4" />
      <path d="M6 20v-2a4 4 0 0 1 4-4h4a4 4 0 0 1 4 4v2" />
      <path d="M15 10l2 2 4-4" />
    </svg>
  ),
  account: (
    <svg
      width="18"
      height="18"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      viewBox="0 0 24 24"
    >
      <circle cx="12" cy="8" r="4" />
      <path d="M6 20v-2a4 4 0 0 1 4-4h4a4 4 0 0 1 4 4v2" />
    </svg>
  ),
  teaching: (
    <svg
      width="18"
      height="18"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      viewBox="0 0 24 24"
    >
      <path d="M2 3h20v14H2zM8 21l4-4 4 4" />
    </svg>
  ),
  grades: (
    <svg
      width="18"
      height="18"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      viewBox="0 0 24 24"
    >
      <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7" />
      <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z" />
    </svg>
  ),
  viewcourse: (
    <svg
      width="18"
      height="18"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      viewBox="0 0 24 24"
    >
      <circle cx="11" cy="11" r="8" />
      <path d="m21 21-4.35-4.35" />
    </svg>
  ),
  register: (
    <svg
      width="18"
      height="18"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      viewBox="0 0 24 24"
    >
      <path d="M12 5v14M5 12h14" />
    </svg>
  ),
  status: (
    <svg
      width="18"
      height="18"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      viewBox="0 0 24 24"
    >
      <path d="M9 11l3 3L22 4" />
      <path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11" />
    </svg>
  ),
  drop: (
    <svg
      width="18"
      height="18"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      viewBox="0 0 24 24"
    >
      <circle cx="12" cy="12" r="10" />
      <path d="M15 9l-6 6M9 9l6 6" />
    </svg>
  ),
  logout: (
    <svg
      width="18"
      height="18"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      viewBox="0 0 24 24"
    >
      <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" />
      <polyline points="16 17 21 12 16 7" />
      <line x1="21" y1="12" x2="9" y2="12" />
    </svg>
  ),
}

const ADMIN_NAV: NavItem[] = [
  { label: "Dashboard", path: "/admin/dashboard", icon: ICONS.dashboard },
  { label: "Manage User", path: "/admin/users", icon: ICONS.users },
  { label: "Manage Major", path: "/admin/majors", icon: ICONS.major },
  {
    label: "Manage Curriculum",
    path: "/admin/curriculum",
    icon: ICONS.curriculum,
  },
  { label: "Manage Course", path: "/admin/courses", icon: ICONS.course },
  { label: "Manage Semester", path: "/admin/semesters", icon: ICONS.semester },
  {
    label: "Manage Reg. Period",
    path: "/admin/registration-period",
    icon: ICONS.registration,
  },
  {
    label: "Manage Reg. Demand",
    path: "/admin/registration-demand",
    icon: ICONS.demand,
  },
  {
    label: "Assign Lecturer",
    path: "/admin/assign-lecturer",
    icon: ICONS.assign,
  },
  { label: "Manage Account", path: "/admin/account", icon: ICONS.account },
]

const LECTURER_NAV: NavItem[] = [
  { label: "Dashboard", path: "/lecturer/dashboard", icon: ICONS.dashboard },
  {
    label: "Teaching Courses",
    path: "/lecturer/courses",
    icon: ICONS.teaching,
  },
  { label: "Student Grades", path: "/lecturer/grades", icon: ICONS.grades },
  { label: "Manage Account", path: "/lecturer/account", icon: ICONS.account },
]

const STUDENT_NAV: NavItem[] = [
  { label: "Dashboard", path: "/student/dashboard", icon: ICONS.dashboard },
  { label: "View Courses", path: "/student/courses", icon: ICONS.viewcourse },
  {
    label: "Course Registration",
    path: "/student/register",
    icon: ICONS.register,
  },
  { label: "Registration Status", path: "/student/status", icon: ICONS.status },
  { label: "Drop Course", path: "/student/drop", icon: ICONS.drop },
  { label: "View Grades", path: "/student/grades", icon: ICONS.grades },
  { label: "Manage Account", path: "/student/account", icon: ICONS.account },
]

function getNav(role: string) {
  if (role === "admin") return ADMIN_NAV
  if (role === "lecturer") return LECTURER_NAV
  return STUDENT_NAV
}

function SidebarContent({
  nav,
  onClose,
  onLogout,
}: {
  nav: NavItem[]
  onClose?: () => void
  onLogout: () => void | Promise<void>
}) {
  return (
    <div className="flex flex-col h-full">
      <div className="px-5 py-5 border-b border-slate-100">
        <div className="flex items-center gap-2.5">
          <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center shrink-0">
            <svg width="18" height="18" fill="white" viewBox="0 0 24 24">
              <path
                d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"
                stroke="white"
                strokeWidth="2"
                fill="none"
              />
            </svg>
          </div>
          <div className="min-w-0">
            <p className="text-sm font-bold text-slate-800 truncate">
              UniRegistrar
            </p>
            <p className="text-xs text-slate-400">Course System</p>
          </div>
        </div>
      </div>
      <nav className="flex-1 overflow-y-auto px-3 py-4 space-y-0.5">
        {nav.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            onClick={onClose}
            className={({ isActive }) =>
              `flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors
              ${
                isActive
                  ? "bg-blue-600 text-white"
                  : "text-slate-600 hover:bg-slate-100 hover:text-slate-800"
              }`
            }
          >
            {item.icon}
            <span>{item.label}</span>
          </NavLink>
        ))}
      </nav>
      <div className="px-3 pb-4 pt-2 border-t border-slate-100">
        <button
          onClick={onLogout}
          className="flex items-center gap-3 w-full px-3 py-2.5 rounded-lg text-sm font-medium text-slate-600 hover:bg-red-50 hover:text-red-600 transition-colors"
        >
          {ICONS.logout}
          <span>Logout</span>
        </button>
      </div>
    </div>
  )
}

interface LayoutProps {
  user: AuthUser
  onLogout: () => void | Promise<void>
  children: React.ReactNode
}

export default function Layout({ user, onLogout, children }: LayoutProps) {
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const navigate = useNavigate()
  const nav = getNav(user?.role ?? "student")

  const handleLogout = async () => {
    await onLogout()
    navigate("/login")
  }

  const roleLabel =
    user?.role === "admin"
      ? "Administrator"
      : user?.role === "lecturer"
        ? "Lecturer"
        : "Student"
  const roleColors: Record<string, string> = {
    admin: "bg-purple-100 text-purple-700",
    lecturer: "bg-blue-100 text-blue-700",
    student: "bg-green-100 text-green-700",
  }

  return (
    <div className="flex h-full bg-slate-50">
      {/* Desktop Sidebar */}
      <aside className="hidden lg:flex flex-col w-60 xl:w-64 shrink-0 bg-white border-r border-slate-200 h-full">
        <SidebarContent nav={nav} onLogout={handleLogout} />
      </aside>

      {/* Mobile Sidebar Overlay */}
      {sidebarOpen && (
        <div className="lg:hidden fixed inset-0 z-40 flex">
          <div
            className="absolute inset-0 bg-black/40"
            onClick={() => setSidebarOpen(false)}
          />
          <div className="relative w-72 bg-white h-full shadow-2xl flex flex-col">
            <SidebarContent
              nav={nav}
              onClose={() => setSidebarOpen(false)}
              onLogout={handleLogout}
            />
          </div>
        </div>
      )}

      {/* Main content */}
      <div className="flex flex-col flex-1 min-w-0 h-full overflow-hidden">
        {/* TopNav */}
        <header className="bg-white border-b border-slate-200 px-4 lg:px-6 py-3 flex items-center justify-between shrink-0">
          <div className="flex items-center gap-3">
            <button
              className="lg:hidden p-2 rounded-lg hover:bg-slate-100 text-slate-500"
              onClick={() => setSidebarOpen(true)}
            >
              <svg
                width="20"
                height="20"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                viewBox="0 0 24 24"
              >
                <line x1="3" y1="6" x2="21" y2="6" />
                <line x1="3" y1="12" x2="21" y2="12" />
                <line x1="3" y1="18" x2="21" y2="18" />
              </svg>
            </button>
            <span className="font-semibold text-slate-800 text-sm hidden sm:block">
              Course Registration System
            </span>
          </div>
          <div className="flex items-center gap-3">
            <span
              className={`hidden sm:inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium ${roleColors[user?.role ?? "student"]}`}
            >
              {roleLabel}
            </span>
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center text-white text-xs font-bold shrink-0">
                {user?.fullName?.charAt(0) ?? "U"}
              </div>
              <div className="hidden sm:block min-w-0">
                <p className="text-sm font-medium text-slate-800 truncate max-w-32">
                  {user?.fullName}
                </p>
              </div>
            </div>
          </div>
        </header>

        {/* Page content */}
        <main className="flex-1 overflow-y-auto p-4 lg:p-6">{children}</main>
      </div>
    </div>
  )
}

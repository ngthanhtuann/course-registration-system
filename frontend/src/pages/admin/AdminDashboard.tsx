import { useEffect, useState } from "react"
import { useNavigate } from "react-router-dom"
import { Card, StatCard, SectionHeader } from "../../components/ui"
import { api } from "../../services/api"
export default function AdminDashboard() {
  const nav = useNavigate()
  const [d, setD] = useState<any>({})
  const [error, setError] = useState("")
  useEffect(() => {
    api.admin
      .dashboard()
      .then(setD)
      .catch((e) => setError(e.message))
  }, [])
  const links = [
    ["Manage Users", "/admin/users", "👤"],
    ["Manage Courses", "/admin/courses", "📚"],
    ["Manage Semesters", "/admin/semesters", "📅"],
    ["Registration Period", "/admin/registration-period", "🗓️"],
    ["Reg. Demand", "/admin/registration-demand", "📊"],
    ["Assign Lecturer", "/admin/assign-lecturer", "🎓"],
  ]
  return (
    <div>
      <SectionHeader
        title="Admin Dashboard"
        subtitle={
          d.active_semester
            ? `Active Semester: ${d.active_semester.semester_name}`
            : "No active semester"
        }
      />
      {error && <p className="mb-4 text-sm text-red-600">{error}</p>}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        <StatCard
          label="Total Students"
          value={d.total_students ?? 0}
          color="blue"
          icon={<span>👥</span>}
        />
        <StatCard
          label="Active Lecturers"
          value={d.active_lecturers ?? 0}
          color="purple"
          icon={<span>🎓</span>}
        />
        <StatCard
          label="Total Courses"
          value={d.total_courses ?? 0}
          color="green"
          icon={<span>📚</span>}
        />
        <StatCard
          label="Registrations"
          value={d.active_registrations ?? 0}
          color="yellow"
          icon={<span>✓</span>}
        />
      </div>
      <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
        {links.map(([label, path, icon]) => (
          <button
            key={path}
            onClick={() => nav(path)}
            className="flex items-center gap-3 p-4 bg-white rounded-xl border border-slate-200 hover:border-blue-300 hover:shadow-sm text-left"
          >
            <div className="w-10 h-10 bg-blue-600 rounded-lg flex items-center justify-center text-lg">
              {icon}
            </div>
            <span className="text-sm font-medium text-slate-700">{label}</span>
          </button>
        ))}
      </div>
      <Card className="p-5 mt-6">
        <p className="text-sm text-slate-500">
          The dashboard values are loaded directly from PostgreSQL through the
          Flask API.
        </p>
      </Card>
    </div>
  )
}

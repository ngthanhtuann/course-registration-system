import { useEffect, useState } from "react"
import { useNavigate } from "react-router-dom"
import { Card, StatCard, SectionHeader, Badge, Alert } from "../../components/ui"
import { api } from "../../services/api"
import type { Student } from "../../types"
export default function StudentDashboard({ user }: { user: Student }) {
  const nav = useNavigate()
  const [regs, setRegs] = useState<any[]>([])
  const [periods, setPeriods] = useState<any[]>([])
  const [curr, setCurr] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState("")
  useEffect(() => {
    let active = true
    Promise.all([
      api.student.registrations(),
      api.student.periods(),
      api.student.curriculum(),
    ])
      .then(([r, p, c]) => {
        if (!active) return
        setRegs(r)
        setPeriods(p)
        setCurr(c)
      })
      .catch((e) => {
        if (active) setError(e.message || "Could not load dashboard.")
      })
      .finally(() => { if (active) setLoading(false) })
    return () => { active = false }
  }, [])
  const active = periods.find((p) => p.current_status === "open")
  const activeRegs = regs.filter((r) => r.status === "Registered")
  return (
    <div>
      <SectionHeader
        title="Student Dashboard"
        subtitle={`Welcome, ${user.fullName} · Major: ${user.major}`}
      />
      {error && <div className="mb-4"><Alert type="error" message={error} /></div>}
      {loading && <Card className="p-5 mb-4">Loading dashboard...</Card>}
      {!loading && !error && <>
      <div className="grid grid-cols-2 lg:grid-cols-3 gap-4 mb-6">
        <StatCard
          label="Curriculum Courses"
          value={curr.length}
          color="blue"
          icon={<span>📚</span>}
        />
        <StatCard
          label="Registered Courses"
          value={activeRegs.length}
          color="green"
          icon={<span>✓</span>}
        />
        <StatCard
          label="Registration Period"
          value={active ? "Open" : "Closed"}
          color="yellow"
          icon={<span>🗓️</span>}
        />
      </div>
      <Card className="p-5 mb-4">
        <h3 className="font-semibold text-slate-800">Registration Period</h3>
        <p className="text-sm text-slate-500 mt-1">
          {active
            ? `${active.start_date} → ${active.end_date}`
            : "There is currently no open registration period."}
        </p>
        {active && (
          <div className="mt-2">
            <Badge label="Open" />
          </div>
        )}
      </Card>
      </>}
      <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
        {[
          ["View Courses", "/student/courses"],
          ["Register Course", "/student/register"],
          ["Registration Status", "/student/status"],
          ["Drop Course", "/student/drop"],
          ["View Grades", "/student/grades"],
        ].map(([x, p]) => (
          <button
            key={p}
            onClick={() => nav(p)}
            className="p-4 bg-white border rounded-xl text-left hover:border-blue-300"
          >
            <span className="text-sm font-medium text-slate-700">{x}</span>
          </button>
        ))}
      </div>
    </div>
  )
}

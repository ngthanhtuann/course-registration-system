import { useEffect, useState } from "react"
import { Card, StatCard, SectionHeader, Badge, Alert } from "../../components/ui"
import { api } from "../../services/api"
import type { Lecturer } from "../../types"
export default function Dashboard({ user }: { user: Lecturer }) {
  const [courses, setCourses] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState("")
  useEffect(() => {
    let active = true
    api.lecturer
      .semesters()
      .then((x) => x[0] ? api.lecturer.teachingCourses(x[0].semester_id) : [])
      .then((data) => { if (active) setCourses(data) })
      .catch((e) => {
        if (active) setError(e.message || "Could not load teaching courses.")
      })
      .finally(() => { if (active) setLoading(false) })
    return () => { active = false }
  }, [])
  const total = courses.reduce((s, c) => s + Number(c.student_count || 0), 0)
  return (
    <div>
      <SectionHeader
        title="Lecturer Dashboard"
        subtitle={`Welcome, ${user.fullName}`}
      />
      {error && <div className="mb-4"><Alert type="error" message={error} /></div>}
      {loading && <Card className="p-5 mb-4">Loading dashboard...</Card>}
      {!loading && !error && <div className="grid grid-cols-2 gap-4 mb-6">
        <StatCard
          label="Teaching Courses"
          value={courses.length}
          color="blue"
          icon={<span>📚</span>}
        />
        <StatCard
          label="Registered Students"
          value={total}
          color="green"
          icon={<span>👥</span>}
        />
      </div>}
      <Card className="p-5">
        <h3 className="font-semibold text-slate-800 mb-3">
          Teaching Qualifications
        </h3>
        <div className="flex flex-wrap gap-2">
          {user.qualifications.length ? (
            user.qualifications.map((q) => <Badge key={q} label={q} />)
          ) : (
            <span className="text-sm text-slate-400">
              No qualifications assigned.
            </span>
          )}
        </div>
      </Card>
      {!loading && !error && <Card className="p-5 mt-4">
        <h3 className="font-semibold text-slate-800 mb-3">
          Current Teaching Courses
        </h3>
        {courses.length ? (
          <div className="space-y-2">
            {courses.map((c) => (
              <div
                key={c.assignment_id}
                className="flex justify-between bg-slate-50 rounded-lg p-3"
              >
                <span className="font-medium">
                  {c.course_code} — {c.course_name}
                </span>
                <span className="text-sm text-slate-500">
                  {c.student_count} students
                </span>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-sm text-slate-400">
            No teaching assignments for the selected semester.
          </p>
        )}
      </Card>}
    </div>
  )
}

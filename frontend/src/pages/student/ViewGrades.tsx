import { useEffect, useState } from "react"
import {
  Card,
  Select,
  Badge,
  DataTable,
  SectionHeader,
  StatCard,
} from "../../components/ui"
import type { Column } from "../../components/ui"
import { api } from "../../services/api"
import type { Student } from "../../types"
export default function ViewGrades({ user: _user }: { user: Student }) {
  const [sems, setSems] = useState<any[]>([])
  const [semester, setSemester] = useState("")
  const [rows, setRows] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState("")
  useEffect(() => {
    let active = true
    api.student
      .semesters()
      .then((s) => {
        if (!active) return
        setSems(s)
        if (s[0]) setSemester(s[0].semester_id)
        else setLoading(false)
      })
      .catch((e) => {
        if (!active) return
        setError(e.message || "Could not load semesters.")
        setLoading(false)
      })
    return () => { active = false }
  }, [])
  useEffect(() => {
    if (!semester) return
    let active = true
    setLoading(true)
    setError("")
    api.student.grades(semester)
      .then((data) => { if (active) setRows(data) })
      .catch((e) => {
        if (active) setError(e.message || "Could not load grades.")
      })
      .finally(() => { if (active) setLoading(false) })
    return () => { active = false }
  }, [semester])
  const passed = rows.filter((r) => r.result_status === "passed")
  const graded = rows.filter((r) => r.grade !== null)
  const avg = graded.length
    ? (graded.reduce((s, r) => s + Number(r.grade), 0) / graded.length).toFixed(
        1,
      )
    : "N/A"
  const cols: Column<any>[] = [
    {
      key: "course_code",
      header: "Course Code",
      render: (r) => <span className="font-mono text-xs">{r.course_code}</span>,
    },
    { key: "course_name", header: "Course Name" },
    { key: "credit", header: "Credits" },
    {
      key: "grade",
      header: "Grade",
      render: (r) =>
        r.grade === null ? (
          <span className="text-slate-400">Not Entered</span>
        ) : (
          <b>{r.grade}</b>
        ),
    },
    {
      key: "result_status",
      header: "Result",
      render: (r) => (
        <Badge
          label={r.result_status ? String(r.result_status) : "Not Entered"}
        />
      ),
    },
  ]
  return (
    <div>
      <SectionHeader
        title="View Grades"
        subtitle="Your academic grades by semester"
      />
      <Card className="p-4 mb-4">
        <Select
          label="Select Semester"
          options={sems.map((s) => ({
            value: s.semester_id,
            label: s.semester_name,
          }))}
          value={semester}
          onChange={(e) => {
            setSemester(e.target.value)
            setRows([])
            setLoading(!!e.target.value)
            setError("")
          }}
        />
      </Card>
      {!loading && !error && <div className="grid grid-cols-3 gap-4 mb-4">
        <StatCard
          label="Courses Passed"
          value={passed.length}
          color="green"
          icon={<span>✓</span>}
        />
        <StatCard
          label="Credits Earned"
          value={passed.reduce((s, r) => s + Number(r.credit), 0)}
          color="blue"
          icon={<span>📚</span>}
        />
        <StatCard
          label="Average Grade"
          value={avg}
          color="purple"
          icon={<span>★</span>}
        />
      </div>}
      <Card>
        <DataTable
          columns={cols}
          rows={rows}
          loading={loading}
          error={error}
          keyFn={(r) => r.course_code}
          emptyText="No grades available for this semester."
        />
      </Card>
    </div>
  )
}

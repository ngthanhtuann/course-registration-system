import { useEffect, useState } from "react"
import {
  Card,
  Select,
  Badge,
  DataTable,
  SectionHeader,
} from "../../components/ui"
import type { Column } from "../../components/ui"
import { api } from "../../services/api"
import type { Student } from "../../types"
export default function ViewRegistrationStatus({
  user: _user,
}: {
  user: Student
}) {
  const [sems, setSems] = useState<any[]>([])
  const [semester, setSemester] = useState("")
  const [rows, setRows] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState("")
  useEffect(() => {
    let active = true
    api.student.semesters()
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
    api.student.registrations(semester)
      .then((data) => { if (active) setRows(data) })
      .catch((e) => {
        if (active) setError(e.message || "Could not load registrations.")
      })
      .finally(() => { if (active) setLoading(false) })
    return () => { active = false }
  }, [semester])
  const periods = Array.from(new Map(
    rows.filter((r) => r.period_id).map((r) => [r.period_id, r]),
  ).values())
  const cols: Column<any>[] = [
    {
      key: "course_code",
      header: "Course Code",
      render: (r) => <span className="font-mono text-xs">{r.course_code}</span>,
    },
    { key: "course_name", header: "Course Name" },
    { key: "credit", header: "Credits" },
    {
      key: "period_name",
      header: "Registration Period",
      render: (r) => r.period_name || r.period_id || "—",
    },
    {
      key: "status",
      header: "Registration Status",
      render: (r) => <Badge label={r.status} />,
    },
  ]
  return (
    <div>
      <SectionHeader
        title="Registration Status"
        subtitle="Your course registrations by semester"
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
          placeholder="Select semester"
        />
      </Card>
      {!loading && !error && periods.map((period) => (
        <Card key={period.period_id} className="p-4 mb-4">
          <div className="flex justify-between">
            <div>
              <p className="font-semibold">{period.period_name || "Registration Period"}</p>
              <p className="text-xs text-slate-500">
                {period.registration_start_date} → {period.registration_end_date}
              </p>
              <p className="text-xs text-slate-500">
                Drop Period: {period.drop_start_date} → {period.drop_end_date}
              </p>
            </div>
            <Badge
              label={
                period.current_registration_status === "open"
                  ? "Open"
                  : period.current_registration_status === "upcoming"
                    ? "Scheduled"
                    : "Closed"
              }
            />
          </div>
        </Card>
      ))}
      <Card>
        <DataTable
          columns={cols}
          rows={rows}
          loading={loading}
          error={error}
          keyFn={(r) => r.registration_id}
          emptyText="No registrations found for this semester."
        />
      </Card>
    </div>
  )
}

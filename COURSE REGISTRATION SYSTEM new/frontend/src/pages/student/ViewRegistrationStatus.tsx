import { useEffect, useState } from "react"
import {
  Card,
  Select,
  Badge,
  DataTable,
  SectionHeader,
} from "../../components/ui"
import type { Column } from "../../components/ui"
import { api } from "../../api"
import type { Student } from "../../types"
export default function ViewRegistrationStatus({
  user: _user,
}: {
  user: Student
}) {
  const [sems, setSems] = useState<any[]>([])
  const [semester, setSemester] = useState("")
  const [rows, setRows] = useState<any[]>([])
  const [period, setPeriod] = useState<any>(null)
  useEffect(() => {
    Promise.all([api.student.semesters(), api.student.periods()])
      .then(([s, p]) => {
        setSems(s)
        if (s[0]) setSemester(s[0].semester_id)
        if (p[0]) setPeriod(p[0])
      })
      .catch(() => {})
  }, [])
  useEffect(() => {
    if (semester) {
      api.student
        .registrations(semester)
        .then(setRows)
        .catch(() => setRows([]))
      api.student
        .periods()
        .then((p) =>
          setPeriod(p.find((x) => x.semester_id === semester) || null),
        )
    }
  }, [semester])
  const cols: Column<any>[] = [
    {
      key: "course_code",
      header: "Course Code",
      render: (r) => <span className="font-mono text-xs">{r.course_code}</span>,
    },
    { key: "course_name", header: "Course Name" },
    { key: "credit", header: "Credits" },
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
          onChange={(e) => setSemester(e.target.value)}
          placeholder="Select semester"
        />
      </Card>
      {period && (
        <Card className="p-4 mb-4">
          <div className="flex justify-between">
            <div>
              <p className="font-semibold">Registration Period</p>
              <p className="text-xs text-slate-500">
                {period.start_date} → {period.end_date}
              </p>
            </div>
            <Badge
              label={
                period.current_status === "open"
                  ? "Open"
                  : period.current_status === "upcoming"
                    ? "Scheduled"
                    : "Closed"
              }
            />
          </div>
        </Card>
      )}
      <Card>
        <DataTable
          columns={cols}
          rows={rows}
          keyFn={(r) => r.registration_id}
          emptyText="No registrations found for this semester."
        />
      </Card>
    </div>
  )
}

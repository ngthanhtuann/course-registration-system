import { useEffect, useState } from "react"
import {
  Card,
  Button,
  Select,
  Badge,
  DataTable,
  SectionHeader,
  Modal,
  Alert,
} from "../../components/ui"
import type { Column } from "../../components/ui"
import { api } from "../../services/api"
export default function ManageRegistrationDemand() {
  const [periods, setPeriods] = useState<any[]>([])
  const [majors, setMajors] = useState<any[]>([])
  const [period, setPeriod] = useState("")
  const [major, setMajor] = useState("")
  const [course, setCourse] = useState("")
  const [rows, setRows] = useState<any[]>([])
  const [students, setStudents] = useState<any[]>([])
  const [msg] = useState("")
  const [err, setErr] = useState("")
  useEffect(() => {
    Promise.all([api.admin.periods(), api.admin.majors()])
      .then(([p, m]) => {
        setPeriods(p)
        setMajors(m)
      })
      .catch((e) => setErr(e.message))
  }, [])
  const load = () => {
    if (!period) return
    api.admin
      .demand(period, major)
      .then(setRows)
      .catch((e) => setErr(e.message))
  }
  useEffect(load, [period, major])
  const view = async (code: string) => {
    try {
      setCourse(code)
      setStudents(await api.admin.demandStudents(code, period, major))
    } catch (e: any) {
      setErr(e.message)
    }
  }
  const cols: Column<any>[] = [
    {
      key: "course_code",
      header: "Course Code",
      render: (r) => <span className="font-mono text-xs">{r.course_code}</span>,
    },
    { key: "course_name", header: "Course Name" },
    { key: "registered_students", header: "Registered Students" },
    {
      key: "actions",
      header: "Details",
      render: (r) => (
        <Button size="sm" variant="ghost" onClick={() => view(r.course_code)}>
          View Students
        </Button>
      ),
    },
  ]
  return (
    <div>
      <SectionHeader
        title="Registration Demand"
        subtitle="Review demand from registrations and use it for class planning"
      />
      <Card className="p-4 mb-4">
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <Select
            label="Registration Period"
            options={periods.map((p) => ({
              value: p.period_id,
              label: `${p.period_name} — ${p.semester_name}`,
            }))}
            value={period}
            onChange={(e) => setPeriod(e.target.value)}
            placeholder="Select period"
          />
          <Select
            label="Major"
            options={majors.map((m) => ({
              value: m.major_code,
              label: m.major_name,
            }))}
            value={major}
            onChange={(e) => setMajor(e.target.value)}
            placeholder="All majors"
          />
        </div>
      </Card>
      {msg && <Alert type="success" message={msg} />}{" "}
      {err && (
        <div className="mb-3">
          <Alert type="error" message={err} />
        </div>
      )}
      <Card>
        <DataTable
          columns={cols}
          rows={rows}
          keyFn={(r) => r.course_code}
          emptyText="No registration demand found."
        />
      </Card>
      <Modal
        open={!!course}
        onClose={() => setCourse("")}
        title={`Registered Students — ${course}`}
        size="sm"
        footer={
          <Button variant="secondary" onClick={() => setCourse("")}>
            Close
          </Button>
        }
      >
        <DataTable
          columns={[
            { key: "student_id", header: "Student ID" },
            { key: "fullname", header: "Name" },
            { key: "email", header: "Email" },
            {
              key: "registration_status",
              header: "Status",
              render: (r) => <Badge label={r.registration_status} />,
            },
          ]}
          rows={students}
          keyFn={(r) => r.student_id}
          emptyText="No students registered."
        />
      </Modal>
    </div>
  )
}

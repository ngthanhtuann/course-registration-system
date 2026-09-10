import { useEffect, useState } from "react"
import {
  Card,
  Badge,
  DataTable,
  SectionHeader,
  ConfirmDialog,
  Button,
  Alert,
} from "../../components/ui"
import type { Column } from "../../components/ui"
import { api } from "../../services/api"
import type { Student } from "../../types"
interface Props {
  user: Student
}
export default function CourseRegistration({ user }: Props) {
  const [, setPeriods] = useState<any[]>([])
  const [period, setPeriod] = useState<any>(null)
  const [rows, setRows] = useState<any[]>([])
  const [confirm, setConfirm] = useState<any>(null)
  const [msg, setMsg] = useState("")
  const [err, setErr] = useState("")
  const load = async () => {
    try {
      const p = await api.student.periods()
      setPeriods(p)
      const open = p.find((x) => x.current_status === "open")
      setPeriod(open || p[0] || null)
      if (open) setRows(await api.student.courses(open.period_id))
    } catch (e: any) {
      setErr(e.message)
    }
  }
  useEffect(() => {
    load()
  }, [])
  useEffect(() => {
    if (period)
      api.student
        .courses(period.period_id)
        .then(setRows)
        .catch((e) => setErr(e.message))
  }, [period])
  const register = async () => {
    if (!confirm || !period) return
    try {
      await api.student.register(confirm.course_code, period.period_id)
      setMsg("Course registered successfully.")
      setConfirm(null)
      setRows(await api.student.courses(period.period_id))
    } catch (e: any) {
      setErr(e.message)
      setConfirm(null)
    }
  }
  const cols: Column<any>[] = [
    {
      key: "course_code",
      header: "Course Code",
      render: (r) => <span className="font-mono text-xs">{r.course_code}</span>,
    },
    { key: "course_name", header: "Course Name" },
    { key: "credit", header: "Credits" },
    {
      key: "available_seats",
      header: "Available Seats",
      render: (r) => (
        <span
          className={
            Number(r.available_seats) <= 0 ? "text-red-600" : "text-green-600"
          }
        >
          {r.available_seats}
        </span>
      ),
    },
    {
      key: "prerequisite_status",
      header: "Prerequisite",
      render: (r) => (
        <Badge
          label={
            r.prerequisite_status === "N/A"
              ? "Satisfied"
              : r.prerequisite_status
          }
        />
      ),
    },
    {
      key: "action",
      header: "Action",
      render: (r) => (
        <Button
          size="sm"
          disabled={
            !period ||
            period.current_status !== "open" ||
            r.reg_status === "Registered" ||
            Number(r.available_seats) <= 0 ||
            r.prerequisite_status === "Not Satisfied"
          }
          onClick={() => setConfirm(r)}
        >
          {r.reg_status === "Registered"
            ? "Registered"
            : Number(r.available_seats) <= 0
              ? "Full"
              : "Register"}
        </Button>
      ),
    },
  ]
  return (
    <div>
      <SectionHeader
        title="Course Registration"
        subtitle={`Major: ${user.major}`}
      />
      {period && (
        <Card className="p-4 mb-4">
          <div className="flex justify-between">
            <div>
              <p className="font-semibold">{period.period_name}</p>
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
      {msg && (
        <div className="mb-3">
          <Alert type="success" message={msg} />
        </div>
      )}
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
          emptyText="No courses available for registration."
        />
      </Card>
      <ConfirmDialog
        open={!!confirm}
        onClose={() => setConfirm(null)}
        onConfirm={register}
        title="Confirm Registration"
        message={`Register for ${confirm?.course_code} — ${confirm?.course_name}?`}
        confirmLabel="Register"
        variant="primary"
      />
    </div>
  )
}

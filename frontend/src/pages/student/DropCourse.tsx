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
export default function DropCourse({ user: _user }: { user: Student }) {
  const [rows, setRows] = useState<any[]>([])
  const [confirm, setConfirm] = useState<any>(null)
  const [msg, setMsg] = useState("")
  const [err, setErr] = useState("")
  const [loading, setLoading] = useState(true)
  const [loadError, setLoadError] = useState("")
  useEffect(() => {
    let active = true
    api.student
      .registrations()
      .then((r) => {
        if (active) setRows(r.filter((x) => x.status === "Registered"))
      })
      .catch((e) => {
        if (active) setLoadError(e.message || "Could not load registrations.")
      })
      .finally(() => { if (active) setLoading(false) })
    return () => { active = false }
  }, [])
  const drop = async () => {
    if (!confirm) return false
    setMsg("")
    setErr("")
    try {
      await api.student.drop(confirm.registration_id)
      setRows((current) => current.filter((r) => r.registration_id !== confirm.registration_id))
      setConfirm(null)
      setMsg("Course dropped successfully.")
      return true
    } catch (e: any) {
      setErr(e.message || "Could not drop the course.")
      return false
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
      key: "drop_start_date",
      header: "Drop Period",
      render: (r) => `${r.drop_start_date} → ${r.drop_end_date}`,
    },
    {
      key: "status",
      header: "Status",
      render: (r) => <Badge label={r.status} />,
    },
    {
      key: "action",
      header: "Action",
      render: (r) => (
        <Button
          size="sm"
          variant="danger"
          onClick={() => setConfirm(r)}
          disabled={r.current_drop_status !== "open"}
        >
          Drop
        </Button>
      ),
    },
  ]
  return (
    <div>
      <SectionHeader
        title="Drop Course"
        subtitle="Drop registered courses during their allowed drop period"
      />
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
          loading={loading}
          error={loadError}
          keyFn={(r) => r.registration_id}
          emptyText="No active registrations."
        />
      </Card>
      <ConfirmDialog
        open={!!confirm}
        onClose={() => setConfirm(null)}
        onConfirm={drop}
        title="Drop Course"
        message={`Drop ${confirm?.course_code} — ${confirm?.course_name}?`}
        confirmLabel="Drop"
      />
    </div>
  )
}

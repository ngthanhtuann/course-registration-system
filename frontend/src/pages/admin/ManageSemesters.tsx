import { useEffect, useState } from "react"
import {
  Card,
  Button,
  Input,
  DataTable,
  SectionHeader,
  Modal,
  ConfirmDialog,
  Alert,
} from "../../components/ui"
import type { Column } from "../../components/ui"
import { api } from "../../services/api"
import type { Semester } from "../../types"
const map = (x: any): Semester => ({
  id: x.semester_id,
  name: x.semester_name,
  startDate: String(x.start_date).slice(0, 10),
  endDate: String(x.end_date).slice(0, 10),
  status:
    String(x.status || "upcoming").toLowerCase() === "active"
      ? "Active"
      : String(x.status || "upcoming").toLowerCase() === "completed"
        ? "Completed"
        : "Upcoming",
})
export default function ManageSemester() {
  const [rows, setRows] = useState<Semester[]>([])
  const [modal, setModal] = useState<"create" | "edit" | null>(null)
  const [selected, setSelected] = useState<Semester | null>(null)
  const [del, setDel] = useState<Semester | null>(null)
  const [form, setForm] = useState({ id: "", name: "", start: "", end: "" })
  const [msg, setMsg] = useState("")
  const [err, setErr] = useState("")
  const [loading, setLoading] = useState(true)
  const [loadError, setLoadError] = useState("")
  const load = async () => {
    setLoading(true)
    setLoadError("")
    try {
      const x = await api.admin.semesters()
      setRows(x.map(map))
    } catch (e: any) {
      setLoadError(e.message)
    } finally {
      setLoading(false)
    }
  }
  useEffect(() => {
    void load()
  }, [])
  const save = async () => {
    try {
      setErr("")
      if (!form.name || !form.start || !form.end)
        throw new Error("All semester fields are required.")
      if (modal === "create")
        await api.admin.createSemester({
          semester_id: form.id || undefined,
          semester_name: form.name,
          start_date: form.start,
          end_date: form.end,
        })
      else if (selected)
        await api.admin.updateSemester(selected.id, {
          semester_name: form.name,
          start_date: form.start,
          end_date: form.end,
        })
      setModal(null)
      setMsg("Semester saved successfully.")
      load()
    } catch (e: any) {
      setErr(e.message)
    }
  }
  const remove = async () => {
    if (!del) return
    try {
      await api.admin.deleteSemester(del.id)
      setDel(null)
      setMsg("Semester deleted successfully.")
      load()
    } catch (e: any) {
      setErr(e.message)
      throw e
    }
  }
  const cols: Column<Semester>[] = [
    {
      key: "id",
      header: "Semester ID",
      render: (r) => <span className="font-mono text-xs">{r.id}</span>,
    },
    {
      key: "name",
      header: "Semester",
      render: (r) => <span className="font-medium">{r.name}</span>,
    },
    { key: "startDate", header: "Start Date" },
    { key: "endDate", header: "End Date" },
    {
      key: "status",
      header: "Status",
      render: (r) => <span className="capitalize">{r.status}</span>,
    },
    {
      key: "actions",
      header: "Actions",
      render: (r) => (
        <div className="flex gap-1">
          <Button
            size="sm"
            variant="secondary"
            onClick={() => {
              setSelected(r)
              setForm({
                id: r.id,
                name: r.name,
                start: r.startDate,
                end: r.endDate,
              })
              setModal("edit")
            }}
          >
            Edit
          </Button>
          <Button size="sm" variant="danger" onClick={() => setDel(r)}>
            Delete
          </Button>
        </div>
      ),
    },
  ]
  return (
    <div>
      <SectionHeader
        title="Manage Semester"
        subtitle="Create and maintain academic semesters"
        actions={
          <Button
            size="sm"
            onClick={() => {
              setForm({ id: "", name: "", start: "", end: "" })
              setModal("create")
            }}
          >
            + Semester
          </Button>
        }
      />
      {msg && <Alert type="success" message={msg} />}{" "}
      {err && (
        <div className="my-3">
          <Alert type="error" message={err} />
        </div>
      )}
      <Card className="mt-4">
        <DataTable
          loading={loading}
          error={loadError}
          columns={cols}
          rows={rows}
          keyFn={(r) => r.id}
          emptyText="No semesters found."
        />
      </Card>
      <Modal
        open={!!modal}
        onClose={() => setModal(null)}
        title={modal === "create" ? "Create Semester" : "Edit Semester"}
        footer={
          <>
            <Button variant="secondary" onClick={() => setModal(null)}>
              Cancel
            </Button>
            <Button onClick={save}>Save</Button>
          </>
        }
      >
        <div className="grid gap-4">
          {modal === "create" && (
            <Input
              label="Semester ID (optional)"
              value={form.id}
              onChange={(e) => setForm({ ...form, id: e.target.value })}
            />
          )}
          <Input
            label="Semester Name"
            value={form.name}
            onChange={(e) => setForm({ ...form, name: e.target.value })}
          />
          <Input
            label="Start Date"
            type="date"
            value={form.start}
            onChange={(e) => setForm({ ...form, start: e.target.value })}
          />
          <Input
            label="End Date"
            type="date"
            value={form.end}
            onChange={(e) => setForm({ ...form, end: e.target.value })}
          />
        </div>
      </Modal>
      <ConfirmDialog
        open={!!del}
        onClose={() => setDel(null)}
        onConfirm={remove}
        title="Delete Semester"
        message={`Delete ${del?.name}? Existing registration periods or assignments may prevent deletion.`}
        confirmLabel="Delete"
      />
    </div>
  )
}

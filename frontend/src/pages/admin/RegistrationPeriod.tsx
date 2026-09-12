import { useEffect, useState } from "react"
import {
  Card,
  Button,
  Input,
  Select,
  Badge,
  SectionHeader,
  Alert,
  DataTable,
  ConfirmDialog,
} from "../../components/ui"
import type { Column } from "../../components/ui"
import { api } from "../../services/api"
import { useAdminList } from "../../services/useAdminList"
import type { Semester, RegistrationPeriod } from "../../types"
const mapS = (x: any): Semester => ({
  id: x.semester_id,
  name: x.semester_name,
  startDate: String(x.start_date).slice(0, 10),
  endDate: String(x.end_date).slice(0, 10),
  status: "Upcoming",
})
const mapP = (x: any): RegistrationPeriod => ({
  id: x.period_id,
  semesterId: x.semester_id,
  startDateTime: String(x.start_date).slice(0, 10),
  endDateTime: String(x.end_date).slice(0, 10),
  dropStartDateTime: String(x.drop_start_date).slice(0, 10),
  dropEndDateTime: String(x.drop_end_date).slice(0, 10),
  status:
    x.current_status === "open"
      ? "Open"
      : x.current_status === "upcoming"
        ? "Scheduled"
        : "Closed",
  periodName: x.period_name || "Registration Period",
})
export default function ManageRegistrationPeriod() {
  const semesterList = useAdminList("semesters")
  const sems = semesterList.data.map(mapS)
  const [rows, setRows] = useState<RegistrationPeriod[]>([])
  const [selected, setSelected] = useState("")
  const [form, setForm] = useState({
    id: "",
    name: "Registration Period",
    start: "",
    end: "",
    dropStart: "",
    dropEnd: "",
  })
  const [edit, setEdit] = useState<string | null>(null)
  const [del, setDel] = useState<RegistrationPeriod | null>(null)
  const [msg, setMsg] = useState("")
  const [err, setErr] = useState("")
  const [loading, setLoading] = useState(true)
  const [loadError, setLoadError] = useState("")
  const [saving, setSaving] = useState(false)
  const load = async () => {
    setLoading(true)
    setLoadError("")
    try {
      const [s, p] = await Promise.all([api.admin.semesters(), api.admin.periods()])
      setSems(s.map(mapS))
      setRows(p.map(mapP))
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
    if (saving) return
    setSaving(true)
    try {
      setErr("")
      if (!selected || !form.start || !form.end || !form.dropStart || !form.dropEnd)
        throw new Error("Semester and all four registration/drop dates are required.")
      if (form.start >= form.end || form.dropStart >= form.dropEnd)
        throw new Error("Each end date must be after its corresponding start date.")
      const semester = sems.find((s) => s.id === selected)
      if (!semester || [form.start, form.end, form.dropStart, form.dropEnd].some(
        (date) => date < semester.startDate || date > semester.endDate,
      )) throw new Error("Registration and drop dates must be within the selected semester.")
      const p = {
        semester_id: selected,
        period_id: form.id || undefined,
        period_name: form.name || "Registration Period",
        start_date: form.start,
        end_date: form.end,
        drop_start_date: form.dropStart,
        drop_end_date: form.dropEnd,
      }
      if (edit) await api.admin.updatePeriod(edit, p)
      else await api.admin.createPeriod(p)
      setMsg("Registration period saved successfully.")
      setEdit(null)
      setSelected("")
      setForm({ id: "", name: "Registration Period", start: "", end: "", dropStart: "", dropEnd: "" })
      load()
    } catch (e: any) {
      setErr(e.message)
    } finally {
      setSaving(false)
    }
  }
  const remove = async () => {
    if (!del) return
    try {
      await api.admin.deletePeriod(del.id)
      setDel(null)
      setMsg("Registration period deleted.")
      load()
    } catch (e: any) {
      setErr(e.message)
      throw e
    }
  }
  const cols: Column<RegistrationPeriod>[] = [
    {
      key: "id",
      header: "Period ID",
      render: (r) => <span className="font-mono text-xs">{r.id}</span>,
    },
    {
      key: "semesterId",
      header: "Semester",
      render: (r) =>
        sems.find((s) => s.id === r.semesterId)?.name || r.semesterId,
    },
    { key: "startDateTime", header: "Registration Start" },
    { key: "endDateTime", header: "Registration End" },
    { key: "dropStartDateTime", header: "Drop Start" },
    { key: "dropEndDateTime", header: "Drop End" },
    {
      key: "status",
      header: "Status",
      render: (r) => <Badge label={r.status} />,
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
              setEdit(r.id)
              setSelected(r.semesterId)
              setForm({
                id: r.id,
                name: (r as any).periodName || "Registration Period",
                start: r.startDateTime,
                end: r.endDateTime,
                dropStart: r.dropStartDateTime,
                dropEnd: r.dropEndDateTime,
              })
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
        title="Registration Period"
        subtitle="Configure separate course registration and drop periods"
      />
      <Card className="p-4 mb-5">
        <h3 className="font-semibold text-slate-800 mb-4">
          {edit ? "Edit" : "Create"} Registration Period
        </h3>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <Select
            label="Semester"
            options={sems.map((s) => ({ value: s.id, label: s.name }))}
            value={selected}
            onChange={(e) => setSelected(e.target.value)}
            placeholder="Select semester"
          />
          <Input
            label="Period Name"
            value={form.name}
            onChange={(e) => setForm({ ...form, name: e.target.value })}
          />
          {!edit && (
            <Input
              label="Period ID (optional)"
              value={form.id}
              onChange={(e) => setForm({ ...form, id: e.target.value })}
            />
          )}
          <Input
            label="Registration Start Date"
            type="date"
            value={form.start}
            onChange={(e) => setForm({ ...form, start: e.target.value })}
          />
          <Input
            label="Registration End Date"
            type="date"
            value={form.end}
            onChange={(e) => setForm({ ...form, end: e.target.value })}
          />
          <Input
            label="Drop Start Date"
            type="date"
            value={form.dropStart}
            onChange={(e) => setForm({ ...form, dropStart: e.target.value })}
          />
          <Input
            label="Drop End Date"
            type="date"
            value={form.dropEnd}
            onChange={(e) => setForm({ ...form, dropEnd: e.target.value })}
          />
        </div>
        <div className="mt-4 flex gap-2">
          <Button disabled={saving || loading || !!loadError} onClick={save}>{saving ? "Saving…" : edit ? "Update" : "Create"}</Button>
          {edit && (
            <Button
              variant="secondary"
              onClick={() => {
                setEdit(null)
                setSelected("")
                setForm({
                  id: "",
                  name: "Registration Period",
                  start: "",
                  end: "",
    dropStart: "",
    dropEnd: "",
                })
              }}
            >
              Cancel
            </Button>
          )}
        </div>
      </Card>
      {msg && <Alert type="success" message={msg} />}{" "}
      {(err || semesterList.error) && (
        <div className="my-3">
          <Alert type="error" message={err || semesterList.error} />
        </div>
      )}
      <Card>
        <DataTable
          loading={loading}
          error={loadError}
          columns={cols}
          rows={rows}
          keyFn={(r) => r.id}
          emptyText="No registration periods found."
        />
      </Card>
      <ConfirmDialog
        open={!!del}
        onClose={() => setDel(null)}
        onConfirm={remove}
        title="Delete Registration Period"
        message={`Delete period ${del?.id}? Existing registrations may prevent deletion.`}
        confirmLabel="Delete"
      />
    </div>
  )
}

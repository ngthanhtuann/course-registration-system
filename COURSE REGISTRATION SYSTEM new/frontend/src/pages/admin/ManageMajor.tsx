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
import { api } from "../../api"
import type { Major } from "../../types"
export default function ManageMajor() {
  const [rows, setRows] = useState<Major[]>([])
  const [modal, setModal] = useState<"create" | "edit" | "view" | null>(null)
  const [selected, setSelected] = useState<Major | null>(null)
  const [form, setForm] = useState({ code: "", name: "" })
  const [del, setDel] = useState<Major | null>(null)
  const [msg, setMsg] = useState("")
  const [err, setErr] = useState("")
  const load = () =>
    api.admin
      .majors()
      .then((x) =>
        setRows(x.map((m) => ({ code: m.major_code, name: m.major_name }))),
      )
      .catch((e) => setErr(e.message))
  useEffect(() => {
    void load()
  }, [])
  const save = async () => {
    setErr("")
    try {
      if (!form.code || !form.name)
        throw new Error("Major code and name are required.")
      if (modal === "create")
        await api.admin.createMajor({
          major_code: form.code.trim(),
          major_name: form.name.trim(),
        })
      else if (selected)
        await api.admin.updateMajor(selected.code, {
          major_name: form.name.trim(),
        })
      setModal(null)
      setMsg("Major saved successfully.")
      load()
    } catch (e: any) {
      setErr(e.message)
    }
  }
  const delMajor = async () => {
    if (!del) return
    try {
      await api.admin.deleteMajor(del.code)
      setDel(null)
      setMsg("Major deleted successfully.")
      load()
    } catch (e: any) {
      setDel(null)
      setErr(e.message)
    }
  }
  const cols: Column<Major>[] = [
    {
      key: "code",
      header: "Major Code",
      render: (r) => <span className="font-mono text-xs">{r.code}</span>,
    },
    {
      key: "name",
      header: "Major Name",
      render: (r) => <span className="font-medium">{r.name}</span>,
    },
    {
      key: "actions",
      header: "Actions",
      render: (r) => (
        <div className="flex gap-1">
          <Button
            size="sm"
            variant="ghost"
            onClick={() => {
              setSelected(r)
              setModal("view")
            }}
          >
            View
          </Button>
          <Button
            size="sm"
            variant="secondary"
            onClick={() => {
              setSelected(r)
              setForm({ code: r.code, name: r.name })
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
        title="Manage Major"
        subtitle="Create and maintain academic majors"
        actions={
          <Button
            size="sm"
            onClick={() => {
              setForm({ code: "", name: "" })
              setModal("create")
            }}
          >
            + Major
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
          columns={cols}
          rows={rows}
          keyFn={(r) => r.code}
          emptyText="No majors found."
        />
      </Card>
      <Modal
        open={!!modal}
        onClose={() => setModal(null)}
        title={
          modal === "create"
            ? "Create Major"
            : modal === "edit"
              ? "Edit Major"
              : "Major Details"
        }
        footer={
          modal === "view" ? (
            <Button variant="secondary" onClick={() => setModal(null)}>
              Close
            </Button>
          ) : (
            <>
              <Button variant="secondary" onClick={() => setModal(null)}>
                Cancel
              </Button>
              <Button onClick={save}>Save</Button>
            </>
          )
        }
      >
        {selected && modal === "view" ? (
          <div className="flex flex-col gap-3">
            <p>
              <b>Code:</b> {selected.code}
            </p>
            <p>
              <b>Name:</b> {selected.name}
            </p>
          </div>
        ) : (
          <div className="flex flex-col gap-4">
            <Input
              label="Major Code"
              value={form.code}
              readOnly={modal === "edit"}
              onChange={(e) => setForm({ ...form, code: e.target.value })}
            />
            <Input
              label="Major Name"
              value={form.name}
              onChange={(e) => setForm({ ...form, name: e.target.value })}
            />
          </div>
        )}
      </Modal>
      <ConfirmDialog
        open={!!del}
        onClose={() => setDel(null)}
        onConfirm={delMajor}
        title="Delete Major"
        message={`Delete ${del?.name}? This is allowed only when no students or curriculum reference it.`}
        confirmLabel="Delete"
      />
    </div>
  )
}

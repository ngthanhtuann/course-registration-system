import { useEffect, useState } from "react"
import {
  Card,
  Button,
  Input,
  Select,
  SearchBox,
  DataTable,
  SectionHeader,
  Modal,
  ConfirmDialog,
  Alert,
} from "../../components/ui"
import type { Column } from "../../components/ui"
import { api } from "../../api"
import type { Course } from "../../types"
const map = (x: any): Course => ({
  code: x.course_code,
  name: x.course_name,
  credits: Number(x.credit),
  prerequisite: x.prerequisite_course_code ?? null,
  capacity: Number(x.max_capacity),
})
export default function ManageCourse() {
  const [courses, setCourses] = useState<Course[]>([])
  const [search, setSearch] = useState("")
  const [modal, setModal] = useState<"create" | "edit" | "view" | null>(null)
  const [selected, setSelected] = useState<Course | null>(null)
  const [del, setDel] = useState<Course | null>(null)
  const [form, setForm] = useState({
    code: "",
    name: "",
    credits: "3",
    capacity: "30",
    prerequisite: "",
  })
  const [msg, setMsg] = useState("")
  const [err, setErr] = useState("")
  const load = () =>
    api.admin
      .courses()
      .then((x) => setCourses(x.map(map)))
      .catch((e) => setErr(e.message))
  useEffect(() => {
    void load()
  }, [])
  const filtered = courses.filter((c) =>
    (c.code + " " + c.name).toLowerCase().includes(search.toLowerCase()),
  )
  const save = async () => {
    try {
      setErr("")
      const p = {
        course_code: form.code.trim(),
        course_name: form.name.trim(),
        credit: Number(form.credits),
        max_capacity: Number(form.capacity),
        prerequisite_course_code: form.prerequisite || null,
      }
      if (modal === "create") await api.admin.createCourse(p)
      else if (selected)
        await api.admin.updateCourse(selected.code, {
          course_name: p.course_name,
          credit: p.credit,
          max_capacity: p.max_capacity,
          prerequisite_course_code: p.prerequisite_course_code,
        })
      setModal(null)
      setMsg("Course saved successfully.")
      load()
    } catch (e: any) {
      setErr(e.message)
    }
  }
  const delCourse = async () => {
    if (!del) return
    try {
      await api.admin.deleteCourse(del.code)
      setDel(null)
      setMsg("Course deleted successfully.")
      load()
    } catch (e: any) {
      setDel(null)
      setErr(e.message)
    }
  }
  const cols: Column<Course>[] = [
    {
      key: "code",
      header: "Course Code",
      render: (r) => <span className="font-mono text-xs">{r.code}</span>,
    },
    {
      key: "name",
      header: "Course Name",
      render: (r) => <span className="font-medium">{r.name}</span>,
    },
    { key: "credits", header: "Credits" },
    {
      key: "prerequisite",
      header: "Prerequisite",
      render: (r) => <span>{r.prerequisite || "None"}</span>,
    },
    { key: "capacity", header: "Capacity" },
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
              setForm({
                code: r.code,
                name: r.name,
                credits: String(r.credits),
                capacity: String(r.capacity),
                prerequisite: r.prerequisite || "",
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
        title="Manage Course"
        subtitle="Create, edit, search and delete courses"
        actions={
          <Button
            size="sm"
            onClick={() => {
              setForm({
                code: "",
                name: "",
                credits: "3",
                capacity: "30",
                prerequisite: "",
              })
              setModal("create")
            }}
          >
            + Course
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
        <div className="p-4 border-b border-slate-100">
          <SearchBox
            value={search}
            onChange={setSearch}
            placeholder="Search by course code or name…"
          />
        </div>
        <DataTable
          columns={cols}
          rows={filtered}
          keyFn={(r) => r.code}
          emptyText="No courses found."
        />
      </Card>
      <Modal
        open={!!modal}
        onClose={() => setModal(null)}
        title={
          modal === "create"
            ? "Create Course"
            : modal === "edit"
              ? "Edit Course"
              : "Course Details"
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
        {modal === "view" && selected ? (
          <div className="grid grid-cols-2 gap-3">
            {[
              ["Code", selected.code],
              ["Name", selected.name],
              ["Credits", selected.credits],
              ["Capacity", selected.capacity],
              ["Prerequisite", selected.prerequisite || "None"],
            ].map(([k, v]) => (
              <div key={String(k)} className="bg-slate-50 p-3 rounded-lg">
                <p className="text-xs text-slate-500">{k}</p>
                <p className="font-semibold text-sm">{v}</p>
              </div>
            ))}
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <Input
              label="Course Code"
              value={form.code}
              readOnly={modal === "edit"}
              onChange={(e) => setForm({ ...form, code: e.target.value })}
            />
            <Input
              label="Course Name"
              value={form.name}
              onChange={(e) => setForm({ ...form, name: e.target.value })}
            />
            <Input
              label="Credits"
              type="number"
              min="1"
              value={form.credits}
              onChange={(e) => setForm({ ...form, credits: e.target.value })}
            />
            <Input
              label="Maximum Capacity"
              type="number"
              min="1"
              value={form.capacity}
              onChange={(e) => setForm({ ...form, capacity: e.target.value })}
            />
            <Select
              label="Prerequisite"
              options={courses
                .filter((c) => c.code !== form.code)
                .map((c) => ({
                  value: c.code,
                  label: `${c.code} — ${c.name}`,
                }))}
              value={form.prerequisite}
              onChange={(e) =>
                setForm({ ...form, prerequisite: e.target.value })
              }
              placeholder="None"
            />
          </div>
        )}
      </Modal>
      <ConfirmDialog
        open={!!del}
        onClose={() => setDel(null)}
        onConfirm={delCourse}
        title="Delete Course"
        message={`Delete ${del?.code}? Existing curriculum, registrations or qualifications may prevent deletion.`}
        confirmLabel="Delete"
      />
    </div>
  )
}

import { useEffect, useState } from "react"
import {
  Card,
  Button,
  Select,
  DataTable,
  SectionHeader,
  ConfirmDialog,
  Alert,
  Input,
} from "../../components/ui"
import type { Column } from "../../components/ui"
import { api } from "../../services/api"
import type { Major, Course } from "../../types"
export default function ManageCurriculum() {
  const [majors, setMajors] = useState<Major[]>([])
  const [courses, setCourses] = useState<Course[]>([])
  const [items, setItems] = useState<any[]>([])
  const [major, setMajor] = useState("")
  const [form, setForm] = useState({ course: "", semester: "1" })
  const [remove, setRemove] = useState<any>(null)
  const [msg, setMsg] = useState("")
  const [err, setErr] = useState("")
  useEffect(() => {
    Promise.all([api.admin.majors(), api.admin.courses()])
      .then(([m, c]) => {
        setMajors(
          m.map((x: any) => ({ code: x.major_code, name: x.major_name })),
        )
        setCourses(
          c.map((x: any) => ({
            code: x.course_code,
            name: x.course_name,
            credits: Number(x.credit),
            prerequisite: x.prerequisite_course_code ?? null,
            capacity: Number(x.max_capacity),
          })),
        )
      })
      .catch((e) => setErr(e.message))
  }, [])
  const load = () =>
    major &&
    api.admin
      .curriculum(major)
      .then(setItems)
      .catch((e) => setErr(e.message))
  useEffect(() => {
    if (major) {
      void load()
    }
  }, [major])
  const available = courses.filter(
    (c) => !items.some((i) => i.course_code === c.code),
  )
  const add = async () => {
    if (!major || !form.course) {
      setErr("Select a major and course.")
      return
    }
    try {
      await api.admin.addCurriculum({
        major_code: major,
        course_code: form.course,
        recommended_semester: Number(form.semester),
      })
      setMsg("Course added to curriculum.")
      setForm({ course: "", semester: "1" })
      load()
    } catch (e: any) {
      setErr(e.message)
    }
  }
  const del = async () => {
    if (!remove) return
    try {
      await api.admin.deleteCurriculum(remove.curriculum_id)
      setRemove(null)
      setMsg("Course removed from curriculum.")
      load()
    } catch (e: any) {
      setRemove(null)
      setErr(e.message)
    }
  }
  const cols: Column<any>[] = [
    {
      key: "course_code",
      header: "Course Code",
      render: (r) => <span className="font-mono text-xs">{r.course_code}</span>,
    },
    {
      key: "course_name",
      header: "Course Name",
      render: (r) => <span className="font-medium">{r.course_name}</span>,
    },
    { key: "credit", header: "Credits" },
    { key: "recommended_semester", header: "Recommended Semester" },
    {
      key: "prerequisite_course_code",
      header: "Prerequisite",
      render: (r) => r.prerequisite_course_code || "None",
    },
    {
      key: "actions",
      header: "Actions",
      render: (r) => (
        <Button size="sm" variant="danger" onClick={() => setRemove(r)}>
          Remove
        </Button>
      ),
    },
  ]
  return (
    <div>
      <SectionHeader
        title="Manage Curriculum"
        subtitle="Assign courses to a major and set recommended semester"
      />
      {msg && <Alert type="success" message={msg} />}{" "}
      {err && (
        <div className="my-3">
          <Alert type="error" message={err} />
        </div>
      )}
      <Card className="p-4 mb-4">
        <Select
          label="Major"
          options={majors.map((m) => ({ value: m.code, label: m.name }))}
          value={major}
          onChange={(e) => setMajor(e.target.value)}
          placeholder="Select major"
        />
      </Card>
      {major && (
        <Card className="p-4 mb-4">
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <Select
              label="Course"
              options={available.map((c) => ({
                value: c.code,
                label: `${c.code} — ${c.name}`,
              }))}
              value={form.course}
              onChange={(e) => setForm({ ...form, course: e.target.value })}
              placeholder="Select course"
            />
            <Input
              label="Recommended Semester"
              type="number"
              min="1"
              value={form.semester}
              onChange={(e) => setForm({ ...form, semester: e.target.value })}
            />
            <div className="flex items-end">
              <Button onClick={add}>+ Add to Curriculum</Button>
            </div>
          </div>
        </Card>
      )}
      <Card>
        <DataTable
          columns={cols}
          rows={items}
          keyFn={(r) => r.curriculum_id}
          emptyText={
            major
              ? "No curriculum courses for this major."
              : "Select a major first."
          }
        />
      </Card>
      <ConfirmDialog
        open={!!remove}
        onClose={() => setRemove(null)}
        onConfirm={del}
        title="Remove Course"
        message={`Remove ${remove?.course_code} from this curriculum?`}
        confirmLabel="Remove"
      />
    </div>
  )
}

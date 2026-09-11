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
import { useAdminList } from "../../services/useAdminList"
import type { Major, Course } from "../../types"
export default function ManageCurriculum() {
  // Hai danh s?ch d?ng l?i cache, kh?ng ch? nhau m?i hi?n th?.
  const majorList = useAdminList("majors")
  const courseList = useAdminList("courses")
  const majors: Major[] = majorList.data.map((m) => ({
    code: m.major_code,
    name: m.major_name,
  }))
  const courses: Course[] = courseList.data.map((c) => ({
    code: c.course_code,
    name: c.course_name,
    credits: Number(c.credit),
    prerequisite: c.prerequisite_course_code ?? null,
    capacity: Number(c.max_capacity),
  }))
  const [items, setItems] = useState<any[]>([])
  const [major, setMajor] = useState("")
  const [form, setForm] = useState({ course: "", semester: "1" })
  const [remove, setRemove] = useState<any>(null)
  const [msg, setMsg] = useState("")
  const [err, setErr] = useState("")
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
      {(err || majorList.error || courseList.error) && (
        <div className="my-3">
          <Alert type="error" message={err || majorList.error || courseList.error} />
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

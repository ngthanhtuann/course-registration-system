import { useEffect, useRef, useState } from "react"
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
  const [loading, setLoading] = useState(true)
  const [loadError, setLoadError] = useState("")
  const [itemsLoading, setItemsLoading] = useState(false)
  const [itemsError, setItemsError] = useState("")
  const [submitting, setSubmitting] = useState(false)
  const itemRequest = useRef(0)
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
      .catch((e) => setLoadError(e.message))
      .finally(() => setLoading(false))
  }, [])
  const load = async () => {
    const request = ++itemRequest.current
    setItemsError("")
    if (!major) {
      setItems([])
      setItemsLoading(false)
      return
    }
    setItemsLoading(true)
    try {
      const data = await api.admin.curriculum(major)
      if (request === itemRequest.current) setItems(data)
    } catch (e: any) {
      if (request === itemRequest.current) setItemsError(e.message)
    } finally {
      if (request === itemRequest.current) setItemsLoading(false)
    }
  }
  useEffect(() => {
    setForm({ course: "", semester: "1" })
    void load()
    return () => { itemRequest.current += 1 }
  }, [major])
  const available = courses.filter(
    (c) => !items.some((i) => i.course_code === c.code),
  )
  const add = async () => {
    if (submitting) return
    if (!major || !form.course) {
      setErr("Select a major and course.")
      return
    }
    setSubmitting(true)
    setErr("")
    try {
      await api.admin.addCurriculum({
        major_code: major,
        course_code: form.course,
        recommended_semester: Number(form.semester),
      })
      setMsg("Course added to curriculum.")
      setForm({ course: "", semester: "1" })
      await load()
    } catch (e: any) {
      setErr(e.message)
    } finally {
      setSubmitting(false)
    }
  }
  const del = async () => {
    if (!remove || submitting) return false
    setSubmitting(true)
    setErr("")
    try {
      await api.admin.deleteCurriculum(remove.curriculum_id)
      setRemove(null)
      setMsg("Course removed from curriculum.")
      await load()
    } catch (e: any) {
      setErr(e.message)
      throw e
    } finally {
      setSubmitting(false)
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
          disabled={loading || !!loadError || submitting}
          options={majors.map((m) => ({ value: m.code, label: m.name }))}
          value={major}
          onChange={(e) => setMajor(e.target.value)}
          placeholder="Select major"
        />
      </Card>
      {major && !loading && !loadError && !itemsLoading && !itemsError && (
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
              <Button disabled={submitting} onClick={add}>+ Add to Curriculum</Button>
            </div>
          </div>
        </Card>
      )}
      <Card>
        <DataTable
          loading={loading || itemsLoading}
          error={loadError || itemsError}
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

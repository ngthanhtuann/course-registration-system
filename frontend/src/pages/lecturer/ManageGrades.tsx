import { useEffect, useState } from "react"
import {
  Card,
  Select,
  DataTable,
  SectionHeader,
  Button,
  Input,
  Alert,
} from "../../components/ui"
import type { Column } from "../../components/ui"
import { api } from "../../services/api"
import type { Lecturer } from "../../types"
export default function ManageStudentGrades({
  user: _user,
}: {
  user: Lecturer
}) {
  const [sems, setSems] = useState<any[]>([])
  const [semester, setSemester] = useState("")
  const [courses, setCourses] = useState<any[]>([])
  const [course, setCourse] = useState("")
  const [rows, setRows] = useState<any[]>([])
  const [msg, setMsg] = useState("")
  const [err, setErr] = useState("")
  const [saving, setSaving] = useState(false)
  useEffect(() => {
    let active = true
    api.lecturer
      .semesters()
      .then((s) => {
        if (!active) return
        setSems(s)
        if (s[0]) setSemester(s[0].semester_id)
      })
      .catch((e) => {
        if (active) setErr(e.message)
      })
    return () => {
      active = false
    }
  }, [])
  useEffect(() => {
    setCourses([])
    setCourse("")
    setRows([])
    if (!semester) return
    let active = true
    api.lecturer
      .teachingCourses(semester)
      .then((c) => {
        if (!active) return
        setCourses(c)
        setCourse(c[0]?.course_code || "")
      })
      .catch((e) => {
        if (active) setErr(e.message)
      })
    return () => {
      active = false
    }
  }, [semester])
  useEffect(() => {
    setRows([])
    setMsg("")
    setErr("")
    if (!semester || !course) return
    let active = true
    api.lecturer
      .students(course, semester)
      .then((students) => {
        if (active) setRows(students)
      })
      .catch((e) => {
        if (active) setErr(e.message)
      })
    return () => {
      // Ignore old results when the selected course changes.
      active = false
    }
  }, [semester, course])
  const save = async (r: any) => {
    if (saving) return
    setMsg("")
    setErr("")
    const input = String(r._grade ?? "").trim()
    if (input === "") {
      setErr("Please enter a grade before saving.")
      return
    }
    const value = Number(input)
    if (!Number.isFinite(value) || value < 0 || value > 10) {
      setErr("Grade must be between 0 and 10.")
      return
    }
    setSaving(true)
    try {
      const result = await api.lecturer.updateGrade(r.registration_id, value)
      setMsg("Grade saved successfully.")
      setRows((prev) =>
        prev.map((x) =>
          x.registration_id === r.registration_id
            ? {
                ...x,
                grade: result.grade,
                result_status: result.result_status,
                _grade: "",
              }
            : x,
        ),
      )
    } catch (e: any) {
      setErr(e.message)
    } finally {
      setSaving(false)
    }
  }
  const cols: Column<any>[] = [
    {
      key: "student_id",
      header: "Student ID",
      render: (r) => <span className="font-mono text-xs">{r.student_id}</span>,
    },
    {
      key: "fullname",
      header: "Student Name",
      render: (r) => <span className="font-medium">{r.fullname}</span>,
    },
    { key: "grade", header: "Current Grade", render: (r) => r.grade ?? "—" },
    {
      key: "input",
      header: "New Grade",
      render: (r) => (
        <Input
          type="number"
          min="0"
          max="10"
          step="0.1"
          value={r._grade ?? ""}
          disabled={saving}
          onChange={(e) =>
            setRows((prev) =>
              prev.map((x) =>
                x.registration_id === r.registration_id
                  ? { ...x, _grade: e.target.value }
                  : x,
              ),
            )
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
          onClick={() => save(r)}
          disabled={saving || String(r._grade ?? "").trim() === ""}
        >
          Save
        </Button>
      ),
    },
  ]
  return (
    <div>
      <SectionHeader
        title="Manage Student Grades"
        subtitle="Enter and update grades for your assigned courses"
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
      <Card className="p-4 mb-4">
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <Select
            label="Semester"
            options={sems.map((s) => ({
              value: s.semester_id,
              label: s.semester_name,
            }))}
            value={semester}
            disabled={saving}
            onChange={(e) => {
              setSemester(e.target.value)
              setCourses([])
              setCourse("")
              setRows([])
            }}
          />
          <Select
            label="Course"
            options={courses.map((c) => ({
              value: c.course_code,
              label: `${c.course_code} — ${c.course_name}`,
            }))}
            value={course}
            disabled={saving}
            onChange={(e) => {
              setCourse(e.target.value)
              setRows([])
            }}
            placeholder="Select course"
          />
        </div>
      </Card>
      <Card>
        <DataTable
          columns={cols}
          rows={rows}
          keyFn={(r) => r.registration_id}
          emptyText="No registered students."
        />
      </Card>
    </div>
  )
}

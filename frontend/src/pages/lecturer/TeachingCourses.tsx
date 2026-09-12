import { useEffect, useState } from "react"
import {
  Card,
  Select,
  DataTable,
  SectionHeader,
  Modal,
  Button,
} from "../../components/ui"
import type { Column } from "../../components/ui"
import { api } from "../../services/api"
import type { Lecturer } from "../../types"
export default function ManageTeachingCourse({
  user: _user,
}: {
  user: Lecturer
}) {
  const [sems, setSems] = useState<any[]>([])
  const [semester, setSemester] = useState("")
  const [courses, setCourses] = useState<any[]>([])
  const [view, setView] = useState<any>(null)
  const [students, setStudents] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState("")
  const [studentsLoading, setStudentsLoading] = useState(false)
  const [studentsError, setStudentsError] = useState("")
  useEffect(() => {
    let active = true
    api.lecturer
      .semesters()
      .then((s) => {
        if (!active) return
        setSems(s)
        if (s[0]) setSemester(s[0].semester_id)
        else setLoading(false)
      })
      .catch((e) => {
        if (!active) return
        setError(e.message || "Could not load semesters.")
        setLoading(false)
      })
    return () => { active = false }
  }, [])
  useEffect(() => {
    if (!semester) return
    let active = true
    setLoading(true)
    setError("")
    api.lecturer.teachingCourses(semester)
      .then((data) => { if (active) setCourses(data) })
      .catch((e) => {
        if (active) setError(e.message || "Could not load teaching courses.")
      })
      .finally(() => { if (active) setLoading(false) })
    return () => { active = false }
  }, [semester])
  useEffect(() => {
    if (!view || !semester) return
    let active = true
    setStudentsLoading(true)
    setStudentsError("")
    api.lecturer.students(view.course_code, semester)
      .then((data) => { if (active) setStudents(data) })
      .catch((e) => {
        if (active) setStudentsError(e.message || "Could not load registered students.")
      })
      .finally(() => { if (active) setStudentsLoading(false) })
    return () => { active = false }
  }, [view, semester])
  const open = (c: any) => {
    setView(c)
    setStudents([])
    setStudentsLoading(true)
    setStudentsError("")
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
    { key: "student_count", header: "Students" },
    {
      key: "action",
      header: "Action",
      render: (r) => (
        <Button size="sm" variant="ghost" onClick={() => open(r)}>
          View Students
        </Button>
      ),
    },
  ]
  return (
    <div>
      <SectionHeader
        title="Manage Teaching Courses"
        subtitle="Courses assigned to you for the selected semester"
      />
      <Card className="p-4 mb-4">
        <Select
          label="Semester"
          options={sems.map((s) => ({
            value: s.semester_id,
            label: s.semester_name,
          }))}
          value={semester}
          onChange={(e) => {
            setSemester(e.target.value)
            setCourses([])
            setView(null)
            setLoading(!!e.target.value)
            setError("")
          }}
        />
      </Card>
      <Card>
        <DataTable
          columns={cols}
          rows={courses}
          loading={loading}
          error={error}
          keyFn={(r) => r.assignment_id}
          emptyText="No teaching courses found."
        />
      </Card>
      <Modal
        open={!!view}
        onClose={() => setView(null)}
        title={`Students — ${view?.course_code || ""}`}
        size="lg"
        footer={
          <Button variant="secondary" onClick={() => setView(null)}>
            Close
          </Button>
        }
      >
        <DataTable
          columns={[
            { key: "student_id", header: "Student ID" },
            { key: "fullname", header: "Name" },
            { key: "email", header: "Email" },
            {
              key: "grade",
              header: "Grade",
              render: (r) => r.grade ?? "Not entered",
            },
          ]}
          rows={students}
          loading={studentsLoading}
          error={studentsError}
          keyFn={(r) => r.registration_id}
          emptyText="No registered students."
        />
      </Modal>
    </div>
  )
}

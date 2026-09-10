import { useEffect, useState } from "react"
import {
  Card,
  Button,
  Select,
  Badge,
  DataTable,
  SectionHeader,
  ConfirmDialog,
  Alert,
} from "../../components/ui"
import type { Column } from "../../components/ui"
import { api } from "../../services/api"
export default function AssignLecturer() {
  const [semesters, setSemesters] = useState<any[]>([])
  const [courses, setCourses] = useState<any[]>([])
  const [assignments, setAssignments] = useState<any[]>([])
  const [semester, setSemester] = useState("")
  const [course, setCourse] = useState("")
  const [lecturers, setLecturers] = useState<any[]>([])
  const [confirm, setConfirm] = useState<any>(null)
  const [err, setErr] = useState("")
  const [msg, setMsg] = useState("")
  useEffect(() => {
    Promise.all([api.admin.semesters(), api.admin.courses()])
      .then(([s, c]) => {
        setSemesters(s)
        setCourses(c)
        if (s[0]) setSemester(s[0].semester_id)
      })
      .catch((e) => setErr(e.message))
  }, [])
  useEffect(() => {
    if (!semester) return
    api.admin
      .assignments(semester)
      .then(setAssignments)
      .catch((e) => setErr(e.message))
  }, [semester])
  useEffect(() => {
    if (!course) {
      setLecturers([])
      return
    }
    api.admin
      .qualifiedLecturers(course)
      .then(setLecturers)
      .catch((e) => setErr(e.message))
  }, [course])
  const assigned = (id: string) =>
    assignments.some(
      (a) =>
        a.lecturer_id === id &&
        a.course_code === course &&
        a.semester_id === semester,
    )
  const assign = async (l: any) => {
    try {
      await api.admin.createAssignment({
        semester_id: semester,
        lecturer_id: l.lecturer_id,
        course_code: course,
      })
      setMsg(`${l.fullname} assigned successfully.`)
      setConfirm(null)
      setAssignments(await api.admin.assignments(semester))
    } catch (e: any) {
      setErr(e.message)
      setConfirm(null)
    }
  }
  const unassign = async (l: any) => {
    const a = assignments.find(
      (x) =>
        x.lecturer_id === l.lecturer_id &&
        x.course_code === course &&
        x.semester_id === semester,
    )
    if (!a) return
    try {
      await api.admin.deleteAssignment(a.assignment_id)
      setMsg("Assignment removed.")
      setAssignments(await api.admin.assignments(semester))
    } catch (e: any) {
      setErr(e.message)
    }
  }
  const cols: Column<any>[] = [
    {
      key: "lecturer_id",
      header: "Lecturer ID",
      render: (r) => <span className="font-mono text-xs">{r.lecturer_id}</span>,
    },
    {
      key: "fullname",
      header: "Lecturer Name",
      render: (r) => <span className="font-medium">{r.fullname}</span>,
    },
    {
      key: "email",
      header: "Email",
      render: (r) => <span className="text-xs">{r.email}</span>,
    },
    {
      key: "status",
      header: "Assignment Status",
      render: (r) => (
        <Badge label={assigned(r.lecturer_id) ? "Assigned" : "Unassigned"} />
      ),
    },
    {
      key: "action",
      header: "Action",
      render: (r) => (
        <Button
          size="sm"
          variant={assigned(r.lecturer_id) ? "secondary" : "primary"}
          onClick={() =>
            assigned(r.lecturer_id) ? unassign(r) : setConfirm(r)
          }
        >
          {assigned(r.lecturer_id) ? "Unassign" : "Assign"}
        </Button>
      ),
    },
  ]
  return (
    <div>
      <SectionHeader
        title="Assign Lecturer"
        subtitle="Only lecturers with a qualification for the selected course can be assigned"
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
      <Card className="p-4 mb-5">
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <Select
            label="Semester"
            options={semesters.map((s) => ({
              value: s.semester_id,
              label: s.semester_name,
            }))}
            value={semester}
            onChange={(e) => setSemester(e.target.value)}
          />
          <Select
            label="Course"
            options={courses.map((c) => ({
              value: c.course_code,
              label: `${c.course_code} — ${c.course_name}`,
            }))}
            value={course}
            onChange={(e) => setCourse(e.target.value)}
            placeholder="Choose a course"
          />
        </div>
      </Card>
      {course ? (
        <Card>
          <div className="px-5 py-4 border-b border-slate-100">
            <h3 className="font-semibold">Qualified Lecturers for {course}</h3>
            <p className="text-xs text-slate-400">
              {lecturers.length} qualified lecturer(s)
            </p>
          </div>
          <DataTable
            columns={cols}
            rows={lecturers}
            keyFn={(r) => r.lecturer_id}
            emptyText="No qualified lecturers. Add a qualification in Manage Users first."
          />
        </Card>
      ) : (
        <Card className="p-12 text-center text-slate-400">
          Select a course to view qualified lecturers.
        </Card>
      )}
      <ConfirmDialog
        open={!!confirm}
        onClose={() => setConfirm(null)}
        onConfirm={() => confirm && assign(confirm)}
        title="Assign Lecturer"
        message={`Assign ${confirm?.fullname} to ${course}?`}
        confirmLabel="Assign"
        variant="primary"
      />
    </div>
  )
}

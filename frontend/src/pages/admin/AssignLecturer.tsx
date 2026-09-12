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
import { useAdminList } from "../../services/useAdminList"
export default function AssignLecturer() {
  const [semesters, setSemesters] = useState<any[]>([])
  const [courses, setCourses] = useState<any[]>([])
  const [majors, setMajors] = useState<any[]>([])
  const [major, setMajor] = useState("")
  const [assignments, setAssignments] = useState<any[]>([])
  const [semester, setSemester] = useState("")
  const [course, setCourse] = useState("")
  const [lecturers, setLecturers] = useState<any[]>([])
  const [confirm, setConfirm] = useState<any>(null)
  const [err, setErr] = useState("")
  const [msg, setMsg] = useState("")
  const [loading, setLoading] = useState(true)
  const [loadError, setLoadError] = useState("")
  const [coursesLoading, setCoursesLoading] = useState(false)
  const [coursesError, setCoursesError] = useState("")
  const [assignmentsLoading, setAssignmentsLoading] = useState(false)
  const [assignmentsError, setAssignmentsError] = useState("")
  const [lecturersLoading, setLecturersLoading] = useState(false)
  const [lecturersError, setLecturersError] = useState("")
  const [submitting, setSubmitting] = useState(false)
  useEffect(() => {
    Promise.all([api.admin.semesters(), api.admin.majors()])
      .then(([s, m]) => {
        setSemesters(s)
        setMajors(m)
        if (s[0]) setSemester(s[0].semester_id)
      })
      .catch((e) => setLoadError(e.message))
      .finally(() => setLoading(false))
  }, [])
  useEffect(() => {
    let active = true
    setAssignmentsError("")
    if (!semester) {
      setAssignments([])
      setAssignmentsLoading(false)
      return
    }
    setAssignmentsLoading(true)
    api.admin.assignments(semester)
      .then((data) => { if (active) setAssignments(data) })
      .catch((e) => { if (active) setAssignmentsError(e.message) })
      .finally(() => { if (active) setAssignmentsLoading(false) })
    return () => { active = false }
  }, [semester])
  useEffect(() => {
    let active = true
    setCourse("")
    setCourses([])
    setCoursesError("")
    if (!major) {
      setCoursesLoading(false)
      return
    }
    setCoursesLoading(true)
    api.admin.curriculum(major)
      .then((data) => { if (active) setCourses(data) })
      .catch((e) => { if (active) setCoursesError(e.message) })
      .finally(() => { if (active) setCoursesLoading(false) })
    return () => { active = false }
  }, [major])
  useEffect(() => {
    let active = true
    setLecturersError("")
    if (!course) {
      setLecturers([])
      setLecturersLoading(false)
      return
    }
    setLecturersLoading(true)
    api.admin.qualifiedLecturers(course)
      .then((data) => { if (active) setLecturers(data) })
      .catch((e) => { if (active) setLecturersError(e.message) })
      .finally(() => { if (active) setLecturersLoading(false) })
    return () => { active = false }
  }, [course])
  const refreshAssignments = async () => {
    setAssignmentsLoading(true)
    setAssignmentsError("")
    try {
      setAssignments(await api.admin.assignments(semester))
    } catch (e: any) {
      setAssignmentsError(e.message)
    } finally {
      setAssignmentsLoading(false)
    }
  }
  const assigned = (id: string) =>
    assignments.some(
      (a) =>
        a.lecturer_id === id &&
        a.course_code === course &&
        a.semester_id === semester,
    )
  const assign = async (l: any) => {
    if (submitting || !semester || !major || !course) return false
    setSubmitting(true)
    setErr("")
    try {
      await api.admin.createAssignment({
        semester_id: semester,
        major_code: major,
        lecturer_id: l.lecturer_id,
        course_code: course,
      })
      setMsg(`${l.fullname} assigned successfully.`)
      setConfirm(null)
      await refreshAssignments()
    } catch (e: any) {
      setErr(e.message)
      throw e
    } finally {
      setSubmitting(false)
    }
  }
  const unassign = async (l: any) => {
    const a = assignments.find(
      (x) =>
        x.lecturer_id === l.lecturer_id &&
        x.course_code === course &&
        x.semester_id === semester,
    )
    if (!a || submitting) return
    setSubmitting(true)
    setErr("")
    try {
      await api.admin.deleteAssignment(a.assignment_id)
      setMsg("Assignment removed.")
      await refreshAssignments()
    } catch (e: any) {
      setErr(e.message)
    } finally {
      setSubmitting(false)
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
          disabled={submitting || assignmentsLoading || !!assignmentsError || !semester}
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
      {(err || semesterList.error || courseList.error) && (
        <div className="mb-3">
          <Alert type="error" message={err || semesterList.error || courseList.error} />
        </div>
      )}
      <Card className="p-4 mb-5">
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <Select
            label="Semester"
            disabled={loading || !!loadError || submitting}
            options={semesters.map((s) => ({
              value: s.semester_id,
              label: s.semester_name,
            }))}
            value={semester}
            onChange={(e) => setSemester(e.target.value)}
          />
          <Select
            label="Major"
            options={majors.map((m) => ({ value: m.major_code, label: m.major_name }))}
            value={major}
            onChange={(e) => { setMajor(e.target.value); setCourse("") }}
            placeholder="Choose a major"
            disabled={loading || !!loadError || submitting}
          />
          <Select
            label="Course"
            disabled={!major || loading || coursesLoading || !!coursesError || submitting}
            options={courses.map((c) => ({
              value: c.course_code,
              label: `${c.course_code} — ${c.course_name}`,
            }))}
            value={course}
            onChange={(e) => setCourse(e.target.value)}
            placeholder={coursesLoading ? "Loading courses…" : major && !coursesError && !courses.length ? "No courses in this curriculum" : "Choose a course"}
          />
        </div>
      </Card>
      {loading && <p role="status" className="mb-3 text-sm text-slate-500">Loading semesters and majors…</p>}
      {(loadError || coursesError) && <Alert type="error" message={loadError || coursesError} />}
      {course ? (
        <Card>
          <div className="px-5 py-4 border-b border-slate-100">
            <h3 className="font-semibold">Qualified Lecturers for {course}</h3>
            {!lecturersLoading && !lecturersError && <p className="text-xs text-slate-400">
              {lecturers.length} qualified lecturer(s)
            </p>}
          </div>
          <DataTable
            loading={loading || lecturersLoading || assignmentsLoading}
            error={loadError || coursesError || lecturersError || assignmentsError}
            columns={cols}
            rows={lecturers}
            keyFn={(r) => r.lecturer_id}
            emptyText="No qualified lecturers. Add a qualification in Manage Users first."
          />
        </Card>
      ) : (
        <Card className="p-12 text-center text-slate-400">
          Select a major and a course to view qualified lecturers.
        </Card>
      )}
      <ConfirmDialog
        open={!!confirm}
        onClose={() => setConfirm(null)}
        onConfirm={() => confirm ? assign(confirm) : false}
        title="Assign Lecturer"
        message={`Assign ${confirm?.fullname} to ${course}?`}
        confirmLabel="Assign"
        variant="primary"
      />
    </div>
  )
}

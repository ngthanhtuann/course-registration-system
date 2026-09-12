import { useEffect, useRef, useState } from "react"
import {
  Card,
  Button,
  Input,
  Select,
  SearchBox,
  Badge,
  DataTable,
  SectionHeader,
  Modal,
  ConfirmDialog,
  FormGrid,
  Alert,
} from "../../components/ui"
import type { Column } from "../../components/ui"
import { api } from "../../services/api"
import { useAdminList } from "../../services/useAdminList"
function CoursePicker({
  selected,
  onChange,
  courses,
}: {
  selected: string[]
  onChange: (x: string[]) => void
  courses: any[]
}) {
  const [open, setOpen] = useState(false)
  const [search, setSearch] = useState("")
  const ref = useRef<HTMLDivElement>(null)
  useEffect(() => {
    const h = (e: MouseEvent) => {
      if (ref.current && !ref.current.contains(e.target as Node)) setOpen(false)
    }
    document.addEventListener("mousedown", h)
    return () => document.removeEventListener("mousedown", h)
  }, [])
  const filtered = courses.filter((c) =>
    (c.course_code + " " + c.course_name)
      .toLowerCase()
      .includes(search.toLowerCase()),
  )
  return (
    <div ref={ref} className="relative">
      <div className="flex flex-wrap gap-1 mb-2">
        {selected.map((code) => (
          <span
            key={code}
            className="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded-full"
          >
            {code}
            <button
              type="button"
              className="ml-1"
              onClick={() => onChange(selected.filter((x) => x !== code))}
            >
              ×
            </button>
          </span>
        ))}
      </div>
      <button
        type="button"
        onClick={() => setOpen(!open)}
        className="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm text-left"
      >
        {selected.length
          ? `${selected.length} course(s) selected`
          : "Select courses…"}
      </button>
      {open && (
        <div className="absolute z-50 mt-1 w-full bg-white border rounded-xl shadow-lg">
          <div className="p-2">
            <input
              autoFocus
              className="w-full border rounded-lg px-2 py-1.5 text-sm"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search courses…"
            />
          </div>
          <div className="max-h-52 overflow-y-auto">
            {filtered.map((c) => (
              <button
                type="button"
                key={c.course_code}
                onClick={() =>
                  onChange(
                    selected.includes(c.course_code)
                      ? selected.filter((x) => x !== c.course_code)
                      : [...selected, c.course_code],
                  )
                }
                className={`w-full text-left px-3 py-2 text-sm ${
                  selected.includes(c.course_code) ? "bg-blue-50" : ""
                }`}
              >
                <span className="font-mono text-xs mr-2">{c.course_code}</span>
                {c.course_name}
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
function chips(codes: string[]) {
  return codes.length ? (
    codes.map((c) => (
      <span
        key={c}
        className="inline-block bg-slate-100 rounded px-1.5 py-0.5 mr-1 text-xs font-mono"
      >
        {c}
      </span>
    ))
  ) : (
    <span className="text-xs text-slate-300">None</span>
  )
}
export default function ManageUser() {
  const userList = useAdminList("users")
  const majorList = useAdminList("majors")
  const courseList = useAdminList("courses")
  const users = userList.data
  const majors = majorList.data
  const courses = courseList.data
  const [search, setSearch] = useState("")
  const [role, setRole] = useState("")
  const [modal, setModal] =
    useState<"student" | "lecturer" | "view" | "edit" | "qual" | null>(null)
  const [selected, setSelected] = useState<any>(null)
  const [del, setDel] = useState<any>(null)
  const [form, setForm] = useState<any>({
    id: "",
    fullName: "",
    email: "",
    password: "",
    major: "",
    dob: "",
    qualifications: [],
  })
  const [qualCourse, setQualCourse] = useState("")
  const [msg, setMsg] = useState("")
  const [err, setErr] = useState("")
  const [loading, setLoading] = useState(true)
  const [loadError, setLoadError] = useState("")
  const load = async () => {
    setLoading(true)
    setLoadError("")
    try {
      const [u, m, c] = await Promise.all([
        api.admin.users(),
        api.admin.majors(),
        api.admin.courses(),
      ])
      setUsers(u)
      setMajors(m)
      setCourses(c)
      return u
    } catch (e: any) {
      setLoadError(e.message)
      return undefined
    } finally {
      setLoading(false)
    }
  }
  useEffect(() => {
    load()
  }, [])
  const normalized = (u: any) => ({
    id: u.user_id,
    username: u.username,
    fullName: u.fullname,
    email: u.email,
    role: u.role,
    status: u.status ? "Active" : "Inactive",
    studentId: u.student_id,
    major: u.major_code,
    lecturerId: u.lecturer_id,
    qualifications: u.qualifications || [],
  })
  const rows = users.map(normalized).filter((u) => {
    const q = search.toLowerCase()
    return (
      (!q ||
        (u.id + " " + u.fullName + " " + u.email + " " + (u.major || ""))
          .toLowerCase()
          .includes(q)) &&
      (!role || u.role === role)
    )
  })
  const openEdit = (u: any) => {
    setSelected(u)
    setForm({
      id: u.id,
      fullName: u.fullName,
      email: u.email,
      password: "",
      major: u.major || "",
      dob: "",
      qualifications: u.qualifications || [],
    })
    setModal("edit")
  }
  const create = async (r: "student" | "lecturer") => {
    try {
      setErr("")
      if (!form.id || !form.fullName || !form.email || !form.password)
        throw new Error("ID, full name, email and password are required.")
      const payload = {
        user_id: form.id.trim(),
        fullname: form.fullName.trim(),
        email: form.email.trim(),
        password: form.password,
        role: r,
        major_code: r === "student" ? form.major : undefined,
        dob: r === "student" ? form.dob || null : undefined,
        qualifications: r === "lecturer" ? form.qualifications : undefined,
      }
      await api.admin.createUser(payload)
      setModal(null)
      setMsg(
        `${r === "student" ? "Student" : "Lecturer"} created successfully.`,
      )
      setForm({
        id: "",
        fullName: "",
        email: "",
        password: "",
        major: "",
        dob: "",
        qualifications: [],
      })
    } catch (e: any) {
      setErr(e.message)
    }
  }
  const save = async () => {
    if (!selected) return
    try {
      setErr("")
      const payload: any = { fullname: form.fullName, email: form.email }
      if (selected.role === "student") payload.major_code = form.major
      payload.qualifications =
        selected.role === "lecturer" ? form.qualifications : undefined
      await api.admin.updateUser(selected.id, payload)
      setModal(null)
      setMsg("User updated successfully.")
    } catch (e: any) {
      setErr(e.message)
    }
  }
  const deactivate = async () => {
    if (!del) return
    try {
      await api.admin.deactivateUser(del.id)
      setDel(null)
      setMsg("User deactivated successfully.")
    } catch (e: any) {
      setErr(e.message)
      throw e
    }
  }
  const addQual = async () => {
    if (!selected || selected.role !== "lecturer" || !qualCourse) {
      setErr("Select a course.")
      return
    }
    try {
      await api.admin.addQualification(selected.lecturerId, qualCourse)
      setQualCourse("")
      setMsg("Teaching qualification added.")
      const freshUsers = await load()
      const fresh = freshUsers
        ?.map(normalized)
        .find((u: any) => u.id === selected.id)
      if (fresh) {
        setSelected(fresh)
        setModal("view")
      }
    } catch (e: any) {
      setErr(e.message)
    }
  }
  const removeQual = async (code: string) => {
    if (!selected) return
    try {
      await api.admin.removeQualification(selected.lecturerId, code)
      setMsg("Teaching qualification removed.")
      const freshUsers = await load()
      const fresh = freshUsers
        ?.map(normalized)
        .find((u: any) => u.id === selected.id)
      if (fresh) setSelected(fresh)
    } catch (e: any) {
      setErr(e.message)
    }
  }
  const cols: Column<any>[] = [
    {
      key: "id",
      header: "ID",
      render: (u) => <span className="font-mono text-xs">{u.id}</span>,
    },
    {
      key: "fullName",
      header: "Full Name",
      render: (u) => <span className="font-medium">{u.fullName}</span>,
    },
    {
      key: "email",
      header: "Email",
      render: (u) => <span className="text-xs">{u.email}</span>,
    },
    {
      key: "role",
      header: "Role",
      render: (u) => (
        <Badge
          label={
            u.role === "admin"
              ? "Administrator"
              : u.role === "lecturer"
                ? "Lecturer"
                : "Student"
          }
        />
      ),
    },
    {
      key: "extra",
      header: "Major / Qualification",
      render: (u) =>
        u.role === "student"
          ? u.major || "—"
          : u.role === "lecturer"
            ? chips(u.qualifications)
            : "—",
    },
    {
      key: "status",
      header: "Status",
      render: (u) => <Badge label={u.status} />,
    },
    {
      key: "actions",
      header: "Actions",
      render: (u) => (
        <div className="flex gap-1 flex-wrap">
          <Button
            size="sm"
            variant="ghost"
            onClick={() => {
              setSelected(u)
              setModal("view")
            }}
          >
            View
          </Button>
          <Button size="sm" variant="secondary" onClick={() => openEdit(u)}>
            Edit
          </Button>
          {u.role !== "admin" && u.status === "Active" && (
            <Button size="sm" variant="danger" onClick={() => setDel(u)}>
              Deactivate
            </Button>
          )}
        </div>
      ),
    },
  ]
  return (
    <div>
      <SectionHeader
        title="Manage User"
        subtitle="Create, view, edit and deactivate system users"
        actions={
          <div className="flex gap-2">
            <Button
              size="sm"
              variant="outline"
              onClick={() => {
                setForm({
                  id: "",
                  fullName: "",
                  email: "",
                  password: "",
                  major: "",
                  dob: "",
                  qualifications: [],
                })
                setModal("student")
              }}
            >
              + Student
            </Button>
            <Button
              size="sm"
              onClick={() => {
                setForm({
                  id: "",
                  fullName: "",
                  email: "",
                  password: "",
                  major: "",
                  dob: "",
                  qualifications: [],
                })
                setModal("lecturer")
              }}
            >
              + Lecturer
            </Button>
          </div>
        }
      />
      {msg && (
        <div className="mb-3">
          <Alert type="success" message={msg} />
        </div>
      )}
      {(err || userList.error || majorList.error || courseList.error) && (
        <div className="mb-3">
          <Alert
            type="error"
            message={err || userList.error || majorList.error || courseList.error}
          />
        </div>
      )}
      <Card>
        <div className="p-4 border-b border-slate-100 flex gap-3">
          <SearchBox
            value={search}
            onChange={setSearch}
            placeholder="Search by ID, name, email or major…"
            className="flex-1"
          />
          <Select
            options={[
              { value: "admin", label: "Administrator" },
              { value: "lecturer", label: "Lecturer" },
              { value: "student", label: "Student" },
            ]}
            value={role}
            onChange={(e) => setRole(e.target.value)}
            placeholder="All Roles"
            className="w-40"
          />
        </div>
        <DataTable
          loading={loading}
          error={loadError}
          columns={cols}
          rows={rows}
          loading={userList.loading}
          keyFn={(u) => u.id}
          emptyText="No users found."
        />
      </Card>
      <Modal
        open={modal === "view"}
        onClose={() => setModal(null)}
        title="User Details"
        size="sm"
        footer={
          <Button variant="secondary" onClick={() => setModal(null)}>
            Close
          </Button>
        }
      >
        {selected && (
          <div className="flex flex-col gap-3">
            <div>
              <b>{selected.fullName}</b>
              <p className="text-xs text-slate-500">{selected.email}</p>
            </div>
            <p className="text-sm">
              Username: <b>{selected.username}</b>
            </p>
            <p className="text-sm">
              Role: <b>{selected.role}</b>
            </p>
            <p className="text-sm">
              Status: <b>{selected.status}</b>
            </p>
            {selected.role === "student" && (
              <>
                <p className="text-sm">
                  Student ID: <b>{selected.studentId}</b>
                </p>
                <p className="text-sm">
                  Major: <b>{selected.major || "—"}</b>
                </p>
              </>
            )}
            {selected.role === "lecturer" && (
              <div className="pt-3 border-t">
                <div className="flex justify-between items-center">
                  <p className="font-semibold text-sm">
                    Teaching Qualifications
                  </p>
                  <Button
                    size="sm"
                    variant="outline"
                    onClick={() => {
                      setQualCourse("")
                      setModal("qual")
                    }}
                  >
                    + Add
                  </Button>
                </div>
                <div className="mt-2 flex flex-col gap-2">
                  {(selected.qualifications || []).map((c: string) => (
                    <div
                      key={c}
                      className="flex justify-between items-center bg-slate-50 rounded p-2"
                    >
                      <span className="font-mono text-xs">{c}</span>
                      <Button
                        size="sm"
                        variant="danger"
                        onClick={() => removeQual(c)}
                      >
                        Remove
                      </Button>
                    </div>
                  ))}
                  {!selected.qualifications?.length && (
                    <span className="text-xs text-slate-400">
                      No qualifications assigned.
                    </span>
                  )}
                </div>
              </div>
            )}
          </div>
        )}
      </Modal>
      <Modal
        open={modal === "qual"}
        onClose={() => setModal("view")}
        title="Add Teaching Qualification"
        size="sm"
        footer={
          <>
            <Button variant="secondary" onClick={() => setModal("view")}>
              Cancel
            </Button>
            <Button onClick={addQual}>Add Qualification</Button>
          </>
        }
      >
        <Select
          label="Course"
          options={courses
            .filter(
              (c) => !(selected?.qualifications || []).includes(c.course_code),
            )
            .map((c) => ({
              value: c.course_code,
              label: `${c.course_code} — ${c.course_name}`,
            }))}
          value={qualCourse}
          onChange={(e) => setQualCourse(e.target.value)}
          placeholder="Select a course"
        />
      </Modal>
      <Modal
        open={modal === "edit"}
        onClose={() => setModal(null)}
        title="Edit User"
        footer={
          <>
            <Button variant="secondary" onClick={() => setModal(null)}>
              Cancel
            </Button>
            <Button onClick={save}>Save</Button>
          </>
        }
      >
        <FormGrid cols={1}>
          <Input
            label="Full Name"
            value={form.fullName}
            onChange={(e) => setForm({ ...form, fullName: e.target.value })}
          />
          <Input
            label="Email"
            type="email"
            value={form.email}
            onChange={(e) => setForm({ ...form, email: e.target.value })}
          />
          {selected?.role === "student" && (
            <Select
              label="Major"
              options={majors.map((m) => ({
                value: m.major_code,
                label: m.major_name,
              }))}
              value={form.major}
              onChange={(e) => setForm({ ...form, major: e.target.value })}
            />
          )}{" "}
          {selected?.role === "lecturer" && (
            <>
              <label className="text-sm font-medium text-slate-700">
                Teaching Qualifications
              </label>
              <CoursePicker
                selected={form.qualifications}
                onChange={(q) => setForm({ ...form, qualifications: q })}
                courses={courses}
              />
            </>
          )}
        </FormGrid>
      </Modal>
      <Modal
        open={modal === "student"}
        onClose={() => setModal(null)}
        title="Create Student"
        footer={
          <>
            <Button variant="secondary" onClick={() => setModal(null)}>
              Cancel
            </Button>
            <Button onClick={() => create("student")}>Create</Button>
          </>
        }
      >
        <FormGrid>
          <Input
            label="Student ID"
            value={form.id}
            onChange={(e) => setForm({ ...form, id: e.target.value })}
          />
          <Input
            label="Full Name"
            value={form.fullName}
            onChange={(e) => setForm({ ...form, fullName: e.target.value })}
          />
          <Input
            label="Email"
            type="email"
            value={form.email}
            onChange={(e) => setForm({ ...form, email: e.target.value })}
          />
          <Input
            label="Date of Birth"
            type="date"
            value={form.dob}
            onChange={(e) => setForm({ ...form, dob: e.target.value })}
          />
          <Select
            label="Major"
            options={majors.map((m) => ({
              value: m.major_code,
              label: m.major_name,
            }))}
            value={form.major}
            onChange={(e) => setForm({ ...form, major: e.target.value })}
            placeholder="Select major"
          />
          <Input
            label="Initial Password"
            type="password"
            value={form.password}
            onChange={(e) => setForm({ ...form, password: e.target.value })}
          />
        </FormGrid>
      </Modal>
      <Modal
        open={modal === "lecturer"}
        onClose={() => setModal(null)}
        title="Create Lecturer"
        footer={
          <>
            <Button variant="secondary" onClick={() => setModal(null)}>
              Cancel
            </Button>
            <Button onClick={() => create("lecturer")}>Create</Button>
          </>
        }
      >
        <FormGrid cols={1}>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <Input
              label="Lecturer ID"
              value={form.id}
              onChange={(e) => setForm({ ...form, id: e.target.value })}
            />
            <Input
              label="Full Name"
              value={form.fullName}
              onChange={(e) => setForm({ ...form, fullName: e.target.value })}
            />
            <Input
              label="Email"
              type="email"
              value={form.email}
              onChange={(e) => setForm({ ...form, email: e.target.value })}
            />
            <Input
              label="Initial Password"
              type="password"
              value={form.password}
              onChange={(e) => setForm({ ...form, password: e.target.value })}
            />
          </div>
          <div>
            <label className="text-sm font-medium text-slate-700">
              Teaching Qualifications
            </label>
            <CoursePicker
              selected={form.qualifications}
              onChange={(q) => setForm({ ...form, qualifications: q })}
              courses={courses}
            />
            <p className="text-xs text-slate-400 mt-1">
              Select the courses this lecturer is qualified to teach.
            </p>
          </div>
        </FormGrid>
      </Modal>
      <ConfirmDialog
        open={!!del}
        onClose={() => setDel(null)}
        onConfirm={deactivate}
        title="Deactivate User"
        message={`Deactivate ${del?.fullName}? They will no longer be able to log in.`}
        confirmLabel="Deactivate"
      />
    </div>
  )
}

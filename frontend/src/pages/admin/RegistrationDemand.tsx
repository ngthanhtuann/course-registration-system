import { useEffect, useMemo, useRef, useState } from "react"

import {
  Card,
  Button,
  Select,
  Badge,
  DataTable,
  SectionHeader,
  Modal,
  Alert,
  SearchBox,
} from "../../components/ui"

import type { Column } from "../../components/ui"

import { api } from "../../services/api"


export default function ManageRegistrationDemand() {
  const [periods, setPeriods] = useState<any[]>([])
  const [majors, setMajors] = useState<any[]>([])

  const [period, setPeriod] = useState("")
  const [major, setMajor] = useState("")
  const [search, setSearch] = useState("")

  const [course, setCourse] = useState("")

  const [rows, setRows] = useState<any[]>([])
  const [students, setStudents] = useState<any[]>([])

  const [msg, setMsg] = useState("")
  const [err, setErr] = useState("")
  const [loading, setLoading] = useState(true)
  const [loadError, setLoadError] = useState("")
  const [demandLoading, setDemandLoading] = useState(false)
  const [demandError, setDemandError] = useState("")
  const [studentsLoading, setStudentsLoading] = useState(false)
  const [studentsError, setStudentsError] = useState("")
  const [exporting, setExporting] = useState(false)
  const studentRequest = useRef(0)


  // =========================================================
  // LOAD PERIODS + MAJORS
  // =========================================================

  useEffect(() => {
    Promise.all([
      api.admin.periods(),
      api.admin.majors(),
    ])
      .then(([p, m]) => {
        setPeriods(p)
        setMajors(m)
      })
      .catch((e) => {
        setLoadError(e.message)
      })
      .finally(() => setLoading(false))
  }, [])


  // =========================================================
  // LOAD DEMAND REPORT
  // =========================================================

  useEffect(() => {
    let active = true
    studentRequest.current += 1
    setCourse("")
    setDemandError("")
    if (!period) {
      setRows([])
      setDemandLoading(false)
      return
    }
    setDemandLoading(true)
    api.admin
      .demand(period, major)
      .then((data) => {
        if (active) setRows(data)
      })
      .catch((e) => {
        if (active) setDemandError(e.message)
      })
      .finally(() => {
        if (active) setDemandLoading(false)
      })
    return () => { active = false }
  }, [period, major])

  const filteredRows = useMemo(() => {
    const keyword = search.trim().toLowerCase()
    if (!keyword) return rows

    return rows.filter((row) =>
      String(row.course_code || "").toLowerCase().includes(keyword) ||
      String(row.course_name || "").toLowerCase().includes(keyword)
    )
  }, [rows, search])

  // =========================================================
  // VIEW STUDENTS
  // =========================================================

  const view = async (code: string) => {
    const request = ++studentRequest.current
    setCourse(code)
    setStudentsError("")
    setStudentsLoading(true)
    try {
      const data = await api.admin.demandStudents(code, period, major)
      if (request === studentRequest.current) setStudents(data)
    } catch (e: any) {
      if (request === studentRequest.current)
        setStudentsError(e?.message || "Could not load registered students.")
    } finally {
      if (request === studentRequest.current) setStudentsLoading(false)
    }
  }
  const exportReport = async () => {
    if (!period || exporting) return
    setExporting(true)
    setErr("")
    setMsg("")
    try {
      const report = await api.admin.demandReport(period, major)
      const url = URL.createObjectURL(report)
      const link = document.createElement("a")
      link.href = url
      link.download = "registration-demand.csv"
      document.body.appendChild(link)
      link.click()
      link.remove()
      window.setTimeout(() => URL.revokeObjectURL(url), 1000)
      setMsg("Demand report generated successfully.")
    } catch (e: any) {
      setErr(e.message || "Could not generate the demand report.")
    } finally {
      setExporting(false)
    }
  }

  // =========================================================
  // TABLE
  // =========================================================

  const cols: Column<any>[] = [
    {
      key: "course_code",
      header: "Course Code",

      render: (r) => (
        <span className="font-mono text-xs">
          {r.course_code}
        </span>
      ),
    },

    {
      key: "course_name",
      header: "Course Name",
    },

    {
      key: "registered_students",
      header: "Registered Students",
    },

    {
      key: "actions",
      header: "Details",

      render: (r) => (
        <Button
          size="sm"
          variant="ghost"
          onClick={() =>
            view(r.course_code)
          }
        >
          View Students
        </Button>
      ),
    },
  ]


  // =========================================================
  // UI
  // =========================================================

  return (
    <div>
      <SectionHeader
        title="Registration Demand"
        subtitle="Review demand from registrations and use it for class planning"
      />

      <Card className="p-4 mb-4">
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">

          <Select
            label="Registration Period"
            disabled={loading || !!loadError || exporting}
            options={periods.map((p) => ({
              value: p.period_id,

              label:
                `${p.period_name} — ${p.semester_name}`,
            }))}
            value={period}
            onChange={(e) =>
              setPeriod(e.target.value)
            }
            placeholder="Select period"
          />

          <Select
            label="Major"
            disabled={loading || !!loadError || exporting}
            options={majors.map((m) => ({
              value: m.major_code,
              label: m.major_name,
            }))}
            value={major}
            onChange={(e) =>
              setMajor(e.target.value)
            }
            placeholder="All majors"
          />

        </div>

        <div className="mt-4">
          <p className="text-sm font-medium text-slate-700 mb-1.5">Search Course</p>
          <SearchBox
            value={search}
            onChange={setSearch}
            placeholder="Search by course code or course name..."
          />
        </div>

        <Button className="mt-4" onClick={exportReport} disabled={!period || loading || demandLoading || !!loadError || !!demandError || exporting}>
          {exporting ? "Generating…" : "Generate Demand Report (CSV)"}
        </Button>
      </Card>


      {msg && (
        <Alert
          type="success"
          message={msg}
        />
      )}


      {err && (
        <div className="mb-3">
          <Alert
            type="error"
            message={err}
          />
        </div>
      )}


      <Card>
        <DataTable
          loading={loading || demandLoading}
          error={loadError || demandError}
          columns={cols}
          rows={filteredRows}
          keyFn={(r) =>
            r.course_code
          }
          emptyText={
            !period
              ? "Select a registration period to view demand."
              : search.trim()
                ? "No courses match your search."
                : "No registration demand found."
          }
        />
      </Card>


      <Modal
        open={!!course}
        onClose={() => {
          studentRequest.current += 1
          setCourse("")
          setStudents([])
        }}
        title={`Registered Students — ${course}`}
        size="sm"
        footer={
          <Button
            variant="secondary"
            onClick={() => {
              studentRequest.current += 1
              setCourse("")
              setStudents([])
            }}
          >
            Close
          </Button>
        }
      >

        <DataTable
          loading={studentsLoading}
          error={studentsError}
          columns={[
            {
              key: "student_id",
              header: "Student ID",
            },

            {
              key: "fullname",
              header: "Name",
            },

            {
              key: "email",
              header: "Email",
            },

            {
              key: "registration_status",
              header: "Status",

              render: (r) => (
                <Badge
                  label={
                    r.registration_status
                  }
                />
              ),
            },
          ]}
          rows={students}
          keyFn={(r) =>
            r.student_id
          }
          emptyText="No students registered."
        />

      </Modal>
    </div>
  )
}
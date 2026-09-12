import { useEffect, useMemo, useState } from "react"

import {
  Card,
  SearchBox,
  DataTable,
  SectionHeader,
  Modal,
  Button,
  Badge,
} from "../../components/ui"

import type { Column } from "../../components/ui"

import { api } from "../../services/api"

import type { Student } from "../../types"


export default function ViewCourses({
  user,
}: {
  user: Student
}) {
  // =========================================================
  // STATE
  // =========================================================

  const [courses, setCourses] = useState<any[]>([])

  const [search, setSearch] = useState("")

  const [view, setView] = useState<any>(null)

  const [loading, setLoading] = useState(true)

  const [error, setError] = useState("")


  // =========================================================
  // LOAD COURSES ONLY ONCE
  // =========================================================

  useEffect(() => {
    let cancelled = false

    async function loadCourses() {
      try {
        setLoading(true)

        setError("")

        const data =
          await api.student.courses("", "")

        if (!cancelled) {
          setCourses(
            Array.isArray(data)
              ? data
              : []
          )
        }
      } catch (err: any) {
        if (!cancelled) {
          setCourses([])

          setError(
            err?.message ||
              "Could not load courses."
          )
        }
      } finally {
        if (!cancelled) {
          setLoading(false)
        }
      }
    }

    loadCourses()

    return () => {
      cancelled = true
    }
  }, [])


  // =========================================================
  // FRONTEND SEARCH
  // =========================================================

  const rows = useMemo(() => {
    const keyword =
      search
        .trim()
        .toLowerCase()

    if (!keyword) {
      return courses
    }

    return courses.filter(
      (course) => {
        const code =
          String(
            course.course_code || ""
          ).toLowerCase()

        const name =
          String(
            course.course_name || ""
          ).toLowerCase()

        return (
          code.includes(keyword) ||
          name.includes(keyword)
        )
      }
    )
  }, [courses, search])


  // =========================================================
  // TABLE COLUMNS
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

      render: (r) => (
        <span className="font-medium">
          {r.course_name}
        </span>
      ),
    },

    {
      key: "credit",

      header: "Credits",
    },

    {
      key: "recommended_semester",

      header: "Recommended Semester",
    },

    {
      key: "prerequisite_status",

      header: "Prerequisite",

      render: (r) => (
        <Badge
          label={
            r.prerequisite_status === "N/A"
              ? "Satisfied"
              : r.prerequisite_status
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
          variant="ghost"
          onClick={() => setView(r)}
        >
          View
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
        title="View Courses"
        subtitle={`Courses in the ${user.major} curriculum`}
      />

      <Card className="p-4 mb-4">
        <SearchBox
          value={search}
          onChange={setSearch}
          placeholder="Search by course code or name…"
        />
      </Card>

      {error && (
        <Card className="p-4 mb-4">
          <p className="text-sm text-red-600">
            {error}
          </p>
        </Card>
      )}

      <Card>
        {loading ? (
          <div className="p-6 text-sm text-slate-500">
            Loading courses...
          </div>
        ) : (
          <DataTable
            columns={cols}
            rows={rows}
            keyFn={(r) =>
              r.course_code
            }
            emptyText="No courses available."
          />
        )}
      </Card>

      <Modal
        open={!!view}
        onClose={() => setView(null)}
        title="Course Details"
        footer={
          <Button
            variant="secondary"
            onClick={() =>
              setView(null)
            }
          >
            Close
          </Button>
        }
      >
        {view && (
          <div className="grid grid-cols-2 gap-3">
            {[
              [
                "Code",
                view.course_code,
              ],

              [
                "Name",
                view.course_name,
              ],

              [
                "Credits",
                view.credit,
              ],

              [
                "Prerequisite",
                view.prerequisite_name ||
                  "None",
              ],

              [
                "Recommended Semester",
                view.recommended_semester,
              ],

              [
                "Capacity",
                view.max_capacity,
              ],
            ].map(([key, value]) => (
              <div
                key={String(key)}
                className="bg-slate-50 p-3 rounded"
              >
                <p className="text-xs text-slate-500">
                  {key}
                </p>

                <p className="text-sm font-semibold">
                  {value}
                </p>
              </div>
            ))}
          </div>
        )}
      </Modal>
    </div>
  )
}
// Chỉ tải code của trang được trỏ tới, không gọi API hay tải mọi trang cùng lúc.
const pages: Record<string, () => Promise<unknown>> = {
  "/admin/users": () => import("../pages/admin/ManageUser"),
  "/admin/majors": () => import("../pages/admin/ManageMajors"),
  "/admin/curriculum": () => import("../pages/admin/ManageCurriculum"),
  "/admin/courses": () => import("../pages/admin/ManageCourses"),
  "/admin/semesters": () => import("../pages/admin/ManageSemesters"),
  "/admin/registration-period": () => import("../pages/admin/RegistrationPeriod"),
  "/admin/registration-demand": () => import("../pages/admin/RegistrationDemand"),
  "/admin/assign-lecturer": () => import("../pages/admin/AssignLecturer"),
  "/admin/account": () => import("../pages/ManageAccount"),
  "/lecturer/courses": () => import("../pages/lecturer/TeachingCourses"),
  "/lecturer/grades": () => import("../pages/lecturer/ManageGrades"),
  "/lecturer/account": () => import("../pages/ManageAccount"),
  "/student/courses": () => import("../pages/student/ViewCourses"),
  "/student/register": () => import("../pages/student/CourseRegistration"),
  "/student/status": () => import("../pages/student/RegistrationStatus"),
  "/student/drop": () => import("../pages/student/DropCourse"),
  "/student/grades": () => import("../pages/student/ViewGrades"),
  "/student/account": () => import("../pages/ManageAccount"),
}

export function prefetchPage(path: string) {
  const load = pages[path]
  if (!load) return // Dashboard đã được tải sẵn trong App.

  // Trình duyệt dùng chung module với React.lazy, không tải lại khi bấm menu.
  // Lỗi tải trước không được làm gián đoạn thao tác hiện tại.
  void load().catch(() => {})
}

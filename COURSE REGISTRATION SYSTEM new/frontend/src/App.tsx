import React, { useEffect, useState } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import type { AuthUser, Student, Lecturer } from './types';
import Layout from './components/Layout';
import { RegistrationProvider } from './context/RegistrationContext';
import Login from './pages/Login';
import ManageAccount from './pages/ManageAccount';
import AdminDashboard from './pages/admin/Dashboard';
import ManageUser from './pages/admin/ManageUser';
import ManageMajor from './pages/admin/ManageMajor';
import ManageCurriculum from './pages/admin/ManageCurriculum';
import ManageCourse from './pages/admin/ManageCourse';
import ManageSemester from './pages/admin/ManageSemester';
import ManageRegistrationPeriod from './pages/admin/ManageRegistrationPeriod';
import ManageRegistrationDemand from './pages/admin/ManageRegistrationDemand';
import AssignLecturer from './pages/admin/AssignLecturer';
import LecturerDashboard from './pages/lecturer/Dashboard';
import ManageTeachingCourse from './pages/lecturer/ManageTeachingCourse';
import ManageStudentGrades from './pages/lecturer/ManageStudentGrades';
import StudentDashboard from './pages/student/Dashboard';
import ViewCourses from './pages/student/ViewCourses';
import CourseRegistration from './pages/student/CourseRegistration';
import ViewRegistrationStatus from './pages/student/ViewRegistrationStatus';
import DropCourse from './pages/student/DropCourse';
import ViewGrades from './pages/student/ViewGrades';
import { api, clearAuth, getStoredUser, saveAuth } from './api';

function ProtectedLayout({ user, onLogout, requiredRole, children }: { user: AuthUser; onLogout: () => void; requiredRole: string; children: React.ReactNode }) {
  if (!user) return <Navigate to="/login" replace />;
  if (user.role !== requiredRole) {
    const redirect = user.role === 'admin' ? '/admin/dashboard' : user.role === 'lecturer' ? '/lecturer/dashboard' : '/student/dashboard';
    return <Navigate to={redirect} replace />;
  }
  return <Layout user={user} onLogout={onLogout}>{children}</Layout>;
}

export default function App() {
  const [user, setUser] = useState<AuthUser>(() => getStoredUser<AuthUser>());
  const [checkingSession, setCheckingSession] = useState(true);

  useEffect(() => {
    let alive = true;
    const restore = async () => {
      if (!user) { if (alive) setCheckingSession(false); return; }
      try {
        const base = await api.me();
        let full: any = base;
        if (base.role === 'student') full = await api.student.profile();
        if (base.role === 'lecturer') full = await api.lecturer.profile();
        const normalized = base.role === 'student'
          ? { id: full.user_id, username: full.username, fullName: full.fullname, email: full.email, role: 'student', status: 'Active', studentId: full.student_id, major: full.major_code }
          : base.role === 'lecturer'
          ? { id: full.user_id, username: full.username, fullName: full.fullname, email: full.email, role: 'lecturer', status: 'Active', lecturerId: full.lecturer_id, qualifications: full.qualifications || [] }
          : { id: full.user_id, username: full.username, fullName: full.fullname, email: full.email, role: 'admin', status: 'Active' };
        if (alive) { setUser(normalized as AuthUser); saveAuth(localStorage.getItem('crs_token') || '', normalized); }
      } catch {
        if (alive) { clearAuth(); setUser(null); }
      } finally { if (alive) setCheckingSession(false); }
    };
    restore();
    return () => { alive = false; };
  }, []);

  const handleLogout = () => { clearAuth(); setUser(null); };
  if (checkingSession) return <div className="min-h-screen flex items-center justify-center text-slate-500">Loading…</div>;

  return (
    <RegistrationProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={user ? <Navigate to={user.role === 'admin' ? '/admin/dashboard' : user.role === 'lecturer' ? '/lecturer/dashboard' : '/student/dashboard'} replace /> : <Login onLogin={setUser} />} />
          <Route path="/admin/*" element={<ProtectedLayout user={user} onLogout={handleLogout} requiredRole="admin"><Routes>
            <Route path="dashboard" element={<AdminDashboard />} /><Route path="users" element={<ManageUser />} /><Route path="majors" element={<ManageMajor />} />
            <Route path="curriculum" element={<ManageCurriculum />} /><Route path="courses" element={<ManageCourse />} /><Route path="semesters" element={<ManageSemester />} />
            <Route path="registration-period" element={<ManageRegistrationPeriod />} /><Route path="registration-demand" element={<ManageRegistrationDemand />} /><Route path="assign-lecturer" element={<AssignLecturer />} />
            <Route path="account" element={<ManageAccount user={user} onLogout={handleLogout} />} /><Route path="*" element={<Navigate to="/admin/dashboard" replace />} />
          </Routes></ProtectedLayout>} />
          <Route path="/lecturer/*" element={<ProtectedLayout user={user} onLogout={handleLogout} requiredRole="lecturer"><Routes>
            <Route path="dashboard" element={<LecturerDashboard user={user as Lecturer} />} /><Route path="courses" element={<ManageTeachingCourse user={user as Lecturer} />} />
            <Route path="grades" element={<ManageStudentGrades user={user as Lecturer} />} /><Route path="account" element={<ManageAccount user={user} onLogout={handleLogout} />} /><Route path="*" element={<Navigate to="/lecturer/dashboard" replace />} />
          </Routes></ProtectedLayout>} />
          <Route path="/student/*" element={<ProtectedLayout user={user} onLogout={handleLogout} requiredRole="student"><Routes>
            <Route path="dashboard" element={<StudentDashboard user={user as Student} />} /><Route path="courses" element={<ViewCourses user={user as Student} />} />
            <Route path="register" element={<CourseRegistration user={user as Student} />} /><Route path="status" element={<ViewRegistrationStatus user={user as Student} />} />
            <Route path="drop" element={<DropCourse user={user as Student} />} /><Route path="grades" element={<ViewGrades user={user as Student} />} /><Route path="account" element={<ManageAccount user={user} onLogout={handleLogout} />} />
            <Route path="*" element={<Navigate to="/student/dashboard" replace />} />
          </Routes></ProtectedLayout>} />
          <Route path="*" element={<Navigate to="/login" replace />} />
        </Routes>
      </BrowserRouter>
    </RegistrationProvider>
  );
}

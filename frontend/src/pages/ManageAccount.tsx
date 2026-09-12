import React, { useState } from "react"
import { useNavigate } from "react-router-dom"
import {
  Card,
  Button,
  Input,
  Alert,
  SectionHeader,
  Badge,
} from "../components/ui"
import type { AuthUser, Student, Lecturer } from "../types"
import { api } from "../services/api"
interface Props {
  user: AuthUser
  onLogout: () => void | Promise<void>
  onUserUpdated: (user: any) => void
}
export default function ManageAccount({ user, onLogout, onUserUpdated }: Props) {
  const navigate = useNavigate()
  const [tab, setTab] = useState<"profile" | "password">("profile")
  const [success, setSuccess] = useState("")
  const [error, setError] = useState("")
  const [fullname, setFullname] = useState(user?.fullName || "")
  const [email, setEmail] = useState(user?.email || "")
  const [currentPassword, setCurrentPassword] = useState("")
  const [newPassword, setNewPassword] = useState("")
  const [confirmPassword, setConfirmPassword] = useState("")
  const [loading, setLoading] = useState(false)
  const student = user?.role === "student" ? user as Student : null
  const lecturer = user?.role === "lecturer" ? user as Lecturer : null
  const handleProfile = async (e: React.FormEvent) => {
    e.preventDefault()
    setError("")
    setSuccess("")
    if (!fullname.trim() || !email.trim()) {
      setError("Full name and email are required.")
      return
    }
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.trim())) {
      setError("Invalid email address.")
      return
    }
    setLoading(true)
    try {
      const result = await api.updateProfile(fullname.trim(), email.trim())
      if (result?.user) onUserUpdated(result.user)
      setSuccess("Profile updated successfully.")
    } catch (err: any) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }
  const handlePassword = async (e: React.FormEvent) => {
    e.preventDefault()
    setError("")
    setSuccess("")
    if (!currentPassword || !newPassword || !confirmPassword) {
      setError("All password fields are required.")
      return
    }
    if (newPassword !== confirmPassword) {
      setError("New passwords do not match.")
      return
    }
    if (newPassword.length < 8) {
      setError("Password must be at least 8 characters.")
      return
    }
    setLoading(true)
    try {
      await api.changePassword(currentPassword, newPassword)
      setCurrentPassword("")
      setNewPassword("")
      setConfirmPassword("")

      // Changing the password revokes every existing JWT, including this one.
      // Clear the current session and require a fresh login with the new password.
      await onLogout()
      navigate("/login")
    } catch (err: any) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }
  const logout = async () => {
    await onLogout()
    navigate("/login")
  }
  return (
    <div className="max-w-2xl mx-auto">
      <SectionHeader
        title="Manage Account"
        subtitle="View and update your account settings"
      />
      <div className="flex gap-2 mb-6 border-b border-slate-200">
        {(["profile", "password"] as const).map((t) => (
          <button
            key={t}
            onClick={() => {
              setTab(t)
              setError("")
              setSuccess("")
            }}
            className={`px-4 py-2.5 text-sm font-medium border-b-2 ${
              tab === t
                ? "border-blue-600 text-blue-600"
                : "border-transparent text-slate-500"
            }`}
          >
            {t === "password" ? "Change Password" : "Profile"}
          </button>
        ))}
      </div>
      {tab === "profile" ? (
        <Card className="p-6">
          <form onSubmit={handleProfile} className="flex flex-col gap-5">
            <div className="flex items-center gap-4 pb-4 border-b border-slate-100">
              <div className="w-16 h-16 bg-blue-600 rounded-full flex items-center justify-center text-white text-2xl font-bold">
                {user?.fullName?.charAt(0)}
              </div>
              <div>
                <p className="font-semibold text-slate-800 text-lg">
                  {user?.fullName}
                </p>
                <Badge
                  label={
                    user?.role === "admin"
                      ? "Administrator"
                      : user?.role === "lecturer"
                        ? "Lecturer"
                        : "Student"
                  }
                />
              </div>
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <Input
                label="Username"
                value={user?.username || ""}
                readOnly
                className="bg-slate-50"
              />
              <Input
                label="Full Name"
                value={fullname}
                onChange={(e) => setFullname(e.target.value)}
              />
              <Input
                label="Email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="sm:col-span-2"
              />
              <Input
                label="Role"
                value={
                  user?.role === "admin"
                    ? "Administrator"
                    : user?.role === "lecturer"
                      ? "Lecturer"
                      : "Student"
                }
                readOnly
                className="bg-slate-50"
              />
            </div>
            {student && (
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-2 border-t border-slate-100">
                <Input
                  label="Student ID"
                  value={student.studentId}
                  readOnly
                  className="bg-slate-50"
                />
                <Input
                  label="Major"
                  value={student.major}
                  readOnly
                  className="bg-slate-50"
                />
              </div>
            )}
            {lecturer && (
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-2 border-t border-slate-100">
                <Input
                  label="Lecturer ID"
                  value={lecturer.lecturerId}
                  readOnly
                  className="bg-slate-50"
                />
                <Input
                  label="Qualifications"
                  value={lecturer.qualifications.join(", ") || "None"}
                  readOnly
                  className="bg-slate-50"
                />
              </div>
            )}
            {success && <Alert type="success" message={success} />}{" "}
            {error && <Alert type="error" message={error} />}
            <Button type="submit" disabled={loading}>
              {loading ? "Saving…" : "Save Changes"}
            </Button>
          </form>
        </Card>
      ) : (
        <Card className="p-6">
          <form
            onSubmit={handlePassword}
            className="flex flex-col gap-4 max-w-sm"
          >
            <Input
              label="Current Password"
              type="password"
              value={currentPassword}
              onChange={(e) => setCurrentPassword(e.target.value)}
            />
            <Input
              label="New Password"
              type="password"
              value={newPassword}
              onChange={(e) => setNewPassword(e.target.value)}
            />
            <Input
              label="Confirm New Password"
              type="password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
            />
            {success && <Alert type="success" message={success} />}{" "}
            {error && <Alert type="error" message={error} />}
            <Button type="submit" disabled={loading}>
              {loading ? "Changing…" : "Change Password"}
            </Button>
          </form>
        </Card>
      )}
      <Card className="p-4 mt-4 border-red-100 bg-red-50">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm font-medium text-red-800">
              Sign out of your account
            </p>
            <p className="text-xs text-red-500 mt-0.5">
              You will be redirected to the login page.
            </p>
          </div>
          <Button variant="danger" onClick={logout} size="sm">
            Logout
          </Button>
        </div>
      </Card>
    </div>
  )
}

import React, { useState } from "react"
import { useNavigate } from "react-router-dom"
import { Button, Input, Alert } from "../components/ui"
import type { AuthUser } from "../types"
import { api, saveAuth } from "../api"

interface LoginProps {
  onLogin: (user: AuthUser) => void
}

export default function Login({ onLogin }: LoginProps) {
  const navigate = useNavigate()

  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")
  const [showPassword, setShowPassword] = useState(false)
  const [error, setError] = useState("")
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError("")

    if (!username.trim() || !password) {
      setError("Please enter your username and password.")
      return
    }

    setLoading(true)

    try {
      // Login
      const result = await api.login(username.trim(), password)

      /*
       * IMPORTANT:
       * Save the JWT BEFORE calling protected APIs such as
       * /api/student/profile or /api/lecturer/profile.
       */
      saveAuth(result.token, result.user)

      const base = result.user
      let full: any = base

      // Get full Student profile
      if (base.role === "student") {
        full = await api.student.profile()
      }

      // Get full Lecturer profile
      if (base.role === "lecturer") {
        full = await api.lecturer.profile()
      }

      // Build frontend user object
      const user: any =
        base.role === "student"
          ? {
              id: full.user_id,
              username: full.username,
              fullName: full.fullname,
              email: full.email,
              role: "student",
              status: "Active",
              studentId: full.student_id,
              major: full.major_code,
            }
          : base.role === "lecturer"
            ? {
                id: full.user_id,
                username: full.username,
                fullName: full.fullname,
                email: full.email,
                role: "lecturer",
                status: "Active",
                lecturerId: full.lecturer_id,
                qualifications: full.qualifications || [],
              }
            : {
                id: base.user_id,
                username: base.username,
                fullName: base.fullname,
                email: base.email,
                role: "admin",
                status: "Active",
              }

      // Save the complete user information
      saveAuth(result.token, user)

      // Update application authentication state
      onLogin(user as AuthUser)

      // Navigate according to role
      if (user.role === "admin") {
        navigate("/admin/dashboard")
      } else if (user.role === "lecturer") {
        navigate("/lecturer/dashboard")
      } else {
        navigate("/student/dashboard")
      }
    } catch (err: any) {
      setError(
        err?.message || "Invalid username or password. Please try again.",
      )
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-slate-100 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-blue-600 rounded-2xl shadow-lg mb-4">
            <svg
              width="32"
              height="32"
              fill="none"
              stroke="white"
              strokeWidth="2"
              viewBox="0 0 24 24"
            >
              <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5" />
            </svg>
          </div>

          <h1 className="text-2xl font-bold text-slate-800">
            Course Registration System
          </h1>

          <p className="text-sm text-slate-500 mt-1">
            University Academic Management
          </p>
        </div>

        <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-8">
          <h2 className="text-lg font-semibold text-slate-800 mb-6">
            Sign in to your account
          </h2>

          <form onSubmit={handleSubmit} className="flex flex-col gap-4">
            <Input
              label="Username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Enter your username"
              autoComplete="username"
            />

            <div className="flex flex-col gap-1">
              <label className="text-sm font-medium text-slate-700">
                Password
              </label>

              <div className="relative">
                <input
                  type={showPassword ? "text" : "password"}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="Enter your password"
                  autoComplete="current-password"
                  className="w-full rounded-lg border border-slate-200 bg-white px-3 py-2 text-sm text-slate-800 focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
                />

                <button
                  type="button"
                  onClick={() => setShowPassword((v) => !v)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-xs text-slate-400"
                >
                  {showPassword ? "Hide" : "Show"}
                </button>
              </div>
            </div>

            {error && <Alert type="error" message={error} />}

            <Button
              type="submit"
              fullWidth
              disabled={loading}
              size="lg"
              className="mt-2"
            >
              {loading ? "Signing in…" : "Sign In"}
            </Button>
          </form>
        </div>
      </div>
    </div>
  )
}

import React, { createContext, useContext } from "react"
import type { AuthUser } from "../types"

type AuthContextValue = {
  user: AuthUser | null
  setUser: (user: AuthUser | null) => void
}

const AuthContext = createContext<AuthContextValue | null>(null)

export function AuthProvider({ children, value }: { children: React.ReactNode; value: AuthContextValue }) {
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth(): AuthContextValue {
  const context = useContext(AuthContext)
  if (!context) throw new Error("useAuth must be used inside AuthProvider")
  return context
}

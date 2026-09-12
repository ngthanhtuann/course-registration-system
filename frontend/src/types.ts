export type Role = "admin" | "lecturer" | "student"

export interface User {
  id: string
  username: string
  fullName: string
  email: string
  role: Role
  status: "Active" | "Inactive"
}

export interface Student extends User {
  role: "student"
  studentId: string
  major: string
}

export interface Lecturer extends User {
  role: "lecturer"
  lecturerId: string
  qualifications: string[]
}

export interface Major {
  code: string
  name: string
}

export interface Course {
  code: string
  name: string
  credits: number
  prerequisite: string | null
  capacity: number
}

export interface Semester {
  id: string
  name: string
  startDate: string
  endDate: string
  status: "Active" | "Upcoming" | "Completed"
}

export interface RegistrationPeriod {
  id: string
  semesterId: string
  startDateTime: string
  endDateTime: string
  dropStartDateTime: string
  dropEndDateTime: string
  status: "Scheduled" | "Open" | "Closed"
  periodName?: string
}

export type AuthUser = Student | Lecturer | User & { role: "admin" } | null

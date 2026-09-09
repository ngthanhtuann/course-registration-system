import type { Student, Lecturer, User, Major, Course, CurriculumItem, Semester, RegistrationPeriod, CourseRegistration, TeachingAssignment } from './types';

// Kept for the original project structure. Runtime application data is loaded from PostgreSQL via api.ts.
export const MAJORS: Major[] = [];
export const COURSES: Course[] = [];
export const CURRICULUM: CurriculumItem[] = [];
export const SEMESTERS: Semester[] = [];
export const REGISTRATION_PERIODS: RegistrationPeriod[] = [];
export const STUDENTS: Student[] = [];
export const LECTURERS: Lecturer[] = [];
export const ALL_USERS: User[] = [];
export const REGISTRATIONS: CourseRegistration[] = [];
export const TEACHING_ASSIGNMENTS: TeachingAssignment[] = [];
export const DEMO_CREDENTIALS: Record<string, { password: string; userId: string }> = {};

import React, { createContext, useContext, useState } from 'react';
import { REGISTRATIONS as INITIAL } from '../data';
import type { CourseRegistration } from '../types';

interface RegistrationContextValue {
  registrations: CourseRegistration[];
  register: (reg: CourseRegistration) => void;
  drop: (studentId: string, courseCode: string, semesterId: string) => void;
  countActive: (courseCode: string, semesterId: string) => number;
}

const Ctx = createContext<RegistrationContextValue | null>(null);

export function RegistrationProvider({ children }: { children: React.ReactNode }) {
  const [registrations, setRegistrations] = useState<CourseRegistration[]>(INITIAL);

  const countActive = (courseCode: string, semesterId: string) =>
    registrations.filter(r => r.courseCode === courseCode && r.semesterId === semesterId && r.status === 'Registered').length;

  const register = (reg: CourseRegistration) => {
    setRegistrations(prev => {
      const exists = prev.find(r => r.studentId === reg.studentId && r.courseCode === reg.courseCode && r.semesterId === reg.semesterId);
      if (exists) return prev.map(r => r.studentId === reg.studentId && r.courseCode === reg.courseCode && r.semesterId === reg.semesterId ? { ...r, status: 'Registered' } : r);
      return [...prev, reg];
    });
  };

  const drop = (studentId: string, courseCode: string, semesterId: string) => {
    setRegistrations(prev => prev.map(r =>
      r.studentId === studentId && r.courseCode === courseCode && r.semesterId === semesterId
        ? { ...r, status: 'Dropped' }
        : r
    ));
  };

  return <Ctx.Provider value={{ registrations, register, drop, countActive }}>{children}</Ctx.Provider>;
}

export function useRegistrations() {
  const ctx = useContext(Ctx);
  if (!ctx) throw new Error('useRegistrations must be used within RegistrationProvider');
  return ctx;
}

BEGIN;

-- Keep existing rows and make the legacy schema expose the names used by backend.
ALTER TYPE user_role ADD VALUE IF NOT EXISTS 'admin';
ALTER TYPE user_role ADD VALUE IF NOT EXISTS 'lecturer';
ALTER TYPE user_role ADD VALUE IF NOT EXISTS 'student';
DROP TRIGGER IF EXISTS trg_students_profile_role ON students;
DROP TRIGGER IF EXISTS trg_lecturers_profile_role ON lecturers;
DROP TRIGGER IF EXISTS trg_registration_seats ON registrations;
DROP TRIGGER IF EXISTS trg_assignment_qualification ON teaching_assignments;
DROP TRIGGER IF EXISTS trg_users_prevent_profile_role_change ON users;

ALTER TABLE users DROP CONSTRAINT IF EXISTS users_role_check;
ALTER TABLE students DROP CONSTRAINT IF EXISTS students_user_id_fkey;
ALTER TABLE lecturers DROP CONSTRAINT IF EXISTS lecturers_user_id_fkey;
ALTER TABLE registration_periods DROP CONSTRAINT IF EXISTS registration_periods_semester_id_fkey;
ALTER TABLE registrations DROP CONSTRAINT IF EXISTS registrations_semester_id_fkey;
ALTER TABLE teaching_assignments DROP CONSTRAINT IF EXISTS teaching_assignments_semester_id_fkey;
ALTER TABLE grades DROP CONSTRAINT IF EXISTS grades_semester_id_fkey;
ALTER TABLE curriculums DROP CONSTRAINT IF EXISTS curriculums_course_id_fkey;
ALTER TABLE grades DROP CONSTRAINT IF EXISTS grades_course_id_fkey;
ALTER TABLE lecturer_qualifications DROP CONSTRAINT IF EXISTS lecturer_qualifications_course_id_fkey;
ALTER TABLE registrations DROP CONSTRAINT IF EXISTS registrations_course_id_fkey;
ALTER TABLE teaching_assignments DROP CONSTRAINT IF EXISTS teaching_assignments_course_id_fkey;
ALTER TABLE courses DROP CONSTRAINT IF EXISTS courses_prerequisite_course_id_fkey;

ALTER TABLE users ALTER COLUMN user_id DROP IDENTITY IF EXISTS;
ALTER TABLE users ALTER COLUMN user_id DROP DEFAULT;
ALTER TABLE semesters ALTER COLUMN semester_id DROP IDENTITY IF EXISTS;
ALTER TABLE semesters ALTER COLUMN semester_id DROP DEFAULT;
ALTER TABLE registration_periods ALTER COLUMN period_id DROP IDENTITY IF EXISTS;
ALTER TABLE registration_periods ALTER COLUMN period_id DROP DEFAULT;
ALTER TABLE teaching_assignments ALTER COLUMN assignment_id DROP IDENTITY IF EXISTS;
ALTER TABLE teaching_assignments ALTER COLUMN assignment_id DROP DEFAULT;
ALTER TABLE registrations ALTER COLUMN registration_id DROP IDENTITY IF EXISTS;
ALTER TABLE registrations ALTER COLUMN registration_id DROP DEFAULT;
ALTER TABLE lecturer_qualifications ALTER COLUMN qualification_id DROP IDENTITY IF EXISTS;
ALTER TABLE lecturer_qualifications ALTER COLUMN qualification_id DROP DEFAULT;
ALTER TABLE curriculums ALTER COLUMN curriculum_id DROP IDENTITY IF EXISTS;
ALTER TABLE curriculums ALTER COLUMN curriculum_id DROP DEFAULT;

ALTER TABLE users ALTER COLUMN user_id TYPE varchar(20) USING user_id::text;
ALTER TABLE students ALTER COLUMN user_id TYPE varchar(20) USING user_id::text;
ALTER TABLE lecturers ALTER COLUMN user_id TYPE varchar(20) USING user_id::text;

ALTER TABLE semesters ALTER COLUMN semester_id TYPE varchar(20) USING semester_id::text;
ALTER TABLE registration_periods ALTER COLUMN semester_id TYPE varchar(20) USING semester_id::text;
ALTER TABLE teaching_assignments ALTER COLUMN semester_id TYPE varchar(20) USING semester_id::text;
ALTER TABLE registrations ALTER COLUMN semester_id TYPE varchar(20) USING semester_id::text;
ALTER TABLE grades ALTER COLUMN semester_id TYPE varchar(20) USING semester_id::text;

ALTER TABLE curriculums RENAME TO curriculum;
ALTER TABLE curriculum ALTER COLUMN curriculum_id TYPE varchar(20) USING curriculum_id::text;
ALTER TABLE teaching_assignments ALTER COLUMN assignment_id TYPE varchar(20) USING assignment_id::text;
ALTER TABLE registrations ALTER COLUMN registration_id TYPE varchar(20) USING registration_id::text;
ALTER TABLE lecturer_qualifications ALTER COLUMN qualification_id TYPE varchar(20) USING qualification_id::text;

ALTER TABLE users ADD COLUMN IF NOT EXISTS password varchar(255);
ALTER TABLE users ADD COLUMN IF NOT EXISTS fullname varchar(100);
ALTER TABLE users ADD COLUMN IF NOT EXISTS email varchar(100);
UPDATE users
SET password = COALESCE(password, password_hash),
    fullname = COALESCE(fullname, username),
    email = COALESCE(email, username || '@local.invalid');
UPDATE users u SET fullname = s.full_name, email = s.email
FROM students s WHERE s.user_id = u.user_id AND u.username <> 'admin';
UPDATE users u SET fullname = l.full_name, email = l.email
FROM lecturers l WHERE l.user_id = u.user_id AND u.username <> 'admin';
DROP TRIGGER IF EXISTS trg_users_prevent_profile_role_change ON users;

ALTER TABLE students ADD COLUMN IF NOT EXISTS dob date;
ALTER TABLE students ADD COLUMN IF NOT EXISTS major_code varchar(20);
UPDATE students s SET dob = date_of_birth, major_code = m.major_code
FROM majors m WHERE m.major_id = s.major_id;

ALTER TABLE lecturers ADD COLUMN IF NOT EXISTS fullname varchar(100);
ALTER TABLE lecturers ADD COLUMN IF NOT EXISTS role varchar(20) DEFAULT 'lecturer';
UPDATE lecturers SET fullname = full_name WHERE fullname IS NULL;

ALTER TABLE courses ADD COLUMN IF NOT EXISTS prerequisite_course_code varchar(20);
ALTER TABLE courses ADD COLUMN IF NOT EXISTS max_capacity integer;
UPDATE courses c SET prerequisite_course_code = p.course_code
FROM courses p WHERE p.course_id = c.prerequisite_course_id;
UPDATE courses SET max_capacity = capacity WHERE max_capacity IS NULL;

ALTER TABLE curriculum ADD COLUMN IF NOT EXISTS major_code varchar(20);
ALTER TABLE curriculum ADD COLUMN IF NOT EXISTS course_code varchar(20);
UPDATE curriculum cu SET major_code = m.major_code
FROM majors m WHERE m.major_id::text = cu.major_id::text;
UPDATE curriculum cu SET course_code = c.course_code
FROM courses c WHERE c.course_id::text = cu.course_id::text;

ALTER TABLE lecturer_qualifications ADD COLUMN IF NOT EXISTS course_code varchar(20);
UPDATE lecturer_qualifications q SET course_code = c.course_code
FROM courses c WHERE c.course_id::text = q.course_id::text;

ALTER TABLE teaching_assignments ADD COLUMN IF NOT EXISTS course_code varchar(20);
UPDATE teaching_assignments ta SET course_code = c.course_code
FROM courses c WHERE c.course_id::text = ta.course_id::text;

ALTER TABLE registration_periods ADD COLUMN IF NOT EXISTS period_name varchar(100);
UPDATE registration_periods SET period_name = name WHERE period_name IS NULL;

ALTER TABLE registrations ADD COLUMN IF NOT EXISTS period_id varchar(20);
ALTER TABLE registrations ADD COLUMN IF NOT EXISTS course_code varchar(20);
ALTER TABLE registrations ADD COLUMN IF NOT EXISTS registration_status varchar(20);
UPDATE registrations r SET course_code = c.course_code
FROM courses c WHERE c.course_id::text = r.course_id::text;
UPDATE registrations r SET period_id = p.period_id::text
FROM registration_periods p WHERE p.semester_id::text = r.semester_id::text AND r.period_id IS NULL;
UPDATE registrations SET registration_status = lower(status::text)
WHERE registration_status IS NULL;

ALTER TABLE curriculum ALTER COLUMN major_code SET NOT NULL;
ALTER TABLE curriculum ALTER COLUMN course_code SET NOT NULL;
ALTER TABLE students ALTER COLUMN major_code SET NOT NULL;
ALTER TABLE courses ALTER COLUMN max_capacity SET NOT NULL;
ALTER TABLE registrations ALTER COLUMN period_id SET NOT NULL;
ALTER TABLE registrations ALTER COLUMN course_code SET NOT NULL;
ALTER TABLE registrations ALTER COLUMN registration_status SET NOT NULL;

ALTER TABLE students ADD CONSTRAINT students_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(user_id);
ALTER TABLE lecturers ADD CONSTRAINT lecturers_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(user_id);
ALTER TABLE registration_periods ADD CONSTRAINT registration_periods_semester_id_fkey FOREIGN KEY (semester_id) REFERENCES semesters(semester_id);
ALTER TABLE registrations ADD CONSTRAINT registrations_semester_id_fkey FOREIGN KEY (semester_id) REFERENCES semesters(semester_id);
ALTER TABLE teaching_assignments ADD CONSTRAINT teaching_assignments_semester_id_fkey FOREIGN KEY (semester_id) REFERENCES semesters(semester_id);
ALTER TABLE grades ADD CONSTRAINT grades_semester_id_fkey FOREIGN KEY (semester_id) REFERENCES semesters(semester_id);
ALTER TABLE curriculum ADD CONSTRAINT curriculums_course_id_fkey FOREIGN KEY (course_id) REFERENCES courses(course_id);
ALTER TABLE grades ADD CONSTRAINT grades_course_id_fkey FOREIGN KEY (course_id) REFERENCES courses(course_id);
ALTER TABLE lecturer_qualifications ADD CONSTRAINT lecturer_qualifications_course_id_fkey FOREIGN KEY (course_id) REFERENCES courses(course_id);
ALTER TABLE registrations ADD CONSTRAINT registrations_course_id_fkey FOREIGN KEY (course_id) REFERENCES courses(course_id);
ALTER TABLE teaching_assignments ADD CONSTRAINT teaching_assignments_course_id_fkey FOREIGN KEY (course_id) REFERENCES courses(course_id);
ALTER TABLE courses ADD CONSTRAINT courses_prerequisite_course_id_fkey FOREIGN KEY (prerequisite_course_id) REFERENCES courses(course_id);

CREATE OR REPLACE FUNCTION validate_profile_role()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
    IF TG_TABLE_NAME = 'students' AND NOT EXISTS (
        SELECT 1 FROM users WHERE user_id = NEW.user_id AND lower(role::text) = 'student'
    ) THEN
        RAISE EXCEPTION 'students.user_id must belong to a STUDENT user';
    ELSIF TG_TABLE_NAME = 'lecturers' AND NOT EXISTS (
        SELECT 1 FROM users WHERE user_id = NEW.user_id AND lower(role::text) = 'lecturer'
    ) THEN
        RAISE EXCEPTION 'lecturers.user_id must belong to a LECTURER user';
    END IF;
    RETURN NEW;
END
$$;

CREATE TRIGGER trg_students_profile_role BEFORE INSERT OR UPDATE ON students
FOR EACH ROW EXECUTE FUNCTION validate_profile_role();
CREATE TRIGGER trg_lecturers_profile_role BEFORE INSERT OR UPDATE ON lecturers
FOR EACH ROW EXECUTE FUNCTION validate_profile_role();
CREATE TRIGGER trg_registration_seats BEFORE INSERT OR UPDATE ON registrations
FOR EACH ROW EXECUTE FUNCTION maintain_registration_seats();
CREATE TRIGGER trg_assignment_qualification BEFORE INSERT OR UPDATE ON teaching_assignments
FOR EACH ROW EXECUTE FUNCTION validate_assignment_qualification();
CREATE TRIGGER trg_users_prevent_profile_role_change BEFORE UPDATE ON users
FOR EACH ROW EXECUTE FUNCTION prevent_profile_role_change();

COMMIT;

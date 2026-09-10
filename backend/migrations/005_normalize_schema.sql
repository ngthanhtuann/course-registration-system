-- Normalize the migrated legacy schema (001-004) to the backend contract.
-- Back up with pg_dump first. Run once, with psql -v ON_ERROR_STOP=1.
-- Conflicting duplicate data aborts the transaction instead of discarding it.
BEGIN;
SET LOCAL lock_timeout = '10s';
LOCK TABLE users, students, lecturers, courses, curriculum, lecturer_qualifications,
    registrations, registration_periods, semesters, teaching_assignments, grades
    IN ACCESS EXCLUSIVE MODE;
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM users WHERE full_name IS DISTINCT FROM fullname)
       OR EXISTS (SELECT 1 FROM students p JOIN users u USING(user_id)
                  WHERE p.full_name IS DISTINCT FROM u.full_name OR p.email IS DISTINCT FROM u.email)
       OR EXISTS (SELECT 1 FROM lecturers p JOIN users u USING(user_id)
                  WHERE p.full_name IS DISTINCT FROM u.full_name OR p.email IS DISTINCT FROM u.email
                     OR p.fullname IS DISTINCT FROM u.full_name)
       OR EXISTS (SELECT 1 FROM students WHERE dob IS DISTINCT FROM date_of_birth)
       OR EXISTS (SELECT 1 FROM courses WHERE capacity IS DISTINCT FROM max_capacity)
       OR EXISTS (SELECT 1 FROM courses c LEFT JOIN courses p ON p.course_id=c.prerequisite_course_id
                  WHERE c.prerequisite_course_code IS DISTINCT FROM p.course_code)
       OR EXISTS (SELECT 1 FROM students s JOIN majors m USING(major_id) WHERE s.major_code IS DISTINCT FROM m.major_code)
       OR EXISTS (SELECT 1 FROM curriculum x JOIN majors m USING(major_id) JOIN courses c USING(course_id)
                  WHERE x.major_code IS DISTINCT FROM m.major_code OR x.course_code IS DISTINCT FROM c.course_code)
       OR EXISTS (SELECT 1 FROM lecturer_qualifications x JOIN courses c USING(course_id) WHERE x.course_code IS DISTINCT FROM c.course_code)
       OR EXISTS (SELECT 1 FROM teaching_assignments x JOIN courses c USING(course_id) WHERE x.course_code IS DISTINCT FROM c.course_code)
       OR EXISTS (SELECT 1 FROM registrations x JOIN courses c USING(course_id)
                  WHERE x.course_code IS DISTINCT FROM c.course_code OR x.registration_status IS DISTINCT FROM lower(x.status::text))
       OR EXISTS (SELECT 1 FROM registration_periods WHERE name IS DISTINCT FROM period_name)
    THEN RAISE EXCEPTION 'Conflicting legacy duplicates; reconcile data before normalization'; END IF;
    IF EXISTS (SELECT 1 FROM users WHERE (account_status::text = 'ACTIVE') IS DISTINCT FROM active_status)
       OR EXISTS (SELECT 1 FROM students p JOIN users u USING(user_id) WHERE (p.status::text='ACTIVE') IS DISTINCT FROM u.active_status)
       OR EXISTS (SELECT 1 FROM lecturers p JOIN users u USING(user_id) WHERE (p.status::text='ACTIVE') IS DISTINCT FROM u.active_status)
    THEN RAISE EXCEPTION 'Conflicting account statuses; reconcile before normalization'; END IF;
    -- Legacy grade rows include authorship metadata: do not silently discard it.
    IF EXISTS (SELECT 1 FROM grades) THEN
        RAISE EXCEPTION 'Legacy grades is not empty; migrate grades and authorship before normalization';
    END IF;
END $$;

-- users is the only source of names, email, password hashes and account state.
ALTER TABLE users DROP COLUMN password, DROP COLUMN fullname, DROP COLUMN account_status;
ALTER TABLE users ALTER COLUMN full_name SET NOT NULL, ALTER COLUMN email SET NOT NULL;
DROP INDEX uq_users_single_admin;
ALTER TABLE users ALTER COLUMN role TYPE varchar(20) USING lower(role::text);
ALTER TABLE users ADD CONSTRAINT users_role_check CHECK (role IN ('admin','lecturer','student'));
ALTER TABLE users ADD CONSTRAINT users_email_key UNIQUE(email);
ALTER TABLE students DROP COLUMN full_name, DROP COLUMN email, DROP COLUMN dob, DROP COLUMN major_code, DROP COLUMN status;
ALTER TABLE lecturers DROP COLUMN full_name, DROP COLUMN fullname, DROP COLUMN email, DROP COLUMN role, DROP COLUMN status;
ALTER TABLE courses DROP COLUMN capacity, DROP COLUMN prerequisite_course_code;
ALTER TABLE courses ALTER COLUMN credit TYPE integer;
ALTER TABLE courses ADD CONSTRAINT courses_max_capacity_check CHECK (max_capacity > 0);
ALTER TABLE courses ADD CONSTRAINT courses_seats_check CHECK (available_seats >= 0 AND available_seats <= max_capacity);
ALTER TABLE curriculum DROP COLUMN major_code, DROP COLUMN course_code;
ALTER TABLE curriculum DROP CONSTRAINT curriculums_recommended_semester_check;
ALTER TABLE curriculum ALTER COLUMN recommended_semester TYPE varchar(20) USING recommended_semester::text;
ALTER TABLE curriculum ALTER COLUMN recommended_semester DROP NOT NULL;
ALTER TABLE lecturer_qualifications DROP COLUMN course_code;
ALTER TABLE teaching_assignments DROP COLUMN course_code;
ALTER TABLE registration_periods DROP COLUMN name, DROP COLUMN status;
ALTER TABLE registration_periods ALTER COLUMN period_name SET NOT NULL;
ALTER TABLE registration_periods ADD CONSTRAINT registration_periods_semester_name_key UNIQUE(semester_id,period_name);
ALTER TABLE registration_periods ADD CONSTRAINT registration_periods_semester_id_fkey FOREIGN KEY(semester_id) REFERENCES semesters(semester_id);
ALTER TABLE registration_periods ADD CONSTRAINT registration_periods_period_semester_key UNIQUE(period_id,semester_id);
ALTER TABLE registrations DROP COLUMN course_code, DROP COLUMN registration_status;
ALTER TABLE registrations ADD CONSTRAINT registrations_period_semester_fkey
    FOREIGN KEY(period_id,semester_id) REFERENCES registration_periods(period_id,semester_id);
ALTER TABLE registrations ALTER COLUMN grade TYPE numeric(4,2);
ALTER TABLE registrations ADD CONSTRAINT registrations_grade_check CHECK(grade IS NULL OR grade BETWEEN 0 AND 10);
ALTER TABLE registrations ADD CONSTRAINT registrations_result_check CHECK(
    (grade IS NULL AND result_status IS NULL) OR
    (grade IS NOT NULL AND result_status IS NOT NULL AND result_status = CASE WHEN grade >= 5 THEN 'passed' ELSE 'not_passed' END));
ALTER TABLE semesters ALTER COLUMN status DROP DEFAULT;
ALTER TABLE semesters ALTER COLUMN status TYPE varchar(20) USING status::text;
ALTER TABLE semesters ALTER COLUMN status SET DEFAULT 'PLANNED';
ALTER TYPE registration_status RENAME TO registration_status_type;
DROP TABLE grades;
-- Obsolete enums are removed only when nothing still depends on them.
DROP TYPE user_role, account_status, person_status, period_status, semester_status, grade_result_status;
COMMIT;

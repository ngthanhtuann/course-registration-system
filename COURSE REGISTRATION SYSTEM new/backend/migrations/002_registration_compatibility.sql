BEGIN;

ALTER TABLE registration_periods DROP CONSTRAINT IF EXISTS registration_periods_semester_id_fkey;
ALTER TABLE registration_periods ALTER COLUMN period_id DROP IDENTITY IF EXISTS;
ALTER TABLE registration_periods ALTER COLUMN period_id DROP DEFAULT;
ALTER TABLE registration_periods ALTER COLUMN period_id TYPE varchar(20) USING period_id::text;

ALTER TABLE registrations ADD COLUMN IF NOT EXISTS grade numeric;
ALTER TABLE registrations ADD COLUMN IF NOT EXISTS result_status varchar(20);
UPDATE registrations r
SET grade = g.grade
FROM grades g
WHERE g.student_id = r.student_id
    AND g.course_id = r.course_id
    AND g.semester_id = r.semester_id
    AND r.grade IS NULL;
UPDATE registrations
SET result_status = CASE
    WHEN grade IS NULL THEN NULL
    WHEN grade >= 5 THEN 'passed'
    ELSE 'not_passed'
END
WHERE result_status IS NULL;

COMMIT;

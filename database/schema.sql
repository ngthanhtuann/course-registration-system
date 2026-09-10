-- Fresh installation only. Existing legacy databases use backend/migrations.

begin;

create type registration_status_type as enum ('REGISTERED', 'DROPPED');


-- 1. user

create table users (
    user_id varchar(20) primary key,
    username varchar(50) not null unique,
    password_hash varchar(255) not null,
    full_name varchar(100) not null,
    email varchar(100) not null unique,
    role varchar(20) not null check (role in ('admin', 'lecturer', 'student')),
    active_status boolean not null default true,
    failed_login_attempts smallint not null default 0 check (failed_login_attempts >= 0),
    lock_until timestamp with time zone,
    created_at timestamp with time zone not null default current_timestamp,
    updated_at timestamp with time zone not null default current_timestamp
);


-- 2. administrator

create table administrators (
    admin_id varchar(20) primary key,
    user_id varchar(20) not null unique,
    foreign key (user_id) references users(user_id)
);


-- 3. major

create table majors (
    major_id bigint generated always as identity primary key,
    major_code varchar(20) not null unique,
    major_name varchar(150) not null unique,
    created_at timestamp with time zone not null default current_timestamp
);


-- 4. lecturer

create table lecturers (
    lecturer_id varchar(30) primary key,
    created_at timestamp with time zone not null default current_timestamp,
    user_id varchar(20) not null unique,
    foreign key (user_id) references users(user_id)
);


-- 5. student

create table students (
    student_id varchar(30) primary key,
    created_at timestamp with time zone not null default current_timestamp,
    user_id varchar(20) not null unique,
    date_of_birth date,
    major_id bigint not null,
    foreign key (user_id) references users(user_id),
    foreign key (major_id) references majors(major_id) on delete restrict
);


-- 6. course

create table courses (
    created_at timestamp with time zone not null default current_timestamp,    course_id bigint generated always as identity primary key,
    course_code varchar(20) not null unique,
    course_name varchar(200) not null,
    credit integer not null check (credit > 0),
    max_capacity integer not null check (max_capacity > 0),
    available_seats integer not null check (available_seats >= 0),
    prerequisite_course_id bigint,
    foreign key (prerequisite_course_id) references courses(course_id),
    check (course_id is distinct from prerequisite_course_id),
    check (available_seats <= max_capacity)
);


-- 7. curriculum

create table curriculum (
    curriculum_id varchar(20) primary key,
    major_id bigint not null,
    course_id bigint not null,
    recommended_semester varchar(20),
    foreign key (major_id) references majors(major_id) on delete cascade,
    foreign key (course_id) references courses(course_id),
    unique (major_id, course_id)
);


-- 8. lecturer qualification

create table lecturer_qualifications (
    qualification_id varchar(20) primary key,
    lecturer_id varchar(30) not null,
    course_id bigint not null,
    foreign key (lecturer_id) references lecturers(lecturer_id) on delete cascade,
    foreign key (course_id) references courses(course_id),
    unique (lecturer_id, course_id)
);


-- 9. semester

create table semesters (
    semester_id varchar(20) primary key,
    semester_name varchar(100) not null unique,
    start_date date not null,
    end_date date not null,
    status varchar(20) not null default 'PLANNED',
    check (end_date > start_date)
);


-- 10. registration period

create table registration_periods (
    period_id varchar(20) primary key,
    semester_id varchar(20) not null,
    period_name varchar(100) not null,
    start_date timestamp with time zone not null,
    end_date timestamp with time zone not null,
    drop_start_date timestamp with time zone not null,
    drop_end_date timestamp with time zone not null,
    unique (semester_id, period_name),
    unique (period_id, semester_id),
    foreign key (semester_id) references semesters(semester_id),
    check (end_date > start_date),
    check (drop_end_date > drop_start_date)
);


-- 11. teaching assignment

create table teaching_assignments (
    assignment_id varchar(20) primary key,
    semester_id varchar(20) not null,
    lecturer_id varchar(30) not null,
    course_id bigint not null,
    foreign key (semester_id) references semesters(semester_id),
    foreign key (lecturer_id) references lecturers(lecturer_id) on delete restrict,
    foreign key (course_id) references courses(course_id),
    unique (semester_id, lecturer_id, course_id)
);


-- 12. registration

create table registrations (
    registration_id varchar(20) primary key,
    student_id varchar(30) not null,
    semester_id varchar(20) not null,
    period_id varchar(20) not null,
    course_id bigint not null,
    status registration_status_type not null default 'REGISTERED',
    registered_at timestamp with time zone not null default current_timestamp,
    dropped_at timestamp with time zone,
    grade numeric(4,2) check (grade is null or (grade >= 0 and grade <= 10)),
    result_status varchar(20),
    foreign key (student_id) references students(student_id) on delete restrict,
    foreign key (semester_id) references semesters(semester_id),
    foreign key (period_id, semester_id) references registration_periods(period_id, semester_id),
    check ((status = 'DROPPED') = (dropped_at is not null)),
    check ((grade is null and result_status is null) or
           (grade is not null and result_status is not null and result_status = case when grade >= 5 then 'passed' else 'not_passed' end)),
    foreign key (course_id) references courses(course_id),
    unique (student_id, semester_id, course_id)
);


-- 13. registration seat function

create function maintain_registration_seats()
returns trigger
language plpgsql
as $$
begin
    if tg_op = 'INSERT' and new.status = 'REGISTERED' then
        update courses
        set available_seats = available_seats - 1
        where course_id = new.course_id
        and available_seats > 0;

        if not found then
            raise exception 'No seats remaining for course %', new.course_id;
        end if;

    elsif tg_op = 'UPDATE'
        and old.status = 'REGISTERED'
        and new.status = 'DROPPED' then

        new.dropped_at := coalesce(new.dropped_at, current_timestamp);

        update courses
        set available_seats = available_seats + 1
        where course_id = old.course_id;

    elsif tg_op = 'UPDATE'
        and old.status = 'DROPPED'
        and new.status = 'REGISTERED' then

        new.dropped_at := null;

        update courses
        set available_seats = available_seats - 1
        where course_id = new.course_id
        and available_seats > 0;

        if not found then
            raise exception 'No seats remaining for course %', new.course_id;
        end if;
    end if;

    return new;
end;
$$;


-- 14. registration seat trigger

create trigger trg_registration_seats
before insert or update on registrations
for each row
execute function maintain_registration_seats();


CREATE FUNCTION prevent_profile_role_change() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
  IF NEW.role <> OLD.role AND (
    EXISTS (SELECT 1 FROM students WHERE user_id = OLD.user_id) OR
    EXISTS (SELECT 1 FROM lecturers WHERE user_id = OLD.user_id)
  ) THEN
    RAISE EXCEPTION 'Cannot change the role of a user with a profile';
  END IF;
  RETURN NEW;
END $$;

CREATE FUNCTION validate_assignment_qualification() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM lecturer_qualifications WHERE lecturer_id = NEW.lecturer_id AND course_id = NEW.course_id) THEN
    RAISE EXCEPTION 'lecturer % is not qualified for course %', NEW.lecturer_id, NEW.course_id;
  END IF;
  RETURN NEW;
END $$;

CREATE FUNCTION validate_profile_role() RETURNS trigger
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

CREATE TRIGGER trg_assignment_qualification BEFORE INSERT OR UPDATE ON teaching_assignments FOR EACH ROW EXECUTE FUNCTION validate_assignment_qualification();

CREATE TRIGGER trg_lecturers_profile_role BEFORE INSERT OR UPDATE ON lecturers FOR EACH ROW EXECUTE FUNCTION validate_profile_role();

CREATE TRIGGER trg_students_profile_role BEFORE INSERT OR UPDATE ON students FOR EACH ROW EXECUTE FUNCTION validate_profile_role();

CREATE TRIGGER trg_users_prevent_profile_role_change BEFORE UPDATE ON users FOR EACH ROW EXECUTE FUNCTION prevent_profile_role_change();

commit;
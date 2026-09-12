-- Fresh installation only: run once on an empty application schema.
-- Capacity is shared by all registration periods in the same semester.
-- Do not apply legacy migrations 001-003 to this schema.

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
    failed_login_attempts integer not null default 0 check (failed_login_attempts >= 0),
    locked_until timestamptz,
    token_version bigint not null default 0 check (token_version >= 0)
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
    major_name varchar(50) not null unique,
    unique (major_id, major_code)
);


-- 4. lecturer

create table lecturers (
    lecturer_id varchar(20) primary key,
    user_id varchar(20) not null unique,
    foreign key (user_id) references users(user_id)
);


-- 5. student

create table students (
    student_id varchar(20) primary key,
    user_id varchar(20) not null unique,
    date_of_birth date,
    major_id bigint not null,
    major_code varchar(20) not null,
    foreign key (major_id, major_code) references majors(major_id, major_code),
    foreign key (user_id) references users(user_id),
    foreign key (major_id) references majors(major_id)
);


-- 6. course

create table courses (
    course_id bigint generated always as identity primary key,
    course_code varchar(20) not null unique,
    course_name varchar(50) not null,
    credit integer not null check (credit > 0),
    max_capacity integer not null check (max_capacity > 0),
    prerequisite_course_code varchar(20) references courses(course_code),
    check (prerequisite_course_code <> course_code),
    unique (course_id, course_code)
);


-- 7. curriculum

create table curriculum (
    curriculum_id varchar(20) primary key,
    major_id bigint not null,
    major_code varchar(20) not null,
    foreign key (major_id, major_code) references majors(major_id, major_code),
    course_id bigint not null,
    course_code varchar(20) not null,
    foreign key (course_id, course_code) references courses(course_id, course_code),
    recommended_semester varchar(20),
    foreign key (major_id) references majors(major_id),
    foreign key (course_id) references courses(course_id),
    unique (major_id, course_id)
);


-- 8. lecturer qualification

create table lecturer_qualifications (
    qualification_id varchar(20) primary key,
    lecturer_id varchar(20) not null,
    course_id bigint not null,
    course_code varchar(20) not null,
    foreign key (course_id, course_code) references courses(course_id, course_code),
    foreign key (lecturer_id) references lecturers(lecturer_id),
    foreign key (course_id) references courses(course_id),
    unique (lecturer_id, course_id)
);


-- 9. semester

create table semesters (
    semester_id varchar(20) primary key,
    semester_name varchar(20) not null,
    start_date date not null,
    end_date date not null,
    status varchar(20),
    check (end_date >= start_date)
);


-- 10. registration period

create table registration_periods (
    period_id varchar(20) primary key,
    semester_id varchar(20) not null,
    period_name varchar(100) not null,
    start_date date not null,
    end_date date not null,
    drop_start_date date not null,
    drop_end_date date not null,
    foreign key (semester_id) references semesters(semester_id),
    check (end_date >= start_date),
    check (drop_end_date >= drop_start_date),
    unique (period_id, semester_id)
);


-- 11. teaching assignment

create table teaching_assignments (
    assignment_id varchar(20) primary key,
    semester_id varchar(20) not null,
    lecturer_id varchar(20) not null,
    course_id bigint not null,
    course_code varchar(20) not null,
    foreign key (course_id, course_code) references courses(course_id, course_code),
    foreign key (semester_id) references semesters(semester_id),
    foreign key (lecturer_id) references lecturers(lecturer_id),
    foreign key (course_id) references courses(course_id),
    unique (semester_id, lecturer_id, course_id)
);


-- 12. registration

create table registrations (
    registration_id varchar(20) primary key,
    student_id varchar(20) not null,
    semester_id varchar(20) not null,
    period_id varchar(20) not null,
    course_id bigint not null,
    course_code varchar(20) not null,
    foreign key (course_id, course_code) references courses(course_id, course_code),
    status registration_status_type not null default 'REGISTERED',
    registration_status text generated always as
        (case when status = 'REGISTERED' then 'registered' else 'dropped' end) stored,
    dropped_at timestamp with time zone,
    grade numeric(4,2) check (grade is null or (grade >= 0 and grade <= 10)),
    result_status varchar(20),
    foreign key (student_id) references students(student_id),
    foreign key (semester_id) references semesters(semester_id),
    foreign key (period_id, semester_id) references registration_periods(period_id, semester_id),
    foreign key (course_id) references courses(course_id),
    unique (student_id, semester_id, course_id)
);


-- Serialize capacity checks on a course row across all backend instances.
create function maintain_registration_seats()
returns trigger language plpgsql as $$
declare
    seat_limit integer;
    occupied bigint;
begin
    if tg_op = 'UPDATE' then
        if (new.student_id, new.course_id, new.semester_id)
            is distinct from (old.student_id, old.course_id, old.semester_id) then
            raise exception 'Registration student, course and semester cannot be changed';
        end if;
    end if;
    select max_capacity into seat_limit from courses
        where course_id = new.course_id for update;
    if new.status = 'REGISTERED' then
        select count(*) into occupied from registrations
            where course_id = new.course_id and semester_id = new.semester_id
              and status = 'REGISTERED' and registration_id <> new.registration_id;
        if occupied >= seat_limit then
            raise exception 'Course capacity has been reached';
        end if;
        new.dropped_at := null;
    elsif tg_op = 'INSERT' or old.status <> new.status then
        new.dropped_at := current_timestamp;
    end if;
    return new;
end;
$$;
create trigger trg_registration_seats before insert or update on registrations
for each row execute function maintain_registration_seats();

create function validate_course_capacity()
returns trigger language plpgsql as $$
begin
    if exists (select 1 from registrations where course_id = new.course_id
               and status = 'REGISTERED' group by semester_id
               having count(*) > new.max_capacity) then
        raise exception 'Capacity cannot be below the registered student count';
    end if;
    return new;
end;
$$;
create trigger trg_course_capacity before update of max_capacity on courses
for each row execute function validate_course_capacity();

create function validate_profile_role()
returns trigger language plpgsql as $$
begin
    if not exists (select 1 from users where user_id = new.user_id and role =
        case tg_table_name when 'students' then 'student'
             when 'lecturers' then 'lecturer' else 'admin' end) then
        raise exception 'Profile must match the account role';
    end if;
    return new;
end;
$$;
create trigger trg_student_role before insert or update on students
for each row execute function validate_profile_role();
create trigger trg_lecturer_role before insert or update on lecturers
for each row execute function validate_profile_role();
create trigger trg_admin_role before insert or update on administrators
for each row execute function validate_profile_role();

create index registrations_course_semester_active on registrations(course_id, semester_id)
where status = 'REGISTERED';
create index registrations_period on registrations(period_id);
create index students_major on students(major_id);
create index curriculum_course on curriculum(course_id);
create index teaching_assignments_lecturer on teaching_assignments(lecturer_id, semester_id);

create table schema_version (
    version integer primary key,
    installed_at timestamptz not null default current_timestamp
);
insert into schema_version(version) values (2);
commit;

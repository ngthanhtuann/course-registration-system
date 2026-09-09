-- Fresh installation only. Existing legacy databases use backend/migrations.
BEGIN;
CREATE TYPE registration_status AS ENUM ('REGISTERED', 'DROPPED');

-- 1. user

create table users (
    user_id varchar(20) primary key,
    username varchar(50) not null unique,
    password varchar(255) not null,
    password_hash varchar(255) not null,
    fullname varchar(100) not null,
    email varchar(100) not null unique,
    role varchar(20) not null check (role in ('admin', 'lecturer', 'student')),
    active_status boolean not null default true
);


-- 2. administrator

create table administrators (
    admin_id varchar(20) primary key,
    user_id varchar(20) not null unique,
    foreign key (user_id) references users(user_id)
);


-- 3. major

create table majors (
    major_id bigint generated always as identity unique,
    major_code varchar(20) primary key,
    major_name varchar(50) not null unique
);


-- 4. lecturer

create table lecturers (
    full_name varchar(100) not null,
    fullname varchar(100) not null,
    email varchar(100) not null,
    lecturer_id varchar(20) primary key,
    user_id varchar(20) not null unique,
    foreign key (user_id) references users(user_id)
);


-- 5. student

create table students (
    full_name varchar(100) not null,
    email varchar(100) not null,
    date_of_birth date,
    major_id bigint not null references majors(major_id),
    student_id varchar(20) primary key,
    user_id varchar(20) not null unique,
    dob date,
    major_code varchar(20) not null,
    foreign key (user_id) references users(user_id),
    foreign key (major_code) references majors(major_code)
);


-- 6. course

create table courses (
    course_id bigint generated always as identity unique,
    capacity integer not null check (capacity > 0),
    available_seats integer not null check (available_seats >= 0),
    course_code varchar(20) primary key,
    course_name varchar(50) not null,
    credit integer not null check (credit > 0),
    prerequisite_course_code varchar(20),
    max_capacity integer not null check (max_capacity > 0),
    foreign key (prerequisite_course_code) references courses(course_code)
);


-- 7. curriculum

create table curriculum (
    major_id bigint not null references majors(major_id),
    course_id bigint not null references courses(course_id),
    curriculum_id varchar(20) primary key,
    major_code varchar(20) not null,
    course_code varchar(20) not null,
    recommended_semester varchar(20),
    foreign key (major_code) references majors(major_code),
    foreign key (course_code) references courses(course_code),
    unique (major_code, course_code)
);


-- 8. lecturer qualification

create table lecturer_qualifications (
    course_id bigint not null references courses(course_id),
    qualification_id varchar(20) primary key,
    lecturer_id varchar(20) not null,
    course_code varchar(20) not null,
    foreign key (lecturer_id) references lecturers(lecturer_id),
    foreign key (course_code) references courses(course_code),
    unique (lecturer_id, course_code)
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
    name varchar(100) not null,
    drop_start_date date not null,
    drop_end_date date not null,
    period_id varchar(20) primary key,
    semester_id varchar(20) not null,
    period_name varchar(100) not null,
    start_date date not null,
    end_date date not null,
    foreign key (semester_id) references semesters(semester_id),
    check (end_date >= start_date)
);


-- 11. teaching assignment

create table teaching_assignments (
    course_id bigint not null references courses(course_id),
    assignment_id varchar(20) primary key,
    semester_id varchar(20) not null,
    lecturer_id varchar(20) not null,
    course_code varchar(20) not null,
    foreign key (semester_id) references semesters(semester_id),
    foreign key (lecturer_id) references lecturers(lecturer_id),
    foreign key (course_code) references courses(course_code),
    unique (semester_id, lecturer_id, course_code)
);


-- 12. registration

create table registrations (
    course_id bigint not null references courses(course_id),
    semester_id varchar(20) not null references semesters(semester_id),
    status registration_status not null,
    dropped_at timestamp with time zone,
    registration_id varchar(20) primary key,
    student_id varchar(20) not null,
    period_id varchar(20) not null,
    course_code varchar(20) not null,
    registration_status varchar(20),
    grade float check (grade is null or (grade >= 0 and grade <= 10)),
    result_status varchar(20),
    foreign key (student_id) references students(student_id),
    foreign key (period_id) references registration_periods(period_id),
    foreign key (course_code) references courses(course_code),
    unique (student_id, period_id, course_code)
);
CREATE FUNCTION maintain_registration_seats() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
  IF TG_OP = 'INSERT' AND NEW.status = 'REGISTERED' THEN
    UPDATE courses SET available_seats = available_seats - 1 WHERE course_id = NEW.course_id AND available_seats > 0;
    IF NOT FOUND THEN RAISE EXCEPTION 'No seats remaining for course %', NEW.course_id; END IF;
  ELSIF TG_OP = 'UPDATE' AND OLD.status = 'REGISTERED' AND NEW.status = 'DROPPED' THEN
    NEW.dropped_at := COALESCE(NEW.dropped_at, CURRENT_TIMESTAMP);
    UPDATE courses SET available_seats = available_seats + 1 WHERE course_id = OLD.course_id;
  ELSIF TG_OP = 'UPDATE' AND OLD.status = 'DROPPED' AND NEW.status = 'REGISTERED' THEN
    NEW.dropped_at := NULL;
    UPDATE courses SET available_seats = available_seats - 1 WHERE course_id = NEW.course_id AND available_seats > 0;
    IF NOT FOUND THEN RAISE EXCEPTION 'No seats remaining for course %', NEW.course_id; END IF;
  END IF;
  RETURN NEW;
END $$;
CREATE TRIGGER trg_registration_seats BEFORE INSERT OR UPDATE ON registrations
FOR EACH ROW EXECUTE FUNCTION maintain_registration_seats();

COMMIT;

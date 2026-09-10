--
-- PostgreSQL database dump
--

\restrict 8z2TDcR4d0SLrqwida9nVIBqLpqII9UBJYKhvce3EAwKJfrfHSNzy2XBMeHsuFb

-- Dumped from database version 16.15
-- Dumped by pg_dump version 16.15

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: registration_status_type; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.registration_status_type AS ENUM (
    'REGISTERED',
    'DROPPED'
);


--
-- Name: maintain_registration_seats(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.maintain_registration_seats() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
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


--
-- Name: prevent_profile_role_change(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.prevent_profile_role_change() RETURNS trigger
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


--
-- Name: validate_assignment_qualification(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.validate_assignment_qualification() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM lecturer_qualifications WHERE lecturer_id = NEW.lecturer_id AND course_id = NEW.course_id) THEN
    RAISE EXCEPTION 'lecturer % is not qualified for course %', NEW.lecturer_id, NEW.course_id;
  END IF;
  RETURN NEW;
END $$;


--
-- Name: validate_profile_role(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.validate_profile_role() RETURNS trigger
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


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: administrators; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.administrators (
    admin_id character varying(20) NOT NULL,
    user_id character varying(20) NOT NULL
);


--
-- Name: courses; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.courses (
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    course_id bigint NOT NULL,
    course_code character varying(20) NOT NULL,
    course_name character varying(200) NOT NULL,
    credit integer NOT NULL,
    max_capacity integer NOT NULL,
    available_seats integer NOT NULL,
    prerequisite_course_id bigint,
    CONSTRAINT courses_available_seats_check CHECK ((available_seats >= 0)),
    CONSTRAINT courses_check CHECK ((course_id IS DISTINCT FROM prerequisite_course_id)),
    CONSTRAINT courses_check1 CHECK ((available_seats <= max_capacity)),
    CONSTRAINT courses_credit_check CHECK ((credit > 0)),
    CONSTRAINT courses_max_capacity_check CHECK ((max_capacity > 0))
);


--
-- Name: courses_course_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.courses ALTER COLUMN course_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.courses_course_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: curriculum; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.curriculum (
    curriculum_id character varying(20) NOT NULL,
    major_id bigint NOT NULL,
    course_id bigint NOT NULL,
    recommended_semester character varying(20)
);


--
-- Name: lecturer_qualifications; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.lecturer_qualifications (
    qualification_id character varying(20) NOT NULL,
    lecturer_id character varying(30) NOT NULL,
    course_id bigint NOT NULL
);


--
-- Name: lecturers; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.lecturers (
    lecturer_id character varying(30) NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    user_id character varying(20) NOT NULL
);


--
-- Name: majors; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.majors (
    major_id bigint NOT NULL,
    major_code character varying(20) NOT NULL,
    major_name character varying(150) NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


--
-- Name: majors_major_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.majors ALTER COLUMN major_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.majors_major_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: registration_periods; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.registration_periods (
    period_id character varying(20) NOT NULL,
    semester_id character varying(20) NOT NULL,
    period_name character varying(100) NOT NULL,
    start_date timestamp with time zone NOT NULL,
    end_date timestamp with time zone NOT NULL,
    drop_start_date timestamp with time zone NOT NULL,
    drop_end_date timestamp with time zone NOT NULL,
    CONSTRAINT registration_periods_check CHECK ((end_date > start_date)),
    CONSTRAINT registration_periods_check1 CHECK ((drop_end_date > drop_start_date))
);


--
-- Name: registrations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.registrations (
    registration_id character varying(20) NOT NULL,
    student_id character varying(30) NOT NULL,
    semester_id character varying(20) NOT NULL,
    period_id character varying(20) NOT NULL,
    course_id bigint NOT NULL,
    status public.registration_status_type DEFAULT 'REGISTERED'::public.registration_status_type NOT NULL,
    registered_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    dropped_at timestamp with time zone,
    grade numeric(4,2),
    result_status character varying(20),
    CONSTRAINT registrations_check CHECK (((status = 'DROPPED'::public.registration_status_type) = (dropped_at IS NOT NULL))),
    CONSTRAINT registrations_check1 CHECK ((((grade IS NULL) AND (result_status IS NULL)) OR ((grade IS NOT NULL) AND (result_status IS NOT NULL) AND ((result_status)::text =
CASE
    WHEN (grade >= (5)::numeric) THEN 'passed'::text
    ELSE 'not_passed'::text
END)))),
    CONSTRAINT registrations_grade_check CHECK (((grade IS NULL) OR ((grade >= (0)::numeric) AND (grade <= (10)::numeric))))
);


--
-- Name: semesters; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.semesters (
    semester_id character varying(20) NOT NULL,
    semester_name character varying(100) NOT NULL,
    start_date date NOT NULL,
    end_date date NOT NULL,
    status character varying(20) DEFAULT 'PLANNED'::character varying NOT NULL,
    CONSTRAINT semesters_check CHECK ((end_date > start_date))
);


--
-- Name: students; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.students (
    student_id character varying(30) NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    user_id character varying(20) NOT NULL,
    date_of_birth date,
    major_id bigint NOT NULL
);


--
-- Name: teaching_assignments; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.teaching_assignments (
    assignment_id character varying(20) NOT NULL,
    semester_id character varying(20) NOT NULL,
    lecturer_id character varying(30) NOT NULL,
    course_id bigint NOT NULL
);


--
-- Name: users; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.users (
    user_id character varying(20) NOT NULL,
    username character varying(50) NOT NULL,
    password_hash character varying(255) NOT NULL,
    full_name character varying(100) NOT NULL,
    email character varying(100) NOT NULL,
    role character varying(20) NOT NULL,
    active_status boolean DEFAULT true NOT NULL,
    failed_login_attempts smallint DEFAULT 0 NOT NULL,
    lock_until timestamp with time zone,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT users_failed_login_attempts_check CHECK ((failed_login_attempts >= 0)),
    CONSTRAINT users_role_check CHECK (((role)::text = ANY ((ARRAY['admin'::character varying, 'lecturer'::character varying, 'student'::character varying])::text[])))
);


--
-- Data for Name: administrators; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.administrators (admin_id, user_id) FROM stdin;
admin01	admin01
\.


--
-- Data for Name: courses; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.courses (created_at, course_id, course_code, course_name, credit, max_capacity, available_seats, prerequisite_course_id) FROM stdin;
\.


--
-- Data for Name: curriculum; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.curriculum (curriculum_id, major_id, course_id, recommended_semester) FROM stdin;
\.


--
-- Data for Name: lecturer_qualifications; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.lecturer_qualifications (qualification_id, lecturer_id, course_id) FROM stdin;
\.


--
-- Data for Name: lecturers; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.lecturers (lecturer_id, created_at, user_id) FROM stdin;
\.


--
-- Data for Name: majors; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.majors (major_id, major_code, major_name, created_at) FROM stdin;
\.


--
-- Data for Name: registration_periods; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.registration_periods (period_id, semester_id, period_name, start_date, end_date, drop_start_date, drop_end_date) FROM stdin;
\.


--
-- Data for Name: registrations; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.registrations (registration_id, student_id, semester_id, period_id, course_id, status, registered_at, dropped_at, grade, result_status) FROM stdin;
\.


--
-- Data for Name: semesters; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.semesters (semester_id, semester_name, start_date, end_date, status) FROM stdin;
\.


--
-- Data for Name: students; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.students (student_id, created_at, user_id, date_of_birth, major_id) FROM stdin;
\.


--
-- Data for Name: teaching_assignments; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.teaching_assignments (assignment_id, semester_id, lecturer_id, course_id) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.users (user_id, username, password_hash, full_name, email, role, active_status, failed_login_attempts, lock_until, created_at, updated_at) FROM stdin;
admin01	admin01	$2b$12$Kx5Ae52VasAkVPHKbC4IcO4kiNfhJWVI4dhdkF01sQLpsGtLIagP.	Ad Van Min	admin1@gmail.com	admin	t	0	\N	2026-09-10 05:01:45.169459+00	2026-09-10 05:01:45.169459+00
\.


--
-- Name: courses_course_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.courses_course_id_seq', 1, false);


--
-- Name: majors_major_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.majors_major_id_seq', 1, false);


--
-- Name: administrators administrators_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.administrators
    ADD CONSTRAINT administrators_pkey PRIMARY KEY (admin_id);


--
-- Name: administrators administrators_user_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.administrators
    ADD CONSTRAINT administrators_user_id_key UNIQUE (user_id);


--
-- Name: courses courses_course_code_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.courses
    ADD CONSTRAINT courses_course_code_key UNIQUE (course_code);


--
-- Name: courses courses_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.courses
    ADD CONSTRAINT courses_pkey PRIMARY KEY (course_id);


--
-- Name: curriculum curriculum_major_id_course_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.curriculum
    ADD CONSTRAINT curriculum_major_id_course_id_key UNIQUE (major_id, course_id);


--
-- Name: curriculum curriculum_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.curriculum
    ADD CONSTRAINT curriculum_pkey PRIMARY KEY (curriculum_id);


--
-- Name: lecturer_qualifications lecturer_qualifications_lecturer_id_course_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.lecturer_qualifications
    ADD CONSTRAINT lecturer_qualifications_lecturer_id_course_id_key UNIQUE (lecturer_id, course_id);


--
-- Name: lecturer_qualifications lecturer_qualifications_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.lecturer_qualifications
    ADD CONSTRAINT lecturer_qualifications_pkey PRIMARY KEY (qualification_id);


--
-- Name: lecturers lecturers_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.lecturers
    ADD CONSTRAINT lecturers_pkey PRIMARY KEY (lecturer_id);


--
-- Name: lecturers lecturers_user_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.lecturers
    ADD CONSTRAINT lecturers_user_id_key UNIQUE (user_id);


--
-- Name: majors majors_major_code_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.majors
    ADD CONSTRAINT majors_major_code_key UNIQUE (major_code);


--
-- Name: majors majors_major_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.majors
    ADD CONSTRAINT majors_major_name_key UNIQUE (major_name);


--
-- Name: majors majors_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.majors
    ADD CONSTRAINT majors_pkey PRIMARY KEY (major_id);


--
-- Name: registration_periods registration_periods_period_id_semester_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.registration_periods
    ADD CONSTRAINT registration_periods_period_id_semester_id_key UNIQUE (period_id, semester_id);


--
-- Name: registration_periods registration_periods_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.registration_periods
    ADD CONSTRAINT registration_periods_pkey PRIMARY KEY (period_id);


--
-- Name: registration_periods registration_periods_semester_id_period_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.registration_periods
    ADD CONSTRAINT registration_periods_semester_id_period_name_key UNIQUE (semester_id, period_name);


--
-- Name: registrations registrations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.registrations
    ADD CONSTRAINT registrations_pkey PRIMARY KEY (registration_id);


--
-- Name: registrations registrations_student_id_semester_id_course_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.registrations
    ADD CONSTRAINT registrations_student_id_semester_id_course_id_key UNIQUE (student_id, semester_id, course_id);


--
-- Name: semesters semesters_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.semesters
    ADD CONSTRAINT semesters_pkey PRIMARY KEY (semester_id);


--
-- Name: semesters semesters_semester_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.semesters
    ADD CONSTRAINT semesters_semester_name_key UNIQUE (semester_name);


--
-- Name: students students_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.students
    ADD CONSTRAINT students_pkey PRIMARY KEY (student_id);


--
-- Name: students students_user_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.students
    ADD CONSTRAINT students_user_id_key UNIQUE (user_id);


--
-- Name: teaching_assignments teaching_assignments_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.teaching_assignments
    ADD CONSTRAINT teaching_assignments_pkey PRIMARY KEY (assignment_id);


--
-- Name: teaching_assignments teaching_assignments_semester_id_lecturer_id_course_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.teaching_assignments
    ADD CONSTRAINT teaching_assignments_semester_id_lecturer_id_course_id_key UNIQUE (semester_id, lecturer_id, course_id);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- Name: teaching_assignments trg_assignment_qualification; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_assignment_qualification BEFORE INSERT OR UPDATE ON public.teaching_assignments FOR EACH ROW EXECUTE FUNCTION public.validate_assignment_qualification();


--
-- Name: lecturers trg_lecturers_profile_role; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_lecturers_profile_role BEFORE INSERT OR UPDATE ON public.lecturers FOR EACH ROW EXECUTE FUNCTION public.validate_profile_role();


--
-- Name: registrations trg_registration_seats; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_registration_seats BEFORE INSERT OR UPDATE ON public.registrations FOR EACH ROW EXECUTE FUNCTION public.maintain_registration_seats();


--
-- Name: students trg_students_profile_role; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_students_profile_role BEFORE INSERT OR UPDATE ON public.students FOR EACH ROW EXECUTE FUNCTION public.validate_profile_role();


--
-- Name: users trg_users_prevent_profile_role_change; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_users_prevent_profile_role_change BEFORE UPDATE ON public.users FOR EACH ROW EXECUTE FUNCTION public.prevent_profile_role_change();


--
-- Name: administrators administrators_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.administrators
    ADD CONSTRAINT administrators_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- Name: courses courses_prerequisite_course_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.courses
    ADD CONSTRAINT courses_prerequisite_course_id_fkey FOREIGN KEY (prerequisite_course_id) REFERENCES public.courses(course_id);


--
-- Name: curriculum curriculum_course_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.curriculum
    ADD CONSTRAINT curriculum_course_id_fkey FOREIGN KEY (course_id) REFERENCES public.courses(course_id);


--
-- Name: curriculum curriculum_major_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.curriculum
    ADD CONSTRAINT curriculum_major_id_fkey FOREIGN KEY (major_id) REFERENCES public.majors(major_id) ON DELETE CASCADE;


--
-- Name: lecturer_qualifications lecturer_qualifications_course_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.lecturer_qualifications
    ADD CONSTRAINT lecturer_qualifications_course_id_fkey FOREIGN KEY (course_id) REFERENCES public.courses(course_id);


--
-- Name: lecturer_qualifications lecturer_qualifications_lecturer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.lecturer_qualifications
    ADD CONSTRAINT lecturer_qualifications_lecturer_id_fkey FOREIGN KEY (lecturer_id) REFERENCES public.lecturers(lecturer_id) ON DELETE CASCADE;


--
-- Name: lecturers lecturers_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.lecturers
    ADD CONSTRAINT lecturers_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- Name: registration_periods registration_periods_semester_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.registration_periods
    ADD CONSTRAINT registration_periods_semester_id_fkey FOREIGN KEY (semester_id) REFERENCES public.semesters(semester_id);


--
-- Name: registrations registrations_course_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.registrations
    ADD CONSTRAINT registrations_course_id_fkey FOREIGN KEY (course_id) REFERENCES public.courses(course_id);


--
-- Name: registrations registrations_period_id_semester_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.registrations
    ADD CONSTRAINT registrations_period_id_semester_id_fkey FOREIGN KEY (period_id, semester_id) REFERENCES public.registration_periods(period_id, semester_id);


--
-- Name: registrations registrations_semester_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.registrations
    ADD CONSTRAINT registrations_semester_id_fkey FOREIGN KEY (semester_id) REFERENCES public.semesters(semester_id);


--
-- Name: registrations registrations_student_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.registrations
    ADD CONSTRAINT registrations_student_id_fkey FOREIGN KEY (student_id) REFERENCES public.students(student_id) ON DELETE RESTRICT;


--
-- Name: students students_major_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.students
    ADD CONSTRAINT students_major_id_fkey FOREIGN KEY (major_id) REFERENCES public.majors(major_id) ON DELETE RESTRICT;


--
-- Name: students students_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.students
    ADD CONSTRAINT students_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- Name: teaching_assignments teaching_assignments_course_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.teaching_assignments
    ADD CONSTRAINT teaching_assignments_course_id_fkey FOREIGN KEY (course_id) REFERENCES public.courses(course_id);


--
-- Name: teaching_assignments teaching_assignments_lecturer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.teaching_assignments
    ADD CONSTRAINT teaching_assignments_lecturer_id_fkey FOREIGN KEY (lecturer_id) REFERENCES public.lecturers(lecturer_id) ON DELETE RESTRICT;


--
-- Name: teaching_assignments teaching_assignments_semester_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.teaching_assignments
    ADD CONSTRAINT teaching_assignments_semester_id_fkey FOREIGN KEY (semester_id) REFERENCES public.semesters(semester_id);


--
-- PostgreSQL database dump complete
--

\unrestrict 8z2TDcR4d0SLrqwida9nVIBqLpqII9UBJYKhvce3EAwKJfrfHSNzy2XBMeHsuFb


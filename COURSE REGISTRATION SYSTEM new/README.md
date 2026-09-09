# Course Registration System

A student-level full-stack Course Registration System using **React + TypeScript + Vite**, **Flask**, and **PostgreSQL**.

The project keeps the original page structure and role separation:

- **Administrator**: users, majors, courses, curriculum, semesters, registration periods, registration demand, lecturer qualifications and teaching assignments.
- **Lecturer**: teaching courses, registered students and grades.
- **Student**: view curriculum courses, register/drop courses, registration status and grades.

## 1. Project structure

```text
COURSE REGISTRATION SYSTEM new/
├── backend/
│   ├── admin.py
│   ├── auth.py
│   ├── config.py
│   ├── create_admin.py
│   ├── database.py
│   ├── lecturer.py
│   ├── main.py
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── api.ts
│   │   ├── components/
│   │   ├── context/
│   │   ├── pages/
│   │   ├── data.ts
│   │   └── types.ts
│   ├── package.json
│   └── vite.config.ts
├── dbschema.sql
└── README.md
```

## 2. Database setup

1. Start PostgreSQL.
2. Create a database named `course_registration_system`.
3. Open `dbschema.sql` in DBeaver and execute the complete file.
4. The database should contain the 12 tables defined in the schema.

The schema is intentionally empty of demonstration users, courses and registrations. Data can be created through the application after login.

### Existing legacy database

If the database already contains the older schema, do not rerun `dbschema.sql` because it can conflict with existing data. First create a PostgreSQL backup, then run these migrations from the `backend` folder:

```bash
python -c "from pathlib import Path; from database import get_db; db=get_db(); db.conn.cursor().execute(Path('migrations/001_legacy_schema_compatibility.sql').read_text()); db.conn.commit(); db.close()"
python -c "from pathlib import Path; from database import get_db; db=get_db(); db.conn.cursor().execute(Path('migrations/002_registration_compatibility.sql').read_text()); db.conn.commit(); db.close()"
```

The migrations preserve existing rows and add compatibility columns for the current backend. A backup is still required before applying them.

## 3. Backend setup

From the project root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r backend/requirements.txt
```

Create `backend/.env` by copying `backend/.env.example`, then set the PostgreSQL password:

```text
db_host=localhost
db_port=5432
db_name=course_registration_system
db_user=postgres
db_password=YOUR_POSTGRES_PASSWORD
JWT_SECRET=change-this-secret
```

### Create the first administrator

From the `backend` folder:

```bash
cd backend
../.venv/bin/python create_admin.py
```

Enter an administrator ID, full name, email and a password of at least 8 characters.

The script creates:

- one row in `users`
- one row in `administrators`

The username is automatically the lower-case version of the Admin ID.

### Start Flask

Keep the virtual environment active and run:

```bash
cd backend
../.venv/bin/python main.py
```

The backend is available at:

```text
http://127.0.0.1:5000
```

Health check:

```text
http://127.0.0.1:5000/api/health
```

Expected response:

```json
{"status":"ok","database":"ok"}
```

## 4. Frontend setup

Open a **second Terminal** from the project root:

```bash
cd "./COURSE REGISTRATION SYSTEM new/frontend"
npm install
npm run dev
```

Vite normally starts the frontend at:

```text
http://localhost:8443
```

The frontend calls the Flask backend at:

```text
http://127.0.0.1:5000
```

If another backend address is required, create `frontend/.env`:

```text
VITE_API_URL=http://127.0.0.1:5000
```

## 5. Correct startup order

Use two Terminal windows.

### Terminal 1 — backend

```bash
cd "COURSE REGISTRATION SYSTEM new"
source .venv/bin/activate
cd backend
../.venv/bin/python main.py
```

### Terminal 2 — frontend

```bash
cd "COURSE REGISTRATION SYSTEM new/frontend"
npm install
npm run dev
```

Then open the Vite URL shown in Terminal 2.

## 6. Authentication

The frontend no longer uses the old demo login data from `data.ts`.

Login flow:

```text
React Login page
      ↓
POST /api/login
      ↓
Flask verifies username + bcrypt password
      ↓
JWT token returned
      ↓
Frontend stores token
      ↓
Role-specific profile is loaded
      ↓
User is redirected to the correct dashboard
```

The token is sent automatically as:

```text
Authorization: Bearer <token>
```

The browser keeps the session in local storage so refreshing the page does not immediately log the user out.

## 7. Administrator functions

### Manage User

Admin can:

- create Student
- create Lecturer
- view users
- edit user information
- deactivate Student/Lecturer accounts
- assign Lecturer teaching qualifications
- remove Lecturer teaching qualifications

When creating a Lecturer, the **Teaching Qualifications** field allows multiple courses to be selected.

A qualification is stored in:

```text
lecturer_qualifications
```

Each qualification connects one lecturer to one course.

### Manage Course

Admin can create, view, search, edit and delete courses, including:

- course code
- course name
- credit
- maximum capacity
- prerequisite

### Curriculum

Admin selects a major, then adds courses and specifies the recommended semester.

### Semester and Registration Period

Admin can create, edit and delete semesters and registration periods. Registration periods must be inside the corresponding semester dates.

### Registration Demand

The page reads actual registrations from PostgreSQL and displays demand by course. A course can also be opened to view the registered students contributing to that demand.

### Assign Lecturer

The assignment page first selects a semester and course. The backend returns only lecturers who have a qualification for that course.

Therefore:

```text
Lecturer qualification
        ↓
Qualified lecturer list
        ↓
Teaching assignment
```

The backend also checks the qualification again when an assignment is submitted. The frontend cannot bypass this rule.

## 8. Lecturer functions

Lecturers can:

- view their profile and qualifications
- view their teaching courses by semester
- view registered students in their assigned courses
- enter/update grades from 0 to 10

Only a lecturer assigned to a course for that semester can update its student grades.

## 9. Student functions

Students can:

- view courses in their major curriculum
- search courses
- see prerequisites and seat availability
- register during an open registration period
- see registration status
- drop a registered course during the configured registration period
- view grades by semester

Registration is validated by the backend for:

- registration period
- student curriculum
- duplicate registration
- already completed course
- prerequisite completion
- course capacity

## 10. Important API endpoints

### Authentication

```text
POST /api/login
GET  /api/me
PUT  /api/account/profile
PUT  /api/account/password
```

### Administrator

```text
GET/POST       /api/admin/users
PUT/DELETE     /api/admin/users/:user_id
GET/POST       /api/admin/majors
PUT/DELETE     /api/admin/majors/:major_code
GET/POST       /api/admin/courses
PUT/DELETE     /api/admin/courses/:course_code
GET            /api/admin/curriculum/:major_code
POST           /api/admin/curriculum
PUT/DELETE     /api/admin/curriculum/:curriculum_id
GET/POST       /api/admin/semesters
PUT/DELETE     /api/admin/semesters/:semester_id
GET/POST       /api/admin/registration-periods
PUT/DELETE     /api/admin/registration-periods/:period_id
GET            /api/admin/registration-demand
GET            /api/admin/registration-demand/:course_code/students
GET/POST       /api/admin/teaching-assignments
DELETE         /api/admin/teaching-assignments/:assignment_id
GET            /api/admin/qualified-lecturers/:course_code
POST           /api/admin/lecturer-qualifications
DELETE         /api/admin/lecturer-qualifications/:lecturer_id/:course_code
```

### Lecturer

```text
GET /api/lecturer/profile
GET /api/lecturer/semesters
GET /api/lecturer/teaching-courses?semester_id=...
GET /api/lecturer/courses/:course_code/students?semester_id=...
PUT /api/lecturer/registrations/:registration_id/grade
```

### Student

```text
GET  /api/student/profile
GET  /api/student/semesters
GET  /api/student/registration-periods
GET  /api/student/curriculum
GET  /api/student/courses
GET  /api/student/registrations
POST /api/student/registrations
PUT  /api/student/registrations/:registration_id/drop
GET  /api/student/grades
```

## 11. Troubleshooting

### `ModuleNotFoundError: No module named 'flask'`

Use the Python executable from the project's virtual environment:

```bash
../.venv/bin/python main.py
```

or activate the environment first:

```bash
source ../.venv/bin/activate
python main.py
```

### `Address already in use` on port 5000

Check which process owns the port:

```bash
lsof -i :5000
```

If an old Flask/Python process is listed, terminate its PID:

```bash
kill PID
```

Then confirm the port is free:

```bash
lsof -i :5000
```

Start Flask again.

### Login says invalid username or password

Confirm that the administrator was created in the same PostgreSQL database configured in `backend/.env`.

Check:

```sql
select user_id, username, fullname, email, role, active_status
from users
order by user_id;
```

The password must be the password entered when `create_admin.py` was run. The database stores a bcrypt hash, not the plain password.

### Frontend opens but data is empty

This is expected for a newly created database. Create data through the Administrator account in this order:

```text
Major
  ↓
Course
  ↓
Curriculum
  ↓
Semester
  ↓
Registration Period
  ↓
Lecturer / Student users
  ↓
Lecturer Qualification
  ↓
Teaching Assignment
  ↓
Student Registration
  ↓
Grades
```

## 12. Development notes

- The original React page/file structure is retained.
- `data.ts` remains as the original data-model file, but application pages now read/write through the Flask API instead of using its old demo data.
- The backend remains split by role/function: `auth.py`, `admin.py`, `lecturer.py`, `student.py`, and `database.py`.
- PostgreSQL remains the single source of truth for application data.
- Lecturer qualification is a real database relationship, not a frontend-only field.
cd "COURSE REGISTRATION SYSTEM new" 
cd backend 
../../.venv/bin/python main.py

## Verification and compatibility fixes

`/api/health` now queries PostgreSQL and returns HTTP 503 when the database is
unavailable. Dates in API JSON use ISO 8601 so frontend date inputs can round-trip.
Startup no longer changes database tables automatically.

Fresh installations: execute `dbschema.sql` in an empty database. This schema
includes the compatibility columns used by the backend; do not run legacy
migrations 001/002 against a fresh installation.

Already migrated legacy installations: after backing up, execute
`backend/migrations/003_administrators_compatibility.sql`. It adds the missing
administrator profile table and preserves existing users. Do not rerun migration
001 on a database where it was already applied.

From the backend directory, using the project virtual environment:

```powershell
& ../../.venv/Scripts/python.exe checks/static_check.py
& ../../.venv/Scripts/python.exe checks/integration_check.py
```

The integration check creates a unique PostgreSQL schema, tests actual committed
API writes and login, then removes only that test schema in a finally block.
It requires permission to create schemas. To test legacy triggers and constraints,
pass `--legacy-dump PATH` with a schema-only `pg_dump --no-owner --no-privileges
--schema=public` export. Existing application data is not copied or changed.

From the frontend directory, `npm run build` now runs TypeScript checking before
Vite. `npm run typecheck` checks types without producing build files.

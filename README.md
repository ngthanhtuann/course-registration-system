# Course Registration System

A simple course registration web system with three roles: **Administrator, Lecturer, and Student**.

The project uses:

- **Frontend:** React + TypeScript + Vite + Tailwind CSS
- **Backend:** Python Flask
- **Database:** PostgreSQL (the project can use Neon PostgreSQL cloud)
- **Authentication:** JWT

## 1. How the system works

```text
User
  |
  v
React Frontend
  |
  | HTTP / JSON
  v
Flask Routes
  |
  v
Models (system logic)
  |
  v
database.py
  |
  v
PostgreSQL / Neon
```

The frontend shows the user interface.  
The Flask routes receive requests from the frontend.  
The model classes contain the main system logic.  
`database.py` connects the backend to PostgreSQL.

## 2. Main functions

### Administrator

- Log in and manage account information.
- View dashboard statistics.
- Create, edit, deactivate and view Student/Lecturer accounts.
- Manage majors.
- Manage courses and prerequisites.
- Manage curriculum.
- Manage semesters.
- Manage registration periods.
- View registration demand and registered students.
- Set lecturer qualifications.
- Assign qualified lecturers to courses.

### Lecturer

- Log in and manage account information.
- View lecturer profile.
- View semesters and assigned teaching courses.
- View students registered in a teaching course.
- Enter and update student grades.

### Student

- Log in and manage account information.
- View profile and curriculum.
- View semesters and registration periods.
- Search/view available courses.
- Register for a course.
- View registration status.
- Drop a registered course during the allowed period.
- View grades.

## 3. Project structure

```text
Course Registration System/
├── backend/
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── setup_database.py
│   ├── create_admin.py
│   ├── requirements.txt
│   ├── models/
│   ├── routes/
│   └── utils/
├── database/
│   └── schema.sql
├── frontend/
│   ├── src/
│   ├── package.json
│   ├── package-lock.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   └── index.html
├── docs/
├── .gitignore
└── README.md
```

`node_modules`, `.env`, `.DS_Store`, Python cache files and other local/generated files are not included in the project source. They are created locally when needed.

## 4. Requirements

Install these tools first:

- Python 3.10 or newer
- Node.js 20 or newer
- npm
- A PostgreSQL database

The group can use one shared Neon PostgreSQL database. In that case, every member connects their local Flask backend to the same database.

## 5. Clone the project

Clone the repository:

```bash
git clone <repository-url>
```

Move into the project folder:

```bash
cd course-registration-system
```

All commands below should be run from the project root unless another folder is specified.

## 6. Backend setup

### macOS / Linux

Create a Python virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install backend packages:

```bash
python -m pip install -r backend/requirements.txt
```

Create the local environment file:

```bash
cp backend/.env.example backend/.env
```

### Windows PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r backend\requirements.txt
Copy-Item backend\.env.example backend\.env
```

## 7. Configure PostgreSQL / Neon

Open `backend/.env`.

For Neon, paste the connection strings supplied by the Neon project:

```env
DATABASE_URL=postgresql://...
DIRECT_DATABASE_URL=postgresql://...
DB_CONNECT_TIMEOUT=15
DB_TIMEZONE=Asia/Ho_Chi_Minh
DB_SSLMODE=

JWT_SECRET=YOUR_RANDOM_SECRET
HOST=127.0.0.1
PORT=5000
FLASK_DEBUG=false
CORS_ORIGINS=http://localhost:8443,http://127.0.0.1:8443
```

`DATABASE_URL` is used by the running backend.  
`DIRECT_DATABASE_URL` is used by `setup_database.py` when it is provided.

If the group uses one shared Neon database, each member creates their own `backend/.env` locally and enters the same shared Neon database information.

Do not send or store the real `.env` through GitHub.

If PostgreSQL is installed locally instead, leave `DATABASE_URL` empty and fill:

```env
db_host=localhost
db_port=5432
db_name=course_registration_system
db_user=postgres
db_password=YOUR_PASSWORD
```

Generate a JWT secret with:

```bash
python -c "import secrets; print(secrets.token_urlsafe(48))"
```

Copy the generated value to `JWT_SECRET`.

**Do not upload or commit `backend/.env`.** It contains private database information and the JWT secret.

## 8. Create the database tables

This step is needed only for a new, empty database.

From the project root:

```bash
python backend/setup_database.py
```

The script reads `database/schema.sql` and creates the project tables, constraints, triggers and schema version.

For a shared Neon database, this command only needs to be run **once**. Other group members who connect to the same already-initialized database do not need to run it again.

## 9. Create the first Admin account

After the database has been created:

```bash
python backend/create_admin.py
```

Enter:

- Admin ID
- Full name
- Email
- Password

The username is the Admin ID converted to lowercase.

For a shared Neon database, only **one group member** needs to create the first Admin account.

After the first Admin exists, the Admin can create Lecturer and Student accounts from the website. Because the accounts are stored in the shared database, other group members can use the same accounts.

## 10. Run the backend

From the project root, with the virtual environment active:

```bash
python backend/main.py
```

Default backend address:

```text
http://127.0.0.1:5000
```

Check the backend:

```text
http://127.0.0.1:5000/
```

Check the backend and database connection:

```text
http://127.0.0.1:5000/api/health
```

A working database should return a response with:

```json
{
  "status": "ok",
  "database": "ok"
}
```

Keep this Terminal running.

## 11. Run the frontend

Open a second Terminal:

```bash
cd frontend
npm install
npm run dev
```

Open:

```text
http://localhost:8443
```

The Vite development server automatically sends `/api` requests to the Flask backend at `http://127.0.0.1:5000`.

Normally, `frontend/.env` is not required for local development.

If the frontend must call a backend at another URL, create `frontend/.env` from the example:

```bash
cp .env.example .env
```

Then set:

```env
VITE_API_URL=https://your-backend-url
```

`VITE_API_URL` is a **backend HTTP URL**, not a PostgreSQL connection string.

## 12. Stop the system

To stop the frontend or backend development server, go to the Terminal where it is running and press:

```text
Ctrl + C
```

If both frontend and backend are running in separate Terminals, stop each one separately.

## 13. Check the code

This checkout does not include a `tests/unit` folder. The checks below do not create output files, but they do not replace full functional tests.

Activate the Python virtual environment and check backend syntax from the project root:

```bash
python -B -c "import ast; from pathlib import Path; [ast.parse(p.read_text()) for p in Path('backend').rglob('*.py')]; print('Python syntax OK')"
```

Frontend TypeScript can be checked with:

```bash
cd frontend
npm run typecheck
```

A production frontend build can be checked with the following command. It creates files in `frontend/dist`, so skip it when no new files are allowed.

```bash
npm run build
```

## 14. Important files

### Backend

- `backend/main.py` - starts Flask, registers the API route groups and provides health endpoints.
- `backend/config.py` - reads JWT settings from `.env`.
- `backend/database.py` - reuses PostgreSQL connections through a small connection pool and provides query helper methods. A pool keeps a connection ready for later requests, avoiding repeated connection setup.
- `backend/setup_database.py` - initializes a new database using `database/schema.sql`.
- `backend/create_admin.py` - creates the first Administrator account.
- `backend/models/` - contains the object-oriented system logic.
- `backend/routes/` - contains HTTP API endpoints for the frontend.
- `backend/utils/` - contains shared authentication, password and HTTP helper functions.

### Frontend

- `frontend/src/App.tsx` - defines application routes for Admin, Lecturer and Student.
- `frontend/src/components/` - reusable user-interface components.
- `frontend/src/pages/` - pages shown for each role.
- `frontend/src/services/api.ts` - sends requests from React to the Flask API.
- `frontend/src/types.ts` - shared TypeScript data types.
- `frontend/src/styles.css` - global styles and Tailwind setup.
- `frontend/vite.config.ts` - Vite configuration and local API proxy.

### Database and documentation

- `database/schema.sql` - creates the PostgreSQL schema and database rules.
- `docs/` - project requirements, design and report documents.

## 15. Shared Neon database

When several group members use the same `DATABASE_URL`, they use the same PostgreSQL database even when they are on different networks.

Example:

```text
Machine A -> local Flask A ----\
                                -> Neon PostgreSQL
Machine B -> local Flask B ----/
```

If Machine A creates a Student account, the data is stored in Neon. Machine B can see and use the same data because its backend connects to the same Neon database.

The same applies to courses, semesters, registrations, grades and other database data.

A tunnel is not required for the database connection because each computer connects directly to Neon through the Internet.

Each member still runs their own local frontend and backend:

```text
Machine A:
React A -> Flask A -> Neon

Machine B:
React B -> Flask B -> Neon
```

## 16. Common problems

### `ModuleNotFoundError`

Make sure the virtual environment is active and install:

```bash
python -m pip install -r backend/requirements.txt
```

### Port 5000 is already in use

Find the old Flask process and stop it, or change `PORT` in `backend/.env`.

### Port 8443 is already in use

Stop the old Vite process before running `npm run dev` again.

### `/api/health` says database unavailable

Check:

- `DATABASE_URL`
- Neon project status
- Internet connection
- PostgreSQL username/password
- SSL parameters in the connection string

### Login does not work

Check that:

- the database schema exists;
- an Admin/user account exists;
- the account is active;
- `JWT_SECRET` is set in `backend/.env`.

## 17. Recommended run order for a new machine

### Using an already-created shared Neon database

For a group member cloning the project for the first time:

```bash
git clone <repository-url>
cd course-registration-system

python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r backend/requirements.txt
cp backend/.env.example backend/.env
```

Fill `backend/.env` with the shared Neon database information.

Then start the backend:

```bash
python backend/main.py
```

Open another Terminal and start the frontend:

```bash
cd frontend
npm install
npm run dev
```

Open:

```text
http://localhost:8443
```

There is **no need** to run `setup_database.py` or `create_admin.py` again if the shared Neon database has already been initialized.

### Using a new empty Neon database for the first time

Complete the backend setup and configure `backend/.env`, then run:

```bash
python backend/setup_database.py
python backend/create_admin.py
```

These two steps only need to be completed once for the shared database.

Then start the system normally:

```bash
python backend/main.py
```

In another Terminal:

```bash
cd frontend
npm install
npm run dev
```

Open:

```text
http://localhost:8443
```

## 18. Quick start summary

### First group member with a new database

```text
Clone project
    ↓
Create .venv
    ↓
Install backend requirements
    ↓
Create backend/.env
    ↓
Add Neon database information
    ↓
Run setup_database.py
    ↓
Run create_admin.py
    ↓
Run backend
    ↓
Run frontend
    ↓
System ready
```

### Other group members

```text
Clone project
    ↓
Create .venv
    ↓
Install backend requirements
    ↓
Create backend/.env
    ↓
Add the SAME Neon database information
    ↓
Run backend
    ↓
Run frontend
    ↓
Use the same system data/accounts
```

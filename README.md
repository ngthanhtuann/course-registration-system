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
├── tests/
│   └── unit/
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

## 5. Backend setup

Open Terminal in the project root.

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

## 6. Configure PostgreSQL / Neon

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

## 7. Create the database tables

This step is needed only for a new, empty database.

From the project root:

```bash
python backend/setup_database.py
```

The script reads `database/schema.sql` and creates the project tables, constraints, triggers and schema version.

Run this only once for the shared database. Other group members who connect to the same already-initialized Neon database do **not** need to run it again.

## 8. Create the first Admin account

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

After the first Admin exists, the Admin can create Lecturer and Student accounts from the website.

## 9. Run the backend

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

## 10. Run the frontend

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

## 11. Run unit tests

Activate the Python virtual environment and run from the project root:

```bash
python -m unittest discover -s tests/unit -v
```

Current unit tests cover examples of:

- User authentication validation
- Course value validation
- Database connection behavior
- Grade/result calculation

Frontend TypeScript can be checked with:

```bash
cd frontend
npm run typecheck
```

A production frontend build can be checked with:

```bash
npm run build
```

## 12. Important files

### Backend

- `backend/main.py` - starts Flask, registers the API route groups and provides health endpoints.
- `backend/config.py` - reads JWT settings from `.env`.
- `backend/database.py` - opens PostgreSQL connections and provides query helper methods.
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
- `frontend/vite.config.ts` - simple Vite configuration and local API proxy.

### Database and tests

- `database/schema.sql` - creates the PostgreSQL schema and database rules.
- `tests/unit/` - basic unit tests.
- `docs/` - project requirements/design/report documents.

## 13. Shared Neon database

When several group members use the same `DATABASE_URL`, they use the same PostgreSQL database even when they are on different networks.

Example:

```text
Machine A -> local Flask A ----\
                                -> Neon PostgreSQL
Machine B -> local Flask B ----/
```

If Machine A creates a Student account, the data is stored in Neon. Machine B can see the same data after its backend connects to the same Neon database.

A tunnel is not required for the database connection because both computers connect directly to Neon through the Internet.

## 14. Common problems

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

## 15. Recommended run order for a new machine

For a machine connecting to an **already-created shared Neon database**:

```bash
# Project root
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r backend/requirements.txt
cp backend/.env.example backend/.env

# Fill backend/.env with the shared database information.

python backend/main.py
```

Then in another Terminal:

```bash
cd frontend
npm install
npm run dev
```

For the **first machine and a new empty database**, run these once before starting the backend:

```bash
python backend/setup_database.py
python backend/create_admin.py
```

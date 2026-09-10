# Course Registration System

The Course Registration System consists of a React + TypeScript + Vite frontend, a Flask backend, and PostgreSQL.

## Structure

```text
Course_Registration_System/
â”œâ”€â”€ backend/
â”‚   â”œâ”€â”€ app.py                 # Flask entry point
â”‚   â”œâ”€â”€ config.py
â”‚   â”œâ”€â”€ database.py
â”‚   â”œâ”€â”€ create_admin.py
â”‚   â”œâ”€â”€ models/                # Domain models
â”‚   â”œâ”€â”€ services/              # Business-service boundary
â”‚   â”œâ”€â”€ routes/                # Flask API blueprints
â”‚   â”œâ”€â”€ utils/                 # Auth, password, HTTP helpers
â”‚   â”œâ”€â”€ migrations/            # Legacy-database migrations
â”‚   â”œâ”€â”€ checks/                # Static and integration checks
â”‚   â””â”€â”€ requirements.txt
â”œâ”€â”€ frontend/
â”‚   â”œâ”€â”€ src/
â”‚   â”‚   â”œâ”€â”€ services/api.ts
â”‚   â”‚   â”œâ”€â”€ components/
â”‚   â”‚   â”œâ”€â”€ context/
â”‚   â”‚   â””â”€â”€ pages/
â”‚   â”œâ”€â”€ package.json
â”‚   â””â”€â”€ vite.config.ts
â”œâ”€â”€ database/
â”‚   â”œâ”€â”€ schema.sql             # Fresh PostgreSQL schema
â”‚   â””â”€â”€ sample_data.sql        # Optional local seed entry point
â”œâ”€â”€ tests/unit/
â”œâ”€â”€ docs/
â””â”€â”€ README.md
```

## Requirements

- Python 3.10+ (recommended 3.11+)
- Node.js 20+
- PostgreSQL 14+
- npm

## Database setup

1. Start PostgreSQL and create the database `course_registration_system`.
2. Run the entire contents of [`database/schema.sql`](database/schema.sql) on an empty database using DBeaver or `psql`:

   ```bash
   psql -U postgres -d course_registration_system -f database/schema.sql
   ```

3. Create `backend/.env` with the connection configuration. Do not commit this file.

   ```env
   db_host=localhost
   db_port=5432
   db_name=course_registration_system
   db_user=postgres
   db_password=YOUR_POSTGRES_PASSWORD
   JWT_SECRET=REPLACE_WITH_A_RANDOM_SECRET_OF_AT_LEAST_32_CHARACTERS
   ```

The fresh schema uses canonical columns directly. Do not run legacy migrations on a database newly created from `database/schema.sql`.

### Legacy database

Back up the database first. Only if the database was created using the old schema should you run the files in `backend/migrations/` in order. Do not rerun an already applied migration. Migration 005 removes duplicate compatibility fields after checking that their data agrees; it stops if legacy grade records need a separate data migration. Run `python backend/checks/schema_check.py` after migration to verify the database contract.

## Backend setup

Run from the project root directory.

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r backend/requirements.txt
```

### Windows PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r backend\requirements.txt
```

### Create the first administrator

After activating the virtual environment:

```bash
cd backend
python create_admin.py
```

Enter the Admin ID, full name, email, and password. The login username is the lowercase Admin ID.

### Run the backend

From the `backend/` directory, while the virtual environment is still active:

```bash
python app.py
```

The backend runs at `http://127.0.0.1:5000`.

Check status:

```text
GET http://127.0.0.1:5000/api/health
```

When PostgreSQL is ready, the API returns:

```json
{"status":"ok","database":"ok"}
```

## Frontend setup and run

Open a second terminal at the project root:

```bash
cd frontend
npm install
npm run dev
```

Vite runs at `http://localhost:8443` by default. In development, Vite proxies `/api` to `http://127.0.0.1:5000`.

If the backend is at a different address, create `frontend/.env`:

```env
VITE_API_URL=http://127.0.0.1:5000
```

## Startup order

1. Start PostgreSQL.
2. Activate `.venv` and run `python app.py` in `backend/`.
3. Run `npm run dev` in `frontend/`.
4. Open the Vite URL shown in the terminal and log in with the administrator account you created.

## Main API

| Role | Prefix |
| --- | --- |
| Authentication/account | `/api/login`, `/api/me`, `/api/account/*` |
| Administrator | `/api/admin/*` |
| Lecturer | `/api/lecturer/*` |
| Student | `/api/student/*` |

All protected endpoints use the header:

```text
Authorization: Bearer <token>
```

## Quality checks

Run from the project root after installing backend dependencies:

```bash
python backend/checks/schema_check.py
python backend/checks/static_check.py
python -m unittest discover -s tests/unit -v
```

The integration check requires PostgreSQL to be running and permission to create schemas. It creates a temporary schema, deletes it automatically when finished, and does not modify existing application data:

```bash
python backend/checks/integration_check.py
```

Check the frontend:

```bash
cd frontend
npm run typecheck
npm run build
```

## Troubleshooting

### Cannot connect to PostgreSQL

Check that PostgreSQL is running, the database exists, and the `db_host`, `db_port`, `db_name`, `db_user`, and `db_password` values in `backend/.env` are correct.

### Port 5000 is already in use

macOS / Linux:

```bash
lsof -i :5000
kill PID
```

Windows PowerShell:

```powershell
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### Frontend opens but does not load data

Confirm that the backend is running, `/api/health` returns `database: ok`, and `VITE_API_URL` is not set incorrectly in `frontend/.env`.

## Additional documentation

- [System specification](docs/system-document.md)

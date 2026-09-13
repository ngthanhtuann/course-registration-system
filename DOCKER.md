# Run with Docker Compose (Windows PowerShell)

This setup runs the Flask backend and Vite frontend in separate containers. It uses the existing PostgreSQL/Neon database configured in `backend/.env`; it does not create a database container.

## First run

1. Open Docker Desktop and wait until the engine is running.
2. Open PowerShell and move into the nested project directory:

   ```powershell
   cd C:\TTNT\course-registration-system
   cd .\course-registration-system
   ```

3. Confirm that `backend/.env` exists and contains a working `DATABASE_URL` and `JWT_SECRET`. If it does not exist, copy the example and edit it:

   ```powershell
   Copy-Item .\backend\.env.example .\backend\.env
   notepad .\backend\.env
   ```

   Do not put real credentials in `compose.yaml` or commit `backend/.env` to Git.

4. Stop any locally running Flask or Vite processes using ports 5000 or 8443, then build and start:

   ```powershell
   docker compose up --build -d
   docker compose ps
   ```

5. Open <http://localhost:8443>. The backend health endpoint is <http://127.0.0.1:5000/api/health>.

## Inspect and stop

```powershell
docker compose logs -f backend
docker compose logs -f frontend
docker compose down
```

Press `Ctrl+C` to stop following logs. Run `docker compose down` when you want to stop the containers. The database data remains in Neon/PostgreSQL.

## After changing source code

The images contain a copy of the code; rebuild them after local edits:

```powershell
docker compose up --build -d
```

The frontend reaches Flask at `http://backend:5000` over the Compose network. For local development without Docker, Vite still uses `http://127.0.0.1:5000` by default. If using PostgreSQL installed on the Windows host instead of Neon, set `db_host=host.docker.internal` in `backend/.env` so the backend container can reach it.

This is a development setup using Vite and Flask's built-in server. It does not provide a production web server or HTTPS.

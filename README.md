# Attendance SaaS — Backend

FastAPI + PostgreSQL backend for an attendance-tracking SaaS. Handles companies,
employees, attendance logs (from a biometric device or manual entry), shifts,
and leave requests.

## Project structure

```
attendance-saas/
├── main.py                    # FastAPI app entry point
├── requirements.txt
├── .env.example                # copy to .env and fill in your DB credentials
├── .gitignore
├── README.md
└── app/
    ├── core/
    │   └── database.py         # SQLAlchemy engine/session setup
    ├── models/                 # SQLAlchemy ORM models (one file per table)
    │   ├── company.py
    │   ├── employee.py
    │   ├── attendance_log.py
    │   ├── shift.py
    │   └── leave.py
    ├── schemas/                 # Pydantic request/response schemas
    │   ├── company.py
    │   └── employee.py
    └── routers/                 # API route handlers
        ├── companies.py
        └── employees.py
```

## 1. Prerequisites

- Python 3.11+
- A free [Supabase](https://supabase.com) account (gives you a hosted Postgres database)

## 2. Create a free Supabase Postgres database

1. Go to [supabase.com](https://supabase.com) and sign up / log in.
2. Click **New project**. Pick any name, set a database password (save it
   somewhere safe), and choose the region closest to you.
3. Wait for the project to finish provisioning (~2 minutes).
4. In the project dashboard, go to **Project Settings → Database**.
5. Under **Connection string**, select the **URI** tab.
   - For local development, the **Session pooler** or direct connection
     string both work fine.
6. Copy that URI — it looks like:
   ```
   postgresql://postgres:[YOUR-PASSWORD]@[HOST]:5432/postgres
   ```
7. Replace `[YOUR-PASSWORD]` with the database password you set in step 2.

## 3. Set up the project locally

```bash
# 1. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # on Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure your database connection
cp .env.example .env
# then open .env and paste your Supabase connection string into DATABASE_URL
```

## 4. Run the API

```bash
uvicorn main:app --reload
```

On startup, the app automatically creates any tables that don't exist yet
(via `Base.metadata.create_all`). This is convenient for local development;
for production, switch to a proper migration tool like **Alembic** instead
of relying on auto-create.

The API will be running at:

- App: http://127.0.0.1:8000
- Interactive docs (Swagger UI): http://127.0.0.1:8000/docs
- Alternative docs (ReDoc): http://127.0.0.1:8000/redoc

## 5. Try it out

Create a company:

```bash
curl -X POST http://127.0.0.1:8000/companies/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Acme Corp"}'
```

Create an employee under that company:

```bash
curl -X POST http://127.0.0.1:8000/employees/ \
  -H "Content-Type: application/json" \
  -d '{"company_id": 1, "name": "Jane Doe", "email": "jane@acme.com", "phone": "9999999999", "device_user_id": "101"}'
```

List employees for a company:

```bash
curl "http://127.0.0.1:8000/employees/?company_id=1"
```

Or just open http://127.0.0.1:8000/docs and try every endpoint interactively.

## Database schema

| Table              | Purpose                                                             |
|--------------------|-----------------------------------------------------------------------|
| `companies`        | Each business/tenant using the SaaS                                  |
| `employees`        | Employees belonging to a company, linked to a biometric device user ID |
| `attendance_logs`  | Punch in/out events, from a device or manual/app entry                |
| `shifts`           | Named shift definitions (start/end time) per company                 |
| `leaves`           | Leave requests per employee with approval status                     |

## What's included vs. what's next

Included: full schema, DB connection setup, and CRUD endpoints for
`companies` and `employees`.

Not yet included (natural next steps): CRUD endpoints for `attendance_logs`,
`shifts`, and `leaves`; authentication/authorization; Alembic migrations;
device webhook/ingestion endpoint for the biometric machine. Ask if you'd
like any of these built out next.

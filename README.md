# LeaveTrack 🗓️

> A lightweight employee leave & absence management system built with Python, Flask,
> and PostgreSQL.

---

> ⚠️ **Heads up** ⚠️
>
> This is a training and technical demonstration project, built as part of a 25-day
> Python pre-training program targeting an Odoo developer interview.
>
> It is not intended for production use, and will not evolve beyond its current scope.
>
> The goal is to demonstrate clean design decisions, not to build a complete product.

---

## What it does

LeaveTrack allows a company to manage employee absence requests end-to-end:

- Submit leave requests (paid leave, sick leave, unpaid leave)
- Approve or reject requests (manager workflow)
- Track leave balances per employee and per year
- Detect overlapping absences
- View absence history and department-level reports

---

## Tech stack

| Layer         | Technology   | Why                                    |
|---------------|--------------|----------------------------------------|
| Language      | Python 3.11+ | Core logic, models, services           |
| Web framework | Flask 3.x    | Thin HTTP layer — routes only          |
| Database      | PostgreSQL   | Production-grade RDBMS, same as Odoo   |
| DB driver     | psycopg2     | Standard PostgreSQL adapter for Python |

> **Design philosophy:** Flask is used strictly as an HTTP layer. All business logic
> lives in `services/` — pure Python, no framework dependency.

---

## Project structure

```
leavetrack/
├── app.py                        # Flask entry point
├── config/
│   └── database.py               # PostgreSQL connection (psycopg2)
├── models/                       # Pure Python data classes
│   ├── enums.py                  # AbsenceStatus enum
│   ├── employee.py
│   ├── department.py
│   ├── absence.py                # Absence base class + PaidLeave / SickLeave / UnpaidLeave
│   ├── absence_type.py
│   └── leave_balance.py
├── repositories/                 # SQL queries via psycopg2 — no business logic
│   ├── employee_repo.py
│   ├── absence_repo.py
│   └── leave_balance_repo.py
├── services/                     # Business logic — no Flask dependency
│   ├── absence_service.py        # Overlap detection, approval workflow
│   └── report_service.py         # Aggregations, CTE queries
├── routes/                       # Flask blueprints — thin layer
│   ├── employees.py
│   ├── absences.py
│   └── reports.py
├── sql/
│   └── schema.sql                # Table definitions + seed data
├── requirements.txt
├── .env.example
└── .gitignore
```

---

## Getting started

### Prerequisites

- Python 3.11+
- PostgreSQL installed and running

```sql
CREATE DATABASE leavetrack;
```

### 1. Clone the repository

```bash
git clone https://github.com/your-username/leavetrack.git
cd leavetrack
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate     # macOS / Linux
venv\Scripts\activate         # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the database connection

```bash
cp .env.example .env
# Edit .env with your credentials
```

```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=leavetrack
DB_USER=postgres
DB_PASSWORD=yourpassword
```

### 5. Initialize the database

```bash
psql -U postgres -d leavetrack -f sql/schema.sql
```

### 6. Run the app

```bash
python app.py
```

The app will be available at `http://localhost:5000`.

---

## Design decisions

### 3-tier architecture
The project is split into three strict layers: **routes** (HTTP), **services**
(business logic), and **repositories** (SQL).
A route never writes SQL. A repository never contains an `if`. 

### Why Flask?
Flask is used as a minimal HTTP layer — nothing more. All business logic is isolated
in `services/`, which has zero Flask dependency and can be tested without an HTTP 
context.

### Why PostgreSQL?
PostgreSQL is the database Odoo uses in production. It natively supports CTEs and
advanced aggregations used in this project's reporting queries.

### Why inheritance for Absence subtypes?
`PaidLeave`, `SickLeave`, and `UnpaidLeave` all share a common structure but differ
in one key business rule: only `PaidLeave` deducts from the annual leave balance.
Inheritance is the natural fit — a `SickLeave` *is* an `Absence`.

### Why a `set` for overlap detection?
Checking date range overlap with a list requires a nested loop — O(m×n).
By building a `set` of all approved absence dates for an employee, each lookup
becomes O(1) average, and the overlap check becomes a simple set intersection.

---

## Key SQL queries

- **Remaining balance per employee** — `SUM` aggregation with `GROUP BY` + `JOIN`
- **Understaffing alert** — employees absent on the same date per department using 
`COUNT` + `HAVING`
- **12-month rolling absences** — CTE to compute cumulative absence days per employee 
over the last year

---

## Entity-Relationship Diagram

See [ERD.mmd](./ERD.mmd) for the full database schema.
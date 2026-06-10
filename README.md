# LeaveTrack 🗓️

> A lightweight employee leave & absence management system built with Python, Flask,
> and PostgreSQL.

---

> ⚠️ **Heads up** ⚠️
> 
> This is a training and technical demonstration project, built as part of a Python
> pre-training program targeting an Odoo developer interview.
> 
> It is not intended for production use, and will not evolve beyond its current scope.
> 
> The goal is to demonstrate clean design decisions, not to build a complete product.

---

> 🗺️ See [ROADMAP.md](./ROADMAP.md) for the development progress.

## What it does

LeaveTrack allows a company to manage employee absence requests end-to-end:

- Submit leave requests (paid leave, sick leave, unpaid leave)
- Approve or reject requests with overlap and balance validation
- Track leave balances per employee, per type, and per year
- Detect overlapping absences before submit and before approval
- Automatic `used_days` increment on approval for paid leave
- View absence history and department-level reports

---

## Tech stack

| Layer         | Technology   | Why                                    |
| ------------- | ------------ | -------------------------------------- |
| Language      | Python 3.11+ | Core logic, models, services           |
| Web framework | Flask 3.x    | Thin HTTP layer, routes only           |
| Database      | PostgreSQL   | Production-grade RDBMS, same as Odoo   |
| DB driver     | psycopg2     | Standard PostgreSQL adapter for Python |

> **Design philosophy:** Flask is used strictly as an HTTP layer. All business logic
> lives in `services/`, pure Python, no framework dependency.

---

## Project structure

```
leavetrack/
├── app.py                        # Flask entry point
├── config/
│   └── database.py               # PostgreSQL connection (psycopg2)
├── models/                       # Pure Python data classes
│   ├── __init__.py
│   ├── enums.py                  # AbsenceStatus enum
│   ├── employee.py
│   ├── department.py
│   ├── absence.py                # Absence abstract base + PaidLeave / SickLeave / UnpaidLeave
│   ├── absence_type.py
│   └── leave_balance.py
├── repositories/                 # SQL queries via psycopg2, no business logic
│   ├── __init__.py
│   ├── employee_repo.py
│   ├── department_repo.py
│   ├── absence_repo.py
│   ├── absence_type_repo.py
│   └── leave_balance_repo.py
├── services/                     # Business logic, no Flask dependency
│   ├── __init__.py
│   ├── absence_service.py        # submit, approve, reject with overlap + balance checks
│   └── report_service.py         # Aggregations, CTE queries
├── routes/                       # Flask blueprints, thin layer
│   ├── __init__.py
│   ├── employees.py
│   ├── absences.py
│   └── reports.py
├── tests/                        # Unit tests (unittest)
│   ├── test_absence.py           # Absence model: date_range, duration, inheritance
│   ├── test_leave_balance.py     # LeaveBalance: remaining, can_approve
│   └── test_overlap.py           # Overlap detection
├── sql/
│   ├── schema.sql                # Table definitions
│   └── seed.sql                  # Diversified seed data (5 depts, 10 employees, 30 absences)
├── ROADMAP.md                    # Development roadmap
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
psql -U postgres -d leavetrack -f sql/seed.sql
```

### 6. Run the app

```bash
python app.py
```

The app will be available at `http://localhost:5000`.

### 7. Run the tests

```bash
python -m unittest discover tests -v
```

Covers model behaviour (`PaidLeave`/`SickLeave`/`UnpaidLeave` inheritance, date range
generation, duration), leave balance logic (`remaining`, `can_approve`, unlimited
types), and set-based overlap detection.

---

## Design decisions

### 3-tier architecture

The project is split into three strict layers: **routes** (HTTP), **services**
(business logic), and **repositories** (SQL).
A route never writes SQL. A repository never contains an `if`.

### Why Flask?

Flask is used as a minimal HTTP layer, nothing more. All business logic is isolated
in `services/`, which has zero Flask dependency and can be tested without an HTTP
context.

### Why PostgreSQL?

PostgreSQL is the database Odoo uses in production. It natively supports CTEs and
advanced aggregations used in this project's reporting queries.

### Why inheritance for Absence subtypes?

`PaidLeave`, `SickLeave`, and `UnpaidLeave` all share a common structure but differ
in one key business rule: only `PaidLeave` deducts from the annual leave balance.
Inheritance is the natural fit, a `SickLeave` _is_ an `Absence`. Subclass
discrimination uses the `code` column (`paid`, `sick`, `unpaid`) rather than labels,
keeping the mapping stable even if labels are translated.

### Why nullable `total_days` in leave_balance?

Types like sick leave and unpaid leave have no annual cap (`max_days_per_year` is
NULL), but we still track `used_days` for reporting. Setting `total_days` to NULL
signals "unlimited", `can_approve()` returns `True` regardless of `used_days`.

### Why a `set` for overlap detection?

Checking date range overlap with a list requires a nested loop, O(m×n).
By building a `set` of all approved absence dates for an employee, each lookup
becomes O(1) average, and the overlap check becomes a simple set intersection.

### Balance update on approval, not on submission

Leave balance `used_days` is incremented only when an absence transitions from
PENDING to APPROVED. This avoids counting requests that are later rejected, and
allows re-checking balance at approval time in case other approvals consumed the
budget in the meantime.

---

## Key SQL queries

- **Remaining balance per employee**, `SUM` aggregation with `GROUP BY` + `JOIN`
- **Understaffing alert**, employees absent on the same date per department using
  `COUNT` + `HAVING`
- **12-month rolling absences**, CTE to compute cumulative absence days per employee
  over the last year

---

## Entity-Relationship Diagram

See [ERD.mmd](./ERD.mmd) for the full database schema.

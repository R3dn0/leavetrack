from dataclasses import dataclass
from datetime import date, datetime, timedelta

import psycopg2.extensions
from psycopg2.extras import RealDictCursor


@dataclass
class BalanceReport:
    employee_id: int
    first_name: str
    last_name: str
    absence_type_code: str
    total_days: int | None
    used_days: int
    remaining: int
    year: int


@dataclass
class UnderstaffingAlert:
    department: str
    date: date
    absent_count: int


@dataclass
class RollingAbsenceReport:
    employee_id: int
    first_name: str
    last_name: str
    total_days: int


class ReportService:
    def __init__(self, conn: psycopg2.extensions.connection) -> None:
        self._conn = conn

    def remaining_balance_per_employee(self) -> list[BalanceReport]:
        with self._conn.cursor(cursor_factory=RealDictCursor) as cur:
            query = """
                SELECT
                    e.id               AS employee_id,
                    e.first_name,
                    e.last_name,
                    at.code           AS absence_type_code,
                    lb.total_days,
                    COALESCE(lb.used_days, 0) AS used_days,
                    lb.total_days - COALESCE(lb.used_days, 0) AS remaining,
                    lb.year
                FROM employee e
                JOIN leave_balance lb ON lb.employee_id = e.id
                JOIN absence_type at  ON at.id = lb.type_id
                WHERE e.is_active = TRUE
                AND lb.total_days IS NOT NULL
                ORDER BY e.last_name, e.first_name, lb.year DESC, at.label
            """
            cur.execute(query)
            rows = cur.fetchall()

        return [BalanceReport(**row) for row in rows]

    def understaffing_alert(
        self,
        threshold: int = 2,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
    ) -> list[UnderstaffingAlert]:
        where_clause = "WHERE a.status = 'approved'"
        params: list = []

        if start_date is not None:
            where_clause += " AND a.end_date >= %s"
            params.append(start_date)
        if end_date is not None:
            where_clause += " AND a.start_date <= %s"
            params.append(end_date)

        with self._conn.cursor(cursor_factory=RealDictCursor) as cur:
            query = f"""
                WITH absence_dates AS (
                    SELECT
                        a.employee_id,
                        generate_series(a.start_date, a.end_date, '1 day'::interval)::date AS absence_date
                    FROM absence a
                    {where_clause}
                )
                SELECT
                    d.name           AS department,
                    ad.absence_date  AS date,
                    COUNT(*)         AS absent_count
                FROM absence_dates ad
                JOIN employee e  ON e.id = ad.employee_id
                JOIN department d ON d.id = e.department_id
                GROUP BY d.name, ad.absence_date
                HAVING COUNT(*) >= %s
                ORDER BY d.name, ad.absence_date
            """
            params.append(threshold)

            cur.execute(query, tuple(params))
            rows = cur.fetchall()

        return [UnderstaffingAlert(**row) for row in rows]

    def rolling_12_months(
        self, reference_date: datetime | None = None
    ) -> list[RollingAbsenceReport]:
        ref = reference_date or datetime.now()
        twelve_months_ago = ref - timedelta(days=365)

        with self._conn.cursor(cursor_factory=RealDictCursor) as cur:
            query = """
                WITH absence_days AS (
                    SELECT
                        a.employee_id,
                        generate_series(a.start_date, a.end_date, '1 day'::interval)::date AS absence_date
                    FROM absence a
                    WHERE a.status = 'approved'
                    AND a.start_date >= %s
                )
                SELECT
                    e.id           AS employee_id,
                    e.first_name,
                    e.last_name,
                    COUNT(*)       AS total_days
                FROM absence_days ad
                JOIN employee e ON e.id = ad.employee_id
                GROUP BY e.id, e.first_name, e.last_name
                ORDER BY total_days DESC
            """
            cur.execute(query, (twelve_months_ago,))
            rows = cur.fetchall()

        return [RollingAbsenceReport(**row) for row in rows]

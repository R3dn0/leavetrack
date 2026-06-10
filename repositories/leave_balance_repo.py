from typing import Any

import psycopg2.extensions
from models import LeaveBalance

_SELECT_COLUMS = """
    lb.id,
    lb.employee_id,
    lb.type_id,
    lb.year,
    lb.total_days,
    lb.used_days
"""


def _row_to_leave_balance(row: tuple[Any, ...]) -> LeaveBalance:
    (
        db_id,
        employee_id,
        type_id,
        year,
        total_days,
        used_days,
    ) = row

    kwargs: dict[str, Any] = dict(
        employee_id=employee_id,
        type_id=type_id,
        year=year,
        total_days=total_days,
        used_days=used_days,
        id=db_id,
    )

    return LeaveBalance(**kwargs)


class LeaveBalanceRepository:
    def __init__(self, conn: psycopg2.extensions.connection) -> None:
        self._conn = conn

    def find_all(self) -> list[LeaveBalance]:
        with self._conn.cursor() as cur:
            query = (
                f"SELECT {_SELECT_COLUMS} FROM leave_balance ORDER BY leave_balance.id"
            )
            cur.execute(query)
            rows = cur.fetchall()

        return [_row_to_leave_balance(r) for r in rows]

    def find_by_employee_id(self, employee_id: int) -> list[LeaveBalance]:
        with self._conn.cursor() as cur:
            query = f"SELECT {_SELECT_COLUMS} FROM leave_balance WHERE employee_id = %s"
            cur.execute(query, (employee_id,))
            rows = cur.fetchall()

        return [_row_to_leave_balance(r) for r in rows]

    def find_by_employee_and_year(
        self, employee_id: int, year: int
    ) -> list[LeaveBalance]:
        with self._conn.cursor() as cur:
            query = f"SELECT {_SELECT_COLUMS} FROM leave_balance "
            query += f"WHERE employee_id = %s and year=%s"
            cur.execute(
                query,
                (
                    employee_id,
                    year,
                ),
            )
            rows = cur.fetchall()

        return [_row_to_leave_balance(r) for r in rows]

    def insert(self, leave_balance) -> LeaveBalance:
        with self._conn.cursor() as cur:
            try:
                cur.execute(
                    "INSERT INTO leave_balance "
                    "(employee_id, type_id, year, total_days, used_days) "
                    "VALUES (%s, %s, %s, %s, %s) RETURNING id",
                    (
                        leave_balance.employee_id,
                        leave_balance.type_id,
                        leave_balance.year,
                        leave_balance.total_days,
                        leave_balance.used_days,
                    ),
                )
                row = cur.fetchone()
                if row is None:
                    raise RuntimeError("INSERT returned no id")
                leave_balance.id = row[0]
                self._conn.commit()

            except Exception as e:
                self._conn.rollback()
                print("Exception:", e)
                raise

        return leave_balance

    def update(self, leave_balance) -> LeaveBalance:
        with self._conn.cursor() as cur:
            try:
                cur.execute(
                    "UPDATE leave_balance SET employee_id = %s, type_id = %s, year = %s, total_days = %s, used_days = %s WHERE id = %s",
                    (
                        leave_balance.employee_id,
                        leave_balance.type_id,
                        leave_balance.year,
                        leave_balance.total_days,
                        leave_balance.used_days,
                        leave_balance.id,
                    ),
                )
                if cur.rowcount == 0:
                    raise KeyError(f"No leave_balance with id={leave_balance.id}")
                self._conn.commit()

            except Exception as e:
                self._conn.rollback()
                print("Exception:", e)
                raise

        return leave_balance

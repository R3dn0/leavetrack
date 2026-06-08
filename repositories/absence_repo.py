from datetime import datetime
from typing import Any

import psycopg2.extensions

from models.absence import Absence, PaidLeave, SickLeave, UnpaidLeave
from models.enums import AbsenceStatus

_SELECT_COLUMNS = """
    a.id,
    a.employee_id,
    a.type_id,
    a.start_date,
    a.end_date,
    a.status,
    a.reason,
    at.code
"""


def _row_to_absence(row: tuple[Any, ...]) -> Absence:
    db_id, employee_id, type_id, start_date, end_date, status, reason, code = row

    return AbsenceRepository.build_absence(
        employee_id=employee_id,
        type_id=type_id,
        start_date=start_date,
        end_date=end_date,
        reason=reason,
        code=code,
        status=AbsenceStatus(status),
        id=db_id,
    )


class AbsenceRepository:
    def __init__(self, conn: psycopg2.extensions.connection) -> None:
        self._conn = conn

    @staticmethod
    def build_absence(
        employee_id: int,
        type_id: int,
        start_date: datetime,
        end_date: datetime,
        reason: str,
        code: str,
        status: AbsenceStatus = AbsenceStatus.PENDING,
        id: int | None = None,
    ) -> Absence:
        kwargs: dict[str, Any] = dict(
            employee_id=employee_id,
            type_id=type_id,
            start_date=start_date,
            end_date=end_date,
            reason=reason,
            status=status,
            id=id,
        )

        if code == "sick":
            return SickLeave(**kwargs)
        if code == "paid":
            return PaidLeave(**kwargs)
        return UnpaidLeave(**kwargs)

    def find_all(self) -> list[Absence]:
        with self._conn.cursor() as cur:
            query = (
                f"SELECT {_SELECT_COLUMNS}"
                f" FROM absence a"
                f" JOIN absence_type at ON a.type_id = at.id"
                f" ORDER BY a.start_date"
            )
            cur.execute(query)
            rows = cur.fetchall()
        return [_row_to_absence(r) for r in rows]

    def find_by_id(self, absence_id: int) -> Absence | None:
        with self._conn.cursor() as cur:
            query = (
                f"SELECT {_SELECT_COLUMNS}"
                f" FROM absence a"
                f" JOIN absence_type at ON a.type_id = at.id"
                f" WHERE a.id = %s"
            )
            cur.execute(query, (absence_id,))
            row = cur.fetchone()
            if not row:
                return None
            return _row_to_absence(row)

    def find_by_employee_id(self, employee_id: int) -> list[Absence]:
        with self._conn.cursor() as cur:
            query = (
                f"SELECT {_SELECT_COLUMNS}"
                f" FROM absence a"
                f" JOIN absence_type at ON a.type_id = at.id"
                f" WHERE a.employee_id = %s"
                f" ORDER BY a.start_date"
            )
            cur.execute(query, (employee_id,))
            rows = cur.fetchall()
        return [_row_to_absence(r) for r in rows]

    def find_by_employee_and_status(
        self, employee_id: int, status: AbsenceStatus
    ) -> list[Absence]:
        with self._conn.cursor() as cur:
            query = (
                f"SELECT {_SELECT_COLUMNS}"
                f" FROM absence a"
                f" JOIN absence_type at ON a.type_id = at.id"
                f" WHERE a.employee_id = %s"
                f" AND a.status = %s"
                f" ORDER BY a.start_date"
            )
            cur.execute(
                query,
                (
                    employee_id,
                    status.value,
                ),
            )
            rows = cur.fetchall()
        return [_row_to_absence(r) for r in rows]

    def insert(self, absence: Absence) -> Absence:
        with self._conn.cursor() as cur:
            try:
                cur.execute(
                    "INSERT INTO absence (employee_id, type_id, start_date, end_date, status, reason) "
                    "VALUES (%s, %s, %s, %s, %s, %s) RETURNING id",
                    (
                        absence.employee_id,
                        absence.type_id,
                        absence.start_date,
                        absence.end_date,
                        absence.status.value,
                        absence.reason,
                    ),
                )
                row = cur.fetchone()
                if row is None:
                    raise RuntimeError("INSERT returned no id")
                self._conn.commit()
                absence.id = row[0]
            except Exception as e:
                self._conn.rollback()
                print("Exception:", e)
                raise
        return absence

    def update_status(self, absence_id: int, status: AbsenceStatus) -> None:
        with self._conn.cursor() as cur:
            try:
                cur.execute(
                    "UPDATE absence SET status = %s WHERE id = %s",
                    (status.value, absence_id),
                )
                if cur.rowcount == 0:
                    raise KeyError(f"No absence with id={absence_id}")
                self._conn.commit()
            except Exception as e:
                self._conn.rollback()
                print("Exception:", e)
                raise

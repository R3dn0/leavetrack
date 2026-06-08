from typing import Any

import psycopg2.extensions

from models.absence_type import AbsenceType

_SELECT_COLUMNS = """
    id,
    label,
    code,
    max_days_per_year,
    is_paid
"""


def _row_to_absence_type(row: tuple[Any, ...]) -> AbsenceType:
    db_id, label, code, max_days_per_year, is_paid = row
    return AbsenceType(
        label=label,
        code=code,
        max_days_per_year=max_days_per_year,
        is_paid=is_paid,
        id=db_id,
    )


class AbsenceTypeRepository:
    def __init__(self, conn: psycopg2.extensions.connection) -> None:
        self._conn = conn

    def find_all(self) -> list[AbsenceType]:
        with self._conn.cursor() as cur:
            query = f"SELECT {_SELECT_COLUMNS}" f" FROM absence_type" f" ORDER BY label"
            cur.execute(query)
            rows = cur.fetchall()

        return [_row_to_absence_type(r) for r in rows]

    def find_by_id(self, type_id: int) -> AbsenceType | None:
        with self._conn.cursor() as cur:
            query = f"SELECT {_SELECT_COLUMNS}" f" FROM absence_type" f" WHERE id = %s"
            cur.execute(query, (type_id,))
            row = cur.fetchone()

            if not row:
                return None

            return _row_to_absence_type(row)

    def insert(self, absence_type: AbsenceType) -> AbsenceType:
        with self._conn.cursor() as cur:
            try:
                cur.execute(
                    "INSERT INTO absence_type (label, code, max_days_per_year, is_paid) "
                    "VALUES (%s, %s, %s, %s) RETURNING id",
                    (
                        absence_type.label,
                        absence_type.code,
                        absence_type.max_days_per_year,
                        absence_type.is_paid,
                    ),
                )
                row = cur.fetchone()

                if row is None:
                    raise RuntimeError("INSERT returned no id")

                self._conn.commit()
                absence_type.id = row[0]

            except Exception as e:
                self._conn.rollback()
                print("Exception:", e)
                raise

        return absence_type

    def update(self, absence_type: AbsenceType) -> None:
        with self._conn.cursor() as cur:
            try:
                cur.execute(
                    "UPDATE absence_type SET label = %s, code = %s, max_days_per_year = %s, is_paid = %s "
                    "WHERE id = %s",
                    (
                        absence_type.label,
                        absence_type.code,
                        absence_type.max_days_per_year,
                        absence_type.is_paid,
                        absence_type.id,
                    ),
                )
                if cur.rowcount == 0:
                    raise KeyError(f"No absence_type with id={absence_type.id}")

                self._conn.commit()

            except Exception as e:
                self._conn.rollback()
                print("Exception:", e)
                raise

    def delete(self, type_id: int) -> None:
        with self._conn.cursor() as cur:
            try:
                cur.execute(
                    "DELETE FROM absence_type WHERE id = %s",
                    (type_id,),
                )
                if cur.rowcount == 0:
                    raise KeyError(f"No absence_type with id={type_id}")

                self._conn.commit()

            except Exception as e:
                self._conn.rollback()
                print("Exception:", e)
                raise

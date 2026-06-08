from typing import Any

import psycopg2.extensions


from models.department import Department

_SELECT_COLUMNS = """
    id,
    name
"""


def _row_to_department(row: tuple[Any, ...]) -> Department:
    (
        db_id,
        name,
    ) = row

    kwargs: dict[str, Any] = dict(name=name, id=db_id)

    return Department(**kwargs)


class DepartmentRepository:
    def __init__(self, conn: psycopg2.extensions.connection) -> None:
        self._conn = conn

    def find_all(self) -> list[Department]:
        with self._conn.cursor() as cur:
            query = f"SELECT {_SELECT_COLUMNS} FROM department ORDER BY name"
            cur.execute(query)
            rows = cur.fetchall()

        return [_row_to_department(r) for r in rows]

    def find_by_id(self, department_id: int) -> Department | None:
        with self._conn.cursor() as cur:
            query = f"SELECT {_SELECT_COLUMNS} FROM department WHERE id = %s"
            cur.execute(query, (department_id,))
            row = cur.fetchone()

            if not row:
                return None

        return _row_to_department(row)

    def insert(self, department: Department) -> Department:
        with self._conn.cursor() as cur:
            try:
                cur.execute(
                    "INSERT INTO department (name) VALUES (%s) RETURNING id",
                    (department.name,),
                )
                row = cur.fetchone()
                if row is None:
                    raise RuntimeError("INSERT returned no id")
                department.id = row[0]
                self._conn.commit()

            except Exception as e:
                self._conn.rollback()
                print("Exception:", e)
                raise

        return department

    def update(self, department: Department) -> Department:
        with self._conn.cursor() as cur:
            try:
                cur.execute(
                    "UPDATE department SET name=%s WHERE id=%s",
                    (
                        department.name,
                        department.id,
                    ),
                )
                if cur.rowcount == 0:
                    raise KeyError(f"No department with id={department.id}")
                self._conn.commit()

            except Exception as e:
                self._conn.rollback()
                print("Exception:", e)
                raise

        return department

    def delete(self, department_id: int) -> None:
        with self._conn.cursor() as cur:
            try:
                cur.execute(
                    "DELETE FROM department WHERE id = %s",
                    (department_id,),
                )
                if cur.rowcount == 0:
                    raise KeyError(f"No department with id={department_id}")
                self._conn.commit()

            except Exception as e:
                self._conn.rollback()
                print("Exception:", e)
                raise

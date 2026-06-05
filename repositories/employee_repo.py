from typing import Any

import psycopg2.extensions

from models.employee import Employee

_SELECT_COLUMNS = """
    employee.id,
    employee.first_name,
    employee.last_name,
    employee.email,
    employee.department_id,
    employee.manager_id,
    employee.hire_date,
    employee.is_active
"""


def _row_to_employee(row: tuple[Any, ...]) -> Employee:
    (
        db_id,
        first_name,
        last_name,
        email,
        department_id,
        manager_id,
        hire_date,
        is_active,
    ) = row

    kwargs: dict[str, Any] = dict(
        first_name=first_name,
        last_name=last_name,
        email=email,
        department_id=department_id,
        manager_id=manager_id,
        hire_date=hire_date,
        id=db_id,
        is_active=is_active,
    )

    return Employee(**kwargs)


class EmployeeRepository:
    def __init__(self, conn: psycopg2.extensions.connection) -> None:
        self._conn = conn

    def find_all(self, active_only: bool = True) -> list[Employee]:
        with self._conn.cursor() as cur:
            query = f"SELECT {_SELECT_COLUMNS} FROM employee"
            if active_only:
                query += f" WHERE is_active = True"
            query += f" ORDER BY employee.last_name"

            cur.execute(query)
            rows = cur.fetchall()
        return [_row_to_employee(r) for r in rows]

    def find_by_id(self, employee_id: int) -> Employee | None:
        with self._conn.cursor() as cur:
            query = f"SELECT {_SELECT_COLUMNS} FROM employee WHERE id = %s"
            cur.execute(query, (employee_id,))
            row = cur.fetchone()

            if not row:
                return None

            return _row_to_employee(row)

    def insert(self, employee: Employee) -> Employee:
        with self._conn.cursor() as cur:
            try:
                cur.execute(
                    f"INSERT INTO employee "
                    f"(first_name, last_name, email, department_id, manager_id, hire_date, is_active) "
                    f"VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id",
                    (
                        employee.first_name,
                        employee.last_name,
                        employee.email,
                        employee.department_id,
                        employee.manager_id,
                        employee.hire_date,
                        employee.is_active,
                    ),
                )
                row = cur.fetchone()
                if row is None:
                    raise RuntimeError("INSERT returned no id")
                employee.id = row[0]
                self._conn.commit()

            except Exception as e:
                self._conn.rollback()
                print("Exception:", e)
                raise

        return employee

    def update(self, employee: Employee) -> Employee:
        with self._conn.cursor() as cur:
            try:
                cur.execute(
                    "UPDATE employee SET first_name = %s, last_name = %s, email = %s, department_id = %s, manager_id = %s, hire_date = %s, is_active = %s WHERE id=%s",
                    (
                        employee.first_name,
                        employee.last_name,
                        employee.email,
                        employee.department_id,
                        employee.manager_id,
                        employee.hire_date,
                        employee.is_active,
                        employee.id,
                    ),
                )
                if cur.rowcount == 0:
                    raise KeyError(f"No employee with id={employee.id}")
                self._conn.commit()

            except Exception as e:
                self._conn.rollback()
                print("Exception:", e)
                raise

        return employee

    def deactivate(self, employee_id: int) -> None:
        with self._conn.cursor() as cur:
            try:
                cur.execute(
                    "UPDATE employee SET is_active = False WHERE id = %s",
                    (employee_id,),
                )
                if cur.rowcount == 0:
                    raise KeyError(f"No employee with id={employee_id}")
                self._conn.commit()

            except Exception as e:
                self._conn.rollback()
                print("Exception:", e)
                raise

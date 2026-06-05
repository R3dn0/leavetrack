from repositories.absence_repo import AbsenceRepository
from repositories.employee_repo import EmployeeRepository
from repositories.leave_balance_repo import LeaveBalanceRepository
from models.enums import AbsenceStatus

from datetime import datetime


class AbsenceService:
    def __init__(
        self,
        absence_repo: AbsenceRepository,
        employee_repo: EmployeeRepository,
        leave_balance_repo: LeaveBalanceRepository,
    ) -> None:
        self._absence = absence_repo
        self._employee = employee_repo
        self._leave_balance = leave_balance_repo

    def _get_approved_dates(self, employee_id: int) -> set:
        absences = self._absence.find_by_employee_and_status(
            employee_id, AbsenceStatus.APPROVED
        )
        dates: set = set()
        for a in absences:
            dates.update(a.date_range())
        return dates

    def _has_overlap(
        self,
        employee_id: int,
        start_date: datetime,
        end_date: datetime,
        exclude_absence_id: int | None = None,
    ) -> bool:
        # Exclude ID in case of an update of absence => not trigger on herself
        absences = self._absence.find_by_employee_id(employee_id)

        for a in absences:
            if exclude_absence_id is not None and a.id == exclude_absence_id:
                continue
            if a.start_date is None or a.end_date is None:
                continue
            if a.start_date <= end_date and a.end_date >= start_date:
                return True
        return False

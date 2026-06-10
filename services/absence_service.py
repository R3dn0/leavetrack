from repositories.absence_repo import AbsenceRepository, build_absence
from repositories.absence_type_repo import AbsenceTypeRepository
from repositories.employee_repo import EmployeeRepository
from repositories.leave_balance_repo import LeaveBalanceRepository
from models import Absence, AbsenceStatus
from datetime import datetime


class AbsenceService:
    def __init__(
        self,
        absence_repo: AbsenceRepository,
        absence_type_repo: AbsenceTypeRepository,
        employee_repo: EmployeeRepository,
        leave_balance_repo: LeaveBalanceRepository,
    ) -> None:
        self._absence = absence_repo
        self._absence_type = absence_type_repo
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
        absence: Absence,
    ) -> bool:
        approved_dates = self._get_approved_dates(employee_id)
        new_dates = set(absence.date_range())
        return bool(approved_dates & new_dates)

    def submit_absence(
        self,
        employee_id: int,
        type_id: int,
        start_date: datetime,
        end_date: datetime,
        reason: str,
    ) -> Absence:
        if employee_id is None:
            raise ValueError("Employee_id can't be None !")
        if type_id is None:
            raise ValueError("Type_id can't be None !")
        if start_date is None:
            raise ValueError("Start_date can't be None !")
        if end_date is None:
            raise ValueError("End_date can't be None !")
        if start_date > end_date:
            raise ValueError("Start date must be before end date")

        employee = self._employee.find_by_id(employee_id)
        if employee is None:
            raise ValueError(f"Employee with id={employee_id} not found")

        absence_type = self._absence_type.find_by_id(type_id)
        if absence_type is None:
            raise ValueError(f"Absence type with id={type_id} not found")

        absence = build_absence(
            employee_id=employee_id,
            type_id=type_id,
            start_date=start_date,
            end_date=end_date,
            reason=reason,
            code=absence_type.code,
        )

        if self._has_overlap(employee_id, absence):
            raise ValueError("Overlap with an approved absence")

        balance = self._leave_balance.find_by_employee_and_year(
            employee_id, start_date.year
        )
        type_balance = next((b for b in balance if b.type_id == type_id), None)
        if type_balance is not None and not type_balance.can_approve(absence.duration):
            raise ValueError(
                f"Insufficient balance: {absence.duration} days requested, "
                f"{type_balance.remaining} remaining"
            )

        absence = self._absence.insert(absence)

        return absence

    def approve_absence(self, absence_id: int) -> Absence:
        absence = self._get_pending_absence(absence_id)

        if absence.start_date is None:
            raise ValueError("Absence has no start date")
        if absence.employee_id is None:
            raise ValueError("Absence has no employee id")

        if self._has_overlap(absence.employee_id, absence):
            raise ValueError("Overlap with an approved absence")

        balance = self._leave_balance.find_by_employee_and_year(
            absence.employee_id, absence.start_date.year
        )
        type_balance = next((b for b in balance if b.type_id == absence.type_id), None)
        if type_balance is not None and not type_balance.can_approve(absence.duration):
            raise ValueError(
                f"Insufficient balance: {absence.duration} days requested, "
                f"{type_balance.remaining} remaining"
            )

        self._absence.update_status(absence_id, AbsenceStatus.APPROVED)
        absence.status = AbsenceStatus.APPROVED

        if type_balance is not None:
            type_balance.used_days += absence.duration
            self._leave_balance.update(type_balance)

        return absence

    def reject_absence(self, absence_id: int) -> Absence:
        absence = self._get_pending_absence(absence_id)
        self._absence.update_status(absence_id, AbsenceStatus.REJECTED)
        absence.status = AbsenceStatus.REJECTED
        return absence

    def _get_pending_absence(self, absence_id: int) -> Absence:
        absence = self._absence.find_by_id(absence_id)
        if absence is None:
            raise ValueError(f"Absence with id={absence_id} not found")
        if absence.status != AbsenceStatus.PENDING:
            raise ValueError(f"Absence {absence_id} is not PENDING")
        return absence

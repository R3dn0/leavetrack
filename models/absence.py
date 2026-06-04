from abc import ABC, abstractmethod
from datetime import datetime, timedelta

from models.enums import AbsenceStatus


class Absence(ABC):
    def __init__(
        self,
        employee_id: int,
        type_id: int,
        start_date: datetime,
        end_date: datetime,
        reason: str,
        status: AbsenceStatus = AbsenceStatus.PENDING,
        id: int | None = None,
    ):
        self._id = id
        self._employee_id = employee_id
        self._type_id = type_id
        self._start_date = start_date
        self._end_date = end_date
        self._status = status
        self._reason = reason

    def __repr__(self) -> str:
        return (
            f"Absence(id={self._id}, employee_id={self._employee_id}, "
            f"type_id={self._type_id}, start_date={self._start_date}, "
            f"end_date={self._end_date}, status={self._status}, "
            f"reason={self._reason!r})"
        )

    @property
    def id(self) -> int | None:
        return self._id

    @property
    def employee_id(self) -> int | None:
        return self._employee_id

    @property
    def type_id(self) -> int | None:
        return self._type_id

    @type_id.setter
    def type_id(self, type_id: int) -> None:
        self._type_id = type_id

    @property
    def start_date(self) -> datetime | None:
        return self._start_date

    @start_date.setter
    def start_date(self, start_date: datetime | None) -> None:
        if (
            start_date is not None
            and self._end_date is not None
            and start_date > self._end_date
        ):
            raise ValueError("Start date must be before end date")
        self._start_date = start_date

    @property
    def end_date(self) -> datetime | None:
        return self._end_date

    @end_date.setter
    def end_date(self, end_date: datetime | None) -> None:
        if (
            end_date is not None
            and self._start_date is not None
            and end_date < self._start_date
        ):
            raise ValueError("Start date must be before end date")
        self._end_date = end_date

    @property
    def status(self) -> AbsenceStatus:
        return self._status

    @status.setter
    def status(self, status: AbsenceStatus) -> None:
        self._status = status

    @property
    def reason(self) -> str | None:
        return self._reason

    @reason.setter
    def reason(self, reason: str) -> None:
        self._reason = reason

    def date_range(self):
        absence_days = []

        if self.start_date is not None and self.end_date is not None:
            cursor = self.start_date.date()
            end = self.end_date.date()
            while cursor <= end:
                absence_days.append(cursor)
                cursor = cursor + timedelta(days=1)

        return absence_days

    @property
    def duration(self) -> int:
        return len(self.date_range())

    @property
    @abstractmethod
    def deducts_from_balance(self) -> bool: ...


class PaidLeave(Absence):
    @property
    def deducts_from_balance(self) -> bool:
        return True


class SickLeave(Absence):
    def __init__(
        self,
        employee_id: int,
        type_id: int,
        start_date: datetime,
        end_date: datetime,
        reason: str,
        status: AbsenceStatus = AbsenceStatus.PENDING,
        id: int | None = None,
        medical_certificate: bool = False,
    ):
        super().__init__(employee_id, type_id, start_date, end_date, reason, status, id)
        self._medical_certificate = medical_certificate

    @property
    def deducts_from_balance(self) -> bool:
        return False

    @property
    def medical_certificate(self) -> bool:
        return self._medical_certificate


class UnpaidLeave(Absence):
    @property
    def deducts_from_balance(self) -> bool:
        return False

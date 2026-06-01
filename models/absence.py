from datetime import datetime, timedelta

from models.enums import AbsenceStatus


class Absence:
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
        if start_date <= self._end_date:
            self._start_date = start_date
        else:
            raise ValueError("Start date must be greater than end date")

    @property
    def end_date(self) -> datetime | None:
        return self._end_date

    @end_date.setter
    def end_date(self, end_date: datetime | None) -> None:
        if end_date >= self._start_date:
            self._end_date = end_date
        else:
            raise ValueError("Start date must be greater than end date")

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

        cursor = self.start_date.date()
        end = self.end_date.date()
        while cursor <= end:
            absence_days.append(cursor)
            cursor = cursor + timedelta(days=1)

        return absence_days

    @property
    def duration(self) -> int:
        return len(self.date_range())

from dataclasses import dataclass, field


@dataclass
class LeaveBalance:
    employee_id: int
    type_id: int
    year: int
    total_days: int | None = None
    used_days: int = 0
    id: int | None = field(default=None)

    @property
    def remaining(self) -> int | None:
        if self.total_days is None:
            return None
        if (self.total_days - self.used_days) < 0:
            raise ValueError("Remaining days cannot be lower than 0 !")
        return self.total_days - self.used_days

    def can_approve(self, requested_days: int) -> bool:
        if self.remaining is None:
            return True
        return self.remaining >= requested_days

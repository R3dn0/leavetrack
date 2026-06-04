from dataclasses import dataclass, field


@dataclass
class LeaveBalance:
    employee_id: int
    type_id: int
    year: int
    total_days: int
    used_days: int = 0
    id: int | None = field(default=None)

    @property
    def remaining(self) -> int:
        return self.total_days - self.used_days

    def can_approve(self, requested_days: int) -> bool:
        return self.remaining >= requested_days

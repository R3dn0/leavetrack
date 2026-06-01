from dataclasses import dataclass, field


@dataclass
class AbsenceType:
    label: str
    max_days_per_year: int
    is_paid: bool = field(default=False)
    id: int | None = field(default=None)

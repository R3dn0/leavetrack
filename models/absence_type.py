from dataclasses import dataclass, field


@dataclass
class AbsenceType:
    label: str
    code: str
    max_days_per_year: int | None
    is_paid: bool = field(default=False)
    id: int | None = field(default=None)

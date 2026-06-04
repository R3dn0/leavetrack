from dataclasses import dataclass, field


@dataclass
class Department:
    name: str
    id: int | None = field(default=None)

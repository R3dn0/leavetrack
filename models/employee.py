from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Employee:
    first_name: str
    last_name: str
    email: str
    department: int
    manager: int
    hire_date: datetime
    id: int | None = field(default=None)
    is_active: bool = field(default=True)


    def __str__(self):
        return (f"{self.first_name} {self.last_name} ({self.email}), "
                f"in department {self.department} under employee {self.manager}). "
                f"Hired {self.hire_date}, still working {self.is_active}")

    def __repr__(self):
        return f"{self.__class__.__name__}({self.id}: {self.first_name}, {self.last_name})"

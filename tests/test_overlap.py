import unittest
from datetime import datetime
from unittest.mock import MagicMock

from models.absence import PaidLeave
from models.enums import AbsenceStatus


class TestHasOverlap(unittest.TestCase):
    def setUp(self):
        self.absence_repo = MagicMock()
        self.absence_type_repo = MagicMock()
        self.employee_repo = MagicMock()
        self.leave_balance_repo = MagicMock()

        from services.absence_service import AbsenceService

        self.service = AbsenceService(
            self.absence_repo,
            self.absence_type_repo,
            self.employee_repo,
            self.leave_balance_repo,
        )

    def _make_approved(self, start: datetime, end: datetime) -> PaidLeave:
        return PaidLeave(
            1, 1, start, end, "approved", status=AbsenceStatus.APPROVED, id=99
        )

    def test_no_existing_absences(self):
        self.absence_repo.find_by_employee_and_status.return_value = []
        absence = PaidLeave(1, 1, datetime(2024, 6, 1), datetime(2024, 6, 5), "new")
        self.assertFalse(self.service._has_overlap(1, absence))

    def test_no_overlap_different_dates(self):
        existing = self._make_approved(datetime(2024, 5, 1), datetime(2024, 5, 5))
        self.absence_repo.find_by_employee_and_status.return_value = [existing]
        absence = PaidLeave(1, 1, datetime(2024, 6, 1), datetime(2024, 6, 5), "new")
        self.assertFalse(self.service._has_overlap(1, absence))

    def test_no_overlap_adjacent_dates(self):
        existing = self._make_approved(datetime(2024, 6, 1), datetime(2024, 6, 5))
        self.absence_repo.find_by_employee_and_status.return_value = [existing]

        absence = PaidLeave(1, 1, datetime(2024, 6, 6), datetime(2024, 6, 10), "new")
        self.assertFalse(self.service._has_overlap(1, absence))

    def test_overlap_start_date(self):
        existing = self._make_approved(datetime(2024, 6, 3), datetime(2024, 6, 7))
        self.absence_repo.find_by_employee_and_status.return_value = [existing]
        absence = PaidLeave(1, 1, datetime(2024, 6, 1), datetime(2024, 6, 5), "new")
        self.assertTrue(self.service._has_overlap(1, absence))

    def test_overlap_end_date(self):
        existing = self._make_approved(datetime(2024, 6, 1), datetime(2024, 6, 5))
        self.absence_repo.find_by_employee_and_status.return_value = [existing]
        absence = PaidLeave(1, 1, datetime(2024, 6, 5), datetime(2024, 6, 10), "new")
        self.assertTrue(self.service._has_overlap(1, absence))

    def test_overlap_fully_inside(self):
        existing = self._make_approved(datetime(2024, 6, 1), datetime(2024, 6, 10))
        self.absence_repo.find_by_employee_and_status.return_value = [existing]
        absence = PaidLeave(1, 1, datetime(2024, 6, 3), datetime(2024, 6, 7), "new")
        self.assertTrue(self.service._has_overlap(1, absence))

    def test_overlap_new_contains_existing(self):
        existing = self._make_approved(datetime(2024, 6, 3), datetime(2024, 6, 7))
        self.absence_repo.find_by_employee_and_status.return_value = [existing]
        absence = PaidLeave(1, 1, datetime(2024, 6, 1), datetime(2024, 6, 10), "new")
        self.assertTrue(self.service._has_overlap(1, absence))

    def test_overlap_exact_same_dates(self):
        existing = self._make_approved(datetime(2024, 6, 1), datetime(2024, 6, 5))
        self.absence_repo.find_by_employee_and_status.return_value = [existing]
        absence = PaidLeave(1, 1, datetime(2024, 6, 1), datetime(2024, 6, 5), "new")
        self.assertTrue(self.service._has_overlap(1, absence))

    def test_overlap_multiple_approved_one_matches(self):
        existing_1 = self._make_approved(datetime(2024, 5, 1), datetime(2024, 5, 5))
        existing_2 = self._make_approved(datetime(2024, 6, 3), datetime(2024, 6, 7))
        existing_3 = self._make_approved(datetime(2024, 7, 1), datetime(2024, 7, 5))
        self.absence_repo.find_by_employee_and_status.return_value = [
            existing_1,
            existing_2,
            existing_3,
        ]
        absence = PaidLeave(1, 1, datetime(2024, 6, 1), datetime(2024, 6, 5), "new")
        self.assertTrue(self.service._has_overlap(1, absence))

    def test_no_overlap_none_dates_in_new_absence(self):
        self.absence_repo.find_by_employee_and_status.return_value = []
        absence = PaidLeave(1, 1, None, None, "new")  # type: ignore
        self.assertFalse(self.service._has_overlap(1, absence))

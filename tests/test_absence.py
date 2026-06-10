import unittest
from datetime import datetime
from unittest.mock import MagicMock

from models.absence import PaidLeave, SickLeave, UnpaidLeave
from models.enums import AbsenceStatus


class TestPaidLeave(unittest.TestCase):
    def setUp(self):
        self.start = datetime(2024, 6, 1)
        self.end = datetime(2024, 6, 5)
        self.leave = PaidLeave(
            employee_id=1,
            type_id=2,
            start_date=self.start,
            end_date=self.end,
            reason="Vacation",
        )

    def test_is_instance_of_absence(self):
        from models.absence import Absence

        self.assertIsInstance(self.leave, Absence)

    def test_deducts_from_balance_true(self):
        self.assertTrue(self.leave.deducts_from_balance)

    def test_inherits_date_range(self):
        expected = [
            datetime(2024, 6, 1).date(),
            datetime(2024, 6, 2).date(),
            datetime(2024, 6, 3).date(),
            datetime(2024, 6, 4).date(),
            datetime(2024, 6, 5).date(),
        ]
        self.assertEqual(self.leave.date_range(), expected)

    def test_inherits_duration(self):
        self.assertEqual(self.leave.duration, 5)

    def test_attributes(self):
        self.assertEqual(self.leave.employee_id, 1)
        self.assertEqual(self.leave.type_id, 2)
        self.assertEqual(self.leave.start_date, self.start)
        self.assertEqual(self.leave.end_date, self.end)
        self.assertEqual(self.leave.reason, "Vacation")
        self.assertEqual(self.leave.status, AbsenceStatus.PENDING)
        self.assertIsNone(self.leave.id)


class TestDateRange(unittest.TestCase):
    def test_single_day(self):
        d = datetime(2024, 6, 15)
        leave = PaidLeave(1, 1, d, d, "test")
        self.assertEqual(leave.date_range(), [d.date()])

    def test_multiple_days(self):
        start = datetime(2024, 1, 1)
        end = datetime(2024, 1, 10)
        leave = PaidLeave(1, 1, start, end, "test")
        result = leave.date_range()
        self.assertEqual(len(result), 10)
        self.assertEqual(result[0], start.date())
        self.assertEqual(result[-1], end.date())

    def test_across_month_boundary(self):
        start = datetime(2024, 1, 30)
        end = datetime(2024, 2, 2)
        leave = PaidLeave(1, 1, start, end, "test")
        result = leave.date_range()
        self.assertEqual(len(result), 4)
        self.assertEqual(
            result,
            [
                datetime(2024, 1, 30).date(),
                datetime(2024, 1, 31).date(),
                datetime(2024, 2, 1).date(),
                datetime(2024, 2, 2).date(),
            ],
        )

    def test_across_year_boundary(self):
        start = datetime(2024, 12, 30)
        end = datetime(2025, 1, 2)
        leave = PaidLeave(1, 1, start, end, "test")
        result = leave.date_range()
        self.assertEqual(len(result), 4)
        self.assertEqual(
            result,
            [
                datetime(2024, 12, 30).date(),
                datetime(2024, 12, 31).date(),
                datetime(2025, 1, 1).date(),
                datetime(2025, 1, 2).date(),
            ],
        )

    def test_leap_year_february(self):
        start = datetime(2024, 2, 28)
        end = datetime(2024, 3, 1)
        leave = PaidLeave(1, 1, start, end, "test")
        result = leave.date_range()
        self.assertEqual(len(result), 3)
        self.assertEqual(
            result,
            [
                datetime(2024, 2, 28).date(),
                datetime(2024, 2, 29).date(),
                datetime(2024, 3, 1).date(),
            ],
        )

    def test_both_dates_none(self):
        leave = PaidLeave(1, 1, None, None, "test")  # type: ignore
        self.assertEqual(leave.date_range(), [])

    def test_start_date_none(self):
        leave = SickLeave(1, 1, None, datetime(2024, 6, 1), "test")  # type: ignore
        self.assertEqual(leave.date_range(), [])

    def test_end_date_none(self):
        leave = UnpaidLeave(1, 1, datetime(2024, 6, 1), None, "test")  # type: ignore
        self.assertEqual(leave.date_range(), [])

    def test_both_dates_set(self):
        start = datetime(2024, 12, 25)
        end = datetime(2024, 12, 25)
        leave = SickLeave(1, 1, start, end, "sick", medical_certificate=True)
        self.assertEqual(leave.date_range(), [start.date()])


if __name__ == "__main__":
    unittest.main()

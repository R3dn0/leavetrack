import unittest

from models.leave_balance import LeaveBalance


class TestRemaining(unittest.TestCase):
    def setUp(self):
        self.lb = LeaveBalance(employee_id=1, type_id=1, year=2024)

    def test_remaining_none_when_total_days_is_none_and_no_used(self):
        self.lb.total_days = None
        self.lb.used_days = 0
        self.assertIsNone(self.lb.remaining)

    def test_remaining_none_when_total_days_is_none_and_used_days_nonzero(self):
        self.lb.total_days = None
        self.lb.used_days = 10
        self.assertIsNone(self.lb.remaining)

    def test_remaining_when_total_days_nonzero_and_no_used(self):
        self.lb.total_days = 10
        self.lb.used_days = 0
        self.assertEqual(self.lb.remaining, 10)

    def test_remaining_when_total_days_nonzero_and_used_days_smaller(self):
        self.lb.total_days = 10
        self.lb.used_days = 3
        self.assertEqual(self.lb.remaining, 7)

    def test_remaining_when_total_days_nonzero_and_used_days_equals(self):
        self.lb.total_days = 10
        self.lb.used_days = 10
        self.assertEqual(self.lb.remaining, 0)

    def test_remaining_when_total_days_nonzero_and_used_days_greater(self):
        self.lb.total_days = 10
        self.lb.used_days = 12
        with self.assertRaises(ValueError):
            self.lb.remaining


class TestLeaveBalanceCanApprove(unittest.TestCase):
    def setUp(self):
        self.lb = LeaveBalance(employee_id=1, type_id=1, year=2024)

    def test_can_approve_when_remaining_none(self):
        self.lb.total_days = None
        self.lb.used_days = 0
        self.assertTrue(self.lb.can_approve(5))

    def test_can_approve_when_remaining_greater_than_requested(self):
        self.lb.total_days = 10
        self.lb.used_days = 0
        self.assertTrue(self.lb.can_approve(3))

    def test_can_approve_when_remaining_equals_requested(self):
        self.lb.total_days = 10
        self.lb.used_days = 0
        self.assertTrue(self.lb.can_approve(10))

    def test_can_approve_when_remaining_smaller_than_requested(self):
        self.lb.total_days = 10
        self.lb.used_days = 0
        self.assertFalse(self.lb.can_approve(12))

    def test_can_approve_when_requested_is_zero(self):
        self.lb.total_days = 0
        self.lb.used_days = 0
        self.assertTrue(self.lb.can_approve(0))

    def test_can_approve_when_remaining_is_zero_and_requested_nonzero(self):
        self.lb.total_days = 0
        self.lb.used_days = 0
        self.assertFalse(self.lb.can_approve(1))


if __name__ == "__main__":
    unittest.main()

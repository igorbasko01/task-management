import unittest

from task_cli.task_priority import TaskPriority


class TaskPriorityTests(unittest.TestCase):
    def test_priority_from_numeric_value_0(self):
        priority = TaskPriority.from_numeric_value(0)
        self.assertEqual(priority.name, "High")

    def test_priority_from_numeric_value_1(self):
        priority = TaskPriority.from_numeric_value(1)
        self.assertEqual(priority.name, "Medium")

    def test_priority_from_numeric_value_2(self):
        priority = TaskPriority.from_numeric_value(2)
        self.assertEqual(priority.name, "Low")

    def test_priority_from_numeric_value_invalid_raises_exception(self):
        with self.assertRaises(ValueError):
            TaskPriority.from_numeric_value(3)
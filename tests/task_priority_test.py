import unittest

from task_cli.task_priority import TaskPriority


class TaskPriorityTests(unittest.TestCase):
    def test_priority_from_numeric_value(self):
        test_cases = {
            0: "High",
            1: "Medium",
            2: "Low"
        }

        for value, expected_name in test_cases.items():
            with self.subTest(value=value):
                priority = TaskPriority.from_numeric_value(value)
                self.assertEqual(priority.name, expected_name)
                self.assertEqual(priority.numeric_value, value)
        
        with self.subTest(name="Invalid Numeric Priority"):
            with self.assertRaises(ValueError):
                TaskPriority.from_numeric_value(3)

    def test_priority_from_name(self):
        test_cases = {
            "High": 0,
            "Medium": 1,
            "Low": 2
        }

        for name, expected_value in test_cases.items():
            with self.subTest(name=name):
                priority = TaskPriority.from_name(name)
                self.assertEqual(priority.numeric_value, expected_value)
        
        with self.subTest(name="Invalid Priority"):
            with self.assertRaises(ValueError):
                TaskPriority.from_name("Invalid Priority")
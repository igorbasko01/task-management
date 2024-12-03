import tempfile
import unittest

from task_cli.task_manager import TaskManager


class TaskManagerTests(unittest.TestCase):
    def test_init_workspace_if_doesnt_exist(self):
        with tempfile.TemporaryDirectory() as tmp:
            task_manager = TaskManager(tmp)
            task_manager.init_workspace()
            self.assertTrue(task_manager.workspace.exists())
            self.assertTrue(task_manager.tasks_dir.exists())
            self.assertTrue(task_manager.task_counter_file.exists())

    def test_init_workspace_should_initialize_counter_with_zero(self):
        with tempfile.TemporaryDirectory() as tmp:
            task_manager = TaskManager(tmp)
            task_manager.init_workspace()
            with task_manager.task_counter_file.open("r") as f:
                counter = f.read()
                self.assertEqual(counter, "0")

    def test_create_task_should_increment_counter(self):
        with tempfile.TemporaryDirectory() as tmp:
            task_manager = TaskManager(tmp)
            task_manager.init_workspace()
            task_manager.create_task("Test Task", "Feature", "Test User")
            with task_manager.task_counter_file.open("r") as f:
                counter = f.read()
                self.assertEqual(counter, "1")

    def test_create_task_should_create_task_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            task_manager = TaskManager(tmp)
            task_manager.init_workspace()
            task_manager.create_task("Test Task", "Feature", "Test User")
            task_file = task_manager.tasks_dir / "TASK-1.md"
            self.assertTrue(task_file.exists())
    
    def test_move_task_should_change_board(self):
        with tempfile.TemporaryDirectory() as tmp:
            task_manager = TaskManager(tmp)
            task_manager.init_workspace()
            task_manager.create_task("Test Task", "Feature", "Test User")
            task_manager.move_task(1, "In Progress")
            task_file = task_manager.tasks_dir / "TASK-1.md"
            with task_file.open() as f:
                content = f.read()
                self.assertIn("board: In Progress", content)

    def test_move_task_should_not_change_other_fields(self):
        with tempfile.TemporaryDirectory() as tmp:
            task_manager = TaskManager(tmp)
            task_manager.init_workspace()
            task_manager.create_task("Test Task", "Feature", "Test User")
            task_manager.move_task(1, "In Progress")
            task_file = task_manager.tasks_dir / "TASK-1.md"
            with task_file.open() as f:
                content = f.read()
                self.assertIn("title: Test Task", content)
                self.assertIn("category: Feature", content)
                self.assertIn("owner: Test User", content)
                self.assertIn("priority: Medium", content)
    
    def test_move_task_should_not_change_other_tasks(self):
        with tempfile.TemporaryDirectory() as tmp:
            task_manager = TaskManager(tmp)
            task_manager.init_workspace()
            task_manager.create_task("Test Task", "Feature", "Test User")
            task_manager.create_task("Test Task 2", "Feature", "Test User")
            task_manager.move_task(1, "In Progress")
            task_file = task_manager.tasks_dir / "TASK-2.md"
            with task_file.open() as f:
                content = f.read()
                self.assertIn("board: Backlog", content)
    
    def test_move_task_should_raise_error_if_task_doesnt_exist(self):
        with tempfile.TemporaryDirectory() as tmp:
            task_manager = TaskManager(tmp)
            task_manager.init_workspace()
            with self.assertRaises(ValueError):
                task_manager.move_task(1, "In Progress")

    def test_move_task_should_raise_error_if_board_is_invalid(self):
        with tempfile.TemporaryDirectory() as tmp:
            task_manager = TaskManager(tmp)
            task_manager.init_workspace()
            task_manager.create_task("Test Task", "Feature", "Test User")
            with self.assertRaises(ValueError):
                task_manager.move_task(1, "Invalid Board")

    def test_update_task_priority(self):
        with tempfile.TemporaryDirectory() as tmp:
            task_manager = TaskManager(tmp)
            task_manager.init_workspace()
            task_manager.create_task("Test Task", "Feature", "Test User")
            task_manager.update_task_priority(1, "High")
            task_file = task_manager.tasks_dir / "TASK-1.md"
            with task_file.open() as f:
                content = f.read()
                self.assertIn("priority: High", content)

    def test_update_task_priority_should_not_change_other_fields(self):
        with tempfile.TemporaryDirectory() as tmp:
            task_manager = TaskManager(tmp)
            task_manager.init_workspace()
            task_manager.create_task("Test Task", "Feature", "Test User")
            task_manager.update_task_priority(1, "High")
            task_file = task_manager.tasks_dir / "TASK-1.md"
            with task_file.open() as f:
                content = f.read()
                self.assertIn("title: Test Task", content)
                self.assertIn("category: Feature", content)
                self.assertIn("owner: Test User", content)
                self.assertIn("board: Backlog", content)

    def test_update_task_priority_should_not_change_other_tasks(self):
        with tempfile.TemporaryDirectory() as tmp:
            task_manager = TaskManager(tmp)
            task_manager.init_workspace()
            task_manager.create_task("Test Task", "Feature", "Test User")
            task_manager.create_task("Test Task 2", "Feature", "Test User")
            task_manager.update_task_priority(1, "High")
            task_file = task_manager.tasks_dir / "TASK-2.md"
            with task_file.open() as f:
                content = f.read()
                self.assertIn("priority: Medium", content)

    def test_update_task_priority_should_raise_error_if_task_doesnt_exist(self):
        with tempfile.TemporaryDirectory() as tmp:
            task_manager = TaskManager(tmp)
            task_manager.init_workspace()
            with self.assertRaises(ValueError):
                task_manager.update_task_priority(1, "High")

    def test_update_task_priority_should_raise_error_if_priority_is_invalid(self):
        with tempfile.TemporaryDirectory() as tmp:
            task_manager = TaskManager(tmp)
            task_manager.init_workspace()
            task_manager.create_task("Test Task", "Feature", "Test User")
            with self.assertRaises(ValueError):
                task_manager.update_task_priority(1, "Invalid Priority")

    def test_update_task_category_should_change_category(self):
        with tempfile.TemporaryDirectory() as tmp:
            task_manager = TaskManager(tmp)
            task_manager.init_workspace()
            task_manager.create_task("Test Task", "Feature", "Test User")
            task_manager.update_task_category(1, "Bug")
            task_file = task_manager.tasks_dir / "TASK-1.md"
            with task_file.open() as f:
                content = f.read()
                self.assertIn("category: Bug", content)
    
    def test_update_task_category_should_not_change_other_fields(self):
        with tempfile.TemporaryDirectory() as tmp:
            task_manager = TaskManager(tmp)
            task_manager.init_workspace()
            task_manager.create_task("Test Task", "Feature", "Test User")
            task_manager.update_task_category(1, "Bug")
            task_file = task_manager.tasks_dir / "TASK-1.md"
            with task_file.open() as f:
                content = f.read()
                self.assertIn("title: Test Task", content)
                self.assertIn("priority: Medium", content)
                self.assertIn("owner: Test User", content)
                self.assertIn("board: Backlog", content)

    def test_update_task_category_should_not_change_other_tasks(self):
        with tempfile.TemporaryDirectory() as tmp:
            task_manager = TaskManager(tmp)
            task_manager.init_workspace()
            task_manager.create_task("Test Task", "Feature", "Test User")
            task_manager.create_task("Test Task 2", "Feature", "Test User")
            task_manager.update_task_category(1, "Bug")
            task_file = task_manager.tasks_dir / "TASK-2.md"
            with task_file.open() as f:
                content = f.read()
                self.assertIn("category: Feature", content)

    def test_update_task_category_should_raise_error_if_task_doesnt_exist(self):
        with tempfile.TemporaryDirectory() as tmp:
            task_manager = TaskManager(tmp)
            task_manager.init_workspace()
            with self.assertRaises(ValueError):
                task_manager.update_task_category(1, "Bug")

    def test_update_task_category_should_raise_error_if_category_is_invalid(self):
        with tempfile.TemporaryDirectory() as tmp:
            task_manager = TaskManager(tmp)
            task_manager.init_workspace()
            task_manager.create_task("Test Task", "Feature", "Test User")
            with self.assertRaises(ValueError):
                task_manager.update_task_category(1, "Invalid Category")
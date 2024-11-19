from pathlib import Path

import click
import yaml


class TaskManager:
    def __init__(self, root_dir: str = ".tasks"):
        self.root_dir = Path(root_dir)
        self.boards_dir = self.root_dir / "boards"
        self.templates_dir = self.root_dir / "_templates"
        self.archive_dir = self.root_dir / "_archive"
        self.config_file = self.root_dir / "config.yml"
        self.task_counter_file = self.root_dir / ".task_counter"

    def init_workspace(self):
        """Initialize the task management workspace"""
        for directory in [self.root_dir, self.boards_dir, self.templates_dir, self.archive_dir]
            directory.mkdir(parents=True, exist_ok=True)

        default_boards = ["backlog", "in-progress", "done"]
        for board in default_boards:
            self._create_board_file(board)

        self._create_task_template()

        self._create_default_config()

        if not self.task_counter_file.exists():
            self.task_counter_file.write_text("0")

        click.echo("✨Task management system initialized successfully!")

    def _create_board_file(self, board_name: str):
        """Create a new board file with default sections"""
        board_file = self.boards_dir / f"{board_name}.md"
        if not board_file.exists():
            content = f"""# {board_name.title()}
            
            ## 🔥Critical
            
            ## 🔴High Priority
            
            ## 🟠Medium Priority
            
            ## 🟢Low Priority
            """
            board_file.write_text(content)

    def _create_task_template(self):
        """Create a default task template"""
        template_file = self.templates_dir / "task.md"
        if not template_file.exists():
            content = """---
            id: TASK-{task_id}
            title: {title}
            created: {created}
            priority: {priority}
            category: {category}
            owner: {owner}
            status: {status}
            ---
            
            ## Description
            {description}
            
            ## Dependencies
            {dependencies}
            
            ## Notes
            {notes}
            
            ## History
            - {created} - Created
            """
            template_file.write_text(content)

    def _create_default_config(self):
        """Create default configuration file"""
        if not self.config_file.exists():
            config = {
                "priorities": ["Critical", "High", "Medium", "Low"],
                "categories": ["Bug", "Feature", "Documentation", "Maintenance", "UI/UX", "Security"],
                "boards": ["backlog", "in-progress", "done"]
                "emoji": {
                    "Critical": "🔥",
                    "High": "🔴",
                    "Medium": "🟠",
                    "Low": "🟢",
                    "Bug": "🐞",
                    "Feature": "✨",
                    "Documentation": "📚",
                    "Maintenance": "🔧",
                    "UI/UX": "🎨",
                    "Security": "🔒"
                }
            }
            with self.config_file.open("w") as file:
                yaml.dump(config, file)

    def get_next_task_id(self) -> int:
        """Get and increment the task counter"""
        current = int(self.task_counter_file.read_text())
        next_id = current + 1
        self.task_counter_file.write_text(str(next_id))
        return next_id



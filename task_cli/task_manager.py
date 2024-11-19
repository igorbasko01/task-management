from datetime import datetime
from pathlib import Path

import click
import frontmatter
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
        for directory in [self.root_dir, self.boards_dir, self.templates_dir, self.archive_dir]:
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
            
## 🔥 Critical
            
## 🔴 High Priority
            
## 🟠 Medium Priority
            
## 🟢 Low Priority
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
                "boards": ["backlog", "in-progress", "done"],
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

    def create_task(self, title: str, description: str, priority: str = "Medium",
                    category: str = "Feature", owner: str = "") -> str:
        """Create a new task and add it to the backlog board"""
        task_id = f"TASK-{self.get_next_task_id():04d}"
        created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        template = (self.templates_dir / "task.md").read_text()

        task_content = template.format(
            task_id=task_id,
            title=title,
            created=created,
            priority=priority,
            category=category,
            owner=owner,
            status="backlog",
            description=description,
            dependencies="- None",
            notes="- None"
        )

        task_file = self.root_dir / "tasks" / f"{task_id}.md"
        task_file.parent.mkdir(exist_ok=True)
        task_file.write_text(task_content)

        self._add_task_to_board("backlog", task_id, title, priority, category, owner)

        return task_id

    def _add_task_to_board(self, board: str, task_id: str, title: str, priority: str, category: str, owner: str):
        """Add a task to a board under the appropriate priority section"""
        board_file = self.boards_dir / f"{board}.md"
        config = yaml.safe_load(self.config_file.read_text())

        lines = board_file.read_text().splitlines()
        priority_section = f"## {config['emoji'][priority]} {priority} Priority"

        section_index = -1
        for i, line in enumerate(lines):
            if line.strip() == priority_section:
                section_index = i
                break

        if section_index == -1:
            lines.append(f"\n{priority_section}\n")
            section_index = len(lines) - 1

        task_line = f"- [ ] {task_id}: {title}"
        task_details = f"  > {config['emoji'][category]} {category}"
        if owner:
            task_details += f" | @{owner}"

        lines.insert(section_index + 1, task_line)
        lines.insert(section_index + 2, task_details)

        board_file.write_text("\n".join(lines))

    def move_task(self, task_id: str, to_board: str):
        """Move a task from one board to another"""
        config = yaml.safe_load(self.config_file.read_text())
        if to_board not in config["boards"]:
            raise ValueError(f"Board '{to_board}' not found in the configuration")

        current_board = None
        for board in config["boards"]:
            board_file = self.boards_dir / f"{board}.md"
            content = board_file.read_text()
            if task_id in content:
                current_board = board
                break

        if not current_board:
            raise ValueError(f"Task '{task_id}' not found in any board")

        task_file = self.root_dir / "tasks" / f"{task_id}.md"
        task = frontmatter.load(str(task_file))

        self._remove_task_from_board(current_board, task_id)

        self._add_task_to_board(
            to_board,
            task_id,
            str(task.metadata["title"]),
            str(task.metadata["priority"]),
            str(task.metadata["category"]),
            str(task.metadata["owner"])
        )

        content = task_file.read_text()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        content += f"- {timestamp} - Moved to {to_board}\n"
        task_file.write_text(content)

    def _remove_task_from_board(self, board: str, task_id: str):
        """Remove a task from a board"""
        board_file = self.boards_dir / f"{board}.md"
        lines = board_file.read_text().splitlines()

        i = 0
        while i < len(lines):
            if task_id in lines[i]:
                lines.pop(i)
                if i < len(lines) and lines[i].startswith(" >"):
                    lines.pop(i)
                break
            i += 1

        board_file.write_text("\n".join(lines))

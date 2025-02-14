# Task Management CLI
A task tracking system Kanban style, that is part of your repository.

## Installation
Installing from git: 
```
pip install git+https://github.com/igorbasko01/task-management.git
```

## Initializing a Workspace
Before starting adding tasks, a workspace initialization is needed.

Initialize a workspace using: `task init`.

It creates a `.tasks` folder in the root of the project. In this folder all the tasks will be
created and stored.

__Note__: The `.tasks` folder shouldn't be ignored by `.gitignore` so the tasks could be tracked with the repository.

## Usage
To add a task use: `task create <task_title>`

It will create a task file in the `.tasks/tasks` folder. eg: 
```shell
> task create "Test task"
✨ Task created: 12
```
It means that a `TASK-12.md` file was created in `.tasks/tasks` folder, and now you can edit it.

To list all tasks: `task list`

To list all tasks in specific board: `task list --board Backlog`

To move a task to a different board: `task move <task_id> <board_name>`, eg `task move 3 "In Progress"`.

Or use an acronym for the board name (instead of `"In Prgress"`), such as: `bl -> Backlog, ip -> In Progress, dn -> Done`

Use `task --help` to list all the different commands.

## Testing
To run the tests of the project use `python -m unittest discover -s tests`.
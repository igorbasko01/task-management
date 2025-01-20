---
id: TASK-17
title: when listing tasks don't show tasks that are old
created: 2025-01-17 14:55:12
priority: Medium
category: Feature
owner: None
board: In Progress
---

## Description
`task list` should not show tasks that are in the "Done" board and are older than 14 days.

Implementation details:
1. The `Task` should have a method to return all move action datetimes.
    1. Method signature: `def get_all_moves(self, of=None) -> List[Tuple[datetiem, Board]]: `
    1. `task.get_all_moves(of=Task.DONE)` - returns a list of datetime objects of all moves to the "Done" board of that task.
    1. `task.get_all_moves()` - returns a list of datetime objects of all moves of that task.
1. The `TaskManager` during listing the tasks should check if the task is currently in the "Done" board and if the latest move to the "Done" board is older than 14 days. If so, it should not be listed.
1. Allow passing the `--all` flag to the `task list` command to show all tasks, including those that are older than 14 days.
1. Allow passing the `--done_in_last_days <days>` flag to the `task list` command to show tasks that are in the "Done" board and are newer than the specified number of days. By default, it should show tasks that are in the "Done" board and were "Done" in the last 14 days.

## Notes


## History
2025-01-17 14:55:12 - Created

2025-01-20 21:41:15 - Moved to In Progress

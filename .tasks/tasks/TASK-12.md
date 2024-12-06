---
id: TASK-12
title: add commit history to task commit
created: 2024-12-06 16:37:53
priority: Medium
category: Feature
owner: 
board: Backlog
---

## Description
When commiting a change, with a task identifier, add a history line with the commit's message.

I assume that a change in the git hooks will be needed.

Sub Tasks:
- [ ] Add cli history update command, eg: `task commit "TASK-12 - allow adding history for commit"`.
- [ ] Add git hook that executes the mentioned `task commit` command.
- [ ] Add a documentation to the README file explaining how to install and use the git hook.

## Notes


## History
2024-12-06 16:37:53 - Created

---
name: task-context
description: Shows active task details, blockers, and dependencies. Use when implementing features, checking status, planning work, or when user asks what they're working on.
allowed-tools: Read, Grep, Glob
---

# Task Context Skill

This skill provides context about current tasks and project state.

## Getting Task Information

### If beads is available

Check current work status:
```bash
bd list --status=in_progress  # Active tasks
bd ready                       # Available tasks
bd blocked                     # Stuck tasks
bd show <id>                   # Task details
```

### If beads is not available

Ask the user:
- What task are you currently working on?
- What are the acceptance criteria?
- Is anything blocking progress?

## Task States

| Status | Meaning |
|--------|---------|
| `open` | Ready to start |
| `in_progress` | Currently being worked on |
| `blocked` | Waiting on something |
| `closed` | Completed |

## Understanding Dependencies

Tasks may depend on other tasks:
- **Blocked by**: Cannot start until these complete
- **Blocks**: Other tasks waiting on this one

Use `bd show <id>` to see the full dependency graph.

## Providing Context

When helping with implementation, include:
1. **Task title and ID** (if using beads)
2. **Acceptance criteria** — what "done" means
3. **Dependencies** — what this needs or enables
4. **Related files** — code that will change

## Quick Commands

| Goal | Command |
|------|---------|
| See all open tasks | `bd list --status=open` |
| See what's active | `bd list --status=in_progress` |
| Check blockers | `bd blocked` |
| Get task details | `bd show <id>` |
| Update status | `bd update <id> --status=<status>` |

---
description: Show current task state, blockers, and project progress
---

# Task Status

Provide a clear view of the current work state and what's actionable.

## Status Report

### 1. Check Current State

If beads is available, run these commands and summarize:
```bash
bd stats                    # Overall project health
bd list --status=in_progress  # Active work
bd blocked                  # What's stuck
bd ready                    # What can be started
```

If beads is not available, ask the user about:
- What they're currently working on
- Any blockers or waiting items
- What's next in the queue

### 2. Present Status Summary

Format the status report as:

```
## Project Status

### Currently Active
- [Task title] - [brief status]

### Blocked
- [Task title] - blocked by: [reason]

### Ready to Start
- [Task title] - [priority]

### Recently Completed
- [Task title] - [when closed]

### Stats
- Open: X | In Progress: X | Blocked: X | Closed: X
```

### 3. Recommend Next Action

Based on the status, suggest:
- If in progress: Continue with `/wip:implement`
- If blocked: What needs to happen to unblock
- If nothing active: Pick from ready queue
- If all done: Celebrate, or plan next feature

## Quick Commands

| Goal | Command |
|------|---------|
| See what's ready | `bd ready` |
| Check blockers | `bd blocked` |
| View specific task | `bd show <id>` |
| Update task status | `bd update <id> --status=<status>` |

---

Would you like a full status report, or information about a specific task?

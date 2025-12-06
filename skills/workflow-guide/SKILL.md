---
name: workflow-guide
description: Provides workflow phase guidance. Use when user asks about next steps, workflow status, available actions, what to do next, or how to proceed with their feature.
allowed-tools: Read, Grep, Glob
---

# WIP Workflow Guide

This skill provides guidance on the WIP workflow phases.

## Workflow Overview

```
brainstorm → plan → implement → test → review → ship
```

## Phase Commands

| Phase | Command | Purpose |
|-------|---------|---------|
| Brainstorm | `/wip:brainstorm` | Explore ideas, gather requirements |
| Plan | `/wip:plan` | Architecture, task breakdown |
| Implement | `/wip:implement` | Focused code writing |
| Test | `/wip:test` | Write and run tests |
| Review | `/wip:review` | Code review, quality checks |
| Ship | `/wip:ship` | Documentation, commit, release |

## Deciding What's Next

### Just starting a new feature?
→ Use `/wip:brainstorm` to explore the idea

### Have clear requirements?
→ Use `/wip:plan` to design and break down work

### Have a task ready to implement?
→ Use `/wip:implement` to focus on coding

### Code written, need tests?
→ Use `/wip:test` to create and run tests

### Ready for feedback?
→ Use `/wip:review` for quality checks

### Everything approved?
→ Use `/wip:ship` to finalize and commit

## Task Management

| Goal | Command |
|------|---------|
| Create a task | `/wip:task:create` |
| Check status | `/wip:task:status` |
| Break down feature | Use `/wip:plan` with breakdown agent |

## Tips

- You can skip phases if they don't apply
- Each phase is independent — start wherever makes sense
- Use `/wip:task:status` anytime to see where you are

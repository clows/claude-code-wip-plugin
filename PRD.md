# Product Requirements Document: Work In Project (WIP)

## Vision

WIP is a Claude Code plugin that provides structured project management workflows for developers working with AI assistance. It guides work from initial brainstorming through shipping, using specialized agents to distribute workload while keeping context focused.

## Target Users

Developers using Claude Code who want:
- Structured approach to feature development
- Task breakdown and tracking without leaving the terminal
- Specialized AI assistance for different phases of work

## Workflow Phases

```
brainstorm → plan → implement → test → review → ship
```

| Phase | Purpose | Entry Command |
|-------|---------|---------------|
| Brainstorm | Explore ideas, gather requirements | `/wip:brainstorm` |
| Plan | Architecture decisions, task breakdown | `/wip:plan` |
| Implement | Focused code writing | `/wip:implement` |
| Test | Test creation and execution | `/wip:test` |
| Review | Code review, standards check | `/wip:review` |
| Ship | Documentation, commit, release | `/wip:ship` |

## Component Architecture

### Commands (User-Invoked Entry Points)

Commands are invoked explicitly via `/wip:*`. Each command sets up context and may spawn agents.

**Workflow commands** (`commands/workflow/`):

| File | Purpose |
|------|---------|
| `brainstorm.md` | Open-ended exploration, idea capture, requirements gathering |
| `plan.md` | Invoke architect agent, create task breakdown, define acceptance criteria |
| `implement.md` | Focus on current task, invoke implementer agent for coding |
| `test.md` | Generate and run tests via tester agent |
| `review.md` | Code review via reviewer agent, check standards compliance |
| `ship.md` | Documentation generation, commit preparation, release notes |

**Task commands** (`commands/task/`):

| File | Purpose |
|------|---------|
| `create.md` | Create a new task/issue with description and acceptance criteria |
| `breakdown.md` | Decompose feature into ordered subtasks with dependencies |
| `status.md` | Show current task state, blockers, and progress |

### Agents (Workload Distribution)

Agents are specialized subagents with focused context and limited tool access. They run in separate context windows to keep prompts small and responses targeted.

**Planning agents** (`agents/planning/`):

| Agent | Tools | Purpose |
|-------|-------|---------|
| `architect.md` | Read, Grep, Glob | System design, API design, technical decisions |
| `breakdown.md` | Read, Grep, Glob | Feature decomposition, dependency ordering, effort estimation |

**Implementation agents** (`agents/implementation/`):

| Agent | Tools | Purpose |
|-------|-------|---------|
| `implementer.md` | Read, Edit, Write, Bash, Grep, Glob | Focused code writing, single-task execution |
| `tester.md` | Read, Edit, Write, Bash, Grep, Glob | Test strategy, test generation, coverage analysis |

**Quality agents** (`agents/quality/`):

| Agent | Tools | Purpose |
|-------|-------|---------|
| `reviewer.md` | Read, Grep, Glob, Bash | Code review, best practices, security checks |
| `documenter.md` | Read, Edit, Write, Grep, Glob | README updates, API docs, inline documentation |

### Skills (Model-Invoked Context)

Skills are **model-invoked** — Claude autonomously decides when to use them based on the task at hand. They provide just-in-time context without bloating every prompt.

**Skill descriptions must include:**
1. What the skill does
2. When Claude should use it
3. Trigger terms users would mention

| Skill | Description Pattern |
|-------|---------------------|
| `workflow-guide/` | "Provides workflow phase guidance. Use when user asks about next steps, workflow status, or available actions." |
| `task-context/` | "Shows active task details, blockers, and dependencies. Use when implementing features, checking status, or planning work." |
| `codebase-patterns/` | "Documents project conventions and coding standards. Use when writing new code, reviewing changes, or onboarding." |

## Optional Integration

### Beads Issue Tracker

`lib/tracker.py` provides a Python wrapper for beads integration:
- Create/update issues from within workflow
- Sync task status between WIP and beads
- Query blockers and dependencies

This is opt-in; the plugin works standalone without beads.

## Component Interaction

```
User invokes /wip:* command
       │
       ▼
Command prompt expands, sets up context
       │
       ▼
Claude spawns specialized agent via Task tool
       │
       ▼
Agent works with limited tools, focused context
       │
       ├──► Agent queries skill if needed (model-invoked)
       │         │
       │         ▼
       │    Skill injects contextual information
       │
       ▼
Agent returns results to main conversation
       │
       ▼
User sees focused output, can continue or switch phases
```

## Success Criteria

1. Developer can go from idea to shipped feature using WIP commands
2. Each agent stays focused (small context, specific expertise, limited tools)
3. Skills reduce prompt bloat by providing info only when relevant
4. Workflow feels natural, not bureaucratic
5. Plugin works standalone; beads integration is optional enhancement

---
description: Decompose a feature into ordered subtasks with dependencies
---

# Task Breakdown — Dispatcher

You are the **dispatcher** for task breakdown work. Your job is to gather context, then delegate to a specialized agent.

## Your Role

1. **Clarify the feature** — Understand what needs to be broken down
2. **Gather context** — Collect scope, constraints, dependencies
3. **Delegate** — Spawn the breakdown agent with full context

## Step 1: Gather Context

Ask the user:
- **What feature?** — What large piece of work needs decomposition?
- **Size constraints?** — How granular should tasks be? (S/M/L guidelines)
- **Dependencies?** — Any known prerequisites or blockers?
- **Existing work?** — Is there related code or prior tasks to consider?
- **Output format?** — Create beads issues, or just provide a list?

If the user references a beads issue, use `bd show <id>` to get the full details.

### Task Sizing Reference
| Size | Typical Scope | Time |
|------|---------------|------|
| S | Single function, small change | < 1 hour |
| M | New component, multiple files | 1-3 hours |
| L | Feature slice, significant change | 3-6 hours |

If a task is larger than L, it should be broken down further.

## Step 2: Delegate to Agent

Once you have enough context, use the **Task tool** to spawn the breakdown agent:

```
subagent_type: wip:planning:breakdown
prompt: |
  ## Feature to Break Down
  [Description of the feature or large task]

  ## Scope
  - [What's included]
  - [What's explicitly excluded]

  ## Size Constraints
  - Maximum task size: [S/M/L]
  - Target granularity: [how small should tasks be]

  ## Known Dependencies
  - [External dependencies]
  - [Prerequisites that must be done first]

  ## Existing Context
  - [Related code or modules]
  - [Prior work to build on]

  ## Output Requirements
  - [Create beads issues: yes/no]
  - [Include acceptance criteria: yes/no]
  - [Show dependency graph: yes/no]
```

## Rules

- **Do NOT break down tasks yourself** — always delegate to the agent
- **Do NOT skip context gathering** — agents create better breakdowns with clear scope
- **Do NOT spawn the agent until** you understand the feature and sizing requirements

## After the Agent Returns

Summarize the breakdown for the user and suggest next steps:
- `/wip:workflow:implement` — Start implementing the first task
- Create beads issues: `bd create --title="[title]" --type=task`
- Add dependencies: `bd dep add [child-id] [parent-id]`

---

What feature would you like to break down?

---
description: Create architecture and task breakdown for a feature
---

# Plan Mode — Dispatcher

You are the **dispatcher** for planning work. Your job is to gather context, then delegate to a specialized agent.

## Your Role

1. **Clarify the feature** — Understand what needs to be planned
2. **Gather context** — Collect requirements, constraints, existing patterns
3. **Delegate** — Spawn the architect agent with full context

## Step 1: Gather Context

Ask the user:
- **What feature?** — What are you building? What problem does it solve?
- **Requirements?** — What are the must-haves? Any output from brainstorming?
- **Constraints?** — Time limits, tech requirements, compatibility needs?
- **Existing patterns?** — What similar features exist in the codebase?
- **Scope boundaries?** — What's explicitly out of scope?

If the user references a beads issue, use `bd show <id>` to get the full details.

To explore the codebase for patterns, you can:
- Look for similar existing features
- Review the project structure
- Check for architectural documentation

## Step 2: Delegate to Agent

Once you have enough context, use the **Task tool** to spawn the architect agent:

```
subagent_type: wip:planning:architect
prompt: |
  ## Feature Overview
  [What is being built and why]

  ## Requirements
  - [Must-have requirement 1]
  - [Must-have requirement 2]
  - [Nice-to-have items]

  ## Constraints
  - [Technical constraints]
  - [Time or resource constraints]
  - [Compatibility requirements]

  ## Existing Patterns
  - [Similar features in the codebase]
  - [Architectural patterns to follow]

  ## Scope
  - In scope: [what's included]
  - Out of scope: [what's explicitly excluded]

  ## Expected Output
  - Architecture decisions with rationale
  - Ordered task breakdown with dependencies
  - Risk assessment
```

## Rules

- **Do NOT create the plan yourself** — always delegate to the agent
- **Do NOT skip context gathering** — agents create better plans with clear requirements
- **Do NOT spawn the agent until** you understand the feature scope and constraints

## After the Agent Returns

Summarize the plan for the user and suggest next steps:
- `/wip:workflow:implement` — Start implementing the first task
- `/wip:task:breakdown` — Further decompose large tasks if needed
- Create beads issues with `bd create` for tracking

---

What feature are you planning? (Or share the output from `/wip:workflow:brainstorm`)

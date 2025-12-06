---
description: Create architecture and task breakdown for a feature
---

# Plan Mode

You are now in **plan mode** — the phase where ideas become actionable implementation plans.

## Your Role

Help the user design and break down their feature by:
- Making architectural decisions with clear rationale
- Decomposing work into ordered, testable tasks
- Identifying dependencies and blockers
- Defining acceptance criteria for each task

## Planning Process

### 1. Understand the Scope
Review what was captured in brainstorming:
- What's the core problem being solved?
- What are the must-have requirements?
- What are the constraints (time, tech, compatibility)?

### 2. Explore the Codebase
Before designing, understand what exists:
- What patterns does the codebase already use?
- Are there similar features to reference?
- What would need to change vs. be created new?

### 3. Make Architectural Decisions
For each significant choice, document:
- **Decision**: What approach are we taking?
- **Alternatives**: What else was considered?
- **Rationale**: Why this choice?

### 4. Break Down into Tasks
Create an ordered list of implementation tasks:
- Each task should be completable in one focused session
- Tasks should have clear acceptance criteria
- Dependencies between tasks should be explicit
- Consider: What can be done in parallel?

## Task Format

For each task, capture:
```
Task: [Clear, action-oriented title]
Depends on: [Previous task IDs, if any]
Acceptance criteria:
- [ ] Specific, testable outcome
- [ ] Another measurable result
```

## Output

When planning is complete, provide:
1. **Architecture summary**: Key technical decisions
2. **Task list**: Ordered implementation steps
3. **Risk assessment**: What could go wrong?
4. **First task**: Ready to start with `/wip:implement`

---

What feature are you planning? (Or share the output from `/wip:brainstorm`)

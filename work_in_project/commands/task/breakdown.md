---
description: Decompose a feature into ordered subtasks with dependencies
---

# Task Breakdown

Break down a large feature into smaller, implementable tasks.

## Process

### 1. Define the Feature
Start with a clear understanding:
- What is the end goal?
- What are the must-haves vs nice-to-haves?
- What existing code is involved?

### 2. Identify Components
Map out what's needed:
- New files or modules to create
- Existing code to modify
- Tests to write
- Documentation to update

### 3. Create Tasks
For each logical piece of work:

```
## Task: [Action-oriented title]
Size: S/M/L
Depends on: [Previous tasks, if any]

### Acceptance Criteria
- [ ] [Specific, testable outcome]
- [ ] [Another measurable result]
```

### 4. Order by Dependencies
Arrange tasks so:
- Prerequisites come first
- Critical path is clear
- Parallel opportunities are noted

## Task Sizing Guide

| Size | Typical Scope | Time |
|------|---------------|------|
| S | Single function, small change | < 1 hour |
| M | New component, multiple files | 1-3 hours |
| L | Feature slice, significant change | 3-6 hours |

If a task is larger than L, break it down further.

## Creating in Beads

If beads is available, create tasks with:
```bash
bd create --title="[title]" --type=task --priority=[1-4]
bd dep add [child-id] [parent-id]  # child depends on parent
```

## Output Format

```
## Feature Breakdown: [Feature Name]

### Tasks (in dependency order)

1. **[Task Title]** (S)
   - [ ] [Acceptance criterion]

2. **[Task Title]** (M) — depends on: 1
   - [ ] [Acceptance criterion]
   - [ ] [Acceptance criterion]

3. **[Task Title]** (S) — depends on: 1
   - [ ] [Acceptance criterion]

### Dependency Graph
1 → 2 → 4
  ↘ 3 ↗

### Notes
[Any important context or risks]
```

---

What feature would you like to break down?

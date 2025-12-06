---
description: Create a new task with description and acceptance criteria
---

# Create Task

Help the user create a well-defined task that can be tracked and implemented.

## Task Creation Process

### 1. Gather Information

Ask the user for:
- **Title**: Clear, action-oriented (e.g., "Add user authentication endpoint")
- **Type**: `feature`, `bug`, `task`, or `chore`
- **Description**: Why this task exists and what needs to be done
- **Acceptance criteria**: Specific, testable outcomes

### 2. Validate the Task

Before creating, check:
- Is the scope clear and achievable in one session?
- Are the acceptance criteria measurable?
- Are dependencies identified?

### 3. Create the Task

If beads is available, create an issue:
```bash
bd create --title="[title]" --type=[type] --priority=[1-4] --description="[description]"
```

If beads is not available, output in this format for manual tracking:
```
## Task: [Title]
Type: [feature|bug|task|chore]
Priority: [P1-P4]

### Description
[Why this exists and what needs to be done]

### Acceptance Criteria
- [ ] [First testable outcome]
- [ ] [Second testable outcome]

### Dependencies
- [None, or list blockers]
```

## Task Quality Checklist

A good task should be:
- [ ] **Specific**: Clear what "done" means
- [ ] **Small**: Completable in one focused session
- [ ] **Independent**: Minimal dependencies on other work
- [ ] **Testable**: Acceptance criteria can be verified

---

What task would you like to create?

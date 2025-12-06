---
description: Prepare documentation, commits, and release notes for shipping
---

# Ship Mode

You are now in **ship mode** — the final phase before code goes live.

## Your Role

Help the user ship with confidence by:
- Ensuring documentation is complete
- Creating clean, descriptive commits
- Preparing release notes if needed
- Verifying everything is ready

## Shipping Checklist

### 1. Pre-Ship Verification
Before shipping, confirm:
- [ ] All tests pass
- [ ] Code has been reviewed
- [ ] No TODO/FIXME items left unresolved
- [ ] No debug code or console.logs remaining

### 2. Documentation
Update docs if needed:
- README changes for new features
- API documentation updates
- Inline comments for complex logic
- Migration notes for breaking changes

### 3. Commit Preparation
Create meaningful commits:
- Atomic commits (one logical change per commit)
- Descriptive commit messages
- Reference issue/task IDs

### 4. Release Notes (if applicable)
Summarize for users:
- What's new
- What's changed
- What's fixed
- Breaking changes (if any)

## Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**: feat, fix, docs, style, refactor, test, chore

**Example**:
```
feat(auth): add password reset flow

Implement password reset via email verification.
Users can now request a reset link from the login page.

Closes #123
```

## Output Format

```
## Ready to Ship: [Feature]

### Changes Summary
[Brief overview of what's being shipped]

### Commits
1. [commit message 1]
2. [commit message 2]

### Documentation Updated
- [x] README
- [x] API docs
- [ ] None needed

### Release Notes
[User-facing summary of changes]

### Ship Commands
$ git add [files]
$ git commit -m "[message]"
$ [any additional commands]
```

## Guidelines

- Don't rush — shipping is permanent
- Double-check for sensitive data
- Verify the build succeeds
- Make commits reviewable

---

What are you ready to ship?

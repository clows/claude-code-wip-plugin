---
name: codebase-patterns
description: Documents project conventions and coding standards. Use when writing new code, reviewing changes, onboarding, or when user asks about project structure or style.
allowed-tools: Read, Grep, Glob
---

# Codebase Patterns Skill

This skill helps understand and follow project conventions.

## Discovering Patterns

Before writing code, explore the existing codebase:

### File Organization
```bash
# Find similar files
ls -la [relevant directories]

# See project structure
find . -type f -name "*.ts" | head -20
```

### Code Conventions
```bash
# Find similar implementations
grep -r "function.*Handler" --include="*.ts"

# Check naming patterns
grep -r "class.*Service" --include="*.ts"
```

## Common Patterns to Look For

### Naming Conventions
- File naming: `kebab-case.ts` vs `PascalCase.ts` vs `camelCase.ts`
- Function naming: `camelCase` vs `snake_case`
- Class naming: Usually `PascalCase`
- Constants: `SCREAMING_SNAKE_CASE`

### Code Structure
- How are modules organized?
- Are there barrel exports (index.ts)?
- How is configuration handled?
- Where do tests live?

### Error Handling
- Custom error types?
- Try/catch patterns?
- Result types?

### Testing Patterns
- Test file naming: `*.test.ts` vs `*.spec.ts`
- Test structure: describe/it vs test
- Mocking approach

## Applying Patterns

When writing new code:

1. **Find an example** — Search for similar functionality
2. **Match the style** — Use the same patterns exactly
3. **Stay consistent** — Don't mix styles within a file
4. **When in doubt, ask** — If patterns conflict, clarify with user

## Quick Searches

| Looking for | Search |
|-------------|--------|
| API routes | `grep -r "router\." --include="*.ts"` |
| Database queries | `grep -r "prisma\|knex\|sql" --include="*.ts"` |
| Error handling | `grep -r "catch\|throw" --include="*.ts"` |
| Tests | `find . -name "*.test.ts" -o -name "*.spec.ts"` |

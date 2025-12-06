---
description: Generate and run tests for your implementation
---

# Test Mode — Dispatcher

You are the **dispatcher** for testing work. Your job is to gather context, then delegate to a specialized agent.

## Your Role

1. **Clarify what to test** — Understand what code needs testing
2. **Gather context** — Collect test framework info, existing patterns, coverage goals
3. **Delegate** — Spawn the tester agent with full context

## Step 1: Gather Context

Ask the user:
- **What to test?** — What implementation, feature, or files need testing?
- **Test framework?** — What testing framework does this project use? (jest, pytest, vitest, etc.)
- **Existing patterns?** — Are there existing tests to follow as examples?
- **Coverage goals?** — Any specific coverage requirements or focus areas?
- **Test types?** — Unit tests, integration tests, e2e tests?

If the user references a beads issue, use `bd show <id>` to get the full details.

To find existing test patterns, you can:
- Look for test directories (`tests/`, `__tests__/`, `spec/`)
- Check for test config files (`jest.config.js`, `pytest.ini`, `vitest.config.ts`)
- Review existing test files for conventions

## Step 2: Delegate to Agent

Once you have enough context, use the **Task tool** to spawn the tester agent:

```
subagent_type: wip:implementation:tester
prompt: |
  ## What to Test
  [Description of the implementation/feature to test]

  ## Test Framework
  [Framework name and any relevant config]

  ## Existing Patterns
  - [Example test files to follow]
  - [Testing conventions used in this codebase]

  ## Coverage Goals
  - [Specific areas that must be covered]
  - [Edge cases to consider]

  ## Test Types Needed
  - [Unit / Integration / E2E]

  ## Files to Test
  - [Source file paths]
```

## Rules

- **Do NOT write tests yourself** — always delegate to the agent
- **Do NOT skip context gathering** — agents write better tests with clear scope
- **Do NOT spawn the agent until** you understand what needs testing and how

## After the Agent Returns

Summarize the test results for the user and suggest next steps:
- If tests pass: `/wip:workflow:review` — Review the code for quality
- If tests pass and reviewed: `/wip:workflow:ship` — Prepare for shipping
- If tests fail: Fix the issues, then run tests again

---

What would you like to test?

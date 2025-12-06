# WIP (Work In Project)

A Claude Code plugin for AI-assisted project management workflows. WIP guides your development from initial idea through shipped feature, using specialized agents and structured commands.

## Prerequisites

- [Claude Code](https://claude.ai/code) installed
- [beads (bd)](https://github.com/steveyegge/beads) CLI installed

## Installation

1. Add the marketplace:
   ```
   /plugin marketplace add github:clows/wip-marketplace
   ```

2. Install the plugin:
   ```
   /plugin install wip
   ```

3. Verify installation:
   ```
   /wip:test
   ```

## Getting Started

### Setting Up a New Project

1. **Initialize beads** in your project directory:
   ```bash
   bd init
   ```
   This creates a `.beads/` directory for issue tracking.

2. **Create your first task**:
   ```bash
   bd create "My first feature" -t feature
   ```
   Or use the command: `/wip:task:create`

3. **Check available work**:
   ```bash
   bd ready
   ```

When you start a Claude Code session, Claude will greet you with your current work status (active tasks, ready work, etc.).

### Adding WIP to an Existing Project

1. **Initialize beads** (if not already done):
   ```bash
   bd init
   ```

2. **Import existing work** (optional):
   - Create issues for in-flight work: `bd create "Existing feature" -t feature`
   - Set priorities: `bd update <id> --priority 1`

3. **Start using WIP commands** - they work immediately after plugin installation.

## Workflow Overview

WIP follows a structured development flow:

```
brainstorm → plan → implement → test → review → ship
```

Each phase has a dedicated command that sets up the right context and spawns specialized agents.

### Typical Workflow Example

**1. Start with an idea:**
```
/wip:workflow:brainstorm
```
Explore requirements, capture ideas, define scope. Creates tasks in beads.

**2. Plan the implementation:**
```
/wip:workflow:plan
```
Design architecture, break down into subtasks, identify dependencies.

**3. Implement a task:**
```
/wip:workflow:implement
```
Focus on a single task. The implementer agent writes code with limited scope.

**4. Add tests:**
```
/wip:workflow:test
```
Generate and run tests for your implementation.

**5. Review changes:**
```
/wip:workflow:review
```
Check code quality, security, and adherence to project patterns.

**6. Ship it:**
```
/wip:workflow:ship
```
Prepare documentation, create commits, and generate release notes.

### Quick Task Management

Check what's ready to work on:
```bash
bd ready
```

See current progress:
```
/wip:task:status
```

Break a large feature into subtasks:
```
/wip:task:breakdown
```

## What Happens Automatically

### Session Hooks

When you start a Claude Code session, WIP injects context about your project into Claude's awareness. Claude will then greet you with:
- Current in-progress work
- Tasks that are ready (no blockers)
- Project statistics

This helps you pick up where you left off without running commands.

### Skills (Model-Invoked)

Claude automatically uses these skills when relevant:

| Skill | Triggered When |
|-------|----------------|
| `workflow-guide` | You ask "what's next?", "what should I do?", or about workflow phases |
| `task-context` | You're implementing features or ask about current task status |
| `codebase-patterns` | Writing new code or reviewing for consistency |

You don't invoke skills directly—Claude decides when they're helpful.

### Specialized Agents

Commands spawn focused agents with limited tools and context:

| Phase | Agent | Purpose |
|-------|-------|---------|
| Planning | `architect` | System design, API decisions |
| Planning | `breakdown` | Feature decomposition, dependencies |
| Implementation | `implementer` | Focused code writing |
| Implementation | `tester` | Test strategy and generation |
| Quality | `reviewer` | Code review, security checks |
| Quality | `documenter` | README, API docs, comments |

Agents run in separate contexts, keeping responses targeted and efficient.

## Command Reference

### Workflow Commands

| Command | Purpose |
|---------|---------|
| `/wip:workflow:brainstorm` | Explore ideas, gather requirements, capture concepts |
| `/wip:workflow:plan` | Create architecture and task breakdown |
| `/wip:workflow:implement` | Focus on implementing a specific task |
| `/wip:workflow:test` | Generate and run tests |
| `/wip:workflow:review` | Review code for quality and security |
| `/wip:workflow:ship` | Prepare commits and release notes |

### Task Commands

| Command | Purpose |
|---------|---------|
| `/wip:task:create` | Create a new task with description and acceptance criteria |
| `/wip:task:status` | Show current task state, blockers, and progress |
| `/wip:task:breakdown` | Decompose a feature into ordered subtasks |

## Beads Integration

WIP uses [beads](https://github.com/steveyegge/beads) for issue tracking. Key commands:

```bash
bd ready              # Show unblocked work
bd list               # All issues
bd create "Title"     # New issue
bd update <id> --status in_progress  # Claim work
bd close <id>         # Complete work
bd show <id>          # Issue details
```

Issues are stored in `.beads/issues.jsonl` and version-controlled with your code.

## Tips

- **Start small**: Use `/wip:workflow:brainstorm` for new ideas, even small ones
- **Check status often**: Run `bd ready` or `/wip:task:status` to stay oriented
- **Let agents focus**: Each agent has a specific job—trust the workflow phases
- **Commit with issues**: The `.beads/` directory should be committed with code changes

## Troubleshooting

**"bd: command not found"**
Install beads: `pip install beads-cli` or see [beads installation](https://github.com/steveyegge/beads)

**No tasks showing at session start**
Run `bd init` in your project, then create some tasks with `bd create`.

**Commands not found after install**
Restart Claude Code or run `/plugin list` to verify WIP is installed.

## License

MIT

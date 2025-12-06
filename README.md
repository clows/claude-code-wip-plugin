# WIP (Work In Project)

A Claude Code plugin for AI-assisted project management workflows.

## Prerequisites

- [Claude Code](https://claude.ai/code) installed
- [beads (bd)](https://github.com/steveyegge/beads) CLI installed and configured

## Installation

1. Add the marketplace:
   ```
   /plugin marketplace add github:clows/wip-marketplace
   ```

2. Install the plugin:
   ```
   /plugin install wip
   ```

## Features

### Workflow Commands

- `/wip:workflow:brainstorm` - Explore ideas and gather requirements
- `/wip:workflow:plan` - Create architecture and task breakdown
- `/wip:workflow:implement` - Focus on implementing a specific task
- `/wip:workflow:test` - Generate and run tests
- `/wip:workflow:review` - Review code for quality and security
- `/wip:workflow:ship` - Prepare commits and release notes

### Task Management

- `/wip:task:create` - Create a new task
- `/wip:task:status` - Show current task state and progress
- `/wip:task:breakdown` - Decompose a feature into subtasks

### Specialized Agents

The plugin includes agents for different development phases:

- **Planning**: `architect`, `breakdown`
- **Implementation**: `implementer`, `tester`
- **Quality**: `reviewer`, `documenter`

### Skills

Context-aware skills that Claude invokes automatically:

- `workflow-guide` - Workflow phase guidance
- `task-context` - Active task details
- `codebase-patterns` - Project conventions

## How It Works

WIP integrates with [beads](https://github.com/steveyegge/beads) for issue tracking. All tasks and progress are tracked through `bd` commands, keeping your workflow organized without cluttering your codebase with TODO markers.

Session hooks automatically provide context about your current work when you start a Claude Code session.

## License

MIT

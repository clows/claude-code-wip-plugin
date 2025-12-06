# CLAUDE.md

**Note**: This project uses [bd (beads)](https://github.com/steveyegge/beads)
for issue tracking. Use `bd` commands instead of markdown TODOs.
See AGENTS.md for workflow details.

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Work In Project (WIP)** is a Claude Code plugin for the marketplace. It provides AI-assisted project management workflows through commands, specialized agents, and contextual skills.

See [PRD.md](PRD.md) for product requirements and component specifications.

## Project Structure

```
wip/                                      # Repository root
├── .beads/                               # Issue tracking database
├── .claude/                              # Claude Code settings
├── .github/                              # GitHub config (Copilot instructions)
├── CLAUDE.md                             # This file
├── AGENTS.md                             # AI agent workflow guide
├── PRD.md                                # Product requirements
├── wip-marketplace/                      # Local marketplace for testing
│   └── .claude-plugin/marketplace.json
└── work_in_project/                      # The plugin itself
    ├── .claude-plugin/plugin.json        # Plugin manifest (required)
    ├── commands/                         # User-invoked slash commands
    │   ├── workflow/                     # Workflow phase commands
    │   └── task/                         # Task management commands
    ├── agents/                           # Specialized subagents
    │   ├── planning/                     # Architecture, task breakdown
    │   ├── implementation/               # Coding, testing
    │   └── quality/                      # Review, documentation
    ├── skills/                           # Model-invoked contextual information
    │   └── */SKILL.md                    # Each skill in its own directory
    ├── lib/                              # Python utilities
    └── scripts/hooks/                    # Python hook scripts
```

## Development Commands

### Testing Python code
```bash
python -m pytest work_in_project/lib/
```

### Testing the plugin locally

Symlink the plugin commands to `.claude/commands/` for immediate testing:

```bash
# From the repository root:
ln -s $(pwd)/work_in_project/commands .claude/commands
```

Changes to `work_in_project/commands/` are instantly available without reloading.

**Alternative: Marketplace installation** (when `/plugin` command is available):

```bash
/plugin marketplace add ./wip-marketplace
/plugin install wip@wip-dev
```

### Managing agents
```bash
/agents  # Interactive agent management UI
```

## Plugin Manifest

`work_in_project/.claude-plugin/plugin.json` requires these fields:

```json
{
  "name": "wip",
  "version": "1.0.0",
  "description": "AI-assisted project management workflows",
  "author": {
    "name": "Your Name"
  }
}
```

## Component Formats

### Commands (`commands/*.md`)
```markdown
---
description: Brief description shown in /help
---

Prompt content that expands when the command is invoked.
```

### Agents (`agents/*.md`)
```markdown
---
name: agent-name
description: When and why to use this agent (shown in /agents)
tools: Read, Edit, Bash, Grep, Glob
model: inherit
---

System prompt defining the agent's role and behavior.
```

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Lowercase letters and hyphens |
| `description` | Yes | Purpose and when to invoke |
| `tools` | No | Comma-separated list; inherits all if omitted |
| `model` | No | `sonnet`, `opus`, `haiku`, or `inherit` |
| `skills` | No | Skills to auto-load for this agent |

### Skills (`skills/*/SKILL.md`)
```markdown
---
name: skill-name
description: What this does AND when to use it (max 1024 chars)
allowed-tools: Read, Grep, Glob
---

Instructions and contextual information for Claude.
```

Skills are **model-invoked** — Claude autonomously decides when to use them based on the description. Write descriptions that include trigger terms users would mention.

## Python Guidelines

- Use type hints
- Tests go in `work_in_project/lib/tests/`
- The `work_in_project/lib/tracker.py` module wraps optional beads integration

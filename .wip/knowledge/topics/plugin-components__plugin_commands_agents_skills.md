# Plugin Components
> Format reference for commands, agents, and skills in Claude Code plugins

## Commands (commands/*.md)

User-invoked via `/command-name`. Expand to prompt text.

```markdown
---
description: Brief description shown in /help
---

Prompt content that expands when invoked.
Use {{arg}} for arguments from /command arg.
```

**Location**: `commands/` or `commands/group/name.md`
**Invocation**: `/wip:group:name` or `/wip:name`

## Agents (agents/*.md)

Specialized subagents spawned via Task tool.

```markdown
---
name: agent-name
description: When to use this agent (shown in Task tool)
tools: Read, Edit, Bash, Grep, Glob
model: inherit
---

System prompt defining agent behavior.
```

| Field | Required | Values |
|-------|----------|--------|
| name | Yes | lowercase-with-hyphens |
| description | Yes | Purpose + trigger conditions |
| tools | No | Comma-separated; inherits all if omitted |
| model | No | sonnet, opus, haiku, inherit |

**Location**: `agents/category/name.md`

## Skills (skills/*/SKILL.md)

Model-invoked contextual information. Claude decides when to use.

```markdown
---
name: skill-name
description: What it does AND when to use (max 1024 chars)
allowed-tools: Read, Grep, Glob
---

Instructions and reference information.
```

**Key difference**: Skills are auto-invoked by Claude based on description matching user intent. Commands require explicit `/invoke`.

**Location**: `skills/skill-name/SKILL.md`

## Hooks (scripts/hooks/*.py)

Python scripts triggered by Claude Code events.

```python
import json, sys

hook_input = json.load(sys.stdin)
# Process event...

output = {
    "hookSpecificOutput": {
        "hookEventName": "SessionStart",
        "additionalContext": "text for Claude"
    },
    "continue": True,
    "suppressOutput": False
}
print(json.dumps(output))
sys.exit(0)
```

## Notes

- Commands show in `/help`, skills don't
- Agent descriptions appear in Task tool selection
- Skill descriptions must include trigger keywords
- Hooks must exit 0 for success
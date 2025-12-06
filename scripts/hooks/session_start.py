#!/usr/bin/env python3
"""
SessionStart hook for WIP plugin.

Loads workflow context at session start by querying beads for
active/ready tasks and outputting current workflow state.

Handles graceful degradation when beads is unavailable.
"""

import json
import sys
from pathlib import Path

# Add lib to path for tracker import
lib_path = Path(__file__).parent.parent.parent / "lib"
sys.path.insert(0, str(lib_path))

from tracker import is_available, list_issues, get_ready, get_stats


SESSION_CLOSE_PROTOCOL = """
## Session Close Protocol

Before completing work, run this checklist:
1. `git status` - Check what changed
2. `git add <files>` - Stage code changes
3. `bd sync --from-main` - Pull beads updates from main
4. `git commit -m "..."` - Commit changes
""".strip()


CORE_RULES = """
## Core Rules
- Track ALL work in beads (no TodoWrite, no markdown TODOs)
- Use `bd create` for new issues
- Check `bd ready` for available work
""".strip()


ESSENTIAL_COMMANDS = """
## Essential Commands
- `bd ready` - Unblocked work
- `bd list --status=in_progress` - Active work
- `bd create --title="..." --type=task` - New issue
- `bd update <id> --status=in_progress` - Claim work
- `bd close <id>` - Complete work
- `bd sync --from-main` - Sync before commit
""".strip()


AGENT_INSTRUCTION = """
**IMPORTANT**: On your first response this session, briefly greet the user with:
- Current active work (if any)
- Ready tasks available
- Keep it to 2-3 lines, e.g.: "You have 1 task in progress and 2 ready. Run `bd ready` for details."
""".strip()


def get_workflow_context() -> str:
    """Build workflow context string for Claude."""
    lines = ["# WIP Workflow Context"]

    # Instruction to display summary to user
    lines.append("")
    lines.append(AGENT_INSTRUCTION)

    # Always show session close protocol first (critical)
    lines.append("")
    lines.append(SESSION_CLOSE_PROTOCOL)

    if not is_available():
        lines.append("")
        lines.append("Beads issue tracker not available. Use `/wip:task:create` to track work manually.")
        return "\n".join(lines)

    # Core rules
    lines.append("")
    lines.append(CORE_RULES)

    # Get in-progress tasks
    success, in_progress = list_issues(status="in_progress")
    if success and in_progress and "No issues found" not in in_progress:
        lines.append("")
        lines.append("## Active Work")
        lines.append(in_progress)

    # Get ready tasks
    success, ready = get_ready()
    if success and ready and "No issues" not in ready.lower():
        lines.append("")
        lines.append("## Ready to Start")
        lines.append(ready)

    # Get stats summary
    success, stats = get_stats()
    if success and stats:
        lines.append("")
        lines.append("## Project Status")
        lines.append(stats)

    # Essential commands reference
    lines.append("")
    lines.append(ESSENTIAL_COMMANDS)

    return "\n".join(lines)


def main():
    # Read hook input (not currently used, but available for future)
    try:
        hook_input = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        hook_input = {}

    # Output workflow context as structured JSON
    context = get_workflow_context()
    output = {
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": context
        },
        "continue": True,
        "suppressOutput": False
    }
    print(json.dumps(output))

    # Exit 0 for success
    sys.exit(0)


if __name__ == "__main__":
    main()

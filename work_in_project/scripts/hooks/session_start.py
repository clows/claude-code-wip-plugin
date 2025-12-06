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


def get_workflow_context() -> str:
    """Build workflow context string for Claude."""
    lines = ["# WIP Workflow Context"]

    if not is_available():
        lines.append("")
        lines.append("Beads issue tracker not available. Use `/wip:task:create` to track work manually.")
        return "\n".join(lines)

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

    # Add quick reference
    lines.append("")
    lines.append("## Quick Commands")
    lines.append("- `bd ready` - Show unblocked work")
    lines.append("- `bd update <id> --status=in_progress` - Claim a task")
    lines.append("- `bd close <id>` - Complete a task")
    lines.append("- `/wip:workflow:implement` - Focus on current task")

    return "\n".join(lines)


def main():
    # Read hook input (not currently used, but available for future)
    try:
        hook_input = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        hook_input = {}

    # Output workflow context
    context = get_workflow_context()
    print(context)

    # Exit 0 for success
    sys.exit(0)


if __name__ == "__main__":
    main()

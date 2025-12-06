#!/usr/bin/env python3
"""
SessionStart hook for WIP plugin.

Outputs dynamic beads data (active tasks, ready tasks, stats).
Static instructions are handled by the prompt hook in hooks/session_greeting.md.

Handles graceful degradation when beads is unavailable.
"""

import json
import sys
from pathlib import Path

# Add lib to path for tracker import
lib_path = Path(__file__).parent.parent.parent / "lib"
sys.path.insert(0, str(lib_path))

from tracker import is_available, list_issues, get_ready, get_stats


def get_workflow_data() -> str:
    """Build workflow data string for Claude (data only, no instructions)."""
    lines = []

    if not is_available():
        lines.append("Beads issue tracker not available.")
        return "\n".join(lines)

    # Get in-progress tasks
    success, in_progress = list_issues(status="in_progress")
    if success and in_progress and "No issues found" not in in_progress:
        lines.append("## Active Work")
        lines.append(in_progress)

    # Get ready tasks
    success, ready = get_ready()
    if success and ready and "No issues" not in ready.lower():
        if lines:
            lines.append("")
        lines.append("## Ready to Start")
        lines.append(ready)

    # Get stats summary
    success, stats = get_stats()
    if success and stats:
        if lines:
            lines.append("")
        lines.append("## Project Status")
        lines.append(stats)

    if not lines:
        lines.append("No active or ready tasks.")

    return "\n".join(lines)


def main():
    # Read hook input (not currently used, but available for future)
    try:
        hook_input = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        hook_input = {}

    # Output workflow data as structured JSON (instructions come from prompt hook)
    data = get_workflow_data()
    output = {
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": data
        },
        "continue": True,
        "suppressOutput": False
    }
    print(json.dumps(output))

    # Exit 0 for success
    sys.exit(0)


if __name__ == "__main__":
    main()

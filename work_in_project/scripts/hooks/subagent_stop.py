#!/usr/bin/env python3
"""
SubagentStop hook for WIP plugin.

Tracks agent work completion by logging which agent finished,
updating beads tasks with progress notes, and checking for
blockers in agent output.
"""

import json
import sys
from pathlib import Path
from typing import Optional

# Add lib to path for tracker import
lib_path = Path(__file__).parent.parent.parent / "lib"
sys.path.insert(0, str(lib_path))

from tracker import is_available, list_issues

# Map agent types to workflow phases
AGENT_PHASES = {
    "architect": "plan",
    "breakdown": "plan",
    "implementer": "implement",
    "tester": "test",
    "reviewer": "review",
    "documenter": "ship",
}

# Keywords that might indicate blockers
BLOCKER_KEYWORDS = [
    "blocked",
    "blocking",
    "cannot proceed",
    "depends on",
    "waiting for",
    "need to first",
    "requires",
    "missing",
    "not found",
    "error:",
    "failed:",
]


def extract_agent_name(hook_input: dict) -> Optional[str]:
    """Extract agent name from hook input."""
    # The Task tool input contains subagent_type
    tool_input = hook_input.get("tool_input", {})
    if isinstance(tool_input, str):
        try:
            tool_input = json.loads(tool_input)
        except json.JSONDecodeError:
            return None

    return tool_input.get("subagent_type")


def check_for_blockers(output: str) -> list[str]:
    """Check agent output for potential blockers."""
    blockers = set()

    for line in output.split("\n"):
        lower_line = line.lower()
        for keyword in BLOCKER_KEYWORDS:
            if keyword in lower_line:
                blockers.add(line.strip())
                break  # Only add line once

    return list(blockers)[:3]  # Limit to 3 blockers


def get_progress_summary(agent_name: str, hook_input: dict) -> Optional[str]:
    """Generate a progress summary based on agent completion."""
    if not is_available():
        return None

    phase = AGENT_PHASES.get(agent_name)
    if not phase:
        return None

    # Get tool output/result if available
    tool_output = hook_input.get("tool_output", "")
    if isinstance(tool_output, dict):
        tool_output = tool_output.get("result", "")

    lines = [f"## Agent Complete: {agent_name}"]
    lines.append(f"Phase: {phase}")

    # Check for blockers in output
    if tool_output:
        blockers = check_for_blockers(str(tool_output))
        if blockers:
            lines.append("")
            lines.append("**Potential blockers detected:**")
            for b in blockers:
                lines.append(f"- {b[:100]}")  # Truncate long lines

    # Show current in-progress tasks
    success, in_progress = list_issues(status="in_progress")
    if success and in_progress and "No issues found" not in in_progress:
        lines.append("")
        lines.append("**Active tasks:**")
        lines.append(in_progress)

    return "\n".join(lines)


def main():
    # Read hook input
    try:
        hook_input = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        hook_input = {}

    # Extract agent name
    agent_name = extract_agent_name(hook_input)

    if agent_name:
        summary = get_progress_summary(agent_name, hook_input)
        if summary:
            print(summary)

    # Exit 0 for success (non-blocking)
    sys.exit(0)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Stop hook for WIP plugin.

Checks workflow phase completion when Claude stops and nudges
toward the next phase (e.g., remind to test after implementing).

Also checks if knowledge base updates might be needed based on
recent code changes.

Outputs reminders as context for the user's next interaction.
"""

import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Optional

# Add lib to path for tracker import
lib_path = Path(__file__).parent.parent.parent / "lib"
sys.path.insert(0, str(lib_path))

from tracker import is_available, list_issues, get_stats


# Workflow phase progression
PHASE_NEXT = {
    "brainstorm": "plan",
    "plan": "implement",
    "implement": "test",
    "test": "review",
    "review": "ship",
    "ship": None,
}

PHASE_COMMANDS = {
    "plan": "/wip:workflow:plan",
    "implement": "/wip:workflow:implement",
    "test": "/wip:workflow:test",
    "review": "/wip:workflow:review",
    "ship": "/wip:workflow:ship",
}


def detect_phase_from_tasks(in_progress_output: str) -> Optional[str]:
    """Try to detect current phase from task types/titles."""
    lower = in_progress_output.lower()

    if "test" in lower:
        return "test"
    elif "review" in lower:
        return "review"
    elif "implement" in lower or "feature" in lower or "bug" in lower:
        return "implement"
    elif "plan" in lower or "design" in lower or "architect" in lower:
        return "plan"
    elif "doc" in lower or "ship" in lower or "release" in lower:
        return "ship"

    return None


def get_completion_check() -> Optional[str]:
    """Check workflow state and return reminder if needed."""
    if not is_available():
        return None

    # Get in-progress tasks
    success, in_progress = list_issues(status="in_progress")
    if not success:
        return None

    has_in_progress = in_progress and "No issues found" not in in_progress

    if has_in_progress:
        # Detect current phase
        phase = detect_phase_from_tasks(in_progress)
        next_phase = PHASE_NEXT.get(phase) if phase else None

        lines = ["## Session End Reminder"]
        lines.append("")
        lines.append("You have tasks still in progress:")
        lines.append(in_progress)

        if next_phase and next_phase in PHASE_COMMANDS:
            lines.append("")
            lines.append(f"When ready, consider moving to **{next_phase}** phase:")
            lines.append(f"  `{PHASE_COMMANDS[next_phase]}`")

        return "\n".join(lines)

    # No in-progress tasks - check if there's ready work
    from tracker import get_ready
    success, ready = get_ready()

    if success and ready and "No issues" not in ready.lower():
        lines = ["## Session End Reminder"]
        lines.append("")
        lines.append("All current tasks complete. Ready work available:")
        lines.append(ready)
        return "\n".join(lines)

    return None


def check_knowledge_updates() -> Optional[str]:
    """Check if knowledge base updates might be needed based on recent changes."""
    # Check if knowledge base exists
    kb_path = Path.cwd() / ".wip" / "knowledge"
    if not kb_path.exists():
        return None

    try:
        # Get recent changes (staged + unstaged)
        result = subprocess.run(
            ["git", "diff", "--name-only", "HEAD"],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode != 0:
            return None

        changed_files = [f for f in result.stdout.strip().split("\n") if f]

        if not changed_files:
            return None

        # Patterns that suggest interface/API changes worth documenting
        significant_patterns = [
            r"api[/\\]",
            r"interface",
            r"schema",
            r"config",
            r"types?\.(ts|py|go)",
            r"__init__\.py",
            r"index\.(ts|js)",
            r"public[/\\]",
            r"exports?",
        ]

        significant_changes = []
        for f in changed_files:
            for pattern in significant_patterns:
                if re.search(pattern, f, re.IGNORECASE):
                    significant_changes.append(f)
                    break

        if not significant_changes:
            return None

        # Check if any knowledge entries might be stale
        # Compare file modification times
        topics_path = kb_path / "topics"
        if topics_path.exists():
            kb_files = list(topics_path.glob("*.md"))
            if kb_files:
                oldest_kb_mtime = min(f.stat().st_mtime for f in kb_files)

                # Check if changed files are newer than oldest KB entry
                stale_entries = []
                for f in significant_changes[:5]:  # Limit to first 5
                    file_path = Path.cwd() / f
                    if file_path.exists():
                        if file_path.stat().st_mtime > oldest_kb_mtime:
                            stale_entries.append(f)

                if stale_entries:
                    lines = ["## Knowledge Base Reminder"]
                    lines.append("")
                    lines.append("Recent changes may warrant knowledge base updates:")
                    for f in stale_entries[:3]:
                        lines.append(f"  - {f}")
                    lines.append("")
                    lines.append("Consider updating `.wip/knowledge/` entries if interfaces changed.")
                    return "\n".join(lines)

        # If we have significant changes but no KB entries yet
        if len(significant_changes) >= 2:
            lines = ["## Knowledge Base Reminder"]
            lines.append("")
            lines.append("Significant files changed that may benefit from documentation:")
            for f in significant_changes[:3]:
                lines.append(f"  - {f}")
            lines.append("")
            lines.append("Consider adding entries to `.wip/knowledge/` for key interfaces.")
            return "\n".join(lines)

    except Exception:
        pass

    return None


def main():
    # Read hook input
    try:
        hook_input = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        hook_input = {}

    # Check for completion reminders
    reminder = get_completion_check()

    if reminder:
        print(reminder)

    # Check for knowledge base update suggestions
    kb_reminder = check_knowledge_updates()

    if kb_reminder:
        if reminder:
            print("")  # Separator
        print(kb_reminder)

    # Exit 0 for success (non-blocking)
    sys.exit(0)


if __name__ == "__main__":
    main()

"""
Beads issue tracker wrapper for WIP plugin.

Provides a Python interface to beads (bd) commands for optional
integration with the WIP workflow. This is opt-in - the plugin
works standalone without beads installed.
"""

import subprocess
import shutil
from dataclasses import dataclass
from typing import Optional


@dataclass
class Issue:
    """Represents a beads issue."""
    id: str
    title: str
    status: str
    priority: Optional[str] = None
    issue_type: Optional[str] = None


def is_available() -> bool:
    """Check if beads (bd) is installed and available."""
    return shutil.which("bd") is not None


def _run_bd(*args: str) -> tuple[bool, str]:
    """Run a bd command and return (success, output)."""
    if not is_available():
        return False, "beads (bd) is not installed"

    try:
        result = subprocess.run(
            ["bd", "--no-daemon", *args],
            capture_output=True,
            text=True,
            timeout=30
        )
        output = result.stdout + result.stderr
        return result.returncode == 0, output.strip()
    except subprocess.TimeoutExpired:
        return False, "Command timed out"
    except Exception as e:
        return False, str(e)


def create_issue(
    title: str,
    issue_type: str = "task",
    priority: int = 2,
    description: Optional[str] = None
) -> tuple[bool, str]:
    """
    Create a new beads issue.

    Args:
        title: Issue title
        issue_type: One of: feature, bug, task, chore
        priority: 1-4 (1 is highest)
        description: Optional description

    Returns:
        (success, issue_id or error message)
    """
    args = [
        "create",
        f"--title={title}",
        f"--type={issue_type}",
        f"--priority={priority}"
    ]
    if description:
        args.append(f"--description={description}")

    success, output = _run_bd(*args)

    if success:
        # Extract issue ID from output like "Created issue: work_in_project-abc"
        for line in output.split("\n"):
            if "Created issue:" in line:
                parts = line.split(":")
                if len(parts) >= 2:
                    return True, parts[1].strip()

    return success, output


def update_status(issue_id: str, status: str) -> tuple[bool, str]:
    """
    Update an issue's status.

    Args:
        issue_id: The issue ID
        status: One of: open, in_progress, closed

    Returns:
        (success, message)
    """
    return _run_bd("update", issue_id, f"--status={status}")


def close_issue(issue_id: str, reason: Optional[str] = None) -> tuple[bool, str]:
    """
    Close an issue.

    Args:
        issue_id: The issue ID
        reason: Optional reason for closing

    Returns:
        (success, message)
    """
    args = ["close", issue_id]
    if reason:
        args.append(f"--reason={reason}")
    return _run_bd(*args)


def add_dependency(child_id: str, parent_id: str) -> tuple[bool, str]:
    """
    Add a dependency between issues.

    Args:
        child_id: The issue that depends on another
        parent_id: The issue that blocks the child

    Returns:
        (success, message)
    """
    return _run_bd("dep", "add", child_id, parent_id)


def get_ready() -> tuple[bool, str]:
    """
    Get issues ready to work (no blockers).

    Returns:
        (success, output listing ready issues)
    """
    return _run_bd("ready")


def get_blocked() -> tuple[bool, str]:
    """
    Get blocked issues.

    Returns:
        (success, output listing blocked issues)
    """
    return _run_bd("blocked")


def get_stats() -> tuple[bool, str]:
    """
    Get project statistics.

    Returns:
        (success, stats output)
    """
    return _run_bd("stats")


def list_issues(status: Optional[str] = None) -> tuple[bool, str]:
    """
    List issues, optionally filtered by status.

    Args:
        status: Optional status filter (open, in_progress, closed)

    Returns:
        (success, output listing issues)
    """
    args = ["list"]
    if status:
        args.append(f"--status={status}")
    return _run_bd(*args)


def show_issue(issue_id: str) -> tuple[bool, str]:
    """
    Show details of a specific issue.

    Args:
        issue_id: The issue ID

    Returns:
        (success, issue details)
    """
    return _run_bd("show", issue_id)

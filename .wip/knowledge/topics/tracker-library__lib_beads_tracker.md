# Tracker Library
> Python wrapper for beads (bd) issue tracking commands

## Interface

```python
from lib.tracker import (
    is_available,      # Check if bd is installed
    create_issue,      # Create new issue
    update_status,     # Update issue status
    close_issue,       # Close an issue
    add_dependency,    # Link issues
    get_ready,         # Get unblocked issues
    get_blocked,       # Get blocked issues
    get_stats,         # Project statistics
    list_issues,       # List with optional status filter
    show_issue,        # Get issue details
)
```

## Data Types

```python
@dataclass
class Issue:
    id: str
    title: str
    status: str  # open, in_progress, closed
    priority: Optional[str]  # 1-4 (1 highest)
    issue_type: Optional[str]  # feature, bug, task, chore
```

## Usage

```python
from lib.tracker import is_available, create_issue, list_issues

# Always check availability first
if not is_available():
    print("beads not installed")
    return

# Create an issue
success, issue_id = create_issue(
    title="Add user auth",
    issue_type="feature",
    priority=2,
    description="Implement OAuth2"
)

# List open issues
success, output = list_issues(status="open")

# All functions return (success: bool, result: str)
```

## Notes

- All functions return  tuple
- Uses  flag for reliability
- 30-second timeout on all commands
- Graceful degradation when bd unavailable
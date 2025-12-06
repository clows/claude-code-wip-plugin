---
description: Update or add knowledge base entries
---

# Knowledge Base Update

You are updating the project's knowledge base with new or changed information.

## Current State

First, check the knowledge base status:

```bash
# List existing entries
cat .wip/knowledge/index.json | python3 -m json.tool

# Get stats
python3 -c "
import sys; sys.path.insert(0, 'lib')
from knowledge import get_stats, is_initialized
if is_initialized():
    success, stats = get_stats()
    print(f'Entries: {stats[\"total_entries\"]}')
    print(f'Total lines: {stats[\"total_lines\"]}')
    print(f'Tags: {stats[\"tags\"]}')
else:
    print('Knowledge base not initialized. Run /wip:knowledge:init first.')
"
```

## Update Workflow

### 1. Identify What Changed

Check recent code changes:
```bash
git diff --name-only HEAD~5  # Last 5 commits
git diff --stat              # Current uncommitted changes
```

### 2. Find Related KB Entries

Search for entries that might need updating:
```bash
grep -i 'keyword' .wip/knowledge/index.json
```

### 3. Update or Create

**To update an existing entry:**
```python
import sys; sys.path.insert(0, 'lib')
from knowledge import update_entry

new_content = """# Updated Title
> Updated summary

## Interface
Updated interface docs...

## Usage
Updated examples...
"""

update_entry("topics/existing__file.md", new_content)
```

**To add a new entry:**
```python
from knowledge import add_entry

add_entry(
    title="New Feature",
    summary="What it does",
    content="## Interface\n...\n\n## Usage\n...",
    tags=["feature", "api"]
)
```

### 4. Verify Changes

After updating:
```bash
# Rebuild index to pick up changes
python3 -c "from lib.knowledge import rebuild_index; print(rebuild_index())"

# Verify entry is searchable
python3 -c "
from lib.knowledge import search
success, entries = search('your keyword')
for e in entries:
    print(f'{e.path}: {e.summary}')
"
```

## Entry Format Reminder

```markdown
# Title
> One-line summary (searchable)

## Interface
Public APIs, function signatures

## Usage
Code examples

## Notes
Gotchas, related info
```

## Common Updates

| Scenario | Action |
|----------|--------|
| API changed | Update Interface section |
| New examples needed | Add to Usage section |
| Bug workaround found | Add to Notes section |
| Module renamed | Delete old entry, create new |
| Entry too large | Split with `check_and_split()` |

## Size Limits

Entries should stay under 250 lines. If larger, they'll be auto-split by `##` sections when updated.

---

What would you like to update in the knowledge base?

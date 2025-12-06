---
description: Update or add knowledge base entries
---

# Knowledge Base Update

You are updating the project's knowledge base with new or changed information.

## Current State

First, check the knowledge base status:

```bash
# Get stats
python3 lib/knowledge.py stats -f text

# List all entries (search with empty query)
python3 lib/knowledge.py search "" -f text
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
python3 lib/knowledge.py search "keyword" -f text
```

### 3. Update or Create

**To update an existing entry:**
```bash
python3 lib/knowledge.py update topics/existing__file.md \
  --content "# Updated Title
> Updated summary

## Interface
Updated interface docs...

## Usage
Updated examples..."
```

**To add a new entry:**
```bash
python3 lib/knowledge.py add \
  --title "New Feature" \
  --summary "What it does" \
  --content "## Interface\n- \`func()\` — description\n\n## Usage\n..." \
  --tags feature,api
```

**To delete an entry:**
```bash
python3 lib/knowledge.py delete topics/obsolete__file.md
```

### 4. Verify Changes

After updating:
```bash
# Rebuild index to pick up changes
python3 lib/knowledge.py rebuild

# Verify entry is searchable
python3 lib/knowledge.py search "your keyword" -f text
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
| Entry too large | Will auto-split by `##` sections on update |

## Size Limits

Entries should stay under 250 lines. If larger, they'll be auto-split by `##` sections when updated.

---

What would you like to update in the knowledge base?

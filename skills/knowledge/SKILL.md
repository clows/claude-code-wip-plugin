---
name: knowledge
description: Queries project knowledge base for interfaces, usage patterns, and examples. Use when implementing features, understanding APIs, looking up how something works, or when user asks about codebase patterns.
allowed-tools: Read, Grep, Glob, Bash
---

# Knowledge Base Skill

This skill provides access to the project's living knowledge base — documented interfaces, patterns, and examples that evolve with the code.

## When to Use This Skill

- Implementing a feature that uses existing APIs
- Looking up how something is done in this project
- Understanding interface contracts before making changes
- Finding code examples for common patterns
- Answering "how does X work?" questions

## Two-Phase Query Process

The knowledge base uses a two-phase query to minimize context usage:

### Phase 1: Search

Query the index to find relevant entries:

```bash
# Search by keywords
python3 lib/knowledge.py search "auth api" --format text

# Search with tag filter
python3 lib/knowledge.py search "endpoint" --tags api,rest --format text

# Get JSON output for programmatic use
python3 lib/knowledge.py search "config"
```

### Phase 2: Load Selected Files

Once you identify relevant entries, load only what you need:

```bash
# Load specific knowledge file(s)
python3 lib/knowledge.py load topics/api__auth.md --format text

# Load multiple files
python3 lib/knowledge.py load topics/api__auth.md topics/config__settings.md
```

## Knowledge File Format

Each file follows this structure:

```markdown
# Title
> One-line summary (appears in search results)

## Interface
Public APIs and function signatures

## Usage
Code examples

## Notes
Important gotchas and related info
```

## Quick Commands

| Goal | Command |
|------|---------|
| Search for topic | `python3 lib/knowledge.py search "topic" -f text` |
| Load specific file | `python3 lib/knowledge.py load topics/file.md -f text` |
| Get KB stats | `python3 lib/knowledge.py stats -f text` |
| List all entries | `python3 lib/knowledge.py search "" -f text` |
| Rebuild index | `python3 lib/knowledge.py rebuild` |

## Filename Convention

Files use `topic__tag1_tag2.md` format:
- `api__auth_jwt.md` — API documentation for JWT auth
- `patterns__error-handling.md` — Error handling patterns
- `components__user-service.md` — User service component

## Updating Knowledge

If you discover outdated or missing knowledge during implementation:

1. **Note the gap** — What's missing or wrong?
2. **Suggest update** — Mention to user that knowledge should be updated
3. **Create/update entry**:

```bash
# Add new entry
python3 lib/knowledge.py add \
  --title "Feature Name" \
  --summary "What it does" \
  --content "## Interface\n..." \
  --tags feature,api

# Update existing entry
python3 lib/knowledge.py update topics/file.md \
  --content "# Updated Title\n> Updated summary\n\n## Interface\n..."
```

## Tips

- Search broadly first, then narrow with tags
- The summary line (`>`) contains the most relevant keywords
- Related entries often share tags
- If knowledge seems stale, check when source files were last modified

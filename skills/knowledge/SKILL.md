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
# Search by keyword in filenames and summaries
grep -i 'keyword' .wip/knowledge/index.json

# Or use the Python module
python3 -c "
import sys; sys.path.insert(0, 'lib')
from knowledge import search
success, entries = search('your keywords here')
if success:
    for e in entries:
        print(f'{e.path}: {e.summary}')
"
```

### Phase 2: Load Selected Files

Once you identify relevant entries, load only what you need:

```bash
# Read specific knowledge file
cat .wip/knowledge/topics/api__auth.md
```

Or programmatically:
```python
from lib.knowledge import load
success, contents = load(['topics/api__auth.md'])
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
| List all entries | `cat .wip/knowledge/index.json \| python3 -m json.tool` |
| Search for topic | `grep -i 'topic' .wip/knowledge/index.json` |
| Read specific file | `cat .wip/knowledge/topics/filename.md` |
| Get KB stats | `python3 -c "from lib.knowledge import get_stats; print(get_stats())"` |

## Filename Convention

Files use `topic__tag1_tag2.md` format:
- `api__auth_jwt.md` — API documentation for JWT auth
- `patterns__error-handling.md` — Error handling patterns
- `components__user-service.md` — User service component

## Updating Knowledge

If you discover outdated or missing knowledge during implementation:

1. **Note the gap** — What's missing or wrong?
2. **Suggest update** — Mention to user that knowledge should be updated
3. **Create/update entry** — Use `lib.knowledge.add_entry()` or `update_entry()`

## Tips

- Search broadly first, then narrow with tags
- The summary line (`>`) contains the most relevant keywords
- Related entries often share tags
- If knowledge seems stale, check when source files were last modified

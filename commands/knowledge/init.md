---
description: Initialize knowledge base from codebase scan
---

# Knowledge Base Initialization

You are initializing the project's knowledge base by scanning the codebase for documentable interfaces.

## Your Task

1. **Scan for key interfaces** — Find public APIs, exported functions, and important modules
2. **Generate knowledge entries** — Create markdown files in `.wip/knowledge/topics/`
3. **Update the index** — Rebuild index.json to include new entries

## What to Document

Focus on these patterns (in priority order):

1. **Public APIs** — REST endpoints, GraphQL schemas, CLI commands
2. **Exported modules** — `__init__.py`, `index.ts`, public interfaces
3. **Configuration** — Config files, environment variables, settings
4. **Core abstractions** — Key classes, patterns, architectural decisions

## File Discovery

Use these commands to find documentable files:

```bash
# Python: Find public modules
find . -name "__init__.py" -o -name "*.py" | grep -v __pycache__ | head -20

# TypeScript/JS: Find index files and types
find . -name "index.ts" -o -name "index.js" -o -name "types.ts" | head -20

# Config files
find . -name "*.json" -o -name "*.yaml" -o -name "*.toml" | grep -E "(config|settings)" | head -10

# API routes
find . -path "*/api/*" -name "*.py" -o -path "*/routes/*" -name "*.ts" | head -20
```

## Knowledge Entry Format

For each significant module/interface, create an entry:

```markdown
# Module Name
> One-line description of what it does

## Interface
- `function_name(args)` → return type
- `ClassName` — brief description

## Usage
\```python
# Example code
\```

## Notes
- Important gotchas
- Related modules
```

## Creating Entries

Use the knowledge library:

```python
import sys
sys.path.insert(0, 'lib')
from knowledge import add_entry, rebuild_index

# Add an entry
add_entry(
    title="Module Name",
    summary="What it does",
    content="## Interface\n...\n\n## Usage\n...",
    tags=["module", "api"]
)

# Or write files directly to .wip/knowledge/topics/
# Then rebuild index
rebuild_index()
```

## Filename Convention

Use `topic__tag1_tag2.md`:
- `lib__tracker_beads.md` — Tracker library for beads
- `api__auth_jwt.md` — Auth API with JWT
- `config__settings.md` — Configuration settings

## Workflow

1. **Explore** — Scan the codebase structure
2. **Identify** — List the most important interfaces (5-10 to start)
3. **Confirm** — Ask user which ones to document
4. **Generate** — Create knowledge entries
5. **Verify** — Show what was created

## Important

- Start with 5-10 key entries, not everything
- Focus on interfaces users of the code need to understand
- Keep entries concise (under 250 lines)
- Ask user for confirmation before bulk generation

---

What codebase would you like to initialize knowledge for? I'll scan for key interfaces.

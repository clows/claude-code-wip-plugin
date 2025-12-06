# Knowledge Library
> API for managing the project knowledge base in .wip/knowledge/

## Interface

```python
from lib.knowledge import (
    # Setup
    is_initialized,    # Check if KB exists
    initialize,        # Create KB structure
    
    # Two-phase query
    search,            # Phase 1: search index
    load,              # Phase 2: load full content
    
    # CRUD operations
    add_entry,         # Create new entry
    update_entry,      # Modify existing
    delete_entry,      # Remove entry
    
    # Maintenance
    rebuild_index,     # Regenerate index.json
    check_and_split,   # Split large files
    get_stats,         # KB statistics
)
```

## Data Types

```python
@dataclass
class KnowledgeEntry:
    path: str      # e.g., "topics/api__auth.md"
    title: str     # From # header
    summary: str   # From > blockquote
    tags: list[str]  # From filename
    lines: int     # Line count
```

## Usage

### Search and Load (Two-Phase)

```python
from lib.knowledge import search, load

# Phase 1: Search index
success, entries = search("auth api", tags=["api"])
for e in entries:
    print(f"{e.path}: {e.summary}")

# Phase 2: Load selected files
success, contents = load(["topics/api__auth.md"])
```

### Add Entry

```python
from lib.knowledge import add_entry

success, path = add_entry(
    title="Auth API",
    summary="JWT authentication endpoints",
    content="## Interface\n...\n## Usage\n...",
    tags=["api", "auth"]
)
# Creates: topics/auth-api__api_auth.md
```

## File Structure

```
.wip/knowledge/
├── index.json      # Search index
└── topics/         # Knowledge files
    └── topic__tag1_tag2.md
```

## Notes

- MAX_LINES = 250 (auto-splits larger files)
- Filename format: `topic__tag1_tag2.md`
- Summary extracted from `> blockquote` after `# title`
- Search scores: title (3pts), summary (2pts), tags (1pt)
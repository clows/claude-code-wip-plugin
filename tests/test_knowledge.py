"""Tests for lib/knowledge.py"""

import json
import pytest
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from lib import knowledge
from lib.knowledge import (
    KnowledgeEntry,
    initialize,
    is_initialized,
    search,
    load,
    add_entry,
    update_entry,
    delete_entry,
    rebuild_index,
    check_and_split,
    get_stats,
    _extract_summary,
    _extract_title,
    _generate_filename,
    _parse_tags_from_filename,
    _score_entry,
    MAX_LINES,
)


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def empty_kb(tmp_path):
    """Create an empty knowledge base."""
    initialize(project_root=tmp_path)
    return tmp_path


@pytest.fixture
def knowledge_base(tmp_path):
    """Create a knowledge base with sample entries."""
    kb_root = tmp_path / ".wip" / "knowledge"
    kb_root.mkdir(parents=True)
    (kb_root / "topics").mkdir()

    # Create sample entries
    (kb_root / "topics" / "api__auth_jwt.md").write_text("""# JWT Authentication
> Token-based auth with refresh flow

## Interface
- `create_token(user_id)` → JWT string
- `verify_token(token)` → user_id or None

## Usage
```python
token = create_token(123)
```

## Notes
Tokens expire after 1 hour.
""")

    (kb_root / "topics" / "api__user_endpoints.md").write_text("""# User API Endpoints
> REST endpoints for user management

## Interface
- GET /users - List all users
- GET /users/:id - Get user by ID
- POST /users - Create user

## Usage
```bash
curl -X GET /api/users
```
""")

    (kb_root / "topics" / "patterns__error-handling.md").write_text("""# Error Handling Patterns
> Consistent error handling across the codebase

## Interface
- `AppError` - Base error class
- `ValidationError` - Input validation failures
- `NotFoundError` - Resource not found

## Usage
```python
raise ValidationError("Invalid email format")
```
""")

    # Initialize index
    rebuild_index(project_root=tmp_path)
    return tmp_path


# ============================================================================
# Unit Tests - Initialization
# ============================================================================

def test_initialize(tmp_path):
    """Creates directory structure and empty index."""
    success, msg = initialize(project_root=tmp_path)

    assert success
    assert (tmp_path / ".wip" / "knowledge" / "index.json").exists()
    assert (tmp_path / ".wip" / "knowledge" / "topics").is_dir()

    # Verify index structure
    with open(tmp_path / ".wip" / "knowledge" / "index.json") as f:
        data = json.load(f)
    assert data["version"] == 1
    assert data["entries"] == []


def test_is_initialized_true(empty_kb):
    """Returns True when KB is properly initialized."""
    assert is_initialized(project_root=empty_kb)


def test_is_initialized_false(tmp_path):
    """Returns False when KB doesn't exist."""
    assert not is_initialized(project_root=tmp_path)


# ============================================================================
# Unit Tests - Search
# ============================================================================

def test_search_by_keyword(knowledge_base):
    """Matches keywords in title, summary, tags."""
    success, entries = search("authentication", project_root=knowledge_base)

    assert success
    assert len(entries) >= 1
    assert any("JWT" in e.title for e in entries)


def test_search_with_tags(knowledge_base):
    """Filters results by tag list."""
    success, entries = search("api", tags=["auth"], project_root=knowledge_base)

    assert success
    # Should find the auth-related entry
    assert all(any("auth" in t.lower() for t in e.tags) for e in entries)


def test_search_scoring(knowledge_base):
    """Title matches rank higher than summary."""
    success, entries = search("JWT", project_root=knowledge_base)

    assert success
    assert len(entries) >= 1
    # JWT is in the title, should be first result
    assert "JWT" in entries[0].title


def test_search_empty_query(knowledge_base):
    """Empty query returns all entries up to limit."""
    success, entries = search("", project_root=knowledge_base)

    assert success
    assert len(entries) == 3  # All sample entries


def test_search_no_matches(knowledge_base):
    """Returns empty list when no matches found."""
    success, entries = search("nonexistent_keyword_xyz", project_root=knowledge_base)

    assert success
    assert len(entries) == 0


# ============================================================================
# Unit Tests - Load
# ============================================================================

def test_load_single_file(knowledge_base):
    """Returns content dict for one path."""
    success, contents = load(["topics/api__auth_jwt.md"], project_root=knowledge_base)

    assert success
    assert "topics/api__auth_jwt.md" in contents
    assert "JWT Authentication" in contents["topics/api__auth_jwt.md"]


def test_load_multiple_files(knowledge_base):
    """Returns content dict for multiple paths."""
    paths = ["topics/api__auth_jwt.md", "topics/api__user_endpoints.md"]
    success, contents = load(paths, project_root=knowledge_base)

    assert success
    assert len(contents) == 2
    assert "JWT" in contents["topics/api__auth_jwt.md"]
    assert "User" in contents["topics/api__user_endpoints.md"]


def test_load_missing_file(knowledge_base):
    """Returns error for non-existent path."""
    success, contents = load(["topics/nonexistent.md"], project_root=knowledge_base)

    # Should fail or return error info
    assert not success or "errors" in contents


# ============================================================================
# Unit Tests - Add Entry
# ============================================================================

def test_add_entry(empty_kb):
    """Creates file with proper format and updates index."""
    success, path = add_entry(
        title="Test Entry",
        summary="A test knowledge entry",
        content="## Interface\nSome content here.",
        tags=["test", "example"],
        project_root=empty_kb
    )

    assert success
    assert path.endswith(".md")

    # Verify file exists
    full_path = empty_kb / ".wip" / "knowledge" / path
    assert full_path.exists()

    # Verify content format
    content = full_path.read_text()
    assert content.startswith("# Test Entry")
    assert "> A test knowledge entry" in content


def test_add_entry_generates_filename(empty_kb):
    """Filename follows topic__tag1_tag2.md convention."""
    success, path = add_entry(
        title="My Feature",
        summary="Feature description",
        content="## Usage\nExample",
        tags=["api", "feature"],
        project_root=empty_kb
    )

    assert success
    assert "__" in path
    assert "api" in path.lower() or "feature" in path.lower()


# ============================================================================
# Unit Tests - Update Entry
# ============================================================================

def test_update_entry(knowledge_base):
    """Modifies existing file and refreshes index."""
    path = "topics/api__auth_jwt.md"
    new_content = """# JWT Authentication Updated
> Updated summary for JWT auth

## Interface
Updated interface info.
"""

    success, msg = update_entry(path, new_content, project_root=knowledge_base)

    assert success

    # Verify content changed
    full_path = knowledge_base / ".wip" / "knowledge" / path
    assert "Updated" in full_path.read_text()

    # Verify index updated
    search_success, entries = search("Updated", project_root=knowledge_base)
    assert search_success
    assert any("Updated" in e.summary for e in entries)


def test_update_entry_not_found(knowledge_base):
    """Returns error for non-existent entry."""
    success, msg = update_entry(
        "topics/nonexistent.md",
        "content",
        project_root=knowledge_base
    )

    assert not success
    assert "not found" in msg.lower()


# ============================================================================
# Unit Tests - Rebuild Index
# ============================================================================

def test_rebuild_index(knowledge_base):
    """Regenerates index from all topic files."""
    # Add a new file manually
    new_file = knowledge_base / ".wip" / "knowledge" / "topics" / "new__manual.md"
    new_file.write_text("# Manual Entry\n> Added manually\n\n## Content\nHere.")

    success, msg = rebuild_index(project_root=knowledge_base)

    assert success
    assert "4" in msg  # Should now have 4 entries

    # Verify new entry is searchable
    search_success, entries = search("Manual", project_root=knowledge_base)
    assert search_success
    assert len(entries) >= 1


# ============================================================================
# Unit Tests - Helper Functions
# ============================================================================

def test_extract_summary():
    """Parses > blockquote line from content."""
    content = """# Title
> This is the summary

## Content
More text here.
"""
    summary = _extract_summary(content)
    assert summary == "This is the summary"


def test_extract_summary_no_blockquote():
    """Returns None when no blockquote present."""
    content = """# Title

## Content
No summary here.
"""
    summary = _extract_summary(content)
    assert summary is None


def test_extract_title():
    """Extracts # title from content."""
    content = "# My Title\n> Summary\n\nContent"
    title = _extract_title(content)
    assert title == "My Title"


def test_generate_filename():
    """Generates proper filename from title and tags."""
    filename = _generate_filename("User Auth", ["api", "security"])
    assert filename == "user-auth__api_security.md"


def test_generate_filename_no_tags():
    """Generates filename without tags."""
    filename = _generate_filename("Simple Entry", [])
    assert filename == "simple-entry.md"


def test_parse_tags_from_filename():
    """Extracts tags from filename."""
    tags = _parse_tags_from_filename("topic__tag1_tag2.md")
    assert tags == ["tag1", "tag2"]


def test_parse_tags_from_filename_no_tags():
    """Returns empty list for filename without tags."""
    tags = _parse_tags_from_filename("simple.md")
    assert tags == []


def test_score_entry():
    """Scores entry against keywords."""
    entry = KnowledgeEntry(
        path="test.md",
        title="JWT Authentication",
        summary="Token-based auth",
        tags=["auth", "jwt"],
        lines=50
    )

    # Title match = 3 points
    score = _score_entry(entry, ["JWT"])
    assert score >= 3

    # Summary match = 2 points
    score = _score_entry(entry, ["Token"])
    assert score >= 2

    # Tag match = 1 point
    score = _score_entry(entry, ["auth"])
    assert score >= 1


# ============================================================================
# Unit Tests - Split Functionality
# ============================================================================

def test_check_and_split_under_limit(knowledge_base):
    """No split when under MAX_LINES."""
    path = "topics/api__auth_jwt.md"
    success, paths = check_and_split(path, project_root=knowledge_base)

    assert success
    assert paths == [path]


def test_check_and_split_over_limit(tmp_path):
    """Splits by ## headers when over MAX_LINES."""
    # Create a large file
    kb_root = tmp_path / ".wip" / "knowledge"
    kb_root.mkdir(parents=True)
    (kb_root / "topics").mkdir()

    # Generate content over MAX_LINES
    sections = []
    for i in range(5):
        section_lines = [f"## Section {i}"]
        section_lines.extend([f"Line {j} of section {i}" for j in range(60)])
        sections.append("\n".join(section_lines))

    content = "# Large File\n> A file that needs splitting\n\n" + "\n\n".join(sections)

    large_file = kb_root / "topics" / "large__test.md"
    large_file.write_text(content)

    # Initialize index
    rebuild_index(project_root=tmp_path)

    # Check and split
    success, paths = check_and_split("topics/large__test.md", project_root=tmp_path)

    assert success
    # Should have split into multiple files
    assert len(paths) > 1


def test_split_generates_filenames(tmp_path):
    """Split files get appropriate tag-based names."""
    kb_root = tmp_path / ".wip" / "knowledge"
    kb_root.mkdir(parents=True)
    (kb_root / "topics").mkdir()

    # Create file with clear sections
    content = """# API Guide
> Complete API documentation

## Authentication
""" + "\n".join([f"Auth line {i}" for i in range(100)]) + """

## Endpoints
""" + "\n".join([f"Endpoint line {i}" for i in range(100)]) + """

## Examples
""" + "\n".join([f"Example line {i}" for i in range(100)])

    (kb_root / "topics" / "api__guide.md").write_text(content)
    rebuild_index(project_root=tmp_path)

    success, paths = check_and_split("topics/api__guide.md", project_root=tmp_path)

    assert success
    if len(paths) > 1:
        # Check that new files have section-based names
        for path in paths:
            assert "api" in path.lower() or "guide" in path.lower()


# ============================================================================
# Unit Tests - Stats
# ============================================================================

def test_get_stats(knowledge_base):
    """Returns correct counts and tag list."""
    success, stats = get_stats(project_root=knowledge_base)

    assert success
    assert stats["total_entries"] == 3
    assert stats["total_lines"] > 0
    assert "auth" in stats["tags"] or "api" in stats["tags"]
    assert isinstance(stats["largest_files"], list)


def test_get_stats_empty(empty_kb):
    """Returns zeros for empty KB."""
    success, stats = get_stats(project_root=empty_kb)

    assert success
    assert stats["total_entries"] == 0
    assert stats["total_lines"] == 0


# ============================================================================
# Integration Tests
# ============================================================================

def test_full_query_flow(knowledge_base):
    """Search → select → load end-to-end."""
    # Phase 1: Search
    success, entries = search("authentication", project_root=knowledge_base)
    assert success
    assert len(entries) >= 1

    # Phase 2: Select and load
    selected_path = entries[0].path
    success, contents = load([selected_path], project_root=knowledge_base)
    assert success
    assert selected_path in contents
    assert len(contents[selected_path]) > 0


def test_add_then_search(empty_kb):
    """New entry appears in search results."""
    # Add entry
    success, path = add_entry(
        title="Searchable Feature",
        summary="This should be findable",
        content="## Details\nMore info.",
        tags=["searchable"],
        project_root=empty_kb
    )
    assert success

    # Search for it
    success, entries = search("Searchable", project_root=empty_kb)
    assert success
    assert len(entries) >= 1
    assert any("Searchable" in e.title for e in entries)


def test_update_reflects_in_search(knowledge_base):
    """Updated summary shows in search."""
    path = "topics/api__auth_jwt.md"

    # Update with new keyword
    new_content = """# JWT Authentication
> Now featuring UNIQUE_KEYWORD_123

## Interface
Updated content.
"""
    success, msg = update_entry(path, new_content, project_root=knowledge_base)
    assert success

    # Search for new keyword
    success, entries = search("UNIQUE_KEYWORD_123", project_root=knowledge_base)
    assert success
    assert len(entries) >= 1


def test_delete_removes_from_search(knowledge_base):
    """Deleted entry no longer appears in search."""
    # First verify it exists
    success, entries = search("JWT", project_root=knowledge_base)
    assert success
    initial_count = len(entries)

    # Delete
    success, msg = delete_entry("topics/api__auth_jwt.md", project_root=knowledge_base)
    assert success

    # Verify gone from search
    success, entries = search("JWT", project_root=knowledge_base)
    assert success
    assert len(entries) < initial_count

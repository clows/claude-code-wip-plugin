"""
Knowledge base utilities for WIP plugin.

Provides search, retrieval, and management functions for the
project knowledge base stored in .wip/knowledge/.
"""

import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Optional


# Constants
KNOWLEDGE_ROOT = ".wip/knowledge"
INDEX_FILE = "index.json"
TOPICS_DIR = "topics"
MAX_LINES = 250


@dataclass
class KnowledgeEntry:
    """Represents an indexed knowledge entry."""
    path: str
    title: str
    summary: str
    tags: list[str]
    lines: int


def get_knowledge_root(project_root: Optional[Path] = None) -> Path:
    """
    Get the knowledge base root directory.

    Args:
        project_root: Optional project root. Uses cwd if not specified.

    Returns:
        Path to .wip/knowledge directory
    """
    root = project_root or Path.cwd()
    return root / KNOWLEDGE_ROOT


def is_initialized(project_root: Optional[Path] = None) -> bool:
    """
    Check if knowledge base exists and has a valid index.

    Returns:
        True if knowledge base is initialized
    """
    kb_root = get_knowledge_root(project_root)
    index_path = kb_root / INDEX_FILE
    topics_path = kb_root / TOPICS_DIR

    if not index_path.exists() or not topics_path.exists():
        return False

    try:
        with open(index_path) as f:
            data = json.load(f)
            return "version" in data and "entries" in data
    except (json.JSONDecodeError, IOError):
        return False


def initialize(project_root: Optional[Path] = None) -> tuple[bool, str]:
    """
    Initialize the knowledge base directory structure.

    Creates:
        .wip/knowledge/
        .wip/knowledge/index.json
        .wip/knowledge/topics/

    Returns:
        (success, message)
    """
    kb_root = get_knowledge_root(project_root)
    topics_path = kb_root / TOPICS_DIR
    index_path = kb_root / INDEX_FILE

    try:
        topics_path.mkdir(parents=True, exist_ok=True)

        index_data = {"version": 1, "entries": []}
        with open(index_path, "w") as f:
            json.dump(index_data, f, indent=2)

        return True, f"Initialized knowledge base at {kb_root}"
    except Exception as e:
        return False, f"Failed to initialize: {e}"


def _load_index(project_root: Optional[Path] = None) -> tuple[bool, dict]:
    """Load the index file."""
    kb_root = get_knowledge_root(project_root)
    index_path = kb_root / INDEX_FILE

    try:
        with open(index_path) as f:
            return True, json.load(f)
    except FileNotFoundError:
        return False, {"error": "Index file not found"}
    except json.JSONDecodeError as e:
        return False, {"error": f"Invalid JSON: {e}"}


def _save_index(data: dict, project_root: Optional[Path] = None) -> tuple[bool, str]:
    """Save the index file."""
    kb_root = get_knowledge_root(project_root)
    index_path = kb_root / INDEX_FILE

    try:
        with open(index_path, "w") as f:
            json.dump(data, f, indent=2)
        return True, "Index saved"
    except Exception as e:
        return False, f"Failed to save index: {e}"


def _extract_summary(content: str) -> Optional[str]:
    """Extract the > blockquote line after the # title."""
    lines = content.strip().split("\n")
    for i, line in enumerate(lines):
        if line.startswith("# "):
            # Look for blockquote on next non-empty line
            for j in range(i + 1, min(i + 3, len(lines))):
                if lines[j].startswith("> "):
                    return lines[j][2:].strip()
    return None


def _extract_title(content: str) -> Optional[str]:
    """Extract the # title from content."""
    for line in content.strip().split("\n"):
        if line.startswith("# "):
            return line[2:].strip()
    return None


def _generate_filename(title: str, tags: list[str]) -> str:
    """Generate filename from title and tags: topic__tag1_tag2.md"""
    # Sanitize title for filename
    topic = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")

    if tags:
        tag_part = "_".join(re.sub(r"[^a-z0-9]+", "-", t.lower()) for t in tags)
        return f"{topic}__{tag_part}.md"
    return f"{topic}.md"


def _parse_tags_from_filename(filename: str) -> list[str]:
    """Extract tags from filename like topic__tag1_tag2.md"""
    name = filename.replace(".md", "")
    if "__" in name:
        _, tag_part = name.split("__", 1)
        return tag_part.split("_")
    return []


def _score_entry(entry: KnowledgeEntry, keywords: list[str]) -> int:
    """Score an entry against search keywords."""
    score = 0
    title_lower = entry.title.lower()
    summary_lower = entry.summary.lower()
    tags_lower = [t.lower() for t in entry.tags]

    for kw in keywords:
        kw_lower = kw.lower()
        # Title matches worth 3 points
        if kw_lower in title_lower:
            score += 3
        # Summary matches worth 2 points
        if kw_lower in summary_lower:
            score += 2
        # Tag matches worth 1 point
        if any(kw_lower in tag for tag in tags_lower):
            score += 1

    return score


def search(
    query: str,
    tags: Optional[list[str]] = None,
    limit: int = 10,
    project_root: Optional[Path] = None
) -> tuple[bool, list[KnowledgeEntry]]:
    """
    Search the knowledge base index for matching entries.

    Phase 1 of two-phase query: returns summaries without full content.

    Args:
        query: Search keywords (matched against title, summary, tags)
        tags: Optional tag filters (e.g., ["api", "auth"])
        limit: Maximum results to return
        project_root: Optional project root

    Returns:
        (success, list of matching KnowledgeEntry objects)
    """
    success, index_data = _load_index(project_root)
    if not success:
        return False, []

    entries = [KnowledgeEntry(**e) for e in index_data.get("entries", [])]

    # Filter by tags if specified
    if tags:
        tags_lower = [t.lower() for t in tags]
        entries = [
            e for e in entries
            if any(t.lower() in [et.lower() for et in e.tags] for t in tags_lower)
        ]

    # Score and sort by relevance
    keywords = query.split()
    if keywords:
        scored = [(e, _score_entry(e, keywords)) for e in entries]
        scored = [(e, s) for e, s in scored if s > 0]
        scored.sort(key=lambda x: x[1], reverse=True)
        entries = [e for e, _ in scored[:limit]]
    else:
        entries = entries[:limit]

    return True, entries


def load(
    paths: list[str],
    project_root: Optional[Path] = None
) -> tuple[bool, dict[str, str]]:
    """
    Load full content of specified knowledge files.

    Phase 2 of two-phase query: loads selected files into context.

    Args:
        paths: List of paths from search results
        project_root: Optional project root

    Returns:
        (success, dict mapping path to file content)
    """
    kb_root = get_knowledge_root(project_root)
    result = {}
    errors = []

    for path in paths:
        full_path = kb_root / path
        try:
            result[path] = full_path.read_text()
        except FileNotFoundError:
            errors.append(f"Not found: {path}")
        except Exception as e:
            errors.append(f"Error reading {path}: {e}")

    if errors and not result:
        return False, {"errors": errors}

    return True, result


def add_entry(
    title: str,
    summary: str,
    content: str,
    tags: list[str],
    project_root: Optional[Path] = None
) -> tuple[bool, str]:
    """
    Add a new knowledge entry to the base.

    Automatically:
        - Generates filename from title and tags
        - Validates content format
        - Splits if exceeds MAX_LINES
        - Updates index

    Args:
        title: Entry title (becomes # header)
        summary: One-line summary (becomes > blockquote)
        content: Full markdown content (## sections)
        tags: List of tags for categorization

    Returns:
        (success, path to created file or error message)
    """
    kb_root = get_knowledge_root(project_root)
    topics_path = kb_root / TOPICS_DIR

    # Generate filename
    filename = _generate_filename(title, tags)
    file_path = topics_path / filename

    # Build full content
    full_content = f"# {title}\n> {summary}\n\n{content}"

    # Check line count
    lines = full_content.split("\n")
    if len(lines) > MAX_LINES:
        # Need to split - delegate to check_and_split after writing
        pass

    try:
        file_path.write_text(full_content)

        # Update index
        success, msg = rebuild_index(project_root)
        if not success:
            return False, f"File created but index update failed: {msg}"

        rel_path = f"{TOPICS_DIR}/{filename}"

        # Check if splitting is needed
        if len(lines) > MAX_LINES:
            split_success, split_paths = check_and_split(rel_path, project_root)
            if split_success and len(split_paths) > 1:
                return True, f"Created and split into: {', '.join(split_paths)}"

        return True, rel_path
    except Exception as e:
        return False, f"Failed to create entry: {e}"


def update_entry(
    path: str,
    content: str,
    project_root: Optional[Path] = None
) -> tuple[bool, str]:
    """
    Update an existing knowledge entry.

    Validates format, handles auto-splitting, updates index.

    Args:
        path: Path to existing entry
        content: New full markdown content

    Returns:
        (success, message)
    """
    kb_root = get_knowledge_root(project_root)
    full_path = kb_root / path

    if not full_path.exists():
        return False, f"Entry not found: {path}"

    try:
        full_path.write_text(content)

        # Rebuild index to pick up changes
        success, msg = rebuild_index(project_root)
        if not success:
            return False, f"Updated but index rebuild failed: {msg}"

        # Check if splitting is needed
        lines = content.split("\n")
        if len(lines) > MAX_LINES:
            split_success, split_paths = check_and_split(path, project_root)
            if split_success and len(split_paths) > 1:
                return True, f"Updated and split into: {', '.join(split_paths)}"

        return True, "Entry updated"
    except Exception as e:
        return False, f"Failed to update: {e}"


def delete_entry(
    path: str,
    project_root: Optional[Path] = None
) -> tuple[bool, str]:
    """
    Delete a knowledge entry.

    Args:
        path: Path to entry to delete

    Returns:
        (success, message)
    """
    kb_root = get_knowledge_root(project_root)
    full_path = kb_root / path

    if not full_path.exists():
        return False, f"Entry not found: {path}"

    try:
        full_path.unlink()
        rebuild_index(project_root)
        return True, f"Deleted: {path}"
    except Exception as e:
        return False, f"Failed to delete: {e}"


def rebuild_index(project_root: Optional[Path] = None) -> tuple[bool, str]:
    """
    Rebuild the index from all knowledge files.

    Scans topics/ directory, extracts summaries from > blockquotes,
    and regenerates index.json.

    Returns:
        (success, message with entry count)
    """
    kb_root = get_knowledge_root(project_root)
    topics_path = kb_root / TOPICS_DIR

    if not topics_path.exists():
        return False, "Topics directory not found"

    entries = []

    for file_path in topics_path.glob("*.md"):
        try:
            content = file_path.read_text()
            title = _extract_title(content) or file_path.stem
            summary = _extract_summary(content) or ""
            tags = _parse_tags_from_filename(file_path.name)
            lines = len(content.split("\n"))

            entries.append({
                "path": f"{TOPICS_DIR}/{file_path.name}",
                "title": title,
                "summary": summary,
                "tags": tags,
                "lines": lines
            })
        except Exception:
            continue

    index_data = {"version": 1, "entries": entries}
    success, msg = _save_index(index_data, project_root)

    if success:
        return True, f"Index rebuilt with {len(entries)} entries"
    return False, msg


def check_and_split(
    path: str,
    project_root: Optional[Path] = None
) -> tuple[bool, list[str]]:
    """
    Check if a file exceeds MAX_LINES and split if needed.

    Splitting rules:
        - Split at ## section boundaries
        - Each split file gets original tags plus section name as tag
        - Original file is replaced with split files

    Args:
        path: Path to check

    Returns:
        (success, list of resulting file paths)
    """
    kb_root = get_knowledge_root(project_root)
    full_path = kb_root / path

    if not full_path.exists():
        return False, [path]

    content = full_path.read_text()
    lines = content.split("\n")

    if len(lines) <= MAX_LINES:
        return True, [path]

    # Parse sections
    sections = []
    current_lines = []
    current_header = None
    title = _extract_title(content)
    summary = _extract_summary(content)
    original_tags = _parse_tags_from_filename(full_path.name)

    for line in lines:
        if line.startswith("## "):
            if current_lines:
                sections.append((current_header, current_lines))
            current_header = line[3:].strip()
            current_lines = [line]
        else:
            current_lines.append(line)

    if current_lines:
        sections.append((current_header, current_lines))

    # If we can't split meaningfully, keep as is
    if len(sections) <= 1:
        return True, [path]

    # Generate split files
    topics_path = kb_root / TOPICS_DIR
    new_paths = []

    for header, section_lines in sections:
        if header is None:
            # Preamble section (title + summary)
            continue

        # Create new file for this section
        section_tag = re.sub(r"[^a-z0-9]+", "-", header.lower()).strip("-")
        new_tags = original_tags + [section_tag]
        new_filename = _generate_filename(f"{title} {header}", new_tags)
        new_path = topics_path / new_filename

        section_content = f"# {title}: {header}\n> {summary} - {header} section\n\n"
        section_content += "\n".join(section_lines)

        try:
            new_path.write_text(section_content)
            new_paths.append(f"{TOPICS_DIR}/{new_filename}")
        except Exception:
            continue

    # Remove original file if we created splits
    if new_paths:
        try:
            full_path.unlink()
            rebuild_index(project_root)
        except Exception:
            pass

    return True, new_paths if new_paths else [path]


def get_stats(project_root: Optional[Path] = None) -> tuple[bool, dict]:
    """
    Get knowledge base statistics.

    Returns:
        (success, {
            "total_entries": int,
            "total_lines": int,
            "tags": list[str],
            "largest_files": list[tuple[str, int]]
        })
    """
    success, index_data = _load_index(project_root)
    if not success:
        return False, {}

    entries = index_data.get("entries", [])

    total_lines = sum(e.get("lines", 0) for e in entries)
    all_tags = set()
    for e in entries:
        all_tags.update(e.get("tags", []))

    largest = sorted(entries, key=lambda e: e.get("lines", 0), reverse=True)[:5]
    largest_files = [(e["path"], e["lines"]) for e in largest]

    return True, {
        "total_entries": len(entries),
        "total_lines": total_lines,
        "tags": sorted(all_tags),
        "largest_files": largest_files
    }


# =============================================================================
# CLI Interface
# =============================================================================


def _output(data: dict, fmt: str = "json") -> None:
    """Output data in specified format."""
    if fmt == "json":
        print(json.dumps(data, indent=2))
    else:
        # Text format - human readable
        if "error" in data:
            print(f"Error: {data['error']}", file=sys.stderr)
        elif "entries" in data:
            for e in data["entries"]:
                print(f"{e['path']}: {e['summary']}")
        elif "contents" in data:
            for path, content in data["contents"].items():
                print(f"--- {path} ---")
                print(content)
                print()
        elif "message" in data:
            print(data["message"])
        elif "total_entries" in data:
            print(f"Entries: {data['total_entries']}")
            print(f"Total lines: {data['total_lines']}")
            print(f"Tags: {', '.join(data['tags'])}")
            if data.get("largest_files"):
                print("Largest files:")
                for path, lines in data["largest_files"]:
                    print(f"  {path}: {lines} lines")
        else:
            print(json.dumps(data, indent=2))


def main() -> int:
    """CLI entry point for knowledge base management."""
    import argparse

    # Common arguments for all subcommands
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument(
        "--project-root",
        type=Path,
        default=None,
        help="Project root directory (default: cwd)"
    )
    common.add_argument(
        "--format", "-f",
        choices=["json", "text"],
        default="json",
        dest="fmt",
        help="Output format (default: json)"
    )

    parser = argparse.ArgumentParser(
        prog="knowledge",
        description="Knowledge base management CLI"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # search command
    search_p = subparsers.add_parser("search", help="Search KB entries", parents=[common])
    search_p.add_argument("query", help="Search keywords")
    search_p.add_argument("--tags", "-t", help="Comma-separated tag filters")
    search_p.add_argument("--limit", "-l", type=int, default=10, help="Max results")

    # load command
    load_p = subparsers.add_parser("load", help="Load file contents", parents=[common])
    load_p.add_argument("paths", nargs="+", help="Paths to load")

    # add command
    add_p = subparsers.add_parser("add", help="Add new entry", parents=[common])
    add_p.add_argument("--title", required=True, help="Entry title")
    add_p.add_argument("--summary", required=True, help="One-line summary")
    add_p.add_argument("--content", required=True, help="Markdown content")
    add_p.add_argument("--tags", "-t", default="", help="Comma-separated tags")

    # update command
    update_p = subparsers.add_parser("update", help="Update existing entry", parents=[common])
    update_p.add_argument("path", help="Path to entry")
    update_p.add_argument("--content", required=True, help="New content")

    # delete command
    delete_p = subparsers.add_parser("delete", help="Delete entry", parents=[common])
    delete_p.add_argument("path", help="Path to entry")

    # stats command
    subparsers.add_parser("stats", help="Show KB statistics", parents=[common])

    # init command
    subparsers.add_parser("init", help="Initialize KB structure", parents=[common])

    # rebuild command
    subparsers.add_parser("rebuild", help="Rebuild index", parents=[common])

    args = parser.parse_args()
    root = args.project_root

    # Dispatch commands
    if args.command == "search":
        tags = args.tags.split(",") if args.tags else None
        success, entries = search(args.query, tags=tags, limit=args.limit, project_root=root)
        data = {"success": success, "entries": [asdict(e) for e in entries]}
        _output(data, args.fmt)
        return 0 if success else 1

    elif args.command == "load":
        success, contents = load(args.paths, project_root=root)
        if success:
            _output({"success": True, "contents": contents}, args.fmt)
            return 0
        else:
            _output({"success": False, "error": str(contents)}, args.fmt)
            return 1

    elif args.command == "add":
        tags = [t.strip() for t in args.tags.split(",") if t.strip()]
        success, result = add_entry(
            title=args.title,
            summary=args.summary,
            content=args.content,
            tags=tags,
            project_root=root
        )
        if success:
            _output({"success": True, "path": result}, args.fmt)
            return 0
        else:
            _output({"success": False, "error": result}, args.fmt)
            return 1

    elif args.command == "update":
        success, msg = update_entry(args.path, args.content, project_root=root)
        _output({"success": success, "message": msg}, args.fmt)
        return 0 if success else 1

    elif args.command == "delete":
        success, msg = delete_entry(args.path, project_root=root)
        _output({"success": success, "message": msg}, args.fmt)
        return 0 if success else 1

    elif args.command == "stats":
        success, stats = get_stats(project_root=root)
        if success:
            _output({"success": True, **stats}, args.fmt)
            return 0
        else:
            _output({"success": False, "error": "Failed to get stats"}, args.fmt)
            return 1

    elif args.command == "init":
        success, msg = initialize(project_root=root)
        _output({"success": success, "message": msg}, args.fmt)
        return 0 if success else 1

    elif args.command == "rebuild":
        success, msg = rebuild_index(project_root=root)
        _output({"success": success, "message": msg}, args.fmt)
        return 0 if success else 1

    return 1


if __name__ == "__main__":
    sys.exit(main())

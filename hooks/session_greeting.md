# WIP Workflow Context

**IMPORTANT**: On your first response this session, briefly greet the user with:
- Current active work (if any)
- Ready tasks available
- Keep it to 2-3 lines, e.g.: "You have 1 task in progress and 2 ready. Run `bd ready` for details."

## Session Close Protocol

Before completing work, run this checklist:
1. `git status` - Check what changed
2. `git add <files>` - Stage code changes
3. `bd sync --from-main` - Pull beads updates from main
4. `git commit -m "..."` - Commit changes

## Core Rules
- Track ALL work in beads (no TodoWrite, no markdown TODOs)
- Use `bd create` for new issues
- Check `bd ready` for available work

## Essential Commands
- `bd ready` - Unblocked work
- `bd list --status=in_progress` - Active work
- `bd create --title="..." --type=task` - New issue
- `bd update <id> --status=in_progress` - Claim work
- `bd close <id>` - Complete work
- `bd sync --from-main` - Sync before commit

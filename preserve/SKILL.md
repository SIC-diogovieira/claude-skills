---
name: preserve
description: Add a permanent, project-level learning (convention, architecture decision, key path, workflow) to the project's hub file in the Obsidian memory vault. Use when the user says "/preserve", "preserve", "guarda isto de forma permanente", or names something that should always be remembered for this project, not just this session.
---

# /preserve

Adds a durable fact to the **current project's** hub file — the equivalent of a permanent `CLAUDE.md` entry, as opposed to a one-off session log (`/compress`).

## Vault and project mapping

Same mapping as `resume`/`compress`. Hub file: `<vault>/Areas/Work/Projects/<Name>/<Name>.md`.

| cwd prefix | Project |
|---|---|
| `/home/diogo-vieira/Documents/Projetos/nord` | `Nord` |
| `/odoo16` | `Odoo16` |
| `/odoo17` | `Odoo17` |
| `/odoo18` | `Odoo18` |
| `/odoo19` | `Odoo19` |

If cwd doesn't map, ask which project before writing. New project hubs start from `System/Templates/Project-Hub.md`.

## Steps

1. Resolve the project and read `<Name>.md`.
2. Take the insight — either passed as an argument to `/preserve`, or from what was just discussed in the conversation if no argument was given.
3. Classify it into one of the hub's core sections (create the section if missing, don't invent new ones beyond these):
   - **Conventions** — coding/naming/process rules specific to this project
   - **Architecture** — structural decisions (why something is shaped the way it is)
   - **Key Paths** — file/dir locations worth remembering
   - **Workflows** — how to run/test/deploy something repeatedly
   - **Tasks** — open tasks (already exists in the hub template, Tasks-plugin checkboxes — see below)
4. For **Tasks** specifically, use the Obsidian Tasks-plugin pipeline instead of a prose bullet:
   - New open item: `- [ ] <description> #project/<name>` (e.g. `#project/odoo16`). Default status is Todo (` `); use `- [B] ...` only for a someday/not-actionable-yet idea (Backlog).
   - Something just got finished that matches an existing open line: move it along in place (`[/]`→`[T]` when implemented; `[R]` only by whoever tested it; `[x]` only by the user) — don't add a duplicate line. States: `[B] [ ] [/] [T] [R] [x] [-]`, see `~/.claude/CLAUDE.md`.
   - No longer worth doing: `- [-] ...` (Cancelled) in place, don't just delete it.
   All other sections keep the existing one-line-bullet behavior. Don't restate existing bullets — check for near-duplicates first and skip if already covered.
5. **Auto-archive check**: after writing, count the lines in `<Name>.md`. If over 280:
   - Move fully-completed/no-longer-relevant bullets (Done/Cancelled tasks, or superseded notes) into `<Name>-Archive.md` in the same folder (create it if missing, just append under a `## Archived` heading with today's date).
   - Never move Conventions, Architecture, Key Paths, or Workflows sections wholesale — only prune individual stale bullets within them if the user confirms they're dead.
   - If nothing is safely archivable, leave the file as-is and tell the user it's over 280 lines so they know.
6. Confirm what was added and where.

If the insight originated in a session log, link it (`[[<session-log>]]`) from the bullet instead of restating the detail.

This is for things that are true going forward, not "what happened in this session" — that's what `/compress` is for.

---
name: resume
description: Load project context from the Obsidian memory vault at session start — recent work, decisions, pending tasks. Use when the user says "/resume", "resume", "carrega o contexto", or starts a session and wants to pick up where they left off.
---

# /resume

Loads context for the **current project** from the memory vault, so the user doesn't have to re-explain where things stand.

## Vault and project mapping

Vault root: `/home/diogo-vieira/Documents/diogo/Diogo`
Projects live at `<vault>/Areas/Work/Projects/<Name>/`, each with:
- `<Name>.md` — project hub (frontmatter + curated Tasks section, Tasks-plugin checkboxes)
- `Memory/` — durable memory notes (decisions, bugs, feedback, reference)
- `Session-Logs/` — dated logs written by `/compress`

Map the current working directory to a project (check longest prefix first):

| cwd prefix | Project |
|---|---|
| `/home/diogo-vieira/Documents/Projetos/nord` | `Nord` |
| `/odoo16` | `Odoo16` |
| `/odoo17` | `Odoo17` |
| `/odoo18` | `Odoo18` |
| `/odoo19` | `Odoo19` |

If cwd matches none of these, tell the user there's no mapped project for this directory and ask whether to create one (don't guess a new mapping silently). New project hubs start from `System/Templates/Project-Hub.md`, which already has the `## Tasks` section and the pipeline convention wired in.

## Arguments

`/resume [N] [keyword]` — both optional, either order:
- `N` (integer) — how many recent session logs to load (default 3)
- `keyword` — also grep `Memory/` and `Session-Logs/` for this term and surface matches

## Steps

1. Resolve the project folder from cwd using the table above.
2. Read `<Project>/<Project>.md` (hub — has the curated Tasks list and any permanent notes `/preserve` added).
3. List `<Project>/Memory/*.md` and skim the ones most likely relevant (recent mtime, or matching `keyword` if given) — don't dump all of them, this is meant to be fast.
4. List `<Project>/Session-Logs/*.md` sorted by filename (dates sort naturally), read the last N.
5. If `keyword` given, grep both folders for it and note any hits not already surfaced.
6. Reply with a short brief: what was being worked on, key recent decisions, open Tasks (from the hub's `## Tasks`). Cite which files the info came from (path, not full content dump).

If `Session-Logs/` is empty (no `/compress` run yet for this project), say so plainly and rely on `Memory/` + the hub file instead of treating it as an error.

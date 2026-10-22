---
name: find-memory
description: Search all projects' memory notes and session logs in the Obsidian vault at once, when you don't remember which project a memory belongs to. Use when the user says "/find <term>", "procura na memória", or asks something like "onde é que guardámos X" without naming a project.
---

# /find

Cross-project search over the memory vault — for when you don't know (or don't want to specify) which project a memory lives in. For a single known project, `/resume <keyword>` is enough and faster; reach for this only when the project isn't known.

## Vault

Root: `/home/diogo-vieira/Documents/diogo/Diogo`
Search scope: `Areas/Work/Projects/*/Memory/*.md` and `Areas/Work/Projects/*/Session-Logs/*.md`

## Steps

1. Take the search term from the `/find <term>` argument (ask for one if missing).
2. Grep case-insensitively across the scope above (filenames and content).
3. Group hits by project (the segment right after `Areas/Work/Projects/`).
4. For each hit, show the project, file, and the matching line(s) with a bit of surrounding context — not the whole file.
5. If there are hits in more than one project, say so explicitly (this is the scenario this skill exists for) rather than silently picking one.
6. If nothing matches, say so — don't guess or paraphrase an unrelated memory as if it were a match.

---
name: compress
description: Save the current session as a dated log in the Obsidian memory vault before ending work. Use when the user says "/compress", "compress", "grava a sessão", or is wrapping up a work session and wants it preserved.
---

# /compress

Writes a session log for the **current project** to the memory vault, so a future `/resume` can pick this up.

## Vault and project mapping

Same mapping as the `resume` skill: vault root `/home/diogo-vieira/Documents/diogo/Diogo`, projects at `<vault>/Areas/Work/Projects/<Name>/`, logs go in `<Name>/Session-Logs/`.

| cwd prefix | Project |
|---|---|
| `/home/diogo-vieira/Documents/Projetos/nord` | `Nord` |
| `/odoo16` | `Odoo16` |
| `/odoo17` | `Odoo17` |
| `/odoo18` | `Odoo18` |
| `/odoo19` | `Odoo19` |

If cwd doesn't map to a project, ask the user which project this session belongs to (or offer to create the folder, using `System/Templates/Project-Hub.md` as the starting hub file) before writing anything.

## Steps

1. Resolve the project from cwd.
2. Ask the user (AskUserQuestion, multiSelect) which of these to include, based on what actually happened in the session — only offer categories that plausibly apply:
   - Key learnings
   - Solutions & fixes
   - Decisions made
   - Files modified
   - Setup & config
   - Tasks (created/advanced/closed)
   - Errors & workarounds
3. Draft the log from the conversation — don't ask the user to write it, extract it from what was actually discussed/done this session.
4. Write to `<Project>/Session-Logs/<YYYY-MM-DD>-<slug>.md` (slug = a few kebab-case words for the session topic) with this shape:

   ```markdown
   ---
   type: session
   date: YYYY-MM-DD
   project: <Project>
   topics: [topic1, topic2]
   outcome: one-line outcome
   ---

   ## Quick Reference
   **Topics:** ...
   **Outcome:** ...

   ## Decisions Made
   - ...

   ## Key Learnings
   - ...

   ## Tasks
   - Created: ... / Advanced: ... / Closed: ...
   ```

   Only include the sections the user selected in step 2 (plus Quick Reference, always). Keep it a distillation — this is not a transcript dump.

   **Tasks section is a narrative pointer, not a duplicate checklist**: the actual checkbox state lives only in the project hub's `## Tasks` (Tasks-plugin format, see `/preserve`). Here just note in prose which task lines this session touched and how (e.g. "Fechei: commit+deploy do distribution log fix"), and update the hub's `## Tasks` checkboxes to match (add new `- [ ] ... #project/<name>` lines, or move states along `[/]`→`[T]`→`[R]`; never mark `[x]` — only the user does, and never mark `[R]` on your own code, see `~/.claude/CLAUDE.md`) as part of this same step — don't leave the hub stale. This is what keeps every session interlinked with the task pipeline instead of narrating work nobody can trace back to an open item.
5. If the same topic/day already has a log, append a new dated section instead of overwriting.
6. **Memory pointers**: for each key point worth remembering long-term (decision, real bug, rule, state), write/update a note in `<Project>/Memory/` (and mirror per the vault-primary-memory rule) that holds only the essentials plus a `[[<session-log-filename-without-.md>]]` link to this log for the full detail. Never re-summarize the log's content into the memory beyond the key point — the log stays the complete source. Add the one-line entry to the project's `Memory/Index.md`.
7. Confirm the file path back to the user.
8. **Push the vault** (`diheen/obsidian-vault`, private): `cd /home/diogo-vieira/Documents/diogo/Diogo && git add -A && git commit -m "<short summary of this session's changes>" && git push` (skip commit+push if `git status --short` is empty).
9. **Push the skills repo if skills changed** (`diheen/claude-skills`, private, working copy at `~/repos/diheen-claude-skills`):
   - Rebuild the staged tree from the live source, resolving symlinks and excluding the vendored Anthropic cache:
     ```bash
     REPO=~/repos/diheen-claude-skills
     for entry in ~/.claude/skills/*; do
       name=$(basename "$entry")
       [ "$name" = synced ] && continue
       [ "$name" = README.md ] && continue   # README is hand-maintained in the repo, don't overwrite
       rsync -a --delete "$(readlink -f "$entry")/" "$REPO/$name/" 2>/dev/null || rsync -a --delete "$entry" "$REPO/$name"
     done
     ```
   - `cd ~/repos/diheen-claude-skills && git add -A && git status --short` — if empty, nothing changed, skip. Otherwise `git commit -m "<what changed>" && git push`.
   - If a new skill directory was added or removed, also update the README's list to match before committing.

Both pushes only run if there's something to push (git status non-empty) — don't create empty commits. If either `git push` fails (e.g. `gh auth status` shows the wrong active account), surface the error to the user instead of retrying blindly — same failure mode as the initial 2026-09-22 setup, where `gh` was authenticated as the wrong account for `diheen`.

Don't invent decisions or outcomes that didn't happen in the session — this log is what a future `/resume` will trust as fact.

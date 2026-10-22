---
name: commit
description: Write a git commit message in the user's own convention ([UPDATE][addon] verb:/[FIX][addon] title + dense technical body). Use whenever the user asks to commit, "faz commit", "cria um commit", or otherwise wants a commit made in any of their repos — this only changes how the message is composed, not the staging/safety workflow.
---

Compose the commit message in this exact house style, then follow the
project's normal commit workflow (review staged diff, never `git add -A`
blindly, never force/skip hooks, only commit what's explicitly asked). This
skill only replaces the message-writing step — everything else about
committing safely stays as already instructed.

Confirmed live across this user's repos (`nord-os`, `nordwire`) as their
current, active convention — not the older per-repo history (`[IMP]`,
`[ADD]`, `[BUG]`, `[UPT]`, OCA-style tags): those are legacy, do not use them.

## Multi-repo requests

When the request spans more than one git repo (e.g. a change that touches
both `nord-os` and `nordwire` for the same feature), always create one
commit per repo -- never a single combined commit, and never ask the user
to pick just one. This holds even when the change is logically one feature
split across repos.

## Never push

This skill only creates the commit locally. Never run `git push`, regardless
of phrasing ("commit and push", "manda isto") — stop right after the commit
and tell the user it's ready to push, unless they explicitly ask for the
push as its own separate instruction in that same message.

## Staging scope

Never stage or commit docs or tests — `Docs/`, `doc/`, `docs/`, any
`*.md`/`CONTEXT.md`/ADRs, and any `tests/`/`test_*.py` path, even when they
sit right next to the code change being committed and even under a broad
`git add`. Leave them untracked/unstaged for the user to commit separately.
If the user explicitly names a docs or test file to commit, that overrides
this default for that file only.

## Title line

```
[TAG][addon] verb: short technical description
```

- **TAG**: `UPDATE` for virtually everything (`[UPDATE]`, all-caps, brackets).
  A bare `[FIX]` with no body is acceptable only for a one-line trivial fix
  that needs no explanation — default to `[UPDATE] fix: ...` otherwise. The
  addon tag right after it is never dropped, even on a bare `[FIX]`:
  `[FIX][nord_sync] fix: typo in the wizard label`.
- **addon**: the literal addon name(s) the commit touches, lowercase,
  exactly as the directory is named on disk (`nordos_nord_sync_core`,
  `nord_sync_mrp`, ...) — never a curated/human label, derive it mechanically
  from the changed files' paths. More than one addon touched in the same
  commit: comma-separated, in the order their segments appear after the
  verb list, e.g. `[UPDATE][nord_sync,nord_sync_mrp]`. When nothing touched
  belongs to an addon (repo-root files, the `nord` framework core itself,
  CI config, ...), omit the second bracket entirely — back to plain
  `[UPDATE] verb: ...` — never invent a placeholder tag.
- **verb**: lowercase, one of `add` / `fix` / `chng` / `delete` / `revert`,
  followed by `: ` (colon, one space). Pick the one that actually matches
  the change. `chng` covers "changed existing behavior without it being a
  bug fix" — never use `modify`, it was the same meaning as `chng` under a
  different word and only added ambiguity.
- **description**: short, telegraphic, lowercase, noun-phrase style — not a
  full sentence, no trailing period. e.g. `add: alert on permanently-failed
  nord sync queue entries`, `fix: nord.job.resource crash on pause/resume
  (_compute_dates)`.
- A single commit bundling more than one distinct change chains
  `verb: description` segments with `; `, each with its own verb:
  `add: defaut fields data; chng: sync queue is transient model`. Reserve
  this for changes that are part of the same coherent effort. When the
  staged changes are logically independent (an unrelated bug fix sitting
  alongside a new feature, neither depending on the other to work),
  propose splitting into separate commits instead of chaining them with
  `;` -- ask the user before splitting, don't silently decide the staging.
- Always English, regardless of what language the conversation is in.

## Body

One blank line after the title, then plain prose paragraphs — no markdown,
no bullet points, no backticks, no code fences. Wrap around 79-81 columns
(match the surrounding paragraph, don't hard-wrap mid-word).

Write it exactly like this codebase's own inline comments/docstrings:
- Name the actual method/field/model touched, written as real identifiers
  (`_nord_sync_alert_permanent_entry_failure()`, `nord_sync_odoo_api_key`,
  `mrp.production`) — never wrapped in backticks, just bare in the prose.
- State what changed AND why it matters — the consequence for a caller, a
  behavior that's now possible, or a gap that's now closed.
- For a fix: give the real root cause, not just the symptom — e.g. "old
  `len(ends) == len(timesheet_ids)` check was always true and never caught
  it" rather than "fixed a crash". If it was a real bug caught live, say so
  plainly ("real bug, caught live: ...").
- Use `--` (double hyphen, spaced) as the em-dash for an aside or
  consequence clause, same as the code comments — not `—`, not `-`.
- Never cite an ADR/Docs/planning-doc reference (`Docs/ADR/0034-...`,
  "per ADR 0006", `Fase N`/`Slice N`, `NordSyncManual*.md`, ...) — same rule
  as this project's code comments, and for the same reason: whoever reads
  `git log` later won't necessarily have the docs repo open next to it.
  Write the actual reasoning/constraint inline instead of pointing at where
  it's written up.
- Skip the body entirely for a genuinely trivial commit (title only, still
  followed by nothing else — no forced filler paragraph).

## Examples

The three below are real, from this user's history — but predate the
`[addon]` tag (added 2026-09-16), so their title lines only show
`[TAG] verb: ...`. New commits always include the addon tag as specified
above; this one is written fresh to show the current full format:

```
[UPDATE][nordos_nord_sync_core] fix: silent Result Push transport failures

_push_nord_sync_result's except branch (timeout, connection refused, 5xx via
raise_for_status) only logged a warning and returned False -- unlike the
success:false branch three lines below it, which already creates a
nord.tasks alert. A job could go done on the Core while the client's MO
stayed confirmed forever with zero indication anywhere that anything
failed. Now creates the same alert in the except branch, with the
exception's message.
```

```
[UPDATE] add: encrypt nord_sync_odoo_api_key at rest

The Odoo client's API key (nord_sync_odoo_api_key) is now stored encrypted
(nord_sync_odoo_api_key_crypt, Fernet key derived from Odoo's own
database.secret) instead of plaintext -- a DB dump alone no longer exposes a
client's live credential. nord_sync_odoo_api_key becomes a compute/inverse
pair over the ciphertext column, transparent to every existing caller.
Migration 1.0.1 re-encrypts whatever plaintext value already exists before
the ORM would otherwise drop the column outright.
```

```
[UPDATE] fix: nord.job.resource crash on pause/resume (_compute_dates)

max(end_date values) blew up comparing datetime to False whenever a resumed
session (new open timesheet) sat alongside an already-closed one --
mapped() always returns one entry per record regardless of falsy values, so
the old len(ends) == len(timesheet_ids) check was always true and never
caught it. all(ends) actually requires every session to be closed before
computing end_date.
```

```
[UPDATE] add: defaut fields data; chng: sync queue is transient model
```

## Trailer

Do not add a `Co-Authored-By: Claude` trailer to the commit message.

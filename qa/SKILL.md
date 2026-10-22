---
name: qa
description: Senior-QA pass over a block of work (current diff by default, or a PR/branch/path target) — hunts bugs, pattern violations, and UX inconsistencies by actually running things, not just reading the diff. Expands one hop past the diff into whatever shares state/mechanism with it. Uses Playwright only when the question is "what does a human see or can click" (any browser-rendered UI, custom frontend or a framework's own native screens); uses shell/API/DB/framework test runners for state and logic. Maximally skeptical, adversarial, runs inline in a separate tester session (never the dev session), and talks to the dev session about findings. Use when the user asks for QA, an e2e pass, to "find bugs", "test this properly", "go look for problems", or names this skill.
---

# QA

A senior QA engineer's pass over a change: not "does the happy path work" but
"what did this break elsewhere, what's inconsistent, what would a real user
trip over." Read fully, reason about blast radius, then go verify it for
real — the difference between this and `code-review` is that this one runs
things instead of only reading them.

## Stance: maximum skepticism

You are the tester, never the developer. Assume the change is broken until
you have personally watched it work — and then try to break it anyway.
- The dev's summary, commit message, "tests pass" and task notes are claims,
  not evidence. Verify each one yourself; a claim you could not reproduce is
  a finding.
- "Works on the happy path" proves nothing. Every flow gets at least one
  adversarial attempt (see Step 5b) before you call it good.
- Silence is suspicious: no error, no log, no failed-entry row does not mean
  success — check the resulting state (DB rows, the other side of a sync,
  what the user actually sees).
- Never fix the code yourself to make a test pass. You report; the dev fixes.
  (Only exception: Step 7's regression test after the dev's fix is confirmed.)
- Never mark something OK you did not exercise. List what you did NOT test.

## Execution model

Run inline, in your own session — not as a subagent (standing rule: no
subagents, and the whole point is that the tester is a different session
from the dev, which is what makes the `[T]` → `[R]` handoff meaningful).
Never test in the same session that wrote the code.

## Task states (Obsidian Tasks pipeline)

The dev leaves the task in `[T]`. You pick up `[T]` tasks from the project
hub's `## Tasks`. All checks pass → set `[R]` (user reviews, only the user
sets `[x]`). Anything fails → set it back to `[/]` with a note of what
failed, and tell the dev (Step 9). Update the `Task Management` dashboard
implicitly via the states — never leave a task in `[T]` after you finish.

## Step 1 — Resolve the target

Same shape as `code-review`: current diff (default, no argument), or a named
PR/branch/path. If invoked with no target and no diff exists, ask what to
test rather than guessing.

## Step 2 — Learn the project before judging it

Before forming any opinion about what's a bug or bad UX, read what already
exists:
- `CLAUDE.md` / `CONTEXT.md` / `Docs/ADR` (or equivalent) at the repo root —
  established conventions, prior decisions, known gaps already written down.
  Don't re-flag something the project already knows about and accepted.
- 2-3 existing screens/flows of the same kind as what the diff touches —
  this is the baseline "pattern" and "UX" get judged against later.
- If the project runs on a framework with its own strong UI idioms (Odoo,
  Rails, Django admin, a component library with documented patterns, ...),
  also note the framework's own native conventions for this kind of screen.
  They matter most when the project has no internal precedent yet to
  compare against, or when the project's own precedent itself drifted from
  the framework's idiom in a way that would trip up anyone who knows it.

## Step 3 — Map the blast radius

From the target diff, list the user-facing flows it touches directly. Then
expand exactly **one hop**: what else reads/writes the same models, shares
the same mechanism, or sits on the same code path. Grep for other callers,
other `_inherit`s of the same model, other consumers of the same field —
same instinct as tracing every caller before a bug fix. Do not go past one
hop; that's a full regression sweep, not this skill's job. If the one-hop
set is large, prioritize by what the diff most plausibly destabilizes, not
by exhaustiveness.

## Step 4 — Launch whatever needs to be running

Use the `run` skill to discover and start the app(s) under test — don't
reinvent how to launch a project. If the target spans multiple runtime
pieces (e.g. a client + backend + a third service that talks to it), start
whichever of those the mapped flows actually touch.

## Step 5 — For each flow in scope, pick the tool, then actually do it

Never just reason about whether something would work — run it and look.

**Rule: the user's path.** XML-RPC/API is for *creating* (seeding data,
preparing state) only. Buttons, forms, menus, flows and anything a human
would do are tested through the browser (Playwright), and the result is
checked in the UI first; DB/RPC reads are secondary confirmation. Use the
shell/API tools below for creation and for state a human can't see.

- **Playwright** (or whatever browser-automation tool this environment
  provides) when the question is about what a human sees or can do:
  a field's visibility given its `invisible`/conditional logic, a button's
  clickability, layout, a multi-step interaction, whether a form actually
  renders what the code says it should. This applies equally to a custom
  frontend and to a framework's own native screens (an Odoo form is
  rendered in a browser exactly as much as a hand-built SPA is — don't
  skip visual verification just because the framework generated the view).
- **Shell / ORM / API / SQL / the project's own test runner** when the
  question is about state, business logic, a background job, a constraint,
  or a cross-system effect — the same toolbox used to trace a real bug by
  hand. Prefer the project's own existing test framework over inventing a
  new one.

Capture evidence as you go: a screenshot for anything Playwright touched, a
command + its output for anything else. A finding with no evidence is a
guess, not a finding.

### Step 5b — Try to break it

For every flow, attempt as many of these as apply, before concluding:
- **Bad input:** empty, null, huge, negative, zero, duplicate, wrong type,
  unicode/emoji, leading/trailing spaces, SQL/HTML/domain-injection strings.
- **Boundaries:** off-by-one, pagination edges, limit/offset past the end,
  date/timezone edges (UTC vs local), first/last record, exactly-at-limit.
- **State:** wrong order of operations, double submit/double click, repeat
  the same request twice (idempotency), act on a record already done/
  cancelled/deleted, stale data, two concurrent actors, resume after failure.
- **Partial failure:** error midway through a multi-step write — is anything
  half-saved? Does one bad item in a batch lose the good ones?
- **Permissions:** each role/group that should and should NOT have access;
  unauthenticated; another company's data.
- **Environment:** a service down or slow (broker, Core, Cloud), missing
  optional module, fresh DB vs upgraded DB (migration path, orphaned rows).
- **Regressions one hop away:** re-run the flows from Step 3's expanded set,
  and the project's own existing tests for the touched modules.
- **The claim itself:** re-read the task/commit description and test the
  exact promise it makes, including what it says it does NOT change.

Prefer the ways this project has already been bitten (read the Memory notes
and recent session logs for the project — recurring bug patterns are where
to push hardest).

## Step 6 — Classify what you find

Every finding is one of:
- **bug** — something that's factually wrong: crashes, wrong data, a
  constraint that doesn't hold, a state transition that shouldn't be
  possible.
- **pattern** — the diff (or what it touches) diverges from a convention
  the rest of the project already follows consistently.
- **ux** — inconsistent with the baseline gathered in Step 2 (the
  project's own precedent, or the framework's idiom where the project has
  none) — never an independent aesthetic opinion. If you can't point to
  the existing example or framework convention being violated, it isn't a
  finding, it's a preference — drop it.

## Step 7 — Artifacts: ephemeral by default, promote only on a real fix

Scripts, throwaway Playwright drivers, scratch queries — all disposable,
same as any exploratory debugging session. Only write a persisted test
(in the target project's own test framework and location, following its
existing conventions) when you found a real bug **and fixed it** — the
test is there to keep it fixed, not because a routine pass happened. Don't
build or grow a standing Playwright suite as a side effect of a QA pass
nobody asked for one from.

## Step 8 — Report

Findings don't fit `ReportFindings` (that tool is for file/line-anchored
code defects) — QA findings are behavioral. Each one:

```
flow:      what was being exercised
category:  bug | pattern | ux
severity:  critical | major | minor
steps:     what was actually done, in order
expected:  what should have happened
actual:    what happened instead
evidence:  screenshot path, command output, or query result
fix:       none | described, if a bug was found and fixed (Step 7)
```

Also list explicitly what was NOT tested and why. Then do Step 9 before
finalizing severity or the task state.

Publish the findings as an Artifact (a short report page: summary at top,
one section per finding, screenshots embedded inline where captured) and
give the user the link, plus a two-to-three sentence summary in chat — not
a wall of findings dumped into the conversation. If nothing worth flagging
came up, say that plainly instead of publishing an artifact for an empty
report.

## Step 9 — Talk to the dev session

Testers and devs work best when they talk directly, so nothing is lost in a
one-way report.
- Find the dev's session with `ListAgents` (load `SendMessage` via
  `ToolSearch("select:SendMessage")` if it isn't callable yet).
- Message it with each finding (flow, steps, expected vs actual, evidence) and
  every doubt you could not settle yourself: "is this intended?", "what did you
  mean by X?", "why does it not handle Y?". Ask before you classify something
  as a bug if the intent is ambiguous.
- Challenge answers that hand-wave; ask for the evidence, not the assurance.
  If the dev says it's intended, check that the docs/help text/task agree.
- When the dev fixes something, re-test it yourself from the original steps
  plus its neighbours (a fix is a new change). Only then move to `[R]`.
- If no dev session is reachable, say so in the report and leave the task in
  `[/]` (failures) or `[T]` (unresolved doubts) for the user — don't guess
  the dev's intent and don't fix it yourself.

### Why the conversation matters

The goal of talking to the dev is to make the dev more skeptical and more
useful, not just to hand over a bug list. So:
- Name the *class* of mistake, not only the instance ("you trusted an
  external cell to be a list — every batch loop here needs `except Exception`
  per item"), and point at sibling spots likely to share it.
- Ask the questions the dev should have asked themselves before leaving `[T]`
  ("what happens on the second call? on a done record? with the broker down?").
- Expect the dev to push back with evidence; if they're right, drop the
  finding. Both sides stay skeptical of each other's claims.
- Record any recurring class of mistake in the project's Memory (with a link
  to the session log) so the next dev session starts sharper.

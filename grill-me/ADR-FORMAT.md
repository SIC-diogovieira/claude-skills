# ADR Format

ADRs live in `Docs/ADR/` and use sequential numbering: `0001-ShortTitle.md`, `0002-ShortTitle.md`, etc.

Create the `Docs/ADR/` directory lazily — only when the first ADR is needed.

## Template

```md
# {Short title of the decision}

{1-3 sentences: what's the context, what did we decide, and why.}
```

That's it. An ADR can be a single paragraph. The value is in recording *that* a decision was made and *why* — not in filling out sections.

## Optional sections

Only include these when they add genuine value. Most ADRs won't need them.

- **Status** frontmatter (`proposed | accepted | deprecated | superseded by ADR-NNNN`) — useful when decisions are revisited
- **Considered Options** — only when the rejected alternatives are worth remembering
- **Consequences** — only when non-obvious downstream effects need to be called out

## Numbering

Scan `Docs/ADR/` for the highest existing number and increment by one.

## When to offer an ADR

All three of these must be true:

1. **Hard to reverse** — the cost of changing your mind later is meaningful
2. **Surprising without context** — a future reader will look at the code and wonder "why on earth did they do it this way?"
3. **The result of a real trade-off** — there were genuine alternatives and you picked one for specific reasons

If a decision is easy to reverse, skip it — you'll just reverse it. If it's not surprising, nobody will wonder why. If there was no real alternative, there's nothing to record beyond "we did the obvious thing."

### What qualifies

- **Architectural shape.** "We're using ECS instead of MonoBehaviour inheritance."
- **Technology choices that carry lock-in.** Engine plugins, networking solutions, serialization approach. Not every library — just the ones that would take significant effort to swap out.
- **Deliberate deviations from the obvious path.** "We're using ScriptableObjects for config instead of JSON because X." Anything where a reasonable reader would assume the opposite.
- **Constraints not visible in the code.** "We can't use package X because of licensing requirements." "Frame budget must stay under 16ms because we target 60fps on mobile."
- **Rejected alternatives when the rejection is non-obvious.** If you considered approach A and picked approach B for subtle reasons, record it — otherwise someone will suggest A again later.

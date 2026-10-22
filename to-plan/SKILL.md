---
name: to-plan
description: Break a spec into an ordered list of vertical slices (tracer bullets), each tagged AFK or HITL. Use when user wants to convert a spec into an implementation plan.
---

# To Plan

Break a spec into an ordered list of independently-grabbable vertical slices (tracer bullets).

## Process

### 1. Gather context

Work from whatever is already in the conversation context. If the user passes a spec file path as an argument, read it.

### 2. Explore the codebase (optional)

If you have not already explored the codebase, do so to understand the current state of the code. Use the project's domain glossary vocabulary (from `CONTEXT.md`), and respect any ADRs in `Docs/ADR/`.

### 3. Draft vertical slices

Break the spec into **tracer bullet** slices. Each slice is a thin vertical slice that cuts through ALL relevant layers end-to-end, NOT a horizontal slice of one layer.

Slices are classified as either:

- **AFK** — can be implemented by an agent autonomously without human interaction. The agent can verify completion through compilation and log checks.
- **HITL** — requires human interaction, such as visual inspection, feel/tuning judgment, design review, or an architectural decision.

Prefer AFK over HITL where possible.

<vertical-slice-rules>
- Each slice delivers a narrow but COMPLETE path through every relevant layer
- A completed slice is demoable or verifiable on its own
- Prefer many thin slices over few thick ones
</vertical-slice-rules>

### 4. Quiz the user

Present the proposed breakdown as a numbered list. For each slice, show:

- **Title**: short descriptive name
- **Type**: AFK / HITL

Ask the user:

- Does the granularity feel right? (too coarse / too fine)
- Are the correct slices marked as AFK and HITL?
- Should any slices be merged or split further?

Iterate until the user approves the breakdown.

### 5. Write the plan

Once approved, save the plan to `Docs/<FeatureName>/<FeatureName>Plan.md` using the slice template below.

<slice-template>

## Phase N: {Title}

**Type**: AFK / HITL

### What to build

A concise description of this vertical slice. Describe the end-to-end behavior, not layer-by-layer implementation.

Avoid specific file paths or code snippets — they go stale fast.

### How to verify

**Agent can check:**
- [ ] Project compiles with zero errors
- [ ] No exceptions in logs during basic execution

**Human should verify:**
- [ ] {What to observe when running the game}
- [ ] {Specific behavior to confirm}
- [ ] {Edge case to check}

</slice-template>

---
name: to-spec
description: Turn the current conversation context into a spec document. Use when user wants to create a spec from the current context.
---

This skill takes the current conversation context and codebase understanding and produces a spec. Do NOT interview the user — just synthesize what you already know.

## Process

1. Explore the repo to understand the current state of the codebase, if you haven't already. Use the project's domain glossary vocabulary (from `CONTEXT.md`) throughout the spec, and respect any ADRs in `Docs/ADR/`.

2. Sketch out the major modules you will need to build or modify to complete the implementation. Check with the user that these modules match their expectations.

3. Write the spec using the template below, then save it to `Docs/<FeatureName>/<FeatureName>Spec.md`.

<spec-template>

## Problem Statement

The problem that the user is facing, from the user's perspective.

## Solution

The solution to the problem, from the user's perspective.

## Behaviors

A LONG, numbered list of concrete behaviors. Each behavior should describe what the player/user can do or what the system should do.

<behavior-examples>
1. The player can dash in the direction they are moving
2. The system cancels the dash if the player takes damage mid-animation
3. The player sees a stamina bar decrease when dashing
</behavior-examples>

This list of behaviors should be extremely extensive and cover all aspects of the feature.

## Implementation Decisions

A list of implementation decisions that were made. This can include:

- The modules that will be built/modified
- Technical clarifications from the developer
- Architectural decisions
- Schema changes
- Specific interactions

Do NOT include specific file paths or code snippets. They may end up being outdated very quickly.

## Validation Criteria

A description of how to verify the feature works correctly. Since automated tests are not available, describe:

- What the human should observe when running the game
- What behavior confirms the feature is working
- Edge cases to manually check
- What error-free logs should look like

## Out of Scope

A description of the things that are out of scope for this spec.

## Further Notes

Any further notes about the feature.

</spec-template>

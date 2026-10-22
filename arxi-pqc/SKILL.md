---
name: arxi-pqc
description: Generate a structured Quality Check (QC) document for an Odoo module feature. Each section has one flat PASSOS list and one flat RESULTADO ESPERADO list, numbered in direct correspondence. No subsections. Use when user asks for a QC, quality check, or "arxi-pqc" for a feature.
---

Produce a Quality Check document for the feature described in the conversation. Do NOT interview the user — synthesize from the conversation context and codebase.

## Rules

- Read the relevant wizard/view/model code before writing. The steps must reflect the real field names, button labels, and menu paths.
- Each section maps to a logical test group (UI, mode behaviour, upload variants, Dropbox verification, etc.).
- Within each section there is exactly ONE **Passos** block and ONE **Resultado Esperado** block. No sub-headings, no ### subdivisions.
- Steps and results are numbered in strict 1-to-1 correspondence: step N produces result N.
- Steps are written as concrete user actions: module to open, button to click, field to fill, value to observe.
- Expected results state the observable outcome explicitly — never just restate the step. Mention field names, values, UI labels, and badge colours where relevant.
- When multiple test cases share a setup (e.g. "upload was already done in step 1"), subsequent steps say "Com base no passo 1, verificar…" to avoid repetition.
- Where a step requires a precondition (e.g. a record with specific data), state it as part of step 1 or an earlier step in the same section.
- Save the final document to `doc/QC_<feature_name>.md` inside the module folder.

## Output template

```markdown
# Quality Check — <Feature Name>

---

## <N>. <Section Title>

**Passos:**
1. <Concrete action — module > menu > field > button>
2. <Next action or observation>
...

**Resultado Esperado:**
1. <Observable outcome for step 1>
2. <Observable outcome for step 2>
...

---
```

Repeat the section block for every logical test group. Typical sections for a migration/wizard feature:

0. Interface / UI
1. Mode — Record Selection (if applicable)
2. Mode + Simulation
3. Mode + Upload without Convert to Link
4. Mode + Upload with Convert to Link
5. Batch Mode — Configuration (if applicable)
6. Batch + Simulation (if applicable)
7. Batch + Upload without Convert to Link (if applicable)
8. Batch + Upload with Convert to Link (if applicable)
9. External system verification (Dropbox, S3, etc.)

Adapt, add or remove sections to fit the actual feature being tested.

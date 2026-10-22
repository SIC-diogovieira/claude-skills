---
name: arxi-manual
description: Generate a technical/API manual (.md + .docx) styled with the ARXI Word template — Endpoints table, numbered sections, dedicated Error Reference and Internal Flow sections, Integration Notes, static reference appendix — plus a matching published Artifact, both carrying real screenshots of the feature/flow wherever one can be captured. Use when the user asks to create a manual, API manual, or technical documentation "like this one"/"igual a este" referring to the ARXI-branded docx template, or explicitly says "arxi-manual".
---

Produce one technical manual per component/system described in the conversation, as both a Markdown
source file and a `.docx` styled with the ARXI template bundled in this skill (`reference.docx`).

Do NOT interview the user before writing — synthesize from the conversation context and the codebase
(read the actual code/config for anything you document; don't invent field names, endpoints, or values).

## Structure (mirrors `INVOICE_CONNECTOR_API_EN.docx`, ARXI's own reference manual)

```
# <System/Component> — <what it does, one line>

## Overview
1-2 short paragraphs: what this component is, its role, and what it does NOT do. If the component has no
HTTP surface at all, say so here in one sentence (e.g. "does not expose or consume any HTTP endpoint —
all interaction happens through the normal Odoo UI") instead of in a dedicated section.

## Endpoints — ONLY when there's at least one real HTTP endpoint
A table of every HTTP endpoint this component exposes or calls:
| Endpoint | Direction | Function |
Omit this entire section (heading included) when the component has none — don't keep the heading with a
placeholder "—" / "Not applicable" row. A manual for a component with no HTTP surface (a UI feature, an
internal batch job, an ORM-only mechanism) skips straight from Overview to the first real numbered topic.

---
(no literal `---` markdown rule here or anywhere else — see Hard Constraints)

## 1. Authentication — only when Endpoints exists and something is actually authenticated
## 2. <first real topic>
## 3. <endpoint deep-dive: Payload table, Request Example, Response>
...
## N. Error Reference
   A table: HTTP code | error/message | cause. This is its OWN numbered section,
   not scattered notes under each endpoint.
## N+1. Internal Flow
   One or more fenced ``` blocks with a numbered pseudocode trace of a real
   request/event end to end. Plain numbered steps, not prose.
## N+2. Integration Notes
   Bullet list, bold lead-in phrase + explanation. The "gotchas a new integrator
   would hit" — non-obvious defaults, what's NOT cumulative, terminal states, etc.

## Static Reference (unnumbered, appendix at the very end)
   Small lookup tables: valid enum values, status codes, IDs — things a reader
   comes back to, not reads linearly.
```

Multiple components (client/server/relay, etc.) → one manual per component, each following this same
shape, cross-referencing the others by name only (don't duplicate their internals).

## Writing rules

- Every payload/endpoint table row must come from real code — grep the actual controller/model, don't
  guess field names.
- No HTTP endpoints found for this component → no `## Endpoints` section at all (see Structure above),
  and no `## 1. Authentication` either. Don't pad the manual with a table whose only row is "—" / "N/A" —
  that's noise a reader has to read past, not information.
- Curl + one client-language (Python is the safe default unless the codebase's own ecosystem suggests
  otherwise) example for every endpoint that's actually callable from outside.
- Error Reference is exhaustive for what the code can actually return — walk every `raise`/error response
  in the endpoint's code path.
- Language: match whatever the user/project uses elsewhere (this skill has been used in Portuguese so
  far) — the template/layout is independent of content language.

## Every manual also ships as an Artifact, with real screenshots

This skill never delivers the `.md`/`.docx` alone. Every time it produces a manual, it also publishes an
HTML Artifact of the same manual, and both deliverables carry real screenshots of the feature/flow in
action wherever one can actually be captured — this is the default now, not something to wait to be asked
for.

**Screenshots are real, not synthetic.** Capture them from an actual running instance of the system being
documented — never mock up, hand-draw, or describe-in-prose a UI that should be a screenshot. If there's
genuinely no way to reach a running instance (no test/dev DB, no safe way to launch one), say so to the
user and ship without screenshots rather than fabricating them — don't let this block finishing the manual.

**How to capture them** (the pattern that worked in this project — adapt paths/commands per project, but
keep the shape):

1. Check for a running instance first, and never touch a live/production database without the user's
   explicit go-ahead for that specific DB — `ps aux | grep <server-binary>` and the DB's own
   `pg_stat_activity` before anything else. Prefer a test/copy database when one exists; only use
   production data with the user's explicit, scoped permission, and even then only read or write inside a
   rolled-back savepoint unless the user is specifically asking for a persisted data change.
2. Launch an isolated instance on a scratch port (never the user's own dev port) against whichever database
   was agreed, with the module/changes already installed (`-u`/`-i` first if this manual documents
   something just built).
3. Drive it headless. Try `chromium-cli` first (per the `run` skill). If unavailable, check for a cached
   Playwright Chromium binary (`~/.cache/ms-playwright/chromium-*/chrome-linux64/chrome`) and
   `npm install playwright-core` into a scratch dir (lightweight — the binary is already cached, nothing to
   download), then drive it with a small Node script:
   `chromium.launch({ executablePath: <cached binary>, args: ['--no-sandbox'] })`.
   - Wait on real content selectors (`.o_list_view .o_data_row`, `.o_form_view .nav-link`, ...), not
     `networkidle` — Odoo's bus/long-poll connections never go idle.
   - A bare `#model=X&view_type=list` hash with no `action=` can hang forever on "Loading…" — resolve the
     view's real `ir.actions.act_window` id first (`ir_model_data` lookup, or navigate via the actual menu)
     and use `#action=<id>&model=X&view_type=list`. A single record's form
     (`#model=X&view_type=form&id=<id>`) works fine without an action id.
   - Force a real reload (`page.goto('about:blank')`, then the target URL) when navigating between
     different models in the same session — same-tab hash-only navigation across unrelated models is flaky
     in the Odoo SPA router.
4. Prefer real, already-existing records over fabricated ones — query for one that already demonstrates the
   behavior (a real consumed/completed/error state) rather than creating throwaway data. Only create data
   when nothing real demonstrates the case.
5. Crop dead whitespace (PIL or similar) before embedding — a full browser-window screenshot is rarely all
   signal; keep the frame tight around what the caption is about.
6. Save the finished PNGs into the manual's own `images/` folder (the one the `.md` already uses).
7. Stop the isolated instance and free the port when done.

**Embedding**: in the `.md`/`.docx`, `![caption](images/name.png){width=100%}` as documented under Hard
Constraints below. In the Artifact, inline them as base64 `data:image/png;base64,...` in the `<img src>`
(a relative `images/` path won't resolve inside a published Artifact) — write the HTML with placeholder
tokens first, then substitute the actual base64 bytes in with a small script, rather than hand-pasting
base64 into the file.

### The Artifact itself

Before writing it, load the `artifact-design` skill and follow its process — this is a **utilitarian
document treatment** (real typographic hierarchy, a considered palette, deliberate spacing) grounded
specifically in the subject being documented each time, never a copy of a previous manual's look pasted
onto new content. Reuse the same content as the `.md` (same sections, same facts, same tables) but author
it as real HTML — adapt the prose for on-screen reading rather than pasting Markdown verbatim, and add a
sticky/numbered table of contents once the manual has enough sections to warrant one.

Publish it (`Artifact` tool) with a real `title`, a one-line `description`, and a `favicon`, right after
the `.docx` is verified — don't leave it for a separate turn. When updating an already-published manual
later, republish the *same* Artifact (same file path this session, or its `url` from another session)
rather than creating a new one, so the link stays stable.

## Hard constraints — things that silently break the .docx (found the hard way)

- **Never write a literal `---` line (Markdown horizontal rule) anywhere in the .md.** Pandoc turns it
  into a legacy VML shape (`<w:pict><v:rect .../></w:pict>`) that Word renders fine and Google Docs does
  not. Separate sections with headings only.
- **Never pass `--toc` to pandoc for this template.** The reference doc has no `TOC1`/`TOC2`/`TOCHeading`
  styles, so the generated Table of Contents field is empty and some readers (Google Docs) fall back to
  rendering it as a bare bullet list instead of a real outline. Section numbers in the headings
  (`## 1. ...`, `## 2. ...`) are the navigation aid instead — plus the native Heading1/2/3 outline that
  every reader already builds from real heading styles.
- **Always convert with `--reference-doc=<this skill's dir>/reference.docx`, never with the raw
  `INVOICE_CONNECTOR_API_EN.docx`.** That original file is ARXI's real template but is itself fragile —
  its `styles.xml` had 155 duplicate `<w:style>` blocks (residue of its own prior generations) and was
  missing definitions for `Table`, `Compact`, `BodyText`, `FirstParagraph`, and `VerbatimChar` — all
  styles pandoc actively uses (`Compact`/`BodyText` for nearly every paragraph including table cells,
  `VerbatimChar` for every inline `code` span, `Table` for every table's border/shading). Undefined-but-
  referenced styles are exactly what produced the bullet-marker/no-border symptoms below. `reference.docx`
  in this skill folder is the same ARXI look (fonts, logo, footer) with all of that fixed — never
  regenerate it from the original without re-applying the same fixes.
- **Always run `rescale_tables.py` on every generated .docx afterward.** Pandoc sizes table columns in
  absolute twips based on Markdown content width, then marks the table as page-percentage — Word honors
  the percentage, other readers (Google Docs) honor the literal column widths instead, so tables render
  narrower than the page even though the percentage says 100%. The script recomputes the column widths to
  literally sum to the page's usable width (read from the document's own `pgSz`/`pgMar`, not hardcoded).
- **Synthetic flow diagrams (hand-drawn/SVG-rendered flowcharts) are opt-in, not part of the default
  structure** — only add them when the user explicitly asks for a diagram/flowchart in this invocation.
  This is separate from real screenshots of the running system, which are now the default for every
  manual (see "Every manual also ships as an Artifact" above) — that rule isn't opt-in. When a synthetic
  diagram is asked for:
  - Render as PNG (e.g. Chrome headless screenshotting a small inline-SVG HTML file — see the pattern
    used for this skill's own diagrams) at a generous device-scale (3-4x the logical SVG size) so it
    stays crisp once stretched to full page width.
  - **Orientation follows the target document's own orientation.** A manual (this template, portrait
    A4/Letter) gets **vertical** flow diagrams — boxes stacked top-to-bottom, full-width, one per row —
    never a wide horizontal left-to-right chain: at page width a horizontal chain is forced short and
    squat, so its internal text renders small even at high source resolution (this was the actual
    complaint behind "size and quality" the first time — not insufficient DPI, wrong aspect ratio for a
    portrait page). A presentation/slide deck (landscape) gets the opposite: horizontal chains. Pick
    orientation from the destination format, not habit.
  - A vertical chain with a fan-out (one box branching to several) needs a real trunk-and-branches
    connector: one vertical line down the trunk's full span, then a short independent horizontal segment
    into each target at its own y. Do not redraw the vertical segment per branch from a shared start
    point — each redraw re-spans the full distance to that branch's y, so every earlier target ends up
    with a stray vertical line drawn straight through its box (looks like strikethrough text).
  - Embed with `![caption](images/name.png){width=100%}` — **the `{width=100%}` is required**. Without
    it, pandoc sizes the image at its "natural" size (derived from raw pixel dimensions, generally
    nowhere near the page width), so it lands small with a lot of dead white space around it regardless
    of how high-resolution the source PNG is. `{width=100%}` makes pandoc emit an explicit
    `wp:extent` scaled to the text column width (verify with `grep -o 'wp:extent cx="[0-9]*"'` — should
    equal the page's usable width in EMU, `usable_width_twips * 635`).
  - **Attribute placement**: `{width=100%}` goes right after the closing `)` of the image syntax,
    `![alt](path){width=100%}` — not inside the parens. A sed/regex edit that isn't anchored on the
    literal `)` will silently put it inside the URL instead (`](path{width=100%})`), which pandoc just
    treats as part of the filename and ignores; always verify the generated `.md` has the attribute
    *outside* the parens before converting.
  - Images alongside the `.md`/`.docx` in an `images/` subfolder.
  - The first time this was done, pandoc's image-with-caption syntax pulled in three more styles this
    reference doc didn't define — `Figure`, `Caption`, `CaptionedFigure`, `ImageCaption` — same
    undefined-style symptom as `Compact`/`BodyText`/etc. They're now baked into `reference.docx`, so this
    is only a problem if `reference.docx` is ever regenerated from scratch instead of patched
    incrementally.
- **Font weight is encoded in the family name, not a separate property.** This template's fonts (Geist,
  Geist Mono) ship as distinct named weight variants (`Geist Mono`, `Geist Mono Medium`,
  `Geist Mono Light`, ...) — real, separately-named typefaces (confirmed: actual `.ttf` files with these
  exact names existed in a font-embedded copy of this docx), not one variable family with a weight
  dial. There is no OOXML property that sets "Geist Mono at weight 300" — only `<w:b/>` for bold/not-bold.
  To get a specific weight, reference to the exact named variant (`w:ascii="Geist Mono Light"`, not
  `"Geist Mono"` with some other weight hint) in `docDefaults`/the relevant style. Dropping the weight
  suffix to "fix" a font-not-appearing problem (see the entry below on Google Fonts naming) silently
  degrades to whatever the base family's default weight is — normal/regular, not light.
- **Known residual, not fully root-caused**: a faint bullet-style artifact can still show on some
  paragraphs in Google Docs even after all of the above (reported as "not as bad" after the fixes, not
  eliminated). Table/Compact/BodyText/FirstParagraph/VerbatimChar were the confirmed undefined-style
  causes; if it recurs, the next place to check is `numbering.xml`'s default list definitions and whether
  `docDefaults`/`Normal` picked up a stray `w:numPr` — diff `used styles vs. defined styles` and `direct
  w:numPr count` the same way this was diagnosed (see git history / conversation, not reproduced here).

## Pipeline

```bash
# 0. If a running instance is reachable, capture real screenshots first (see
#    "Every manual also ships as an Artifact" above) and save them into images/ —
#    the .md's image references need the files to already exist.

# 1. Write the .md file(s), following the structure above, referencing any
#    captured screenshots with ![caption](images/name.png){width=100%}.

# 2. Convert — no --toc, always this skill's reference.docx:
pandoc MANUAL.md -o MANUAL.docx --reference-doc="$(dirname "$0")/reference.docx"
# (if invoking by hand, replace "$(dirname "$0")" with this skill's actual directory)

# 3. Force full-width tables:
python3 <skill-dir>/rescale_tables.py MANUAL.docx

# 4. Sanity-check before handing back — undefined/duplicate styles are silent until opened elsewhere:
python3 - <<'PYEOF'
import zipfile, re
from collections import Counter
f = "MANUAL.docx"
z = zipfile.ZipFile(f)
doc = z.read('word/document.xml').decode('utf-8')
styles = z.read('word/styles.xml').decode('utf-8')
used = (set(re.findall(r'w:pStyle w:val="([^"]+)"', doc))
        | set(re.findall(r'w:rStyle w:val="([^"]+)"', doc))
        | set(re.findall(r'w:tblStyle w:val="([^"]+)"', doc)))
defined = re.findall(r'w:styleId="([^"]+)"', styles)
dups = {k: v for k, v in Counter(defined).items() if v > 1}
print("undefined styles used:", used - set(defined))
print("duplicate styleIds:", dups)
print("has ARXI branding:", "ARXI" in z.read('word/footer1.xml').decode('utf-8'))
PYEOF
# Expect: undefined=set(), dups={}, has ARXI branding=True. Investigate before delivering if not.

# 5. Build the Artifact: same content as the .md, authored as real HTML (load
#    artifact-design first), same captured screenshots inlined as base64.
#    Publish it with the Artifact tool, then hand back both links.
```

Save the `.md` next to the `.docx` (same basename), in the location the user's other manuals for this
project already live (check for a `Docs/manuals/`-style convention before creating a new one).

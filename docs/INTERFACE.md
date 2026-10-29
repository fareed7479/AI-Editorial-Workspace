# Interface walkthrough
**A small editorial studio in the Fieldnotes theme**

[Open application](https://fieldnotes-editorial-workspace.vercel.app/) · [Docs](README.md) · [Product decisions](PRODUCT.md)

## The route through the app

| View | Use it to | What persists |
| --- | --- | --- |
| Landing | Understand the workflow and enter/explore the sample | Navigation only |
| My workspace | Search, filter, sort and reopen projects | Saved projects/material |
| Research desk | Add/read sources and inspect brief/evidence | Sources and saved brief |
| Writing studio | Save text, review proposals and decide on changes | Original/current text and revisions |
| Compare revisions | Inspect differences, metrics and prior versions | Saved history |
| Export | Download saved Markdown and references | Download, not a publishing action |

There is no application login, sign-out or password gate. All Vercel production/preview links are also public. Older preview URLs represent older source versions; use production for the current demonstration.

## Landing and library

The cream/forest/sage palette, serif headings and restrained cards preserve the original editorial theme. Landing illustrations are CSS compositions, not screenshots of stored user content.

The library provides project search, source-count filters, title/date/source-count sorting, grid/list views, and saved source/brief/draft previews. Full-source dialogs offer more reading room; the sidebar toggle expands the editorial desk. This library browses application records, not files on the visitor's computer.

## Research controls

Paste articles, reports or tweet text, optionally retain an original URL, or try URL-only extraction. Inaccessible publishers show errors; manual paste remains available. Reliability labels are chosen by the editor. Sources without public URLs are visibly identified.

Build the baseline brief after collecting three sources. Review attributed excerpts, analysis prompts, audience and angle. Configured Gemini tools can add synthesis, contradictions and uncertainty; generated evidence remains unverified.

## Draft and suggestion controls

| Control | Behavior |
| --- | --- |
| Save draft | Preserve first original; record changed saved versions |
| Save & check writing | Analyze saved text with deterministic checks |
| Proposed rewrite | Editable; some passages require a reviewed replacement |
| Accept / Reject | Apply one decision; overlapping pending proposals become stale |
| Compare revisions | Inspect saved original/current text and history |
| Export | Download saved text; unsaved editor changes are excluded |

Unsaved-change prompts protect navigation and unload. There is no background autosave or one-click revision restore.

## Gemini panel

The panel exposes readiness/model, remaining requests, progress, safe errors and recent jobs. Writing/newsletter requests require saved state; research/newsletters require three sources. Generated newsletters appear as reviewable previews. **Use this draft** saves a revision; generating alone does not overwrite the draft.

## Feedback, accessibility and verification

Native dialogs, labeled inputs/buttons, visible loading/error/empty states and responsive layouts support the core flow. Public landing, a preview landing and frontend API reads return HTTP 200. Historical desktop/mobile checks exist, but a fresh complete deployed browser run remains pending. See [TESTING.md](TESTING.md).

# Product and engineering note
**Assignment Part D · Decisions behind Fieldnotes**

[Live app](https://fieldnotes-editorial-workspace.vercel.app/) · [Coverage](REQUIREMENTS.md) · [Architecture](ARCHITECTURE.md)

## Product thinking

| PDF question | Decision |
| --- | --- |
| Who is the primary user? | A newsletter editor interpreting AI developments for founders, builders and business operators. |
| Most important problem? | Moving from collected information to a defensible angle and readable draft without losing evidence or the author's qualifications. |
| Core workflow? | Collect at least three sources → review an attributed brief → save a draft → inspect and decide on suggestions → compare → export. |
| Priorities and omissions? | Prioritize source provenance, clear failure states, three useful writing checks and reversible editorial decisions. Omit news discovery, scheduling, collaboration, publishing and independent fact-checking. |
| How would usefulness be measured? | Observe time to a usable brief, time to an editor-approved draft, source-reference defects, accepted suggestions later reversed, and blinded editor ratings for clarity/meaning. These are proposed measures, not collected usage statistics. |

## Engineering

| PDF question | Decision |
| --- | --- |
| How is it structured? | React/Vite provides a small editorial interface; FastAPI validates requests; SQLAlchemy/Alembic manage persistent projects, sources, drafts, jobs and quotas. SQLite supports local use; Neon PostgreSQL supports Vercel. |
| AI versus deterministic logic? | Extraction/ranking, writing rules, metrics, offsets, revision handling and evidence checks are deterministic. Optional Gemini supplies research synthesis, contextual suggestions and proposed newsletters. No hidden model fallback is presented as AI output. |
| Inaccessible URLs and missing content? | Display the import error and allow pasted text. Retain the original URL when provided; show when a source has no public link. Reject empty/short and duplicate inputs; never invent content. |
| Unreliable output or failed requests? | Check schemas, known source IDs, exact excerpts, saved draft versions and input fingerprints. Show sanitized errors; preserve prior content; retain generation status. Bound provider retries and request size. A newsletter is a preview until explicitly applied. |
| How do links support claims? | Provenance comes from stored records, not model-supplied URLs. Exact excerpt checks establish textual attribution; they do not establish truth, independence or that an inference follows from the excerpt. The editor reviews context and meaning. |
| Another day of work? | Finish one-time live Gemini evaluation and full deployed browser acceptance; test inaccessible publishers and adversarial evidence; improve sentence/technical-term checks. For a long-lived public service, add per-user data isolation and stronger abuse controls. |

## Editorial judgment

| PDF question | Decision |
| --- | --- |
| What makes writing clear and useful? | A specific event, enough reader context, attributed evidence, explicit uncertainty and a practical implication. Preserve necessary technical detail instead of forcing every sentence to be short. |
| How would improvement be evaluated? | Compare original/revised drafts with source access and a fixed rubric: clarity, factual accuracy, qualification retention, audience relevance and usefulness. Have editors rate versions without knowing which was revised. Inspect changed claims, not just word counts. |
| What should never happen automatically? | Inventing facts, actors or citations; removing uncertainty; changing numerical claims, licensing or hardware conditions; erasing the original; mass-accepting edits; or publishing a draft. |

## Scope and trade-offs

- **Small app:** custom CSS/components and tab/hash navigation preserve a readable editorial theme without adding a UI framework.
- **Simple schema:** briefs and revision details use JSON inside relational records; this is a pragmatic single-workspace choice, not a collaboration design.
- **Conservative rules:** passive voice is only a candidate; a reviewed rewrite may be required. Long/technical prose can remain unchanged when context warrants it.
- **Explicit source limits:** three usable records can all come from one organization. Reliability labels are editor-supplied.
- **Public demonstration:** login was removed and all Vercel deployment URLs made public at the owner's request. Visitors share saved material and AI quota; this is not a private or multi-tenant service.
- **Assignment versus extensions:** the PDF asks for a lightweight tool, not production readiness. Later landing/library, Gemini and cloud phases were additional owner requests; the original time limit is not claimed as verified.

## Worked example

The [342-word newsletter](SAMPLE_NEWSLETTER.md) turns three publisher sources into a qualified deployment question. Its [before/after](BEFORE_AFTER.md) removes two pieces of optional emphasis using the actual writing engine. It preserves numerical claims and citations, and leaves longer technical passages for human review.

**Verification boundary:** cloud core-workflow checks, 54 backend tests and two frontend tests passed. Real Gemini output and the full deployed browser flow remain pending; [TESTING.md](TESTING.md) records the evidence.

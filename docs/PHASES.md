# Delivery phases and requirement matrix

Implemented against the recovered Python + SQL + React assignment plan. Scope assumptions and departures are explicit in PRODUCT.md and AI_DISCLOSURE.md.

| Phase | Delivered | Verification | Status |
| --- | --- | --- | --- |
| 1 · Foundation | FastAPI, SQLAlchemy, React/TypeScript/Vite, PostgreSQL/SQLite configuration | Dependency install and production build | Complete |
| 2 · Research | Persisted projects and article/report/tweet sources, minimum 3, duplicate detection, evidence URLs/excerpts, reliability, speculation, what/why/who/angle | API + extraction boundary tests | Complete, extractive mode |
| 3 · Writing | Long sentences, filler, passive candidates; passage/explanation/rewrite; accept/reject; originals, revisions, metrics | Backend and live browser flows | Complete |
| 4 · Workspace | Responsive research/editor/compare views, loading/empty/error states, unsaved guards, export | Desktop and mobile browser workflows and screenshots | Complete |
| 5 · Verification | Pytest, Vitest, Playwright, CI with PostgreSQL migrations and end-to-end checks | 20 backend + 2 frontend + 4 browser tests pass locally | Local checks complete; remote CI unverified |
| 6 · Handoff | Setup, product note, architecture, schema/API, AI disclosure, sourced newsletter, before/after and sample seed | 365-word retrospective, sources inspected; seed executed | Complete |
| 7 · Release | Dependency locks, Docker/Compose, launch scripts, validation record, GitHub commits | Production build and SQLite migration round trip | Source delivery complete; Docker/PostgreSQL runtime unverified locally |

## Requirement traceability

| Requirement | Implementation | Evidence |
| --- | --- | --- |
| Three or more sources | SourceInput, add_source, build_brief | test_complete_persisted_workflow |
| Article/URL/tweet input | Source form; optional HTTPX extraction | Browser pasted-source test; controlled import tests |
| Structured what/why/who/angle | research.py with per-source evidence and analysis fields | Brief API assertions; real sample seed |
| Original-source links | Source URLs, evidence URLs, Markdown references | API and browser export tests |
| Fact vs analysis/speculation | source_claim or speculation; verified=false; analysis prompts labeled | test_speculation_and_topic_prompts |
| Reliability | Editor-supplied primary/secondary/unverified with caveat | Source form and brief disclosure |
| At least 3 actionable writing checks | writing.py | test_three_checks_and_metrics |
| Passage, rationale, rewrite, accept/reject | SuggestionCard and decide | Desktop/mobile editing tests |
| Preserve original and compare | Draft.original, revisions, Compare Revisions | Persistence and accept/reject tests |
| Useful metrics | Word/sentence counts, average length, long sentences, reading time | Unit and UI displays |
| Sample 300–500-word editorial output | SAMPLE_NEWSLETTER.md, three linked primary sources | 365 words before source list, including heading/date |
| Before/after example | BEFORE_AFTER.md | Explicit decisions and preserved qualifications |
| Documentation and reproducibility | README, PRODUCT, ARCHITECTURE, AI_DISCLOSURE, TESTING, locks, CI, launchers | Actual validation record |

## Deliberate scope decisions

No mandatory model key: extractive research and deterministic writing functions run locally. Source claims are not verified facts; analysis is an editorial prompt, not a generated conclusion. Pasted source text is first class and no fictional content is substituted for failed imports. The in-app demo is explicitly fictional, while the separate sourced newsletter is an August 2025 retrospective.

The custom React UI replaces the proposed Tailwind/shadcn/Router layer; this small workspace uses tab state. External LLM adapters, authentication and multi-user editing are not implemented. No MongoDB, Express, Next.js, LangChain, vector database, agents, queues or Redis were introduced. Public API exposure is outside the validated single-editor setup.

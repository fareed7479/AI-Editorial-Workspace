# Delivery phases

| Phase | Scope | Acceptance |
| --- | --- | --- |
| 1 | Foundation | Python/FastAPI, SQLAlchemy/Alembic, PostgreSQL/SQLite, React/TypeScript/Vite, reproducible setup |
| 2 | Research | Persist projects and 3+ articles/URLs/tweets; attributable excerpts, reliability, source claims vs analysis, what/why/who and angles |
| 3 | Writing | Long sentences, filler, passive candidates; passage/explanation/rewrite; accept/reject, original/revisions, metrics |
| 4 | Workspace | Responsive research/editor/compare workflow, loading/empty/error states, export |
| 5 | Verification | Controlled API/unit/UI tests, CI, failures and edge cases |
| 6 | Handoff | Product, architecture, database/API, AI disclosure, sample newsletter and before/after |
| 7 | Release | Build, tests, resolve failures, final commit, document limits |

Each phase has its own commit. Validation evidence is in TESTING.md.

## Decisions

Use extractive research and deterministic writing checks without API keys. Excerpts are attributed source claims, never independently verified facts. Editorial implications are explicitly labeled analysis. Pasted article/tweet content is first class; URL import is optional. No invented source content or fake LLM results. No agents, Redis, queues or vector databases. Optional model integration is deferred. Single editor deployment; authentication is required before exposing the write-enabled server publicly.

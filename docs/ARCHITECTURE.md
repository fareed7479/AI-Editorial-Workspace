# Architecture, persistence, and API

**Purpose:** map the current code to its components, stored data, HTTP contract, and editing lifecycle.

[Documentation guide](README.md) · [Product](PRODUCT.md) · [Testing](TESTING.md) · [Cloud roadmap](ROADMAP.md)

## Current system

| Component | Implementation | Responsibility |
| --- | --- | --- |
| Browser UI | React, TypeScript, Vite, Lucide | Project navigation; research, editing, comparison, state feedback |
| API client | [api.ts](../frontend/src/api.ts) | JSON requests, readable errors, export URL |
| HTTP service | [main.py](../backend/app/main.py) | FastAPI routes, Pydantic validation, persistence coordination |
| Persistence | [database.py](../backend/app/database.py) | SQLAlchemy models, engine, request-scoped sessions |
| Research | [research.py](../backend/app/research.py) | URL validation/import, excerpt ranking, speculation cues, analysis prompts |
| Writing | [writing.py](../backend/app/writing.py) | Metrics, checks, suggestion decisions, offset/version handling |
| Schema history | [migrations/](../backend/migrations/) | Alembic upgrade/downgrade |

The UI calls /api endpoints on the configured API origin. FastAPI reads/writes SQL and returns the saved workspace. Optional URL imports fetch and extract a public page before storage. There is **no runtime LLM client, generation stream, queue, or background worker**.

## Stack and repository boundaries

- **Frontend:** custom React components and CSS; one workspace uses tab state rather than a routing framework.
- **Backend:** synchronous FastAPI endpoints with SQLAlchemy sessions and Pydantic request schemas.
- **Database:** SQLite for local development; PostgreSQL driver and schema migration path prepared for deployment.
- **Extraction:** HTTPX, Trafilatura, and BeautifulSoup.
- **Verification:** Pytest/HTTPX, Vitest, and Playwright; see [TESTING.md](TESTING.md).

## Landing and workspace view state

The root URL renders Landing.tsx; #/workspace selects the workspace without a routing dependency. Hash changes support browser navigation and guard unsaved draft text. WorkspaceLibrary.tsx reuses GET /api/projects and GET /api/projects/{id} for browsing and previews, so the SQL schema and backend API are unchanged. SourceReader.tsx and ProjectDialog.tsx use native modal dialogs. The existing App.tsx still owns editing and saved project state. See [INTERFACE.md](INTERFACE.md).

## Relational model

IDs are generated UUID strings stored in string columns. The database has three application tables:

| Table | Main fields | Relationships and constraints |
| --- | --- | --- |
| projects | id, title, created_at, brief JSON nullable | One-to-many sources; optional one-to-one draft |
| sources | id, project_id, title, url nullable, content, kind, reliability, created_at | Foreign key and index on project_id |
| drafts | id, project_id, original, current, version, suggestions JSON, revisions JSON | Unique project_id; foreign key to project |

ORM relationships configure dependent-record cleanup; foreign keys declare cascade deletion. No project-delete endpoint or UI is currently exposed.

| JSON payload | Stored content |
| --- | --- |
| Brief | Method, per-source items, selected evidence, analysis fields, overall angle, limitations |
| Evidence | Source ID/title/URL, exact excerpt, source_claim or speculation, verified=false |
| Suggestion | ID, kind, passage, character offsets, replacement, explanation, manual-edit flag, status |
| Revision | Previous version number, previous text, reason for the change |

Current JSON columns avoid extra tables for a small single-editor history. No vector database or full-text index is required by the implemented workflow.

## HTTP API

All paths below begin **/api**. Request/response schemas can be explored at [local /docs](http://127.0.0.1:8000/docs).

| Method | Path | Request / effect |
| --- | --- | --- |
| GET | /health | SQL connectivity check and deterministic-mode response |
| GET | /projects | List project ID, title, source count |
| POST | /projects | title; create project, HTTP 201 |
| GET | /projects/{id} | Sources, saved brief, draft, suggestions, history, metrics |
| POST | /projects/{id}/sources | title, optional url/content, kind, reliability; HTTP 201 |
| DELETE | /projects/{id}/sources/{source_id} | Remove source and clear saved brief |
| POST | /projects/{id}/brief | Require 3+ sources; build and persist brief |
| PUT | /projects/{id}/draft | text; version required when updating an existing draft |
| POST | /projects/{id}/analyze | Exact saved text and current version; replace suggestions |
| POST | /projects/{id}/suggestions/{sid} | action=accept/reject, current version, optional replacement |
| GET | /projects/{id}/export | Saved Markdown draft and source references |

Example payloads:

~~~json
{"title": "This week's local inference briefing"}
~~~

~~~json
{"title": "Source title", "url": "https://example.com/report", "content": "Paste at least 40 characters of original source content here.", "kind": "report", "reliability": "unverified"}
~~~

~~~json
{"action": "accept", "version": 2, "replacement": "The reviewed replacement passage."}
~~~

The example source URL is illustrative. Sending it without pasted content would request an actual import; it is not a supplied article.

| Response | Meaning |
| --- | --- |
| 404 | Project or source not found |
| 409 | Draft version/text is stale; reload or save before continuing |
| 422 | Invalid input or unmet workflow precondition |

## Editing and invalidation rules

1. **First save:** set original and current text; original is not subsequently overwritten.
2. **Manual edit:** save prior current text in history, update current, increment version, clear suggestions. Saving identical text does not add a revision.
3. **Analyze:** require exact saved text/version; generate a fresh set of suggestions.
4. **Reject:** mark the chosen suggestion rejected; text and draft version stay unchanged.
5. **Accept:** verify the stored passage at its offsets; save previous text, apply rewrite, increment version, mark it accepted.
6. **After acceptance:** shift later offsets and mark overlapping pending suggestions stale. Run checks again when needed.
7. **Compare/export:** use saved server state. Source changes clear the brief but do not automatically regenerate or rewrite the draft.

Sequential stale requests are rejected. The version check is **not an atomic compare-and-swap transaction**, so simultaneous multi-editor writes require further work. History is inspectable, not a full restore/undo API.

## Input and import boundaries

| Input | Limit / behavior |
| --- | --- |
| Project title | 1–160 characters; blank values rejected |
| Source title | 1–240 characters; blank values rejected |
| Source URL | Up to 2,048 characters; HTTP(S), no credentials, standard ports only |
| Sources | Up to 20 per project; minimum 3 to build brief |
| Source content | At least 40 characters; pasted input up to 50,000 |
| Draft/replacement | Up to 50,000 characters per input |
| Imported body | Up to 2,000,000 bytes; extracted text capped at 50,000 characters |
| Network behavior | 12-second HTTPX timeout; no redirect following; reject non-global DNS addresses and unsupported response types |

DNS validation and connection resolution happen separately; network egress restrictions are still needed to address DNS rebinding. React renders content as text rather than injected HTML. See [AI_DISCLOSURE.md](AI_DISCLOSURE.md).

## Local operation and deployment state

Run the API from backend/ so the default SQLite URL resolves to backend/editorial.db. SQLite creates a fresh local schema on startup; PostgreSQL requires Alembic migrations before traffic. Close the local API before copying a SQLite backup. PostgreSQL backup/restore should be tested against a separate database before changing production configuration.

[compose.yaml](../compose.yaml) defines a local PostgreSQL/API/web topology with readiness checks. It has not been executed successfully in the recorded environment. The [CI workflow](../.github/workflows/ci.yml) declares PostgreSQL migration and browser checks; no remote success is asserted here.

**Planned:** adapt the FastAPI entrypoint and frontend routing for Vercel, connect managed PostgreSQL, add access controls, and introduce a validated Gemini adapter. The architecture above describes current code, not those future services.

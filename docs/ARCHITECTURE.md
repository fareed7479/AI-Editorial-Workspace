# Architecture and API
**React/Vite · FastAPI · SQLAlchemy/Alembic · SQLite/Neon**

[Docs](README.md) · [Product decisions](PRODUCT.md) · [Deployment](DEPLOYMENT.md)

## Request and data flow

~~~mermaid
flowchart TD
  UI["Browser: editorial workspace"] --> API["FastAPI: validation and mutations"]
  API --> DB["SQL: content, revisions, jobs, quota"]
  API --> Rules["Deterministic research and writing"]
  API --> Gemini["Optional Gemini: validated proposals"]
  Rules --> API
  Gemini --> API
~~~

The production frontend proxies /api to the API project. Local development uses VITE_API_URL. Backend credentials never enter the React bundle. Source/draft text is sent to Google only for explicit Gemini generation.

## Code responsibilities

| Module | Responsibility |
| --- | --- |
| frontend/src/App.tsx | Workspace state, source/draft actions, unsaved-change guards |
| Landing / WorkspaceLibrary / SourceReader / ProjectDialog | Entry page, saved-material browsing, full-source and creation dialogs |
| AIStudioPanel | Progress, history, error display and newsletter preview/application |
| backend/app/main.py | Content API, validation, origin checks, no-store responses |
| research.py / writing.py | Extraction/ranking; metrics, checks and exact-offset decisions |
| gemini.py / ai_schemas.py / ai_editorial.py | SDK transport; schemas; prompts and evidence/meaning checks |
| ai_routes.py / limits.py | Generation lifecycle, replay, SQL quota, stale-state checks |
| config.py / database.py / serializers.py | Settings, SQL models/sessions and API representations |
| migrations | Additive schema upgrades |

## Persistent model

| Table | Main content |
| --- | --- |
| projects | UUID, title, created time, nullable brief JSON |
| sources | Project FK, title, optional original URL, text, type, reliability, created time |
| drafts | Unique project FK, immutable original, current text, version, suggestions/revisions JSON |
| generation_jobs | UUID request ID, project FK, kind/status, model/provider, input fingerprint, usage/result/error metadata |
| request_quotas | Atomic counters keyed by UTC AI day or other quota key |

Projects own sources and an optional draft. Briefs/revisions use JSON rather than separate tables to keep the single-workspace model small. Relationships configure dependent-record cleanup; no project-delete/restore UI is exposed. PostgreSQL mutations lock the project row; SQLite remains local single-editor use.

## Content HTTP contract

All routes below start with **/api**. There are no application login/session endpoints.

| Method | Path | Effect |
| --- | --- | --- |
| GET | /health | Check SQL connectivity and report configured mode |
| GET / POST | /projects | List summaries / create a project |
| GET | /projects/{id} | Load sources, brief, draft, metrics and history |
| POST | /projects/{id}/sources | Validate/import and save source; clear brief |
| DELETE | /projects/{id}/sources/{source_id} | Remove source; clear brief |
| POST | /projects/{id}/brief | Require three sources; save deterministic brief |
| PUT | /projects/{id}/draft | Save text; require version for an existing draft |
| POST | /projects/{id}/analyze | Require exact saved text/version; replace suggestions |
| POST | /projects/{id}/suggestions/{sid} | Accept/reject with version and optional reviewed replacement |
| GET | /projects/{id}/export | Download saved Markdown and references |

## Gemini HTTP contract

| Method | Path | Effect |
| --- | --- | --- |
| GET | /ai/config / /ai/usage | Non-secret readiness, model/limits and daily quota |
| POST | /projects/{id}/ai/generate | UUID, kind and draft version; NDJSON progress/result |
| GET | /projects/{id}/ai/jobs | Most recent ten jobs |
| GET | /projects/{id}/ai/jobs/{job_id} | One persisted job/result |
| POST | /projects/{id}/ai/jobs/{job_id}/apply | Explicit, version-checked newsletter application |

Typical failures: 404 missing record; 409 stale state or incompatible request replay; 422 invalid input/precondition; 429 cap/provider quota; 503 missing provider/cloud configuration. Streaming failures use a labeled error event after HTTP streaming begins. [AI integration](AI_INTEGRATION.md) describes replay and cancellation limits.

## Editing lifecycle

1. First save establishes original/current text.
2. A changed manual save records prior text, increments version and clears suggestions.
3. Analysis uses the exact saved text; reject changes status only.
4. Accept verifies passage offsets, stores the prior version and applies the reviewed replacement.
5. Later offsets shift; overlapping pending suggestions become stale.
6. Recheck after edits. Compare/export use saved state, not unsaved editor text.

Source changes invalidate the brief; changed sources/brief/draft invalidate an in-flight AI result. Applying a newsletter stores a revision and preserves the original. There is no auto-publication or background autosave.

## Input boundaries

| Input | Limit |
| --- | --- |
| Project / source title | 160 / 240 characters |
| Original URL | 2048 characters; public HTTP(S), no URL credentials or unusual ports |
| Source text / draft / replacement | 50000 characters per input |
| Sources | At most 20 per project; at least 3 for research/newsletter |
| Imported response | At most 2000000 bytes; extracted text capped at 50000 |
| Import timeout | 12 seconds; no redirect following |
| AI request / response | Configurable; see AI_INTEGRATION.md |

Import validation rejects non-global resolved addresses and unsupported content types. DNS validation and connection resolution remain separate: DNS-rebinding protection is incomplete. Reliability is a label, not fact-checking. React renders source content as text.

## Operations

SQLite creates a local schema for zero-setup use. Vercel requires PostgreSQL and migrations; its filesystem is not persistent storage. API builds run migrations, rollback-safe non-AI verification and backend tests. Frontend builds run tests, TypeScript and Vite. There is no queue, agent framework, vector database or multi-tenant account layer.

[Validation](TESTING.md) · [Disclosure](AI_DISCLOSURE.md) · [Requirement mapping](REQUIREMENTS.md)

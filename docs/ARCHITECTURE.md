# Architecture, data and API

React (Vite/TypeScript) calls a synchronous FastAPI service over JSON. SQLAlchemy persists relational records; Alembic owns deployment schema changes. SQLite is the local fallback and PostgreSQL is the configured deployment database. HTTPX imports public pages; Trafilatura and BeautifulSoup extract text. The research and writing services are separate Python functions.

## Data model

| Table | Columns | Relationships |
| --- | --- | --- |
| projects | UUID id, title, created_at, brief JSON nullable | 1:N sources; 1:1 draft |
| sources | UUID id, project_id FK, title, URL nullable, text, kind, reliability, created_at | Indexed project FK; cascade deletion |
| drafts | UUID id, unique project_id FK, original, current, version, suggestions JSON, revisions JSON | Original preserved across manual and accepted edits |

Evidence JSON contains source ID/title/URL, exact excerpt, type, verification flag. Suggestions include stable IDs, character offsets, passage, rewrite, explanation, manual-edit flag and status. Revisions contain prior saved text/version/reason. JSON columns work on SQLite and PostgreSQL; full-text/vector indexing is unnecessary for this scope.

## Endpoints

All routes begin /api. Interactive schemas: GET /docs.

| Method | Path | Behavior |
| --- | --- | --- |
| GET | /health | Database connectivity and deterministic mode |
| GET / POST | /projects | List / create projects |
| GET | /projects/{id} | Entire persisted workspace |
| POST | /projects/{id}/sources | Add pasted or URL-imported source |
| DELETE | /projects/{id}/sources/{source_id} | Remove source; invalidate brief |
| POST | /projects/{id}/brief | Require 3+ sources; persist extractive brief |
| PUT | /projects/{id}/draft | Initial text or manual edit; version required on update |
| POST | /projects/{id}/analyze | Analyze exact saved text and version |
| POST | /projects/{id}/suggestions/{sid} | accept/reject, version, optional replacement |
| GET | /projects/{id}/export | Download saved text and source references |

Validation errors: 422; missing resources: 404; stale draft: 409. Text input is capped at 50,000 characters, source counts at 20, imports at 2 MB. Redirects, URL credentials and unusual ports are rejected. DNS checks block non-global addresses, but infrastructure egress restrictions are still needed against DNS rebinding. No raw HTML is rendered in React.

## State and concurrency

The server is authoritative; React reloads each mutation response. SQLite writes survive restarts. Draft decisions adjust offsets for later suggestions and mark overlaps stale. Manual edits clear old suggestions. Sequential stale requests are rejected by version checks; this is not a transactional simultaneous-editor collaboration protocol. A future multi-user release needs atomic compare-and-swap updates and identity/ownership rules.

## Operations

Single API instance, single frontend, one SQL database. Back up PostgreSQL with pg_dump; restore to a separate database before switching DATABASE_URL. For SQLite, stop the API before copying editorial.db. Do not check database files or .env into Git. Deploy migrations before traffic. A static frontend build alone cannot host the Python API.

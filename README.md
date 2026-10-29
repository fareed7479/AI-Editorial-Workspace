# Fieldnotes · AI Editorial Workspace

An evidence-first research desk and writing studio for a single newsletter editor. React/TypeScript/Vite, Python/FastAPI and SQLAlchemy. PostgreSQL is the deployment database; SQLite provides a zero-service local start. No LLM key is needed.

Dependency versions verified for this delivery are pinned in backend/requirements.lock and frontend/package-lock.json. backend/requirements.txt lists the supported top-level ranges.

## Start locally

Requires Python 3.10+ and Node 22+. From the repository root:

~~~powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r backend\requirements.lock
npm ci --prefix frontend
.\scripts\dev.ps1
~~~

On macOS/Linux use .venv/bin/python, then sh scripts/dev.sh. Open http://127.0.0.1:5173. The Windows script starts a hidden backend and stops it when the foreground frontend exits. To run separately:

~~~powershell
# Terminal 1, from backend/
..\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000
# Terminal 2, from frontend/
npm run dev
~~~

The API is at http://127.0.0.1:8000; interactive API docs are at /docs. SQLite data lives in backend/editorial.db when launched as above. Always launch from backend/ so the same database is used.

## Walk through the product

1. Create a project, or open the explicitly fictional sample from the overview.
2. Add three distinct sources: original URLs with pasted content, pasted articles/tweets without URLs, or URL-only imports. Supply a title and your reliability assessment.
3. Build the brief. Review attributed excerpts, speculation labels and analysis prompts. Claims are not automatically fact-checked.
4. Write or paste a draft in the Writing Studio. Save & check writing.
5. Review long sentences, filler phrases and passive-voice candidates. Edit rewrites before accepting if needed; reject suggestions you do not want. Overlapping suggestions become stale; run checks again.
6. Compare the immutable original with the current draft and inspect prior versions. Export the saved draft plus source references as Markdown.

Unsaved drafts are guarded during navigation and page unload. There is no background save. Export uses the saved draft.

## Configuration

.env.example lists variables; the file is a reference, not loaded automatically by every command. Set backend environment variables in the terminal, or use uvicorn --env-file ../.env. Put VITE_API_URL in frontend/.env.local if needed. Defaults work without configuration.

| Variable | Purpose | Default |
| --- | --- | --- |
| DATABASE_URL | SQLAlchemy database URL; use postgresql+psycopg:// for PostgreSQL | sqlite:///./editorial.db |
| CORS_ORIGINS | Comma-separated exact frontend origins | localhost:5173 and 127.0.0.1:5173 over HTTP |
| VITE_API_URL | API origin compiled into frontend | http://127.0.0.1:8000 |
| POSTGRES_PASSWORD | Required for Compose; use a URL-safe strong password | none |

For PostgreSQL, from backend/ set DATABASE_URL then run alembic upgrade head before starting. SQLite auto-creates fresh tables; Alembic also supports fresh SQLite databases. Do not run the initial migration on an auto-created SQLite database; use a new database or, only after checking the existing schema matches, alembic stamp head.

## Container deployment

Create a root .env with POSTGRES_PASSWORD set, then docker compose up --build. Open http://localhost:8080. API is on localhost:8000; PostgreSQL stays inside Docker with a persistent volume. Exposed services bind to loopback. Migrations run before API startup.

This single-editor application has no login. Public hosting requires an authenticated gateway, HTTPS, request limits and restricted outbound networking. Do not expose the write-enabled API directly. Container and live PostgreSQL validation status is recorded in docs/TESTING.md.

## Real-source sample

With the API running, execute .venv/Scripts/python.exe scripts/seed_sample.py from the repository root. It creates the dated real-source retrospective using attributed editorial paraphrases; it does not download or invent article text. The in-app sample remains explicitly fictional for repeatable tests.

## Checks

~~~powershell
cd backend
..\.venv\Scripts\python.exe -m pytest -q
cd ../frontend
npm test
npm run build
npx playwright install chromium
# Start backend first, then:
npm run test:e2e
~~~

Playwright starts/reuses the frontend and tests desktop and 390px mobile against the real backend. It uses synthetic sources, never live publisher content. Test-created projects persist in the development database; CI uses a temporary database.

## Documentation

- [Phase and requirement matrix](docs/PHASES.md)
- [Product note](docs/PRODUCT.md)
- [Architecture, schema and API](docs/ARCHITECTURE.md)
- [AI disclosure and reliability](docs/AI_DISCLOSURE.md)
- [Actual validation results](docs/TESTING.md)
- [Real-source newsletter sample](docs/SAMPLE_NEWSLETTER.md)
- [Before/after example](docs/BEFORE_AFTER.md)

## Limits

Research is extractive with deterministic topic-specific editorial prompts, rather than generative synthesis. It cannot establish truth or source independence. Writing rules can flag acceptable prose and miss complex grammar. Passive candidates and some long sentences need a human rewrite. URL import rejects redirects, private/reserved hosts, non-text formats and large responses; publishers can block extraction. Paste text instead. See the disclosure for DNS/egress limits. Local inference and external LLM APIs are not integrated. The sample project is fictional; the separate sourced newsletter is an explicitly dated retrospective.

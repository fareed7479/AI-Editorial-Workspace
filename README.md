# Fieldnotes | AI Editorial Workspace

**Collect evidence. Develop a brief. Edit with control.**

Fieldnotes is a single-editor workspace built with **React + TypeScript, Python + FastAPI, and SQL**. It connects source collection, research assistance, draft editing, revision comparison, and Markdown export in one interface.

> **Current status — October 29, 2026:** the local workflow is implemented and tested. Research is extractive; writing checks are rule-based. **Gemini integration, streaming, authentication, and Vercel deployment are planned, not implemented.**

[Quick start](#quick-start) · [Workflow](#the-editorial-workflow) · [Feature status](#feature-status) · [Documentation](docs/README.md) · [Next phases](docs/ROADMAP.md)

## Quick start

### Existing project setup

If dependencies are already installed, open PowerShell in the repository root:

~~~powershell
.\scripts\dev.ps1
~~~

Open **[http://127.0.0.1:5173](http://127.0.0.1:5173)**. Keep the terminal open; press **Ctrl+C** to stop the frontend and let the launcher stop its backend process. The launcher uses ports 5173 and 8000; stop another app using those ports before starting.

### First-time setup on Windows

Requires **Python 3.10+** and **Node.js 22+**:

~~~powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r backend\requirements.lock
npm ci --prefix frontend
.\scripts\dev.ps1
~~~

Use a working Python executable if the Windows python command opens an installation alias. The launcher uses the virtual environment after it has been created.

### First-time setup on macOS/Linux

~~~sh
python3 -m venv .venv
.venv/bin/python -m pip install -r backend/requirements.lock
npm ci --prefix frontend
sh scripts/dev.sh
~~~

No Docker, cloud database, or LLM key is needed for the default local workflow.

| Address | Purpose |
| --- | --- |
| [Frontend](http://127.0.0.1:5173) | Editorial workspace |
| [API health](http://127.0.0.1:8000/api/health) | Backend/database connectivity |
| [API documentation](http://127.0.0.1:8000/docs) | Interactive endpoint schemas |

## The editorial workflow

1. **Create a project** or choose **Open sample project** for a fictional demonstration.
2. **Collect at least three distinct sources.** Paste article, report, or tweet text; optionally retain an original URL. URL-only import is supported where the publisher permits extraction.
3. **Build a brief.** Review linked excerpts, reported claims, heuristic speculation labels, and editorial analysis prompts.
4. **Write a draft.** The first saved text becomes the preserved original. There is no background autosave.
5. **Save & check writing.** Review long sentences, filler phrases, and passive-voice candidates; change a proposed rewrite, accept it, or reject it.
6. **Compare revisions.** Inspect the original, current version, metrics, and prior saved text. Overlapping edits require fresh checks.
7. **Export Markdown.** Download the saved draft and source references. Export does not include unsaved editor text.

Research assistance does not establish whether a claim is true. The editor remains responsible for evidence, technical meaning, and publication decisions.

## Feature status

| Area | Available now | Limit or remaining work |
| --- | --- | --- |
| Projects | Create, list, search, reopen | No account ownership or collaboration |
| Sources | Paste/import, classify, remove, reject duplicates | Publisher restrictions; reliability is editor-supplied |
| Research | Source-linked extracts and what/why/who/angle fields | No LLM synthesis or independent fact-checking |
| Writing | Three checks and individual accept/reject | Complex rewrites need human review |
| Revisions | Original preservation, version history, metrics | No transactional simultaneous-editor protocol |
| Interface | Responsive research, writing, comparison, and state handling | Mobile viewport tested; no native mobile app |
| Delivery | Tests, CI configuration, dependency locks, containers | Cloud runtime and public deployment unverified |
| Gemini/Vercel | Agreed next direction | Integration and deployment not started |

## Project structure

| Path | Responsibility |
| --- | --- |
| [frontend/](frontend/) | React UI, API client, sample inputs, unit/browser tests |
| [backend/app/](backend/app/) | FastAPI routes, SQL models, research and writing functions |
| [backend/migrations/](backend/migrations/) | Alembic schema history |
| [backend/tests/](backend/tests/) | Controlled API and service tests |
| [scripts/](scripts/) | Local launchers and real-source sample seeder |
| [docs/](docs/README.md) | Product, implementation, evidence, examples, and roadmap |
| [.github/workflows/ci.yml](.github/workflows/ci.yml) | Automated test/build/PostgreSQL checks |
| [compose.yaml](compose.yaml) | Local container topology; not a Vercel deployment |

## Configuration and persistence

The defaults work without an environment file. [.env.example](.env.example) lists supported variables; the launch script does **not** automatically load a root .env. Set backend variables in the shell, or start Uvicorn with --env-file ../.env. Vite reads frontend/.env.local separately.

| Variable | Used by | Purpose/default |
| --- | --- | --- |
| DATABASE_URL | Backend | sqlite:///./editorial.db locally; PostgreSQL uses postgresql+psycopg:// |
| CORS_ORIGINS | Backend | Exact allowed origins; defaults to HTTP localhost:5173 and 127.0.0.1:5173 |
| VITE_API_URL | Frontend build/dev | API origin; default http://127.0.0.1:8000 |
| POSTGRES_PASSWORD | Docker Compose | Required URL-safe password for the container database |

Launch the backend from **backend/** so local data consistently uses **backend/editorial.db**. A different working directory can create a different SQLite file. Database files and secrets are ignored by Git.

For PostgreSQL, set DATABASE_URL and run alembic upgrade head from backend/ before serving requests. SQLite auto-creates a fresh local schema. Do not run the initial migration over an auto-created SQLite schema; use a fresh database or, only after confirming an exact schema match, stamp its migration state.

## Tests and build

~~~powershell
# From the repository root
cd backend
..\.venv\Scripts\python.exe -m pytest -q
cd ..\frontend
npm test
npm run build
npx playwright install chromium
# With the backend running in another terminal:
npm run test:e2e
~~~

Use ../.venv/bin/python on macOS/Linux. Playwright starts/reuses the frontend and tests the real API. Test-created projects remain in the selected database; use a disposable database when needed.

**Recorded local results:** 20 backend tests, 2 frontend tests, 4 desktop/mobile browser tests, the production build, and a SQLite migration round trip passed. These are prior implementation results, not tests rerun by this documentation refresh. See [TESTING.md](docs/TESTING.md) for evidence and limits.

## Samples and containers

- **Fictional UI sample:** open it from the overview; no external source fetch is needed.
- **Real-source retrospective:** read [SAMPLE_NEWSLETTER.md](docs/SAMPLE_NEWSLETTER.md). With the API running, execute .venv/Scripts/python.exe scripts/seed_sample.py from the root. Each run creates a new project using attributed editorial paraphrases.
- **Docker Compose:** create a root .env containing POSTGRES_PASSWORD, start Docker Desktop, then run docker compose up --build. The proposed local endpoints are http://localhost:8080 and http://localhost:8000. PostgreSQL uses a persistent volume; exposed services bind to loopback. **This container path has not been verified because the Docker engine was unavailable.**

## Documentation

| Read this | For |
| --- | --- |
| [Documentation guide](docs/README.md) | Where to start and how the documents fit together |
| [Product note](docs/PRODUCT.md) | User journey, scope, and design decisions |
| [Architecture and API](docs/ARCHITECTURE.md) | Components, persistence, endpoints, and edit behavior |
| [Phases and requirements](docs/PHASES.md) | Delivered phases, requirement evidence, and commit history |
| [Testing](docs/TESTING.md) | Actual results, reproduction commands, and gaps |
| [AI disclosure](docs/AI_DISCLOSURE.md) | Runtime behavior, data flow, safeguards, and limitations |
| [Newsletter sample](docs/SAMPLE_NEWSLETTER.md) | A dated, sourced editorial example |
| [Before/after example](docs/BEFORE_AFTER.md) | Review decisions and meaning preservation |
| [Roadmap](docs/ROADMAP.md) | Planned Gemini and Vercel phases |

**Deployment boundary:** this is a single-editor application without login or AI usage controls. Protect the backend before public exposure. Gemini credentials, managed PostgreSQL, and verified Vercel configuration belong to the next phases.

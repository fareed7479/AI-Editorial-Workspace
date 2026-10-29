# Testing and validation record

**Purpose:** distinguish observed results from configured checks and make the local verification workflow reproducible.

[Documentation guide](README.md) · [Phase matrix](PHASES.md) · [Architecture](ARCHITECTURE.md) · [Future acceptance criteria](ROADMAP.md)

> **Evidence date:** October 29, 2026. Results below come from the original implementation session. The documentation refresh itself did not rerun the app tests; the subsequent UI follow-up is recorded separately below. No successful remote CI/deployment run is claimed.

## Landing/library follow-up — October 29, 2026

After the documentation refresh, the interface was extended with a landing page, searchable grid/list project library, saved-material previews, native dialogs, full-source reading, and an expandable editor.

| Follow-up check | Observed result |
| --- | --- |
| Frontend Vitest | Existing 2 tests passed |
| TypeScript + Vite production build | Passed after the final source change; 1,586 modules transformed |
| Full desktop/mobile Playwright suite | 10 passed in 43.9 seconds after list-preview labeling and mobile overflow fixes |
| Final preview auto-scroll refinement | Affected desktop/mobile preview cases rechecked: 2 passed in 18.6 seconds |
| Visual review | Desktop landing and project library screenshots inspected; mobile illustration overflow fixed and viewport assertion passed |
| Visible preview handoff | Browser panel could not open; existing local services returned successful responses and browser tests worked |

Coverage now includes landing-to-workspace/back navigation, project search/filter/sort, grid/list selection, no-results reset, actual saved source/brief/draft previews, complete source text, Escape dismissal, preview visibility, wider editor mode, and cancelled unsaved-draft navigation. Original research/editing/export flows also passed. The existing running local API/frontend were reused; backend code, database schema, and dependency lists were unchanged. Backend tests were not rerun for this UI-only follow-up. Test-created projects remain in the selected local database.

The original baseline record below is retained as historical evidence. Gemini, cloud database/deployment, and remote CI verification limits remain unchanged.

## Recorded environment

| Item | Recorded version/configuration |
| --- | --- |
| Host | Windows |
| Python | 3.10.0 |
| Node.js | 24.19.0 |
| Backend dependencies | [requirements.lock](../backend/requirements.lock); supported top-level ranges in [requirements.txt](../backend/requirements.txt) |
| Frontend dependencies | [package-lock.json](../frontend/package-lock.json) |
| Browser | Chromium 156; desktop 1440 × 1000 and mobile viewport 390 × 844 |
| Local database | SQLite |

## Results and gaps

| Check | Recorded result | Interpretation |
| --- | --- | --- |
| Pytest | 20 passed in 1.18 seconds | API/service checks passed locally |
| Vitest | 2 passed | Fictional sample provenance, length, and check candidates passed |
| TypeScript + Vite | Production build passed; 1,581 modules transformed | Compilation/bundling verified |
| Playwright desktop | 2 passed | Live frontend/API workflow verified |
| Playwright mobile viewport | 2 passed | Responsive browser workflow verified; not physical-device testing |
| SQLite migrations | Upgrade → downgrade → upgrade passed on a fresh database | Migration round trip verified locally |
| API health | HTTP 200; SQL query succeeded | Local backend/database connected |
| Real-source seed | Project, 3 sources, brief, saved draft created | Seeder exercised successfully |
| Visual QA | Overview screenshots inspected on desktop/mobile; writing/compare screenshots collected | No overview layout overflow observed |
| Docker/live PostgreSQL locally | Not run; Docker Desktop engine unavailable | Container and live PostgreSQL runtime remain unverified |
| Remote CI | Workflow configuration committed | No successful remote run claimed |
| Visible preview handoff | Codex browser panel failed to open | Loopback services and automated browser tests worked independently |
| Gemini / Vercel | Not implemented/deployed | No live provider or cloud workflow validation |

## What the tests cover

| Suite | Files | Main checks |
| --- | --- | --- |
| Backend API/services | [test_workflow.py](../backend/tests/test_workflow.py), [conftest.py](../backend/tests/conftest.py) | Persistence, 3-source gate, evidence URLs, unverified claims, duplicates/deletion, original/history, accept/reject, stale versions, overlaps/offsets, passive manual review, metrics, speculation/topics, export |
| Import boundaries | Same backend suite | Redirect rejection, unsupported content, 2 MB limit, short content, valid HTML, private/link-local/loopback/IPv6 addresses |
| Frontend unit | [sample.test.ts](../frontend/src/sample.test.ts) | 3 distinct explicitly fictional inputs and a 300–500-word draft containing writing-check candidates |
| Browser workflow | [workflow.spec.ts](../frontend/e2e/workflow.spec.ts) | Source collection, brief, draft checks, decisions, comparison, reload persistence, Markdown download, mobile horizontal overflow |

API fixtures use isolated in-memory SQLite. Browser tests use the running API and its selected database; their created projects persist there. Import tests mock DNS/HTTP responses rather than depending on live publisher pages. Frontend unit tests do not establish broad React component coverage.

## Reproduce locally

Install dependencies using the [root setup instructions](../README.md#quick-start). From the repository root:

~~~powershell
cd backend
..\.venv\Scripts\python.exe -m pytest -q
cd ..\frontend
npm test
npm run build
npx playwright install chromium
~~~

Start the backend in a separate terminal, from backend/:

~~~powershell
..\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000
~~~

Then run npm run test:e2e from frontend/. Playwright starts or reuses the frontend outside CI. Use ../.venv/bin/python on macOS/Linux. To keep test projects separate, set DATABASE_URL to a disposable database before starting the API.

### SQLite migration check

Use a **new, disposable database path**, from backend/:

~~~powershell
$env:DATABASE_URL = 'sqlite:///./migration-check.db'
..\.venv\Scripts\python.exe -m alembic upgrade head
..\.venv\Scripts\python.exe -m alembic downgrade base
..\.venv\Scripts\python.exe -m alembic upgrade head
Remove-Item Env:DATABASE_URL
~~~

The downgrade removes that database's application tables. Never run this round trip against valuable data. Do not apply the initial migration to an already auto-created local schema without first reconciling its migration state.

## CI configuration and evidence

The [workflow](../.github/workflows/ci.yml) declares Python 3.12/Node 22, a PostgreSQL service, backend tests, PostgreSQL migration/schema checks, frontend tests/build, and browser tests against the PostgreSQL-backed API. This differs from the recorded local Python/Node/SQLite environment and still needs a confirmed remote run.

Screenshots are generated under ignored frontend/test-results. Traces are retained on browser test failure. CI uploads that directory on failure. Generated local evidence is not a tracked, permanent artifact in the repository.

## Failures resolved during implementation

| Failure | Resolution |
| --- | --- |
| Extraction dependency could not import its cleaner | Added lxml_html_clean |
| Newer Pytest failed during Windows startup | Constrained runner to 8.x |
| Browser tab selectors were too exact | Used accessible-name matching |
| Filler rule matched a partial word | Added end-boundary handling |
| Large test parameter exceeded Windows environment limits | Added concise parameter IDs |

One upstream Starlette TestClient/HTTPX deprecation warning remained; tests passed and the warning was not suppressed.

## Documentation refresh validation

The documentation-only refresh on October 29, 2026 checked all 10 Markdown files for local link targets, heading anchors, balanced code fences, and replacement characters. Six PowerShell example blocks parsed successfully without execution. The newsletter article body remained unchanged, and comparison against the pre-refresh GitHub tree confirmed that only Markdown files were modified. No application tests were rerun for these prose changes.

## Outstanding verification

Live PostgreSQL, container builds, remote CI, HTTPS/public deployment, physical phones, simultaneous-editor concurrency, and Gemini generation remain unverified. Model output needs a separate evaluation of evidence, meaning preservation, invalid citations, quota failures, and stale responses after integration; passing existing deterministic tests will not prove those future capabilities.

## Phases 8–12 verification (October 29, 2026)

- Backend: 55 tests passed (controlled SDK/API responses; no live Gemini key used).
- Frontend: 2 Vitest tests passed with one worker. An earlier unrestricted parallel run exhausted local memory; the test command now bounds workers.
- Production Vite build passed; TypeScript build is checked by the Vercel build command.
- Browser: all 14 desktop/mobile tests passed in an isolated temporary SQLite workspace; final runner exited 0. Earlier teardown file locks were resolved by launching the Windows test API directly through the base Python executable with the virtual environment package path.
- Migration 002 upgrades the isolated database before browser tests. Existing local workspace data is not used.
- Coverage includes authentication/errors, evidence references, invalid JSON, quotas/replay, stale generation, original preservation, reviewed newsletter application, and existing source/edit/export flows.

Run isolated browser verification from the repository root:

~~~powershell
.\.venv\Scripts\python.exe scripts/verify_stack.py
~~~

Live Gemini responses, managed PostgreSQL migration, production session/proxy behavior and persistence after redeployment remain unverified. A protected frontend preview is only a build check, not the complete deployed workflow.

The protected Vercel frontend build reached READY. Its initial audit flagged legacy Vitest/mock worker dependencies; Vitest was updated to 5.0.5 with compatible Vite 6.4.5, and the subsequent npm install audit reported zero vulnerabilities. Test runner remains limited to one worker. This tooling update does not change the application interface.

Both updated protected Vercel builds reached READY, and the frontend HTML returned HTTP 200. API invocation reached the configured startup guard and failed because PostgreSQL/access prerequisites were absent from that deployment. Generated access credentials and the owner-provided Gemini key have since been placed in the backend environment; PostgreSQL is still missing. The live Gemini SDK smoke check returned provider_timeout; an independent Google endpoint request also timed out. Neither check establishes provider success.

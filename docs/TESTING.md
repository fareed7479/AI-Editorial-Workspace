# Testing and validation record

**Purpose:** distinguish observed results from configured checks and make the local verification workflow reproducible.

[Documentation guide](README.md) · [Phase matrix](PHASES.md) · [Architecture](ARCHITECTURE.md) · [Future acceptance criteria](ROADMAP.md)

> **Evidence date:** October 29, 2026. Results below come from the original implementation session. This documentation refresh does not represent a new application test run or prove a successful remote CI/deployment run.

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

# Validation record

Verified October 29, 2026 on Windows, Python 3.10.0 and Node 24.19.0. Tested dependency snapshots are in backend/requirements.lock and frontend/package-lock.json.

| Check | Actual result |
| --- | --- |
| Backend Pytest | 20 passed in 1.18 seconds |
| Frontend Vitest | 2 passed |
| TypeScript + Vite production build | Passed; 1,581 modules transformed |
| Playwright Chromium 156 desktop 1440 × 1000 | 2 passed |
| Playwright Chromium 156 mobile viewport 390 × 844 | 2 passed |
| SQLite Alembic upgrade → downgrade → upgrade | Passed, fresh migration-check database |
| Live API health | HTTP 200, SQL connectivity, deterministic mode |
| Real-source sample seed | Created project, three source records, brief and saved draft |
| Desktop/mobile visual screenshots | Inspected overview layouts; no overflow; writing/compare screenshots also collected by tests |
| Docker Compose / live PostgreSQL locally | Not run: Docker Desktop engine unavailable |
| Remote GitHub CI | Configuration committed; no successful CI run claimed |
| Visible in-app preview handoff | Failed in Codex browser panel; loopback services and automated browser tests worked |

## Coverage

API tests exercise project persistence, the three-source gate, source attribution, unverified claims, source deletion and duplicates, original preservation, acceptance and rejection, sequential version conflicts, stale/overlapping suggestion invalidation, offset shifts, human-required passive rewrites and export. Pure-service checks cover three writing rules, empty metrics, speculation tagging and topic-specific analysis prompts.

Import tests use controlled HTTP responses for success, redirects, non-text types, oversized bodies and insufficient text. DNS is mocked for loopback, private, link-local and IPv6 loopback addresses. No live publisher request is necessary for these tests.

Browser tests use the real React UI and FastAPI/SQLite service: create a project, add pasted sources, build a sample brief, save/check a draft, accept/reject, compare versions, reload persistence, download Markdown and check mobile horizontal overflow. Screenshots are saved inside ignored frontend/test-results and retained in CI artifacts when a test fails. These are mobile viewport tests, not a physical-phone install.

## Resolved failures

- Added lxml_html_clean after source extraction could not import its transitive cleaner.
- Constrained Pytest to 8.x after the newer runner failed during Windows startup.
- Corrected accessible-name tab selectors in browser tests.
- Prevented the filler rule from matching partial words such as in order toad.
- Named large-response test parameters to avoid Windows environment variable limits in Pytest.

One upstream Starlette TestClient deprecation warning remains for its HTTPX transport. The tests pass. No warning suppression is installed.

## Limits

Live PostgreSQL, Docker image builds, HTTPS/public deployment, real mobile hardware and multi-user concurrency are unverified. CI provisions PostgreSQL, migrates up/down/up and runs the browser flows against it. Network import remains subject to publisher restrictions and the DNS-rebinding limitation disclosed in AI_DISCLOSURE.md. The word/sentence heuristics are English-oriented and are not semantic quality measures.

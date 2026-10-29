# Validation record
**Observed evidence, reproducible checks and explicit limits**

[Docs](README.md) · [Requirement coverage](REQUIREMENTS.md) · [Release](DEPLOYMENT.md)

> [!NOTE]
> “Implemented”, “build passed” and “verified end to end” are different claims. This record does not treat controlled model responses as successful live Gemini output.

## Current verification snapshot

| Area | Recorded result | Scope |
| --- | --- | --- |
| Backend | 54 passed; one Starlette/httpx deprecation warning | Vercel build, Python 3.12 |
| Frontend unit tests | 2 passed | Vitest 5.0.5, one worker |
| Frontend compilation/bundle | Passed | TypeScript + Vite |
| Neon migration | alembic upgrade head passed | Managed PostgreSQL |
| Cloud core workflow | RELEASE_CORE_OK / RELEASE_ROLLBACK_OK | Real Neon + FastAPI TestClient, non-AI |
| Production/preview landing | HTTP 200 | Public access after protection removal |
| Frontend API proxy | Health and project reads HTTP 200 | Production frontend → API → Neon |
| Actual editorial replay | 344 → 342 body words; 2 accepted edits | Same deterministic functions used by API |
| Live Gemini | Not verified | Earlier SDK/independent requests timed out |
| Complete deployed browser run | Not verified | Local Windows startup blocker; no fresh full pass claimed |

Verified cloud builds: API dpl_4z7GJxap9TmSDAESyj7SsPsEYAow from ae68ae9; frontend dpl_DZfWsDN9YNfKzdgMJubWGa86L7YE from ade4cc7. Later source changes in this documentation refresh do not change the application runtime.

## What the tests cover

| Layer | Relevant checks |
| --- | --- |
| Research/ingestion | Three-source gate, duplicate/invalid source handling, controlled import errors, attribution |
| Writing | Long/filler/passive checks, metrics, exact offsets, accept/reject, overlapping/stale proposals |
| Persistence/API | Draft versions, original/revisions, saved export, source invalidation |
| Gemini (controlled) | Structured parsing, invalid evidence, known source IDs, repeated passages, numeric preservation, stale results |
| Generation lifecycle | Request cap, cached replay, history/status, reviewed newsletter application |
| Access | Direct workspace without login, rejected untrusted write origins, PostgreSQL required in cloud |

The cloud core check creates only diagnostic material inside a rollback transaction. A subsequent deployed project read returned an empty list. It does not mutate the owner's existing content or permanently consume the application's AI quota.

## Editorial example replay

~~~powershell
.\.venv\Scripts\python.exe scripts/build_sample_comparison.py
~~~

Observed output: 344 original words, 342 revised words, two accepted edits, original preserved, numbers/citations preserved. The script regenerates [BEFORE_AFTER.md](BEFORE_AFTER.md) from the [final sample](SAMPLE_NEWSLETTER.md), using the application's analyze/decide/metrics functions. No network, model or database call is made.

The editor selected two filler removals. Long sentences remain for review; the example demonstrates a bounded decision sequence, not broad writing-quality improvement.

## Run the checks

~~~powershell
# Backend, from backend/
..\.venv\Scripts\python.exe -m pytest -q

# Frontend, from repository root
npm test --prefix frontend
npm run build --prefix frontend

# Disposable local DB and separate API/web ports
.\.venv\Scripts\python.exe scripts/verify_stack.py

# Non-AI check against configured, migrated DB; from backend/
..\.venv\Scripts\python.exe verify_release.py
~~~

The isolated browser runner never uses the owner's workspace database. It retains API/web startup logs for diagnosis.

## Browser history and current blocker

A historical pre-login-removal run passed all 14 desktop/mobile tests. A later login-removal run passed direct-entry/Gemini-review/navigation checks but encountered library/editing timeouts before the environment disconnected.

The latest rerun did not reach the tests: a stack trace showed Python 3.10 blocked in socket.socketpair during Windows asyncio Proactor initialization, before API startup. This is not reported as a newly passing browser suite. The project also declares browser and PostgreSQL migration checks in CI; remote CI success has not been established.

## Remaining release acceptance

- One separately approved real Gemini brief/writing/newsletter run; inspect source support and meaning.
- A complete deployed browser workflow with reload, reviewed edits and export.
- Genuine staging isolation before treating public previews as a safe test environment.
- Publisher/import and semantic quality evaluation beyond controlled fixtures.

No recurring deployment check makes billable model requests. Container runtime, backup/restore, multi-user isolation and broad accessibility audits are not verified.

## Documentation QA

The original five-page assignment PDF was read in full for this refresh. Fourteen Markdown documents were checked: 87 relative links resolved, and all tilde code fences were balanced. The editorial reproduction script was rerun successfully after the sample metadata update. Public production/preview HTML and frontend API project reads returned HTTP 200 after Vercel protection was removed at the owner's explicit request.

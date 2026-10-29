# Deployment and operations
**Vercel frontend + FastAPI API · Neon PostgreSQL**

[Live site](https://fieldnotes-editorial-workspace.vercel.app/) · [Docs](README.md) · [Validation](TESTING.md)

## Current release

| Service | Root / runtime | Production URL |
| --- | --- | --- |
| Frontend | frontend · Vite / Node 24 build | https://fieldnotes-editorial-workspace.vercel.app |
| API | backend · FastAPI / Python 3.12 · Mumbai function region | https://fieldnotes-editorial-api.vercel.app |
| Database | Managed Neon PostgreSQL | Backend-only pooled/direct connection variables |

Vercel scope: fareeds-projects-1f497a11. Both production builds reached READY. API health/project listing and the frontend API proxy return HTTP 200.

> [!IMPORTANT]
> The owner explicitly requested public production **and preview** URLs. Vercel Authentication is disabled for both projects; application login is also removed. This is a shared demonstration, not a private multi-user deployment.

Current frontend rewrites target the production API, including from frontend previews. **Do not treat previews as isolated staging.** Older preview URLs retain their historical source versions. Preview write requests can also be rejected when their origin is not in CORS_ORIGINS; public visibility is not a claim that every historical preview is a fully compatible current workspace. Separate preview databases alone would not isolate a frontend that still proxies production.

## Build and release checks

| Project | Build command |
| --- | --- |
| API | python -m alembic upgrade head && python verify_release.py && python -m pytest -q |
| Frontend | npm test && npm run build |

The API check exercises the core workflow against Neon inside an external transaction with savepoints, then rolls back diagnostics. It does not make model calls. Backend checks report 54 passed; frontend checks report 2 passed plus TypeScript/Vite success.

Migrations are additive and run before serving a new API build. Do not downgrade a live database for a test. Verify a backup/restore process before operating this as a long-lived service.

## Environment setup

| Variable | Placement |
| --- | --- |
| DATABASE_URL / POSTGRES_URL | API project; DATABASE_URL takes precedence |
| DATABASE_URL_UNPOOLED | Direct connection available for migration/operations if needed |
| GEMINI_API_KEY / GEMINI_MODEL | API project only |
| AI_* limits | API project; default daily request cap 20 |
| CORS_ORIGINS | Exact allowed frontend origins for writes |
| VITE_API_URL | Unset for production same-origin proxy |

Never commit keys or put database/provider credentials in VITE_ variables. Environment changes require a new deployment. Legacy WORKSPACE_PASSWORD/SESSION_SECRET values are unused.

## Connect or replace Neon

1. In the API project, open Storage and select/create the Neon resource.
2. Choose a suitable region/plan; optional managed Auth is not used by this app.
3. Storage → database → Connect Project → fieldnotes-editorial-api.
4. Use the default variable prefix; confirm DATABASE_URL or POSTGRES_URL in API Settings → Environment Variables.
5. Remove a stale SQLite DATABASE_URL if it would override the intended PostgreSQL fallback.
6. For genuine staging, configure both a separate database branch **and** a frontend proxy targeting its matching API deployment.
7. Migrate, deploy, check health and verify content persistence. Do not upload the local SQLite file automatically.

Local settings load backend/.env → root .env → root .env.local → process variables. Restart the backend after changing database selection.

## Smoke checks and acceptance

| Check | Observed state |
| --- | --- |
| Public production landing | HTTP 200 |
| Public preview landing | HTTP 200 |
| Frontend /api/health proxy | HTTP 200; SQL health ok |
| Frontend /api/projects | HTTP 200 |
| Core Neon mutation workflow | Passed; diagnostic data rolled back |
| Latest API runtime error scan | No errors returned for the checked deployment |
| Real Gemini generation | Pending approved one-time verification |
| Full deployed browser workflow | Pending; local Windows runner blocked before startup |

backend/verify_release.py --live-ai is a separate manual opt-in that can make up to three billable generations. It is not in recurring builds. Public-link approval does not imply approval to run that check.

## Known operating limits

No per-user ownership, restore UI, automated backups, error-tracking integration, currency budget or independent fact-checking is provided. Provider billing/retention and database recovery policies remain owner responsibilities. The app is an assignment/demo scope, not a claim of production readiness.

[Outstanding work](ROADMAP.md) · [AI/data boundaries](AI_DISCLOSURE.md)

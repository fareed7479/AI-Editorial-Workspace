# Vercel deployment

## Topology

Two projects use the same GitHub repository. The Vite site proxies /api to FastAPI so session cookies stay on the browser's site. Secrets remain in the API project. PostgreSQL is durable storage; Vercel's filesystem is not the database.

| Project | Root | Runtime | State |
| --- | --- | --- | --- |
| fieldnotes-editorial-workspace | frontend | Vite, Node 24 build | Linked; protected frontend build READY |
| fieldnotes-editorial-api | backend | FastAPI, Python 3.12, Mumbai region | Linked; database/environment setup pending |

Vercel scope: fareeds-projects-1f497a11. Both projects initially use Vercel Authentication for all deployments. A protected preview is not a public release.

## Required configuration

Create managed PostgreSQL (the connected Neon integration is available), then attach it to the API project. Use a separate preview database/branch. Put DATABASE_URL or POSTGRES_URL, GEMINI_API_KEY, GEMINI_MODEL, WORKSPACE_PASSWORD (12+ characters), SESSION_SECRET (32+ characters), and CORS_ORIGINS in the backend environment. Do not prefix credentials with VITE_. Only public API-origin configuration may reach React.

For local setup, use the ignored root .env. Settings load backend/.env, root .env, root .env.local, then process variables; the last value wins. Database selection happens at startup, so restart after changing DATABASE_URL. The generated local workspace password is in that file; it is not the Gemini key. Keep all values private.

Default AI cap: 20 requests per UTC day for this single workspace. Failed provider attempts count; cached replay does not. This cap is not a money budget; configure provider billing limits separately if needed.

## Database migration

Run from backend with the intended DATABASE_URL configured:

~~~powershell
..\.venv\Scripts\python.exe -m alembic upgrade head
~~~

Migration 002 only adds generation_jobs and request_quotas, leaving existing projects, sources and drafts intact. Run migrations once before serving a release; they do not run on every function invocation. Never downgrade a live database for a smoke test. The local SQLite database is not automatically uploaded or replaced.

## Routing and protection

frontend/vercel.json proxies /api to the API production domain. The API project domain list confirms fieldnotes-editorial-api.vercel.app as its assigned alias; it will serve the API only after a production deployment. Do not set VITE_API_URL to localhost in production. The same-origin proxy is required for reliable HttpOnly sessions.

Once PostgreSQL migration and application login are verified, the API production URL needs to accept the frontend proxy (Vercel Authentication on every API deployment otherwise blocks it). Keep preview deployments protected; use the application's password/session gate for production. Only change platform protection after the application gate works. Configure CORS_ORIGINS to the exact frontend production origin. Production and preview must not share writable data.

## Release checks

1. Add backend secrets through the connected Vercel project; redeploy after changing them.
2. Migrate managed PostgreSQL and verify expected tables.
3. Deploy API; check /api/health and authenticated project access.
4. Confirm production alias and frontend rewrite; deploy frontend.
5. Sign in through the frontend, create disposable sources, generate a real Gemini brief, review a newsletter, apply it, accept/reject writing suggestions, reload and export.
6. Recheck persistence after redeployment and verify unauthenticated writes are blocked.

Current credential-dependent gates: real Gemini request, managed PostgreSQL migration, API production health and deployed editorial workflow. Do not describe the project as end-to-end deployed until these pass.

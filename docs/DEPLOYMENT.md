# Vercel and Neon setup

## Application flow

Landing → Open workspace → project library → editorial workspace. Application login/logout, session endpoints and password requirements were removed at the owner's request. Legacy WORKSPACE_PASSWORD and SESSION_SECRET variables are ignored and can be removed. Existing data and Gemini request limits are preserved.

Anyone who reaches an unprotected deployment can read/edit the shared workspace and use its AI quota. Vercel platform protection is separate and remains unchanged; its own authentication screen may still appear.

## Create or connect Neon

1. Open https://vercel.com/fareeds-projects-1f497a11 and select fieldnotes-editorial-api.
2. Open Storage → Create Database (or Browse Marketplace) → Neon. If you already have a Neon database, open that resource and choose Connect Project instead of creating another.
3. Use the installed Neon integration. Name it fieldnotes-editorial, choose a nearby region (Mumbai if offered), and review/select the Free plan if suitable. Leave optional Auth disabled: this app does not use it.
4. In Storage → your database → Connect Project, select fieldnotes-editorial-api, not the frontend project.
5. Select Production. For Preview, enable isolated preview branching rather than sharing writable production data. Leave Production unchecked under Create database branch for deployment.
6. Leave Custom Prefix empty/default, then click Connect.
7. In API project → Settings → Environment Variables, confirm DATABASE_URL or POSTGRES_URL is present for Production. DATABASE_URL takes precedence; remove a stale SQLite value if POSTGRES_URL is the intended cloud connection.
8. Tell the implementation agent the database is connected so migrations and deployment can be verified. Do not paste credentials in chat.

The integration injects connection variables automatically. For an external Neon account, use its Connect dialog to copy the PostgreSQL URL into a sensitive DATABASE_URL variable on the API project. Preserve sslmode=require. Never expose credentials through VITE_ variables.

## Local use and migration

For local PostgreSQL, put the intended DATABASE_URL in the ignored root .env. Configuration loads backend/.env, root .env, root .env.local, then process variables (last wins). Restart after changing the database. Existing SQLite data is not automatically copied or deleted.

Run from backend against the intended database before serving traffic:

~~~powershell
..\.venv\Scripts\python.exe -m alembic upgrade head
~~~

Use a direct/unpooled URL for migration if required by the provider. Do not downgrade a live database for testing. Existing migrations add tables without clearing content.

## Deployment

| Project | Root | Runtime | Production domain |
| --- | --- | --- | --- |
| fieldnotes-editorial-api | backend | Python 3.12 / FastAPI | fieldnotes-editorial-api.vercel.app |
| fieldnotes-editorial-workspace | frontend | Vite / Node 24 build | fieldnotes-editorial-workspace.vercel.app |

The frontend proxies /api to the API production alias. Keep VITE_API_URL unset in production and configure API CORS_ORIGINS to the exact frontend origin. Existing Vercel protection must allow the proxy before public release; application login removal does not change platform protection. Environment changes need a new deployment.

After connecting Neon, verify migrations, API health, frontend routing, real Gemini output, source → brief → reviewed newsletter → editing → reload → export, and persistence after redeployment. Earlier protected builds reached READY, but API invocation failed its missing PostgreSQL startup requirement. Live Gemini requests previously timed out. Full production acceptance remains pending.

Official guide: https://neon.com/docs/guides/vercel-managed-integration.

Latest frontend verification: production build dpl_DZfWsDN9YNfKzdgMJubWGa86L7YE reached READY from ade4cc7, with 2 Vitest tests and TypeScript/Vite build passing. Public access is still intentionally blocked pending explicit owner approval after automatic review. Approval is also required for the one-time live Gemini generations; recurring deployment checks remain non-AI.

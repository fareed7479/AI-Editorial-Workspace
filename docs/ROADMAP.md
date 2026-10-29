# Remaining delivery and acceptance

The local phases 1–7 remain intact. Gemini extends the existing FastAPI/React app; it does not replace its deterministic tools or original/revision history.

| Phase | Delivered | Verification / remaining gate |
| --- | --- | --- |
| 8 — Gemini foundation | Official Python SDK, structured schemas, configurable limits, sanitized failures | Controlled tests pass; live key required |
| 9 — AI research | Per-source claims, exact excerpt checks, synthesis, uncertainty, contradictions | Controlled evidence checks pass; live editorial evaluation pending |
| 10 — AI writing | Exact-passage suggestions, numerical safeguards, cited 300–500-word newsletters | Controlled tests pass; live model evaluation pending |
| 11 — Streaming and usage | Progress stream, persisted jobs, request IDs, daily cap, explicit newsletter apply, direct workspace access | Local API/UI checks; see TESTING.md |
| 12 — Cloud readiness | PostgreSQL migration, Vercel entrypoint and linked API/web projects | Managed database credentials and cloud migration required |
| 13 — Deployment | Vercel projects connected to this repository | Both protected preview builds READY; production promotion waits for PostgreSQL and health checks |
| 14 — Final verification | Isolated browser and API coverage prepared | Live sources → Gemini brief → draft → editing → export still required |

## Owner input needed

The supplied Gemini key is now in the ignored root .env and Vercel backend secret store; live verification timed out. Connect the Neon database to fieldnotes-editorial-api or put its PostgreSQL DATABASE_URL in that same file. Keep passwords/keys out of chat and Git. WORKSPACE_PASSWORD and SESSION_SECRET are backend-only; local generated values must remain private.

## Completion criteria

A phase is not cloud-complete just because its source is committed. Final sign-off requires a real model request, a successful PostgreSQL migration, protected production URLs, persistence across reload/deployment, and the deployed editorial workflow. Preview and production databases must be separate. No automatic transfer or deletion of the existing local SQLite workspace is performed.

[Integration](AI_INTEGRATION.md) · [Deployment](DEPLOYMENT.md) · [Validation](TESTING.md)

> **Access update:** application login/logout and password/session requirements have been removed at the owner’s request. Landing opens the workspace directly. Database requirements and Gemini request limits remain. Platform-level Vercel protection is separate. See [deployment and Neon setup](DEPLOYMENT.md).

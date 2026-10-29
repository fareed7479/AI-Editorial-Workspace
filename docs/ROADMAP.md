# Delivery status and remaining acceptance

Existing landing, library, research, editing, original/revision history and export behavior remain intact. The app uses React/Vite + FastAPI + SQLAlchemy; no additional agent platform or account system was introduced.

| Phase | Implemented / verified | Remaining acceptance |
| --- | --- | --- |
| 8 — Gemini foundation | Official SDK, configuration, structured schemas, bounded limits and sanitized errors | Successful real provider response |
| 9 — AI research | Checked source IDs/excerpts, synthesis, uncertainty and contradictions; controlled tests pass | Live editorial evaluation |
| 10 — AI writing | Exact-passage suggestions and cited newsletter previews; originals preserved | Real model writing/newsletter evaluation |
| 11 — Streaming and usage | Progress, request history, replay, SQL daily quota and stale-result handling | Deployed streamed result verification |
| 12 — Cloud readiness | Neon connected, Alembic applied, cloud core workflow and 54 backend tests pass | Confirm isolated preview branching before writable preview use |
| 13 — Deployment | API and frontend production builds READY | Platform protection blocks frontend proxy; public-release approval required |
| 14 — Final verification | Cloud SQL/API core checks pass and roll back diagnostics; direct deployed API reads pass | Live Gemini and full deployed browser workflow |

Application login was removed at the owner's request. Legacy password/session variables are ignored. Vercel platform protection remains enabled. Public access would allow anyone who reaches the production site/API to read and edit this shared workspace and consume its AI quota.

Automatic approval review rejected recurring billable model calls in deployment builds. Recurring checks use migrations, a non-AI rollback-safe workflow check and Pytest only. A separately approved one-time check can make up to three billable Gemini requests. Automatic review also rejected weakening platform protection without explicit approval.

The local browser rerun is blocked before startup by a Windows asyncio socket-pair hang. Earlier browser results remain historical evidence, not fresh deployed acceptance. Do not mark phases 13–14 fully complete until the remaining gates pass.

[Deployment](DEPLOYMENT.md) · [AI behavior](AI_INTEGRATION.md) · [Validation](TESTING.md)

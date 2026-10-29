# Roadmap | Gemini and Vercel

**Purpose:** turn the requested cloud AI product into bounded implementation phases while preserving the working Python + SQL + React baseline.

[Documentation guide](README.md) · [Completed phases](PHASES.md) · [Current architecture](ARCHITECTURE.md) · [Verification baseline](TESTING.md)

> **Planning status — October 29, 2026:** the user requested Gemini cloud output and deployment on Vercel, then asked for documentation improvements before implementation. Nothing in this roadmap is implemented or deployed by this documentation update.

## Target behavior

An editor supplies sources, requests a grounded Gemini brief, develops or generates an editable newsletter draft, reviews contextual suggestions, compares saved versions, and exports the result. Existing deterministic checks remain available as a clearly labeled mode. The editor retains final control of meaning and publication.

| Capability | Current | Target |
| --- | --- | --- |
| Research | Ranked excerpts and topic templates | Contextual synthesis with valid supporting source IDs/excerpts |
| Writing | Three rule-based checks | Additional Gemini clarity, structure, tone, and nuance suggestions |
| Newsletter | Manually written draft and supplied examples | Editable 300–500-word draft generated from the brief |
| Progress | Request loading state | On-demand generation, then progressive/streamed output |
| Persistence | Local SQLite; PostgreSQL configuration | Verified managed PostgreSQL |
| Hosting | Local launchers; container files | Verified Vercel frontend and Python API |
| Access and usage | Single editor, no login | Protected access and bounded AI usage before public exposure |

## Proposed deployment shape

| Component | Proposed destination | Work required |
| --- | --- | --- |
| React/Vite | Vercel frontend project | Build configuration, API routing, environment settings |
| FastAPI | Vercel backend project from the same repository | Compatible entrypoint, runtime dependencies, timeouts |
| SQL | Managed PostgreSQL | Provision connection, migrations, pooling and persistence verification |
| Generation | Gemini API called by FastAPI | Server-side credential, model configuration, validated responses |

Two Vercel projects are the proposed starting arrangement, not a linked configuration. The local SQLite file is not the production database. Docker Compose is a separate local container path; it is not Vercel Functions configuration.

## Remaining implementation phases

| Phase | Deliverables | Acceptance criteria |
| --- | --- | --- |
| 8. Gemini foundation | Python SDK/client, configuration, Pydantic response schemas, timeouts, bounded retries, explicit provider errors | Controlled success/error tests; one credentialed live request succeeds |
| 9. Research generation | Cross-source synthesis, what/why/who, contradictions, angles, uncertainty, source references | Generated source IDs exist; quoted evidence matches stored input; missing/invalid evidence is rejected or clearly flagged |
| 10. Writing generation | Contextual suggestions and an editable 300–500-word newsletter option | No silent overwrite; passage mapping, accept/reject, originals, and revisions still work |
| 11. Streaming and usage | Progress/stream handling, request limits, usage metadata, stale-result protection | Partial, failed, repeated, and outdated requests behave predictably; unfinished JSON is not saved as a valid result |
| 12. Cloud readiness | Managed PostgreSQL, access protection, Vercel entrypoints/routing, secret configuration | Migrations and cloud build pass; runtime does not depend on writable local data files |
| 13. Deployment | Link repository/services, apply environment configuration, create deployments | Frontend and API respond; secrets remain backend-only; database connection succeeds |
| 14. Cloud verification | Deployed browser workflows, real Gemini evaluation, persistence/error checks, updated docs | Sources → brief → draft → review → comparison → export succeeds after reload/redeployment |

Each implementation phase should include its tests, documentation updates, and a Git commit. Mark completion only after its acceptance criteria are observed. Credential-dependent checks must be recorded separately from mock/control tests.

## Generation contract

- **Evidence:** model responses must name submitted source IDs and preserve supporting excerpts. A valid citation structure is not proof that an interpretation is true.
- **Draft control:** request generation against a known source/draft version; do not apply an outdated response to newer saved text.
- **Suggestion control:** retain affected passage, explanation, editable replacement, and accept/reject decisions. Do not fabricate actors or alter numbers/technical qualifications silently.
- **Failure behavior:** show invalid-key, quota, timeout, malformed-response, and unavailable-model failures clearly. Never disguise deterministic fallback as a Gemini response.
- **Metadata:** store provider/model, generation timestamp, source/draft version, and available usage information without exposing credentials.

## What real-time means here

| Term | Meaning | Scope |
| --- | --- | --- |
| On-demand AI | Generate from the current submitted material when requested | Planned |
| Streaming | Display progress/text as generation arrives | Planned after the basic integration |
| Current-news retrieval | Find new information on external sites with dates/provenance | Separate feature; not automatically supplied by a Gemini key |

Automatic news monitoring, scheduled publication, multi-user collaboration, and native apps remain outside these phases unless separately scoped.

## Access and configuration needed

| Item | Needed for | Handling |
| --- | --- | --- |
| Gemini API credential | Live generation and evaluation | Backend environment only; never React variables or Git |
| Vercel account/project access | Link and deploy services | Use connected tooling; verify available capabilities before deploying |
| Managed PostgreSQL connection | Durable cloud records | Backend secret; migrations before serving traffic |
| Exposure decision | Protected demo versus broader use | Add suitable access controls and usage limits before exposure |

Proposed future variables include GEMINI_API_KEY and GEMINI_MODEL; **the current application does not read them**. Existing variables remain documented in the [root README](../README.md). Model choice and provider quotas must be checked when integration is implemented; no specific model, pricing tier, or budget is promised here.

## Deployment and review checklist

- [ ] Gemini adapter and response validation implemented.
- [ ] Actual generated claims/revisions reviewed on representative sources.
- [ ] Invalid citations and stale results handled safely.
- [ ] Access protection and usage limits implemented.
- [ ] PostgreSQL migrations, pooling, backup plan, and persistence verified.
- [ ] Vercel preview and production environments configured separately.
- [ ] Backend credentials absent from browser bundles and logs.
- [ ] Deployed desktop/mobile workflows and failure states pass.
- [ ] Phase matrix, validation record, and AI disclosure updated with observed results.

## Reference documentation

Official references for implementation planning; they do not establish a successful project deployment:

- [Gemini API keys](https://ai.google.dev/gemini-api/docs/api-key)
- [Gemini structured outputs](https://ai.google.dev/gemini-api/docs/structured-output)
- [FastAPI on Vercel](https://vercel.com/docs/frameworks/backend/fastapi)
- [Vercel Python runtime](https://vercel.com/docs/functions/runtimes/python)
- [SQLite and Vercel storage constraints](https://vercel.com/kb/guide/is-sqlite-supported-in-vercel)

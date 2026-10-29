# Documentation guide

**Purpose:** help a reviewer, developer, or editor find the right explanation without reading every file in sequence.

> **Baseline:** local Python + SQL + React workflow delivered on October 29, 2026. Gemini and Vercel are requested next steps, not current runtime capabilities. This refresh changes documentation only.

## Choose a reading path

| Your goal | Read in this order |
| --- | --- |
| Run and explore the app | [Root README](../README.md), then [Product](PRODUCT.md) |
| Review implementation completeness | [Phases](PHASES.md), then [Testing](TESTING.md) |
| Understand or change code | [Architecture](ARCHITECTURE.md), then [AI disclosure](AI_DISCLOSURE.md) |
| Review editorial output | [Newsletter](SAMPLE_NEWSLETTER.md), then [Before/after](BEFORE_AFTER.md) |
| Prepare Gemini and deployment work | [Roadmap](ROADMAP.md), with [Phases](PHASES.md) as the baseline |

## Document responsibilities

| File | What it explains | What it does not claim |
| --- | --- | --- |
| [README.md](../README.md) | Setup, daily workflow, configuration, repository map | That a local build is a live cloud deployment |
| [PRODUCT.md](PRODUCT.md) | User needs, supported actions, design decisions, scope | That every proposed feature is implemented |
| [ARCHITECTURE.md](ARCHITECTURE.md) | Modules, schema, requests, edit lifecycle, operations | Transactional multi-user support |
| [PHASES.md](PHASES.md) | Phases 1–7, requirement traceability, source history | Completion of future Gemini/Vercel work |
| [TESTING.md](TESTING.md) | Recorded checks, commands, gaps, resolved failures | New test runs or unobserved CI success |
| [AI_DISCLOSURE.md](AI_DISCLOSURE.md) | AI-assisted development, deterministic runtime, data boundaries | Runtime LLM calls or automatic fact verification |
| [SAMPLE_NEWSLETTER.md](SAMPLE_NEWSLETTER.md) | Real-source, dated editorial example | Current-week news or independent model testing |
| [BEFORE_AFTER.md](BEFORE_AFTER.md) | A conservative editing example and decision sequence | An automatic Gemini rewrite or benchmark |
| [ROADMAP.md](ROADMAP.md) | Planned phases 8–14 and acceptance criteria | Credentials provisioned or deployments completed |

## Supporting material

- [sample_sources.json](sample_sources.json): attributed paraphrases used by the real-source sample seeder; not downloaded full articles.
- [seed_sample.py](../scripts/seed_sample.py): creates a sample project through the running API; the full sample Markdown becomes its draft.
- [CI workflow](../.github/workflows/ci.yml): intended automated checks; execution status is separate from configuration.
- [Dependency locks](../backend/requirements.lock): backend snapshot; the frontend snapshot is [package-lock.json](../frontend/package-lock.json).

## How status is expressed

| Label | Meaning |
| --- | --- |
| Implemented | Behavior exists in the current code |
| Verified locally | A specific recorded local check passed |
| Configured / unverified | Files exist, but a successful runtime check is not established |
| Planned | Agreed next work; code and verification are still pending |

When code changes, update its owning document, the phase status, and the validation record together. Keep historical results dated, include verification limits, and commit documentation with the feature it describes.

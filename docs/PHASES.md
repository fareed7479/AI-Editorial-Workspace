# Delivery history
**What changed and what the evidence supports**

[Docs](README.md) · [PDF coverage](REQUIREMENTS.md) · [Validation](TESTING.md)

## Phases 1–7 · Local baseline

| Phase | Deliverable | Qualification |
| --- | --- | --- |
| 1 · Foundation | React/Vite, FastAPI, SQL and environment setup | Stack choice is allowed by the PDF |
| 2 · Research | Persistent sources, extraction, three-source gate, attributed brief | Extractive/heuristic baseline |
| 3 · Writing | Three checks, decisions, metrics, originals/revisions | Rules require editorial judgment |
| 4 · Workspace | Research/writing/compare, export and responsive state feedback | Historical browser evidence recorded separately |
| 5 · Verification | Pytest, Vitest, Playwright and CI configuration | CI configuration is not proof of a remote run |
| 6 · Handoff | Product/engineering notes, newsletter, editing example | Example later upgraded to an actual deterministic replay |
| 7 · Release preparation | Locks, launchers, Docker/Compose and migrations | Container runtime remains unverified |

Initial phase commits are retained in [repository history](https://github.com/fareed7479/AI-Editorial-Workspace/commits/main). The original README bootstrap and phase commits record source delivery, not independent runtime acceptance.

## Interface follow-up

The owner requested a landing page in the same editorial theme and more room to browse saved material. Added: searchable/sortable grid/list project library, previews, full-source dialogs, modal creation and expandable workspace.

## Phases 8–14 · Owner-requested cloud extension

| Phase | Delivered | Acceptance |
| --- | --- | --- |
| 8 · Gemini foundation | SDK, settings, schemas, errors and bounds | Controlled tests pass; real response pending |
| 9 · AI research | Evidence-checked summaries/synthesis/uncertainty | Live editorial evaluation pending |
| 10 · AI writing | Exact-passage proposals and cited newsletter previews | Live model evaluation pending |
| 11 · Progress and usage | Streams, SQL jobs/quota, replay, stale-result checks | Controlled API/UI evidence |
| 12 · Cloud readiness | Neon connected/migrated, Vercel entrypoints/routing | Cloud core checks pass |
| 13 · Deployment | API/frontend production READY; all URLs public | Landing/API proxy reads HTTP 200 |
| 14 · Final verification | 54 backend and 2 frontend tests, cloud core workflow | Full deployed browser and real Gemini still pending |

## Subsequent decisions

| Change | Reason / result |
| --- | --- |
| Remove application login | Owner requested landing → workspace directly; legacy session variables unused |
| Open production and preview links | Explicit owner request; shared data/quota are public |
| Keep build verification non-AI | Avoid recurring billable generations; live check stays opt-in |
| Recheck original assignment PDF | Distinguish actual PDF deliverables from the longer implementation plan |
| Reproduce editorial edits | Same writing engine applies two reviewed filler removals and verifies originals/numbers/citations |

Current documentation separates source implementation from verification limits. No claim is made that all phases are fully accepted or that elapsed work stayed within the original assignment time limit.

[Current acceptance gates](ROADMAP.md)

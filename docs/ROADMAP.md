# Remaining work
**Acceptance gates, not a feature wishlist**

[Docs](README.md) · [Coverage](REQUIREMENTS.md) · [Evidence](TESTING.md)

## Delivered

| Area | Current state |
| --- | --- |
| Research/writing baseline | Implemented; core API workflow verified against Neon |
| Landing/library/editor | Implemented; current full browser acceptance remains pending |
| Gemini integration | Implemented with controlled validation tests |
| Database and deployment | Migrated Neon; production API/frontend READY |
| Public access | Production and preview URLs public at the owner's request |
| Assignment docs/output | PDF-mapped note, 342-word sourced sample and actual writing-engine replay |

## Finish verification

| Priority | Work | Done when |
| --- | --- | --- |
| 1 | Approved one-time real Gemini check | Brief, writing suggestions and newsletter complete with valid evidence and human semantic review |
| 2 | Full deployed browser pass | Sources → brief → save → reviewed decisions → compare → reload → export works |
| 3 | Import evaluation | Allowed/blocked publishers and pasted fallback behave predictably |
| 4 | Quality evaluation | Blinded original/revised review shows clarity gains without factual/technical loss |

Live verification can incur provider charges and is never in recurring builds. Public-access approval did not authorize the separate one-time model run.

## If extending beyond the assignment

Add per-user isolation and stronger abuse controls before storing private content. Isolate preview APIs/databases and their frontend routing; test backups/restore; improve sentence and terminology checks; add error monitoring. Do not add news discovery, collaboration or automated publishing merely to increase feature count.

The original PDF asks for a lightweight 6–8-hour exercise, not production readiness. Additional owner-requested cloud/UI work should not be presented as verified work inside that limit.

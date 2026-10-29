# Submission guide
**Fieldnotes · AI Editorial Workspace**

[Live application](https://fieldnotes-editorial-workspace.vercel.app/) · [Repository](https://github.com/fareed7479/AI-Editorial-Workspace) · [Quick start](../README.md#run-locally)

> [!TIP]
> Review in this order: **live workflow → product decisions → sample and edits → requirement coverage → validation limits**.

## The assignment handoff

| Deliverable | Document | What to look for |
| --- | --- | --- |
| Application and setup | [Root README](../README.md) | Public link, local commands, environment variables |
| Product/engineering note | [PRODUCT.md](PRODUCT.md) | All Part D questions answered concisely |
| Sourced newsletter | [SAMPLE_NEWSLETTER.md](SAMPLE_NEWSLETTER.md) | 342-word body, context, practical implication, attributed links |
| Before and after | [BEFORE_AFTER.md](BEFORE_AFTER.md) | Exact feedback, accepted decisions, actual writing-engine replay |
| Coverage review | [REQUIREMENTS.md](REQUIREMENTS.md) | Original PDF sections mapped to code, artifacts and limits |

## Technical reading paths

| Goal | Read |
| --- | --- |
| Understand the interface | [INTERFACE.md](INTERFACE.md) |
| Change backend, schema or API | [ARCHITECTURE.md](ARCHITECTURE.md) |
| Understand Gemini validation | [AI_INTEGRATION.md](AI_INTEGRATION.md) |
| Review data use and AI disclosure | [AI_DISCLOSURE.md](AI_DISCLOSURE.md) |
| Operate Vercel and Neon | [DEPLOYMENT.md](DEPLOYMENT.md) |
| Assess observed results | [TESTING.md](TESTING.md) |
| Inspect delivery history / outstanding work | [PHASES.md](PHASES.md) · [ROADMAP.md](ROADMAP.md) |

## Evidence labels

| Label | Meaning |
| --- | --- |
| Implemented | Behavior is present in source |
| Verified | A named recorded check passed |
| Pending | Acceptance has not been demonstrated |
| Historical | Earlier evidence; not a fresh test of the current deployment |

The public demo is a shared workspace without login or per-user isolation. Preview links are also public at the owner's request. Live Gemini and full deployed browser acceptance remain pending; deterministic core checks and cloud deployment evidence are recorded separately.

The sample source notes are attributed paraphrases in [sample_sources.json](sample_sources.json). They are not independently verified full-article downloads. Do not confuse the fictional in-app sample with the real-source retrospective.

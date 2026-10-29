# Gemini integration
**Optional cloud assistance with explicit editorial review**

[Docs](README.md) · [Architecture](ARCHITECTURE.md) · [Disclosure](AI_DISCLOSURE.md)

> [!IMPORTANT]
> The integration and controlled tests exist. A successful real Gemini response has **not** been verified. Previous live attempts timed out. Normal deployment builds never make model calls.

## Two visible paths

| Path | What it does |
| --- | --- |
| Deterministic tools | Extract/rank source text; provide analysis prompts; check sentence length/filler/passive candidates; calculate metrics |
| Gemini tools | Propose synthesis, contextual writing suggestions and cited newsletters using submitted context |

A failed Gemini operation is shown as a failure. Rule-based output is not relabeled as Gemini.

## Configuration and bounds

| Setting | Current default |
| --- | --- |
| SDK | Official google-genai Python SDK, pinned in requirements |
| Model | GEMINI_MODEL, default gemini-3.8-flash; configurable |
| Input / output | 80000 characters / 8192 tokens |
| Provider timeout | 60 seconds; bounded total stream handling |
| Transport attempts | At most 2; no UI auto-regeneration |
| Shared request cap | 20 requests per UTC day |

Credentials are backend-only. The model default was checked against provider documentation during implementation; availability for a specific account still needs a live request. Failed provider operations consume the application's reserved request; cached replay does not. The cap is not a currency budget and does not represent provider billing.

## Validation by operation

| Operation | Required checks | Saved behavior |
| --- | --- | --- |
| Research brief | Three sources; exactly one summary per source; known source IDs; exact excerpts; stored provenance | Save only validated brief; interpretation/uncertainty stays labeled |
| Writing review | Saved draft/version; exact passage occurrence; numerical-value preservation | Add individual suggestions; do not rewrite current text |
| Newsletter | Saved brief and three sources; 300–500-word body; numbered citations; exact evidence from at least three sources | Store preview; source list comes from server records |
| Apply newsletter | Explicit action; unchanged input fingerprint/draft version | Create saved revision; preserve original |

Matching an excerpt proves textual correspondence, not factual truth or semantic entailment. Numerical preservation does not guarantee that a rewrite preserves meaning.

## Stream and request lifecycle

The API sends started → progress → complete/error NDJSON events. Progress shows received character counts; partial model JSON is buffered, never treated as a completed draft. Schema and editorial validation precede saving.

A request UUID identifies one project/kind/version snapshot. Completed replay returns the saved result without regenerating or reapplying it. Inputs changed since generation are rejected. Jobs retain status, timestamps, model and token metadata.

Cancellation attempts to close the request and mark it cancelled; check history before retrying. Hard process termination can leave a running record. This is a synchronous request stream, not a durable queue/background worker.

## Failure handling

| Failure | User-facing outcome |
| --- | --- |
| Missing key / input limit / unmet precondition | Clear configuration or validation message; no provider call |
| Provider authentication/model/quota/timeout | Sanitized, labeled failure; no credential/provider-body disclosure |
| Invalid JSON/schema/evidence | Reject result; preserve existing workspace content |
| Project changes during generation | Reject stale result |
| Stream interrupted after saving | History/replay can establish saved state; avoid blind retry |

The system treats source/draft text as untrusted data and instructs Gemini to use supplied material only. It enables no browsing/tool retrieval, disables automatic continuation and requests store=false. That flag is not a guarantee about all provider retention/logging.

## Live verification policy

backend/verify_release.py is non-AI by default. Its --live-ai mode is manual opt-in and can make up to three billable generations; it is not part of recurring builds. A one-time live run still awaits explicit approval. [TESTING.md](TESTING.md) separates controlled evidence from live acceptance.

Official references: [Python SDK](https://googleapis.github.io/python-genai/) · [Structured outputs](https://ai.google.dev/gemini-api/docs/structured-output) · [Models](https://ai.google.dev/gemini-api/docs/models)

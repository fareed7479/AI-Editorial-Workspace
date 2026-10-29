# AI disclosure and reliability

**Purpose:** explain how this repository was developed, what its current runtime actually does, where data goes, and which decisions remain the editor's responsibility.

[Documentation guide](README.md) · [Product](PRODUCT.md) · [Architecture](ARCHITECTURE.md) · [Gemini roadmap](ROADMAP.md)

## Development versus runtime

| Context | Actual behavior |
| --- | --- |
| Development | An AI coding assistant implemented the repository following the Python + SQL + React plan |
| Current research runtime | Python extracts/ranks source sentences and selects topic-based analysis prompts |
| Current writing runtime | Deterministic rules flag long sentences, filler, and passive-voice candidates |
| External model calls | None: no Gemini, OpenAI, Ollama, or other LLM client is integrated |
| Next requested work | Gemini cloud generation and Vercel deployment; still pending |

No model key is required, read, or stored by the current implementation. There is no hidden provider fallback or simulated Gemini response. [TESTING.md](TESTING.md) separates recorded local results from unverified deployment assumptions.

## Interpreting research output

| Label or field | What it means | What it does not establish |
| --- | --- | --- |
| source_claim | An attributed statement selected from supplied/extracted source text | Independently verified fact |
| speculation | Selected words suggest uncertainty or a prediction | Complete contextual classification |
| verified=false | The app has not independently checked the claim | That the source is necessarily false |
| Primary/secondary/unverified | Editor-supplied source classification | Automated credibility scoring |
| Why / audience / angle | Explicit editorial analysis prompts selected by topic | LLM synthesis or proven impact |

Selected excerpts can omit context. Three source records can share one publisher or repeat one announcement. The editor must check dates, provenance, independence, technical qualifications, and conflicting evidence before publication.

## Data flow and trust boundaries

| Data/action | Current destination or behavior |
| --- | --- |
| Pasted sources and drafts | Browser-to-backend requests, then the configured SQL database |
| URL-only import | Server requests the submitted public page and extracts text |
| Draft content | Not sent to any LLM provider |
| Export | Saved draft plus source references downloaded as Markdown |
| Webfonts | CSS can request Google Fonts; system fallback fonts work offline |
| Analytics | No analytics integration installed |

Source content is treated as text, not executed as instructions. React does not inject it as raw HTML. The app does not implement encryption or access control for local database files; protect the host and database appropriately.

## Safeguards already present

- Import validation blocks non-global resolved addresses, credentials in URLs, uncommon ports, redirects, unsupported response types, and oversized bodies.
- Drafts preserve the original and prior saved text; individual suggestions can be edited, accepted, or rejected.
- Overlapping suggestions become stale; sequential stale-version requests are rejected.
- Passive rewrites require human input rather than inventing an actor. Some long sentences also need a reviewed rewrite.

## Remaining limitations

| Limit | Practical consequence |
| --- | --- |
| DNS validation and connection resolution are separate | DNS rebinding is not fully prevented; deploy with restricted network egress |
| No login or project ownership | This is a protected single-editor baseline, not a public multi-tenant service |
| Non-atomic version checks | Simultaneous-editor concurrency is not solved |
| Rule-based writing | False positives, missed grammar, changed emphasis, and imperfect sentence boundaries remain possible |
| No independent verification | Accepted rewrites and cited claims still require editorial review |

There is no automatic mass-accept, publication, semantic fact-checking, or plagiarism detection. Metrics describe text; they are not measures of factual correctness or overall quality.

## Sample provenance

| Sample | Provenance |
| --- | --- |
| In-app demo | Fictional material, explicitly labeled and marked unverified |
| [Newsletter](SAMPLE_NEWSLETTER.md) | August 2025 retrospective using three real pages from one publisher; not independent corroboration or a model evaluation |
| [Before/after](BEFORE_AFTER.md) | Illustrative editorial text and reviewed decisions; not a measured performance benchmark |
| [Seeder inputs](sample_sources.json) | Attributed editorial paraphrases, not verbatim full articles |

## Disclosure required after Gemini integration

Before enabling cloud generation, update this document to identify the provider/model configuration, which source/draft text is transmitted, response retention and usage behavior, failure/fallback labeling, and completed live evaluations. Credentials must remain backend-only. These are future requirements described in [ROADMAP.md](ROADMAP.md), not present capabilities.

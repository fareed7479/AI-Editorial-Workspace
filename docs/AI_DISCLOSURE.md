# AI disclosure and reliability

## Development

This repository was implemented with an AI coding assistant following the user's Python + SQL + React plan. Tests and reported checks are distinguished from unverified deployment assumptions in TESTING.md.

## Runtime

No OpenAI, Gemini, Ollama or other LLM is called. No key is needed or stored. Research uses extractive Python heuristics; writing uses deterministic rules. There is no hidden API fallback or simulated model response. Imported web pages are treated as text, never executable instructions.

A brief preserves source excerpts and URLs. The verification flag remains false even when a source is classified primary. Speculative language is tagged heuristically; a missed label must not be read as proof of fact. Why/why-now/audience/angle text is explicitly editorial analysis, not established evidence. Model-generated synthesis is deliberately absent; evaluate whether extractive assistance meets the intended editorial depth before submission.

## Trust boundaries

Pasted text stays in the configured database. URL import makes a server-side request only to the submitted page and does not send draft content. Webfont requests may contact Google Fonts; fallback system fonts work offline. No analytics are installed.

Private/reserved address resolution, redirects, uncommon ports, credentials, unsupported formats and oversized imports are blocked. DNS validation and connection resolution are separate operations; DNS rebinding remains a limitation. Restrict egress at the network layer before deploying URL import on an exposed network. No authentication or tenant isolation is implemented; use a protected single-editor environment.

## Writing safeguards

The original and prior saved versions persist. No automatic mass-accept is provided. Passive rewrites need the editor to identify the actor rather than fabricating one. Long-sentence splits can change rhythm; review context. Filler removal can change emphasis. Deterministic rules are fallible, and accepted text is not fact-checked. Technical claims, numbers, licenses and source interpretation remain the editor's responsibility.

## Samples

The in-app sample is fictional and explicitly marked unverified. The separate sample newsletter uses three real primary-source pages, clearly dated as an August 2025 retrospective. These pages share one publisher and are not independent corroboration. They demonstrate source attribution, not a claim to have evaluated the model.

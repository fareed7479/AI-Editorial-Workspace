# Gemini integration delivery

This document records phases 8–14 as they are implemented. Existing landing, library, research, editing, comparison and exports remain the baseline.

## Phase 8: foundation

- Official google-genai Python SDK; configuration reads backend/.env, root .env, root .env.local, then process variables (highest priority).
- Credentials are never returned to React or included in configuration representations.
- Structured Pydantic schemas for research, writing suggestions and newsletter output.
- Bounded input/output, provider timeouts, bounded transport retry, sanitized provider failures, no automatic continuation.
- Streaming structured responses are buffered and schema-validated; partial JSON is never persisted as a finished result.
- GEMINI_MODEL is configurable; the initial default is gemini-3.8-flash, checked against official model documentation on October 29, 2026.

Live Gemini validation requires the user's key. A foundation implementation is not a claim that a real provider request or deployment has passed. Later sections will record research/writing persistence, UI, usage controls and actual verification.

Official references: [Python SDK](https://googleapis.github.io/python-genai/), [models](https://ai.google.dev/gemini-api/docs/models), [structured outputs](https://ai.google.dev/gemini-api/docs/structured-output).

## Phase 9: source-grounded research

Research conversion requires one summary per submitted source, exact supporting excerpts and known source IDs. Titles, URLs and reliability labels come from stored records rather than model output. Synthesis, uncertainty and evidence-backed contradictions remain explicitly editorial interpretation. Five controlled research tests passed; real Gemini output still requires live evaluation. Request routing/persistence is connected in phase 11.

## Phase 10: reviewed AI writing

Gemini writing suggestions map exact passages (including repeated occurrences), keep numerical values intact and remain individually editable/acceptable/rejectable. Newsletter output must have a 300–500-word body and valid numbered citations backed by exact excerpts from at least three stored sources. It is a reviewable result, not an automatic draft overwrite. Six writing/newsletter validation tests passed; model evaluation is still credential-dependent.

## Phase 11: streaming, persistence and access

The API streams NDJSON started/progress/complete/error events. Progress reports character counts; raw partial model JSON is not inserted into drafts. A completed response must pass both schema and editorial validation before being saved. Cancelled/failed calls retain a request record. Hard process termination can leave a running record; history makes that state visible and a new request needs a new UUID.

Generation jobs persist model, timestamps, status, input fingerprint and provider token metadata. A repeated completed request ID replays its saved result without another provider call or quota charge. Changed inputs and stale draft versions are rejected. A UTC daily SQL-backed request cap survives process restarts; it is not a spending budget. Failed provider attempts count. SDK transport retry is bounded; the UI does not silently regenerate failed editorial output.

Research saves only after evidence checks. Writing adds individually reviewable suggestions without rewriting the draft. Newsletters remain saved previews until Use this draft; applying preserves the original and prior version. Changes during generation prevent stale results from being applied.

Single-editor access uses an eight-hour signed HttpOnly session, constant-time password comparison, origin checks and a shared SQL login-attempt limit. Hosted startup fails closed without PostgreSQL, a strong session secret and a workspace password. This is one private editor workspace, not multi-tenant accounts or collaboration.

Controlled verification: 55 backend tests passed, including malformed provider output, evidence references, numerical preservation, stale results, quota/replay and authentication. Live provider and deployed verification remain separate gates.

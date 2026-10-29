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

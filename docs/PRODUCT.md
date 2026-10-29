# Product note

Fieldnotes helps a newsletter editor turn a pile of sources into a considered draft. The product is intentionally small: one editor, a project per story, a research desk, a writing studio and a comparison view.

## Research decisions

Sources are explicit records, not disposable prompt text. Require at least three distinct inputs before building a brief, retain original URLs and excerpts, and show editor-supplied reliability. Duplicate URLs and repeated content are rejected. Removing or adding a source invalidates the prior brief so it cannot silently cite outdated inputs.

Extractive summaries keep the evidence visible without API keys. Heuristic speculation labels and topic-specific implications remain starting points for judgment. Three inputs do not guarantee three independent sources; the editor must check provenance, dates, conflicts and qualifications.

## Writing decisions

Rules cover long sentences, filler and passive-voice candidates. Each suggestion shows the passage, rationale and proposed text. The editor can change a rewrite, accept it or reject it. Passive clauses cannot be safely rewritten by inventing an actor; these require an explicit human rewrite. Accepting an overlapping suggestion invalidates affected suggestions. The original is immutable; saved versions remain available for inspection. Version checks catch stale sequential requests.

Metrics show words, sentence count, average sentence length, long sentences and estimated reading time. These describe text, not its truth or overall quality. A 300–500 word target is guidance, not a hard save limit.

## Deliberate omissions

No multi-user collaboration, automated publication, background agents or mandatory LLM integration. No semantic fact-checking, semantic plagiarism detection or generic readability score claimed as a quality verdict. The implemented UI uses custom accessible components and Lucide rather than a shadcn/Router/Tailwind dependency layer; one workspace does not require page routing. This is a documented simplification of the proposed frontend tooling.

## Next improvements

Evaluate extractive briefs on real editorial tasks, add date/source-independence controls, introduce an optional schema-validated model adapter with per-claim evidence, then add authentication and transactional multi-editor concurrency only if deployment needs them.

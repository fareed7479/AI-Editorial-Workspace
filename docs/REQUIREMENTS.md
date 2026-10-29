# Assignment coverage
**Source: FDE Intern Take Home Assignment — This Week in AI · 5 pages**

[Submission guide](README.md) · [Product note](PRODUCT.md) · [Validation](TESTING.md)

> [!NOTE]
> This matrix was checked against the original PDF, not the longer implementation plan. The PDF leaves the model, input method, architecture and interface open; it does not require a particular framework, user accounts or a publishing platform.

## Part A · Research Assistant (PDF pages 1–2)

| Requirement | Implementation / artifact | Status and limit |
| --- | --- | --- |
| At least three articles or URLs | Source form; /projects/{id}/brief gate; [research.py](../backend/app/research.py) | Verified in API checks; three records do not guarantee independent publishers |
| Articles, tweets or URLs | Pasted text plus optional public-URL extraction | Implemented; blocked publishers/social sites use manual text |
| Concise structured summaries | Source-linked extracts; optional Gemini summaries | Extractive path verified; live Gemini pending |
| What happened / why / who | Brief fields and audience-oriented analysis | Implemented; analysis is labeled |
| Evidence and original links | Stored source IDs, URLs and excerpts | Checked provenance; no independent truth verification |
| Facts versus analysis/speculation | source_claim/speculation labels, analysis fields, verified=false | Heuristic baseline; Gemini output also needs editorial review |
| At least one useful angle | Overall/per-source angle fields | Implemented |

## Part B · Writing Assistant (PDF pages 2–3)

| Requirement | Implementation / artifact | Status and limit |
| --- | --- | --- |
| At least three quality checks | Long sentences, filler phrases, passive candidates in [writing.py](../backend/app/writing.py) | Verified; passive detection is heuristic |
| Passage, explanation, rewrite | Suggestion cards and editable replacement | Verified; some rewrites require human input |
| Accept/reject | Version-aware decisions with exact offsets | Verified; overlapping suggestions become stale |
| Preserve original | First saved draft remains original | Verified; manual saves/accepted edits retain prior text |
| Compare original and revision | Compare tab and revision history | Implemented; no automatic restore button |
| Useful metrics with interpretation | Words, sentence averages, reading time | Descriptive, not quality/factuality scores |
| Preserve meaning and technical nuance | Human decisions; optional numerical/evidence guards | Safeguards reduce risk; they do not guarantee semantic equivalence |

## Part C · Editorial output (PDF pages 3–4)

| Requirement | Evidence | Qualification |
| --- | --- | --- |
| Headline, event and reader context | [Final newsletter](SAMPLE_NEWSLETTER.md) | Dated August 2025 retrospective, not current-week news |
| Analysis and practical implication | Labeled analysis and workload-specific evaluation proposal | No benchmark was performed for the article |
| Source links | Three attributed original links | All from the same publisher; not independent corroboration |
| Approximately 300–500 words | 342-word body under the application's word counter | Excludes headline, metadata and references |
| Run draft through Writing Assistant | [Before/after](BEFORE_AFTER.md), [reproduction script](../scripts/build_sample_comparison.py) | Actual deterministic application-service run; not a captured UI session or Gemini generation |
| Show feedback and resulting changes | Two exact filler removals, original/revision text and metrics | Numbers/citations preserved; this small example is not a quality benchmark |

## Part D · Decisions (PDF page 4)

[PRODUCT.md](PRODUCT.md) answers every requested product, engineering and editorial-judgment question, including omissions, usefulness measures, failure handling, evidence limitations and one-more-day improvements.

## Deliverables, disclosure and constraints (PDF pages 4–5)

| Item | Evidence / interpretation |
| --- | --- |
| Deployed URL or reproducible local setup | Public [site](https://fieldnotes-editorial-workspace.vercel.app/) and root setup commands |
| Source and clear README | This repository; secrets excluded |
| Product note | PRODUCT.md |
| Final sample and before/after | SAMPLE_NEWSLETTER.md and BEFORE_AFTER.md |
| Tools / contribution disclosure | AI_DISCLOSURE.md distinguishes assistant implementation from owner configuration |
| Small scope and reasonable assumptions | No discovery, collaboration, fact-checking or automated publishing |
| 6–8-hour assignment limit | Original constraint; actual elapsed time is not independently tracked. Later cloud/UI phases were owner-requested extensions, not claimed as work completed inside that limit |
| Core end-to-end behavior | Cloud non-AI API workflow verified; full deployed browser and real Gemini acceptance still pending |

## Remaining acceptance

A reviewer should not infer that every optional AI feature has passed because the site is public. Live provider success, semantic review of generated output and a fresh complete deployed browser run remain outstanding. See [ROADMAP.md](ROADMAP.md).

The assignment's submission instructions are informational only; no email or submission has been sent.

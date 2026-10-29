# Product note

> **Gemini delivery update:** optional source-grounded research, exact-passage writing suggestions, reviewed newsletter generation, progress/history and private single-editor access now exist. Rule-based tools remain available. Submitted sources/draft context are sent to Google only when you request generation. Model output is checked for structure and exact evidence references, not independently verified for truth. Live Gemini and deployment acceptance remain pending. See [AI integration](AI_INTEGRATION.md) and [deployment](DEPLOYMENT.md).


**Purpose:** explain who Fieldnotes serves, how its workflow behaves, and why the current scope is deliberately small.

[Documentation guide](README.md) · [Architecture](ARCHITECTURE.md) · [Delivery status](PHASES.md) · [Next phases](ROADMAP.md)

## Product in one paragraph

Fieldnotes helps a newsletter editor collect sources, inspect evidence, develop a research brief, and improve a draft without losing the original. It combines a research desk, writing studio, and comparison view. The editor controls every accepted rewrite and remains responsible for factual meaning and publication.

> **Current product:** a single-editor workspace with deterministic tools and optional Gemini research/writing. Cloud production acceptance is pending.

## User journey

| Stage | Editor action | Application response |
| --- | --- | --- |
| Start | Create or reopen a project | Persist the project and its source/draft state |
| Gather | Add article, report, or tweet text; optionally import a URL | Store provenance, content, type, and an editor-selected reliability label |
| Research | Build after collecting three distinct sources | Return attributed extracts, speculation cues, and what/why/who/angle fields |
| Draft | Write or paste text, then save | Preserve the first saved text as the original |
| Review | Run checks and edit/accept/reject suggestions | Apply only reviewed changes; retain prior text and invalidate overlaps |
| Compare | Open comparison/history | Show saved original/current text and descriptive metrics |
| Export | Download Markdown | Include the saved draft and source list |

The sidebar supports project search and selection. Loading, error, empty, and success states explain progress. Unsaved-change prompts guard project/tab changes and page unload; editing is not automatically saved.

## Landing and browsing follow-up

A separate themed landing page now leads into a project library with search, filters, sorting, grid/list views, and real saved-material previews. Native dialogs support project creation and full-source reading. A sidebar toggle expands the editorial space. These are local UI improvements delivered before the remaining cloud phases; see [INTERFACE.md](INTERFACE.md).

## Implemented capabilities and their limits

| Capability | Current behavior | Important qualification |
| --- | --- | --- |
| Source collection | Pasted text or public URL import, up to 20 sources | Duplicate checking is based on canonical URL or identical trimmed content, not semantic similarity |
| Research gate | Requires at least three distinct records | Three records do not establish three independent publishers |
| Evidence | Exact selected excerpts retain source IDs/titles/URLs | Source claims remain unverified |
| Reliability | Primary, secondary, or unverified | The editor chooses the label; the app does not investigate credibility |
| Speculation | Recognizes selected words such as may and might | Heuristics miss context and can misclassify |
| Editorial perspective | Topic-specific analysis prompts | These are templates, not generative cross-source synthesis |
| Writing | Long sentences, filler, passive candidates | Rules are English-oriented and do not understand all grammar or nuance |
| Suggestions | Editable proposal, explanation, accept/reject | Some long/passive rewrites require explicit human input |
| Revisions | Original plus previous saved text, versioned current draft | History is inspectable; no one-click restore workflow is implemented |
| Metrics | Word/sentence counts, average length, long sentences, reading time | Counts describe text; they do not prove truth or quality |
| Responsive UI | Desktop and mobile browser layouts | No installable desktop/mobile app is delivered |

## Design decisions

### Evidence remains visible

Sources are persistent records rather than disposable prompt text. A brief links claims to the records that support them. Adding or removing a source clears the prior brief, preventing a stale source set from looking current.

### The editor owns the rewrite

No mass-accept or automatic publication is provided. Filler removal can change emphasis; sentence splitting can alter relationships; passive rewrites can invent an actor. The UI keeps the proposed text editable and the original accessible.

### Small architecture, clear responsibilities

React manages one tab-based workspace. FastAPI owns validation and mutations. SQL stores projects, sources, drafts, and revisions. Custom components and Lucide replace the proposed Tailwind/shadcn/Router layer; this is a documented tooling simplification, not an unfinished page-routing feature.

### Metrics support judgment

The 300–500-word target guides newsletter length; it is not a save limit. Reading time uses 200 words per minute. A shorter sentence or lower word count is not automatically a better editorial result.

## Samples and delivered evidence

| Material | Intended use |
| --- | --- |
| Fictional in-app sample | Explore the workflow repeatably without relying on a publisher |
| [Real-source newsletter](SAMPLE_NEWSLETTER.md) | Review a dated editorial output with explicit provenance |
| [Before/after example](BEFORE_AFTER.md) | See how reviewed edits preserve qualifications |
| [Validation record](TESTING.md) | Separate implemented behavior from observed test results |

## Remaining scope

**Agreed next:** Gemini-powered synthesis and contextual writing, editable newsletter generation, streaming/progress, usage controls, managed PostgreSQL, protected access, and verified Vercel deployment. See [ROADMAP.md](ROADMAP.md) for acceptance criteria.

**Outside the current delivery:** automatic news discovery, scheduled monitoring, automated newsletter publishing, collaboration, independent semantic fact-checking, and native apps. These require additional product decisions; connecting Gemini does not supply them automatically.

# AI disclosure and editorial reliability
**What was built, what is verified, and who makes the decisions**

[Docs](README.md) · [Product note](PRODUCT.md) · [Evidence](TESTING.md)

## Development contribution

| Contributor/tool | Recorded role |
| --- | --- |
| AI coding assistant | Implemented and revised application code, tests, deployment configuration, docs and reproducible examples |
| Owner | Supplied project direction and credentials, connected Vercel/Neon, requested login removal and public access |
| React/Vite, FastAPI, SQLAlchemy/Alembic | Application framework, API and persistence |
| HTTPX, Trafilatura, BeautifulSoup | Accessible public-page retrieval/extraction |
| Pytest, Vitest, Playwright | Controlled tests and browser checks |
| Google Gemini | Optional runtime generation; successful live response remains unverified |

The repository was substantially assistant-implemented; it is not presented as unaided manual owner work. Recorded checks—not the presence of tests or AI-generated code—support verification claims.

## Runtime data boundaries

| Action | Data destination |
| --- | --- |
| Save source/draft | API and configured SQL database |
| Import URL | Backend fetches the submitted accessible public page |
| Request Gemini | Relevant submitted sources/saved draft/brief are sent to Google |
| Export | Saved Markdown and source references download to the browser |
| Webfonts | CSS may load Google Fonts; fallback fonts are available |

Provider keys/database credentials stay server-side and outside Git. Gemini requests store=false, but provider logging/retention depends on the service and account terms. Jobs store validated results, usage and failure metadata in SQL.

> [!WARNING]
> All production and preview deployment URLs are public at the owner's request. There is no application login or per-user ownership. Do not place private material in this shared demo; visitors can read/edit it and use its quota.

## What labels establish

| Label | Meaning | Not established |
| --- | --- | --- |
| source_claim / excerpt | Attributed source statement | Independent verification |
| speculation | Uncertainty cue or explicit model classification | Perfect contextual interpretation |
| Analysis / angle | Editorial interpretation | Proven impact or factual certainty |
| verified=false | No independent fact-check was performed | That the claim is necessarily false |
| Primary / secondary / unverified | Editor-selected reliability | Automated credibility investigation |

Source IDs and exact quotations are checked; stored links are used rather than invented model URLs. These checks do not prove that a broader generated claim logically follows from an excerpt. Three sources can repeat one publisher's claims.

## Editorial control and limitations

- Originals and saved prior versions are retained; suggestions are individual decisions.
- Long/passive passages may require a reviewed rewrite; technical complexity can be justified.
- Accepted changes can alter emphasis despite improved metrics. Check actors, conditions, numbers, licensing and hardware qualifications.
- Import safeguards reject private/local resolved targets and oversized/unsupported content, but DNS-rebinding protection is incomplete.
- No plagiarism detection, semantic fact-checking, collaboration isolation, auto-publication or mass-accept exists.
- Public preview environments must not be assumed isolated from production merely because both have database variables.

## Example integrity

[The newsletter](SAMPLE_NEWSLETTER.md) is a dated, sourced retrospective, not a real-model benchmark. [The comparison](BEFORE_AFTER.md) is a reproduced run of the actual deterministic writing service, not a browser capture or Gemini output. All three original sources are from one publisher; that limitation remains explicit.

[Verification record](TESTING.md) · [Outstanding work](ROADMAP.md)

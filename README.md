<div align="center">

# Fieldnotes
### AI Editorial Workspace

Evidence-backed research. Clearer drafts. Editorial control.

[Open live application](https://fieldnotes-editorial-workspace.vercel.app/) · [Submission guide](docs/README.md) · [Assignment checklist](docs/REQUIREMENTS.md)

</div>

---

> [!IMPORTANT]
> **Public demo:** production and preview links are accessible without application or Vercel login. This is a shared workspace: visitors can read/edit saved material and use the shared AI quota. Use demonstration content, not private documents.

## Review the submission

| PDF deliverable | Where to review |
| --- | --- |
| Working application | [Live site](https://fieldnotes-editorial-workspace.vercel.app/) or local setup below |
| Source and setup | This repository and [.env.example](.env.example) |
| Product and engineering note | [Decisions and trade-offs](docs/PRODUCT.md) |
| 300–500-word editorial output | [342-word newsletter body](docs/SAMPLE_NEWSLETTER.md) |
| Original, feedback and revision | [Reproduced before/after](docs/BEFORE_AFTER.md) |
| Requirement coverage | [PDF-to-implementation matrix](docs/REQUIREMENTS.md) |

The five-page **FDE Intern Take Home Assignment — This Week in AI** is the source of the checklist. It allows deterministic, LLM or mixed writing checks and a reproducible local setup. Gemini/Vercel extensions were added at the owner's request; live model acceptance is still pending.

## Try the editorial workflow

1. Open the landing page and choose **Open workspace**.
2. Create a project, or choose **Open sample project** for clearly labeled fictional material.
3. Add at least three distinct sources: paste article/report/tweet text, or import an accessible public URL.
4. Build a brief; inspect excerpts, source links, reported claims, analysis and the newsletter angle.
5. Save a draft and choose **Save & check writing**. Edit, accept or reject individual proposals.
6. Compare the preserved original, current text, revisions and descriptive metrics.
7. Export the saved draft and references as Markdown.

Optional Gemini controls add research synthesis, contextual writing review and newsletter previews. A generated newsletter changes the draft only after **Use this draft**.

## Run locally

**Requires:** Python 3.10+ and Node.js 22.12+ (24 recommended).

~~~powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r backend\requirements.lock
npm ci --prefix frontend
.\scripts\dev.ps1
~~~

macOS/Linux: use python3, .venv/bin/python and sh scripts/dev.sh.

| Address | Purpose |
| --- | --- |
| http://127.0.0.1:5173 | Landing and workspace |
| http://127.0.0.1:8000/api/health | API/database health |
| http://127.0.0.1:8000/docs | API schemas |

Local rule-based tools need no provider key. The launcher uses ports 8000/5173; keep its terminal open and stop it with Ctrl+C. If Windows python opens an installation alias, use a working Python executable to create the virtual environment.

## Configuration

Copy [.env.example](.env.example) to the ignored root .env if needed; preserve any existing secret file.

| Variable | Purpose / default |
| --- | --- |
| DATABASE_URL | SQLite locally; PostgreSQL required on Vercel |
| POSTGRES_URL | Database fallback when DATABASE_URL is absent |
| GEMINI_API_KEY | Backend-only key for optional Gemini |
| GEMINI_MODEL | Configurable; current default gemini-3.8-flash |
| AI_DAILY_REQUEST_LIMIT | Shared UTC request cap, default 20; not a currency budget |
| AI_TIMEOUT_SECONDS | Provider timeout, default 60 |
| AI_MAX_INPUT_CHARS / AI_MAX_OUTPUT_TOKENS | Default 80000 / 8192 |
| CORS_ORIGINS | Allowed frontend origins |
| VITE_API_URL | Local API origin; leave unset in production to use the proxy |

Settings precedence: backend/.env → root .env → root .env.local → process variables. Restart after database changes. Keys and database URLs never belong in VITE_ variables or Git. Legacy WORKSPACE_PASSWORD/SESSION_SECRET values are ignored.

## What is verified

| Check | Recorded result |
| --- | --- |
| Migrated Neon + core API workflow | Passed; diagnostic writes rolled back |
| Backend tests in Vercel build | 54 passed |
| Frontend tests / TypeScript / production build | 2 passed / passed / passed |
| Public landing, preview landing and frontend API reads | HTTP 200 |
| Reproduced editorial comparison | 344 → 342 body words; 2 accepted edits; originals/numbers/citations preserved |
| Real Gemini response | **Not yet verified**; previous attempts timed out |
| Complete deployed browser flow | **Not yet verified**; Windows local runner blocked before startup |

See [validation details](docs/TESTING.md). A successful build or citation match does not prove model quality or factual truth.

## Repository map

| Path | Responsibility |
| --- | --- |
| frontend/src | Landing, project library, research/writing/compare UI |
| backend/app | API, SQL models, extraction, deterministic checks, Gemini adapter |
| backend/migrations | Alembic schema history |
| backend/tests / frontend/e2e | Controlled service/API and desktop/mobile checks |
| scripts | Launchers, sample seeding and reproducible editorial example |
| docs | Requirement coverage, decisions, architecture, examples and release evidence |

[Architecture](docs/ARCHITECTURE.md) · [Gemini behavior](docs/AI_INTEGRATION.md) · [Deployment](docs/DEPLOYMENT.md) · [AI disclosure](docs/AI_DISCLOSURE.md) · [Delivery history](docs/PHASES.md)

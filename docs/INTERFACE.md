# Landing page and workspace library

> **Gemini delivery update:** optional source-grounded research, exact-passage writing suggestions, reviewed newsletter generation, progress/history and direct workspace access now exist. Rule-based tools remain available. Submitted sources/draft context are sent to Google only when you request generation. Model output is checked for structure and exact evidence references, not independently verified for truth. Live Gemini and deployment acceptance remain pending. See [AI integration](AI_INTEGRATION.md) and [deployment](DEPLOYMENT.md).


**Purpose:** explain the interface follow-up added before the Gemini/Vercel implementation phases.

[Documentation guide](README.md) · [Product](PRODUCT.md) · [Architecture](ARCHITECTURE.md) · [Validation](TESTING.md)

## Entry points and visual theme

| View | Local URL | Purpose |
| --- | --- | --- |
| Landing | [http://127.0.0.1:5173](http://127.0.0.1:5173) | Introduce Fieldnotes, explain the editorial process, and enter the application |
| Workspace library | [http://127.0.0.1:5173/#/workspace](http://127.0.0.1:5173/#/workspace) | Browse saved projects and preview their material |
| Editorial desk | Open a project from the library/sidebar | Use the existing research, writing, and comparison tabs |

The landing page keeps the existing cream, forest-green, sage, and serif style. Its paper-and-note illustrations are CSS layouts, not screenshots of actual stored content. Product claims describe currently implemented features; the project workspace exposes Gemini controls when the backend is configured.

## Landing page

- **Open workspace** and the main call to action enter the application.
- **Explore a sample** creates and opens the explicitly fictional sample project.
- **The process** and **The workspace** links move to sections on the landing page.
- The Fieldnotes brand in the workspace returns to the landing page.
- Browser back navigation is supported through hash-based view state; no page-router dependency was added.

The landing page itself does not need an API request. Project loading, creation, and sample actions require the backend. Returning to the workspace can retain the selected project while the application remains mounted.

## Project library

| Control | Behavior |
| --- | --- |
| Search | Filter project titles; clear with the search control |
| All projects / 3+ sources / Gathering sources | Filter by stored source count; three sources do not prove independence or verification |
| Sort | Preserve API newest-first order, sort titles A–Z, or sort by source count |
| Grid / list | Switch between roomy cards and compact rows |
| New project | Open a native dialog with a title field and inline error feedback |
| Project title | Open the project in the research desk |
| Preview | Load the selected project's real saved sources, brief, and draft |
| Reset search & filters | Restore the unfiltered library after a no-results search |
| My workspace | Return from an editorial project to the library |

Counts come from stored project records. The library contains saved editorial projects and their material; it does not enumerate files on the user's computer.

## Saved-material preview

The preview panel fetches full project state using the existing project API. It shows source count, draft word count, and three material views:

| View | What appears |
| --- | --- |
| Sources | Stored titles, types, and reliability labels; click a source to read it |
| Brief | The saved angle and source-summary count, or a useful missing-brief state |
| Draft | Version, word count, and the first 900 characters of saved text; open the studio for full editing |

On a narrow screen, the preview stacks below the library and opening it scrolls the panel into view. Empty material is shown honestly; the UI does not fabricate a brief or draft.

## Reading and editing space

**Read full source** opens a native modal dialog containing the complete stored text, original link when present, word count, and reliability label. Escape or the close control dismisses it; native modal behavior keeps keyboard focus inside while open. Stored claims remain unverified.

**Expand workspace** hides the project sidebar to free horizontal space. **Show sidebar** restores it. Research, writing, comparison, and export continue to use the same saved project state.

Unsaved-draft prompts guard leaving the editor for the library or landing page. Comparison/export still use saved text; this change does not add autosave, file uploads, cloud generation, or public hosting.

## Implementation and verification

| File | Responsibility |
| --- | --- |
| [Landing.tsx](../frontend/src/Landing.tsx) | Landing narrative, section links, entry actions |
| [WorkspaceLibrary.tsx](../frontend/src/WorkspaceLibrary.tsx) | Search/filter/sort, views, real project previews |
| [SourceReader.tsx](../frontend/src/SourceReader.tsx) | Full stored-source modal |
| [ProjectDialog.tsx](../frontend/src/ProjectDialog.tsx) | Accessible project creation dialog |
| [experience.css](../frontend/src/experience.css) | Matching theme, responsive layout, workspace space controls |
| [App.tsx](../frontend/src/App.tsx) | View navigation and existing editorial workflow integration |
| [landing-library.spec.ts](../frontend/e2e/landing-library.spec.ts) | Landing/library desktop and mobile workflow checks |

The backend/schema and dependency lists are unchanged. See [TESTING.md](TESTING.md) for dated results. Gemini and Vercel remain in [ROADMAP.md](ROADMAP.md).

> **Access update:** application login/logout and password/session requirements have been removed at the owner’s request. Landing opens the workspace directly. Database requirements and Gemini request limits remain. Platform-level Vercel protection is separate. See [deployment and Neon setup](DEPLOYMENT.md).

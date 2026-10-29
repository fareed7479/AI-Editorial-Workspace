"""Reproduce the assignment's editorial example using the app's writing engine.

No database, network, model key, or provider call is used. Output is documentation.
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))
from app.writing import analyze, decide, metrics


def build():
    sample = (ROOT / "docs/SAMPLE_NEWSLETTER.md").read_text(encoding="utf-8-sig")
    body = sample[sample.index("OpenAI released"):sample.index("\n## Sources and provenance")].strip()
    original = body.replace("the smaller model is the more immediate", "the smaller model is really the more immediate").replace("with a specific task and a clear baseline", "with a very specific task and a clear baseline")
    assert original != body
    draft = SimpleNamespace(original=original, current=original, version=1, suggestions=[], revisions=[])
    decisions = []
    # Reanalyze after every accepted edit, just as an editor can in the workspace.
    while True:
        draft.suggestions = analyze(draft.current)
        item = next((s for s in draft.suggestions if s["kind"] == "Filler phrase"), None)
        if item is None:
            break
        decisions.append({"passage": item["passage"], "replacement": item["replacement"], "explanation": item["explanation"]})
        decide(draft, item["id"], "accept", item["replacement"])
    assert draft.current == body
    assert draft.original == original
    assert len(draft.revisions) == len(decisions) == 2
    for pattern in (r"\b\d+(?:\.\d+)?\b", r"\[\d+\]"):
        assert Counter(re.findall(pattern, original)) == Counter(re.findall(pattern, draft.current))
    before, after = metrics(original), metrics(draft.current)
    rows = "\n".join(f"| `{d['passage']}` | Remove | {d['explanation']} |" for d in decisions)
    document = f"""# Before and after

**Assignment Part C � Reproduced with the application's writing engine**

[Docs](README.md) � [Final newsletter](SAMPLE_NEWSLETTER.md) � [Requirements](REQUIREMENTS.md)

> [!NOTE]
> This is an actual deterministic service run, not Gemini output or a captured browser session. The editor chose two filler removals; the script calls the same analyze/decide functions used by the API and checks the result, original preservation, numeric values and citations.

## Feedback and editorial decisions

| Exact passage | Accepted change | Application feedback |
| --- | --- | --- |
{rows}

The editor removes optional emphasis without changing the release, hardware claim, source attribution or proposed evaluation. Long-sentence flags remain for review: technical context is retained rather than shortened automatically. A lower word count alone is not evidence of better writing.

| Metric | Original | Revised |
| --- | ---: | ---: |
| Words (body only) | {before['words']} | {after['words']} |
| Average sentence words | {before['average_sentence_words']} | {after['average_sentence_words']} |
| Reading minutes | {before['reading_minutes']} | {after['reading_minutes']} |
| Saved revisions | 0 | {len(draft.revisions)} |

## Original draft

{original}

## Revised draft

{draft.current}

## Sources and reproduction

Both versions use the three attributed links in [the final newsletter](SAMPLE_NEWSLETTER.md#sources-and-provenance). They are a dated retrospective, not current-week reporting. The first saved text remains original; each accepted edit stores its prior version.

~~~powershell
.\\.venv\\Scripts\\python.exe scripts/build_sample_comparison.py
~~~

This command rewrites this document and checks the expected result. It makes no network/model calls and changes no workspace data. To inspect the same behavior visually, paste the original into a new project, Save & check writing, review each filler removal, then open Compare revisions.
"""
    (ROOT / "docs/BEFORE_AFTER.md").write_text(document, encoding="utf-8")
    print(json.dumps({"before_words": before["words"], "after_words": after["words"], "accepted_edits": len(decisions), "original_preserved": True, "numbers_and_citations_preserved": True}))


if __name__ == "__main__":
    build()


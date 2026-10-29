"""Conservative, deterministic checks with offsets and explicit review."""
import re
from uuid import uuid4

FILLERS = {"in order to": "to", "due to the fact that": "because", "at this point in time": "now", "it is important to note that ": "", "very ": "", "really ": ""}
WORD_RE = re.compile(r"\b[\w’'-]+\b")
SENTENCE_RE = re.compile(r"[^.!?\n]+(?:[.!?]+|$)")


def metrics(text):
    words = WORD_RE.findall(text)
    lengths = [len(WORD_RE.findall(m.group())) for m in SENTENCE_RE.finditer(text) if WORD_RE.search(m.group())]
    average = round(len(words) / max(len(lengths), 1), 1)
    return {"words": len(words), "sentences": len(lengths), "average_sentence_words": average,
            "long_sentences": sum(n > 25 for n in lengths), "reading_minutes": round(len(words) / 200, 1)}


def suggestion(kind, text, start, end, replacement, explanation, manual=False):
    return {"id": str(uuid4()), "kind": kind, "passage": text[start:end], "start": start, "end": end,
            "replacement": replacement, "explanation": explanation, "requires_edit": manual, "status": "pending"}


def analyze(text):
    findings = []
    for phrase, replacement in FILLERS.items():
        for match in re.finditer(r"\b" + re.escape(phrase), text, flags=re.I):
            rewritten = replacement.capitalize() if match.group()[0].isupper() else replacement
            findings.append(suggestion("Filler phrase", text, match.start(), match.end(), rewritten,
                                       "Shorten this phrase. Check that the emphasis still matches your meaning."))
    for match in SENTENCE_RE.finditer(text):
        passage = match.group()
        if len(WORD_RE.findall(passage)) > 25:
            split = re.search(r";\s+|,\s+(?=and\b|but\b)", passage)
            replacement = passage
            manual = True
            if split:
                right = passage[split.end():]
                replacement = passage[:split.start()] + ". " + right[:1].upper() + right[1:]
                manual = False
            findings.append(suggestion("Long sentence", text, match.start(), match.end(), replacement,
                                       "More than 25 words. Split at a natural clause boundary, keeping qualifications and technical terms.", manual))
        passive = re.search(r"\b(?:is|are|was|were|be|been|being)\s+(?:\w+ly\s+)?(?:\w+ed|built|written|made|given|shown|known|taken|seen)\b", passage, re.I)
        if passive:
            findings.append(suggestion("Passive voice candidate", text, match.start(), match.end(), passage,
                                       "Consider ‘actor + action + object’. Name the actor only if the source identifies it; passive voice can be appropriate. Edit the proposed rewrite before accepting.", True))
    return sorted(findings, key=lambda s: (s["start"], s["kind"]))


def decide(draft, suggestion_id, action, replacement=None):
    item = next((s for s in draft.suggestions if s["id"] == suggestion_id), None)
    if item is None:
        raise ValueError("Suggestion not found. Run the checks again.")
    if item["status"] != "pending":
        raise ValueError("This suggestion was already resolved or became stale.")
    updated = [dict(s) for s in draft.suggestions]
    chosen = next(s for s in updated if s["id"] == suggestion_id)
    if action == "reject":
        chosen["status"] = "rejected"
        draft.suggestions = updated
        return
    rewrite = replacement if replacement is not None else item["replacement"]
    if item["requires_edit"] and (not rewrite.strip() or rewrite == item["passage"]):
        raise ValueError("Provide a reviewed rewrite for this suggestion.")
    start, end = item["start"], item["end"]
    if draft.current[start:end] != item["passage"]:
        raise ValueError("The draft has changed. Run checks again.")
    previous = draft.current
    draft.current = previous[:start] + rewrite + previous[end:]
    delta = len(rewrite) - (end - start)
    chosen["status"] = "accepted"
    chosen["replacement"] = rewrite
    for other in updated:
        if other["id"] == suggestion_id or other["status"] != "pending":
            continue
        if other["start"] < end and other["end"] > start:
            other["status"] = "stale"
        elif other["start"] >= end:
            other["start"] += delta
            other["end"] += delta
    draft.suggestions = updated
    draft.revisions = [*draft.revisions, {"version": draft.version, "text": previous, "reason": item["kind"]}]
    draft.version += 1

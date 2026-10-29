import pytest
from app.ai_editorial import writing_result, newsletter_result
from app.gemini import AIError
from test_ai_research import snapshot


def test_writing_maps_repeated_passage_and_preserves_numbers():
    data = snapshot()
    data["draft_text"] = "We use 16 GB in order to test. We use 16 GB in order to test."
    output = {"suggestions": [{"kind": "Clarity", "passage": "We use 16 GB in order to test.", "replacement": "We use 16 GB to test.", "explanation": "Shorter phrase with the same qualification.", "occurrence": 1}], "summary": "Review wording."}
    result = writing_result(output, data)
    assert result["suggestions"][0]["start"] == data["draft_text"].rfind("We use")
    output["suggestions"][0]["replacement"] = "We use 32 GB to test."
    with pytest.raises(AIError, match="numerical"):
        writing_result(output, data)


def test_writing_rejects_hallucinated_passage():
    output = {"suggestions": [{"kind": "Tone", "passage": "Invented passage.", "replacement": "Changed passage.", "explanation": "Test.", "occurrence": 0}], "summary": "Test."}
    with pytest.raises(AIError, match="does not match"):
        writing_result(output, {"draft_text": "Actual saved text."})


def newsletter():
    return {"title": "A controlled test", "body": ("Careful editorial context matters. " * 80) + " Sources support the discussion [1] [2] [3].", "evidence": [{"source_id": f"s{i}", "excerpt": f"Source {i} reports a controlled local evaluation with 16 GB of memory."} for i in range(1, 4)]}


def test_newsletter_is_reviewable_and_cites_real_sources():
    result = newsletter_result(newsletter(), snapshot())
    assert 300 <= result["body_words"] <= 500
    assert "## Sources" in result["text"]
    assert "https://example.com/3" in result["text"]


@pytest.mark.parametrize("change", ["length", "citation", "evidence"])
def test_newsletter_rejects_invalid_body(change):
    output = newsletter()
    if change == "length": output["body"] = "Short sentence. " * 30 + "[1] [2] [3]"
    if change == "citation": output["body"] += " [99]"
    if change == "evidence": output["evidence"][2]["source_id"] = "invented"
    with pytest.raises(AIError):
        newsletter_result(output, snapshot())

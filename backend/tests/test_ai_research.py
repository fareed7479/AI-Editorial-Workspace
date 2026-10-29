import copy
import pytest
from app.ai_editorial import research_result
from app.gemini import AIError


def snapshot():
    return {"sources": [{"id": f"s{i}", "source_number": i, "title": f"Source {i}", "url": f"https://example.com/{i}", "reliability": "unverified", "content": f"Source {i} reports a controlled local evaluation with 16 GB of memory. The result needs independent review."} for i in range(1, 4)], "draft_text": "", "brief": None}


def research_output():
    return {"items": [{"source_id": f"s{i}", "claims": [{"text": "The publisher reports a local evaluation.", "type": "source_claim", "evidence": [{"source_id": f"s{i}", "excerpt": f"Source {i} reports a controlled local evaluation with 16 GB of memory."}]}], "why_it_matters": "Analysis: evaluate the specific workload.", "who_should_care": "Builders testing local inference.", "angle": "Compare the evidence with deployment requirements."} for i in range(1, 4)], "synthesis": "The sources describe local tests, not production guarantees.", "contradictions": [], "uncertainties": ["Independent evaluation is missing."], "angle": "Availability versus suitability."}


def test_research_citations_use_server_provenance():
    result = research_result(research_output(), snapshot())
    assert result["method"] == "gemini"
    assert len(result["items"]) == 3
    evidence = result["items"][0]["what_happened"][0]
    assert evidence["url"] == "https://example.com/1"
    assert evidence["verified"] is False
    assert result["items"][0]["why_it_matters"]["type"] == "analysis"


@pytest.mark.parametrize("change", ["source", "quote", "missing", "duplicate"])
def test_research_rejects_invalid_evidence(change):
    value = copy.deepcopy(research_output())
    if change == "source": value["items"][0]["claims"][0]["evidence"][0]["source_id"] = "invented"
    if change == "quote": value["items"][0]["claims"][0]["evidence"][0]["excerpt"] = "This quotation does not occur in the source."
    if change == "missing": value["items"][2]["source_id"] = "missing"
    if change == "duplicate": value["items"][2]["source_id"] = "s1"
    with pytest.raises(AIError):
        research_result(value, snapshot())

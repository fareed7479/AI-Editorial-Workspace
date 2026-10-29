import pytest
from pydantic import ValidationError
from app.ai_schemas import WritingOutput
from app.config import get_settings


def test_settings_secrets_are_not_repr(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "private-test-key")
    settings = get_settings()
    assert settings.gemini_api_key == "private-test-key"
    assert "private-test-key" not in repr(settings)


def test_invalid_limits_fail_without_exposing_values(monkeypatch):
    monkeypatch.setenv("AI_DAILY_REQUEST_LIMIT", "0")
    with pytest.raises(ValueError, match="AI_DAILY_REQUEST_LIMIT"):
        get_settings()


def test_provider_schema_rejects_unknown_fields():
    with pytest.raises(ValidationError):
        WritingOutput.model_validate({"summary": "ok", "suggestions": [], "unexpected": "value"})


def test_stream_is_validated_and_client_closed(monkeypatch):
    from types import SimpleNamespace
    import app.gemini as adapter
    closed = []
    class Client:
        def __init__(self, **kwargs):
            self.models = SimpleNamespace(generate_content_stream=lambda **kw: iter([SimpleNamespace(text='{"suggestions":[],"summary":"Review complete."}', usage_metadata=None)]))
        def close(self): closed.append(True)
    monkeypatch.setenv("GEMINI_API_KEY", "synthetic-test-key")
    monkeypatch.setattr(adapter.genai, "Client", Client)
    events = list(adapter.iter_gemini("Review this test draft.", WritingOutput))
    assert events[0]["type"] == "progress"
    assert events[-1]["value"]["summary"] == "Review complete."
    assert closed == [True]


def test_invalid_provider_output_is_not_returned(monkeypatch):
    from types import SimpleNamespace
    import app.gemini as adapter
    class Client:
        def __init__(self, **kwargs):
            self.models = SimpleNamespace(generate_content_stream=lambda **kw: iter([SimpleNamespace(text='{"broken":', usage_metadata=None)]))
        def close(self): pass
    monkeypatch.setenv("GEMINI_API_KEY", "synthetic-test-key")
    monkeypatch.setattr(adapter.genai, "Client", Client)
    with pytest.raises(adapter.AIError, match="invalid structured"):
        list(adapter.iter_gemini("Review draft.", WritingOutput))


@pytest.mark.parametrize("code,expected", [(400,"provider_request"),(401,"provider_auth"),(403,"provider_auth"),(404,"model_unavailable"),(429,"provider_quota"),(503,"provider_unavailable")])
def test_provider_errors_are_sanitized(code, expected):
    from types import SimpleNamespace
    from app.gemini import map_provider_error
    error = map_provider_error(SimpleNamespace(code=code, message="sensitive upstream payload"))
    assert error.code == expected
    assert "sensitive" not in str(error)


def test_provider_schema_uses_supported_constraints():
    from app.gemini import provider_schema
    schema = provider_schema(WritingOutput)
    assert "summary" in schema["properties"]
    assert "minLength" not in schema["properties"]["summary"]
    assert schema["additionalProperties"] is False

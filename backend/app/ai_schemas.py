from typing import Literal
from pydantic import BaseModel, ConfigDict, Field


class StructuredModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Evidence(StructuredModel):
    source_id: str
    excerpt: str = Field(min_length=10, max_length=2000)


class Claim(StructuredModel):
    text: str = Field(min_length=1, max_length=1200)
    type: Literal["source_claim", "speculation", "analysis"]
    evidence: list[Evidence] = Field(min_length=1, max_length=3)


class SourceSummary(StructuredModel):
    source_id: str
    claims: list[Claim] = Field(min_length=1, max_length=3)
    why_it_matters: str = Field(min_length=1, max_length=1200)
    who_should_care: str = Field(min_length=1, max_length=800)
    angle: str = Field(min_length=1, max_length=800)


class Observation(StructuredModel):
    text: str = Field(min_length=1, max_length=1200)
    evidence: list[Evidence] = Field(min_length=1, max_length=4)


class ResearchOutput(StructuredModel):
    items: list[SourceSummary] = Field(min_length=3, max_length=20)
    synthesis: str = Field(min_length=1, max_length=2000)
    contradictions: list[Observation] = Field(max_length=8)
    uncertainties: list[str] = Field(max_length=10)
    angle: str = Field(min_length=1, max_length=1200)


class WritingSuggestion(StructuredModel):
    kind: Literal["Clarity", "Structure", "Tone", "Technical nuance"]
    passage: str = Field(min_length=1, max_length=3000)
    replacement: str = Field(min_length=1, max_length=4000)
    explanation: str = Field(min_length=1, max_length=1000)
    occurrence: int = Field(default=0, ge=0, le=100)


class WritingOutput(StructuredModel):
    suggestions: list[WritingSuggestion] = Field(max_length=12)
    summary: str = Field(min_length=1, max_length=1200)


class NewsletterOutput(StructuredModel):
    title: str = Field(min_length=1, max_length=200)
    body: str = Field(min_length=300, max_length=10000)
    evidence: list[Evidence] = Field(min_length=3, max_length=12)

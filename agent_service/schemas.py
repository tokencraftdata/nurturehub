from typing import Literal

from pydantic import BaseModel, Field


class SuggestionRequest(BaseModel):
    child_id: str = Field(pattern=r"^[A-Za-z0-9_-]{1,80}$")
    kind: Literal["meal", "sport"]


class ChildContext(BaseModel):
    age_band: Literal["under_6", "6_to_9", "10_to_12", "13_to_17"]
    liked_foods: list[str] = Field(max_length=12)
    disliked_foods: list[str] = Field(max_length=12)
    allergens: list[str] = Field(max_length=20)
    recent_activities: list[str] = Field(max_length=12)
    recent_energy: list[Literal["low", "good", "high"]] = Field(max_length=7)
    parent_consent_for_ai: bool = False


class Recommendation(BaseModel):
    title: str = Field(min_length=3, max_length=90)
    reason: str = Field(min_length=3, max_length=240)
    steps: list[str] = Field(min_length=1, max_length=5)
    duration_minutes: int = Field(ge=5, le=90)
    safety_note: str = Field(min_length=3, max_length=180)
    ai_used: bool
    parent_review_required: bool = True

import re

from fastapi import HTTPException

from .schemas import ChildContext, Recommendation


UNSAFE_HEALTH_LANGUAGE = re.compile(
    r"\b(diagnos|treat|cure|weight[- ]?loss|calorie restriction|supplement dosage|BMI)\b",
    re.IGNORECASE,
)


def require_ai_consent(context: ChildContext) -> None:
    if not context.parent_consent_for_ai:
        raise HTTPException(409, "A parent must enable AI suggestions first")


def require_minor_privacy_configuration(context: ChildContext, zdr_approved: bool) -> None:
    if context.age_band != "13_to_17" and not zdr_approved:
        raise HTTPException(
            503,
            "AI is disabled for children under 13 until Zero Data Retention is approved; use local matching",
        )


def validate_output(result: Recommendation, allergens: list[str]) -> Recommendation:
    combined = " ".join([result.title, result.reason, result.safety_note, *result.steps])
    if UNSAFE_HEALTH_LANGUAGE.search(combined):
        raise HTTPException(422, "The recommendation crossed a health-advice boundary")
    for allergen in allergens:
        if allergen and re.search(rf"\b{re.escape(allergen)}\b", combined, re.IGNORECASE):
            raise HTTPException(422, "The recommendation may conflict with a saved allergen")
    return result

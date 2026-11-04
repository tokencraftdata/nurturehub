import pytest
from fastapi import HTTPException

from agent_service.guardrails import require_minor_privacy_configuration, validate_output
from agent_service.schemas import ChildContext, Recommendation


def context(age_band="under_6"):
    return ChildContext(age_band=age_band, liked_foods=[], disliked_foods=[], allergens=["peanut"], recent_activities=[], recent_energy=[], parent_consent_for_ai=True)


def test_under_13_ai_is_off_without_zdr():
    with pytest.raises(HTTPException) as error:
        require_minor_privacy_configuration(context(), False)
    assert error.value.status_code == 503


def test_allergen_mention_is_rejected():
    result = Recommendation(title="Snack", reason="Familiar", steps=["Add peanut butter"], duration_minutes=5, safety_note="Adult reviews", ai_used=True)
    with pytest.raises(HTTPException):
        validate_output(result, ["peanut"])


def test_medical_or_weight_advice_is_rejected():
    result = Recommendation(title="Sport", reason="For weight loss", steps=["Walk"], duration_minutes=15, safety_note="Adult reviews", ai_used=True)
    with pytest.raises(HTTPException):
        validate_output(result, [])

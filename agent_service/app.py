import os

from fastapi import Depends, FastAPI
from mangum import Mangum

from .agent import make_recommendation
from .auth import Principal, authenticated_parent
from .guardrails import require_ai_consent, require_minor_privacy_configuration
from .repository import ChildRepository
from .schemas import Recommendation, SuggestionRequest


app = FastAPI(title="NurtureHub private recommendation agent", docs_url=None, redoc_url=None)


@app.post("/v1/suggestions", response_model=Recommendation)
def suggest(request: SuggestionRequest, parent: Principal = Depends(authenticated_parent)) -> Recommendation:
    context = ChildRepository().load_for_parent(parent.user_id, request.child_id)
    require_ai_consent(context)
    require_minor_privacy_configuration(
        context, os.getenv("OPENAI_ZDR_APPROVED", "false").lower() == "true"
    )
    return make_recommendation(request.kind, context)


handler = Mangum(app)

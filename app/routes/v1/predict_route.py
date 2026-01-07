from fastapi import APIRouter, Form, Request, Header
from typing import Literal
from app.controllers.v1.credit_scoring import CreditScoring

router = APIRouter()


@router.post("/predict")
async def predict(
    request: Request,

    x_demo_language: Literal["uz", "ru", "en"] = Header(
        default="en",
        alias="x-demo-app-language"
    ),

    marital_status: str = Form(...),
    date_birth: str = Form(...),
    gender: str = Form(...),
    region: str = Form(...),
    city: str = Form(...),
    family_members: int = Form(...),
    education: str = Form(...),
    job_position: str = Form(...),
    loan_amount: int = Form(...),
    interest_rate: int = Form(...),
    loan_term: int = Form(...),
    cycle: int = Form(...),
    loan_purpose: str = Form(...),
):
    request.state.language = x_demo_language

    payload = {
        "marital_status": marital_status,
        "date_birth": date_birth,
        "gender": gender,
        "region": region,
        "city": city,
        "family_members": family_members,
        "education": education,
        "job_position": job_position,
        "loan_amount": loan_amount,
        "interest_rate": interest_rate,
        "loan_term": loan_term,
        "cycle": cycle,
        "loan_purpose": loan_purpose,
    }

    controller = CreditScoring(request)
    return controller.make_credit_score(payload)

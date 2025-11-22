from fastapi import APIRouter
from app.routes.v1.predict_route import router as PredictRouter

router = APIRouter(prefix="/v1")
router.include_router(PredictRouter)

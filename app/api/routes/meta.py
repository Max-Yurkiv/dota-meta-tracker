from fastapi import APIRouter, Query
from app.schemas.meta import MetaRecommendationsResponse, PlayerRole
from app.services.meta import meta_service

router = APIRouter(prefix="/meta", tags=["Meta"])


@router.get("/recommendations/{steam_id}", response_model=MetaRecommendationsResponse)
async def get_meta_recommendations(
    steam_id: int,
    role: PlayerRole = Query(..., description="Оберіть позицію (pos1 - pos5)"),
):
    return await meta_service.get_recommendations(steam_id, role)
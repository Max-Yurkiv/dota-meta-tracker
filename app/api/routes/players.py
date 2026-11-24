from fastapi import APIRouter
from app.schemas.player import PlayerProfileResponse
from app.services.opendota import opendota_service

router = APIRouter(prefix="/players", tags=["Players"])


@router.get("/{steam_id}", response_model=PlayerProfileResponse)
async def get_player(steam_id: int):
    return await opendota_service.get_player_profile(steam_id)
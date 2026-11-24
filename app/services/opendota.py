import httpx
from fastapi import HTTPException
from app.core.config import settings
from app.schemas.player import PlayerProfileResponse

RANK_NAMES = {
    1: "Herald",
    2: "Guardian",
    3: "Crusader",
    4: "Archon",
    5: "Legend",
    6: "Ancient",
    7: "Divine",
    8: "Immortal",
}


class OpenDotaService:
    @staticmethod
    def normalize_account_id(steam_id: int) -> int:
        if steam_id > settings.STEAM_ID_64_BASE:
            return steam_id - settings.STEAM_ID_64_BASE
        return steam_id

    @staticmethod
    def decode_rank(rank_tier: int | None) -> str:
        if not rank_tier:
            return "Uncalibrated / Hidden"
        medal = rank_tier // 10
        stars = rank_tier % 10
        name = RANK_NAMES.get(medal, "Unknown")
        return name if medal == 8 else f"{name} {stars}"

    async def get_player_profile(self, steam_id: int) -> PlayerProfileResponse:
        account_id = self.normalize_account_id(steam_id)
        url = f"{settings.OPENDOTA_BASE_URL}/players/{account_id}"

        async with httpx.AsyncClient() as client:
            response = await client.get(url)

        if response.status_code != 200:
            raise HTTPException(status_code=502, detail="Помилка при зверненні до OpenDota API")

        data = response.json()
        profile = data.get("profile")

        if not profile:
            raise HTTPException(
                status_code=404,
                detail="Профіль не знайдено або у гравця закрита історія матчів",
            )

        return PlayerProfileResponse(
            account_id=account_id,
            nickname=profile.get("personaname"),
            avatar=profile.get("avatarfull"),
            rank_tier=data.get("rank_tier"),
            rank_name=self.decode_rank(data.get("rank_tier")),
        )


opendota_service = OpenDotaService()
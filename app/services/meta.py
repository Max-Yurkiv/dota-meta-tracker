import json
import httpx
from fastapi import HTTPException
from redis.exceptions import RedisError

from app.core.config import settings
from app.core.redis import redis_client
from app.schemas.meta import (
    HeroRecommendation,
    MetaRecommendationsResponse,
    PlayerRole,
)
from app.services.opendota import opendota_service

ROLE_TAGS: dict[PlayerRole, set[str]] = {
    PlayerRole.pos1: {"Carry"},
    PlayerRole.pos2: {"Nuker", "Escape"},
    PlayerRole.pos3: {"Durable", "Initiator"},
    PlayerRole.pos4: {"Support", "Disabler"},
    PlayerRole.pos5: {"Support"},
}


class MetaService:
    async def get_hero_stats(self) -> list[dict]:
        """Повертає статистику всіх героїв (із кешу Redis або OpenDota)."""
        cache_key = "meta:hero_stats"

        try:
            cached = await redis_client.get(cache_key)
            if cached:
                return json.loads(cached)
        except RedisError:
            pass

        url = f"{settings.OPENDOTA_BASE_URL}/heroStats"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)

        if response.status_code != 200:
            raise HTTPException(
                status_code=502,
                detail="Не вдалося отримати статистику героїв із OpenDota",
            )

        stats = response.json()

        try:
            await redis_client.setex(
                cache_key,
                settings.HERO_STATS_CACHE_TTL,
                json.dumps(stats),
            )
        except RedisError:
            pass

        return stats

    async def get_recommendations(
        self,
        steam_id: int,
        role: PlayerRole,
        limit: int = 5,
    ) -> MetaRecommendationsResponse:
        player = await opendota_service.get_player_profile(steam_id)

        bracket = (player.rank_tier // 10) if player.rank_tier else 4
        bracket = max(1, min(8, bracket))

        pick_key = f"{bracket}_pick"
        win_key = f"{bracket}_win"
        required_tags = ROLE_TAGS[role]

        hero_stats = await self.get_hero_stats()
        recommendations: list[HeroRecommendation] = []

        for hero in hero_stats:
            hero_roles = set(hero.get("roles", []))
            if not hero_roles.intersection(required_tags):
                continue

            picks = hero.get(pick_key, 0)
            wins = hero.get(win_key, 0)

            if picks < 50:
                continue

            winrate = round((wins / picks) * 100, 2)
            recommendations.append(
                HeroRecommendation(
                    hero_id=hero["id"],
                    name=hero["localized_name"],
                    image=f"{settings.OPENDOTA_CDN_URL}{hero.get('img', '')}",
                    picks=picks,
                    wins=wins,
                    winrate=winrate,
                )
            )

        recommendations.sort(key=lambda h: h.winrate, reverse=True)

        return MetaRecommendationsResponse(
            account_id=player.account_id,
            rank_name=player.rank_name,
            rank_bracket=bracket,
            role=role,
            heroes=recommendations[:limit],
        )


meta_service = MetaService()
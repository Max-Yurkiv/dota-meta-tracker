from enum import Enum
from pydantic import BaseModel


class PlayerRole(str, Enum):
    pos1 = "pos1"
    pos2 = "pos2"
    pos3 = "pos3"
    pos4 = "pos4"
    pos5 = "pos5"


class HeroRecommendation(BaseModel):
    hero_id: int
    name: str
    image: str
    picks: int
    wins: int
    winrate: float


class MetaRecommendationsResponse(BaseModel):
    account_id: int
    rank_name: str
    rank_bracket: int
    role: PlayerRole
    heroes: list[HeroRecommendation]
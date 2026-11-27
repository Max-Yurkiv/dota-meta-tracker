from pydantic import BaseModel


class PlayerProfileResponse(BaseModel):
    account_id: int
    nickname: str | None
    avatar: str | None
    rank_tier: int | None
    rank_name: str
    from_cache: bool = False
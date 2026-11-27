class Settings:
    PROJECT_NAME: str = "Dota 2 Meta Tracker"
    OPENDOTA_BASE_URL: str = "https://api.opendota.com/api"
    OPENDOTA_CDN_URL: str = "https://cdn.cloudflare.steamstatic.com"
    STEAM_ID_64_BASE: int = 76561197960265728

    REDIS_URL: str = "redis://localhost:6379/0"
    PLAYER_CACHE_TTL: int = 900       
    HERO_STATS_CACHE_TTL: int = 3600  
    
settings = Settings()
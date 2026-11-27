from fastapi import FastAPI
from app.api.routes import meta, players
from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(players.router)
app.include_router(meta.router)


@app.get("/")
async def root():
    return {"message": "Dota 2 Meta Tracker API is running"}
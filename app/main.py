from fastapi import FastAPI
from app.core.config import settings
from app.api.routes import players

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(players.router)


@app.get("/", tags=["Health"])
async def root():
    return {"status": "ok", "message": f"{settings.PROJECT_NAME} is running"}
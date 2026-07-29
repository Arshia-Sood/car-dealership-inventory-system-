from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.api.vehicles import router as vehicles_router
from app.core.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    version="0.1.0",
    debug=settings.DEBUG,
)

app.include_router(auth_router)
app.include_router(vehicles_router)


import os
from fastapi import FastAPI
from app.core.modules.auth.router import router as auth_router 
from app.core.modules.profile.router import router as profile_router
from fastapi.staticfiles import StaticFiles
from app.core.config import settings

app = FastAPI(
    title="Flight Booking API",
    description="سیستم جامع رزرواسیون بلیط هواپیما",
    version="1.0.0"
)

os.makedirs(settings.UPLOADS_DIR, exist_ok=True)

app.mount("/static", StaticFiles(directory=str(settings.STATIC_DIR)), name="static")

@app.get("/")
def root():
    return {"message": "Welcome to the Flight Booking Backend API!"}

app.include_router(auth_router)
app.include_router(profile_router)


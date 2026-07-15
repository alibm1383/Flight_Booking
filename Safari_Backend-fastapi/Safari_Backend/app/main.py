import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.modules.auth.router import router as auth_router
from app.core.modules.profile.router import router as profile_router
from app.core.modules.users.router import router as users_router
from app.core.config import settings

app = FastAPI(
    title="Flight Booking API",
    description="سیستم جامع رزرواسیون بلیط هواپیما",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs(settings.UPLOADS_DIR, exist_ok=True)

app.mount(
    "/static",
    StaticFiles(directory=str(settings.STATIC_DIR)),
    name="static"
)

@app.get("/")
def root():
    return {
        "message": "Welcome to the Flight Booking Backend API!"
    }

app.include_router(auth_router)
app.include_router(profile_router)
app.include_router(users_router)
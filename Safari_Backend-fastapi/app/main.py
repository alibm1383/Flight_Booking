from fastapi import FastAPI
from app.core.modules.auth.router import router as auth_router 

app = FastAPI(
    title="Flight Booking API",
    description="سیستم جامع رزرواسیون بلیط هواپیما",
    version="1.0.0"
)

app.include_router(auth_router)

@app.get("/")
def root():
    return {"message": "Welcome to the Flight Booking Backend API!"}
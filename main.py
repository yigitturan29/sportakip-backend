from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine, Base

from routes import exercises, workouts, nutrition, ai
from routes import auth 
app = FastAPI(
    title="SportakipAI API",
    description="Spor takip ve AI tabanlı antrenman öneri sistemi",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Tablolar yoksa oluştur (SQLite için yeterli, Alembic gerekmez)
Base.metadata.create_all(bind=engine)

app.include_router(exercises.router, prefix="/exercises", tags=["Hareketler"])
app.include_router(workouts.router,  prefix="/workouts",  tags=["Antrenmanlar"])
app.include_router(nutrition.router, prefix="/nutrition", tags=["Beslenme"])
app.include_router(ai.router,        prefix="/ai",        tags=["AI Öneriler"])
app.include_router(auth.router, prefix="/auth", tags=["Auth"]) 

@app.get("/health", tags=["Sistem"])
def health_check():
    return {"durum": "aktif", "uygulama": "SportakipAI", "db": "SQLite"}

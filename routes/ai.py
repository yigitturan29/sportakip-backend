from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from app.schemas.workout import AIWorkoutRequest, PerformanceLog
from app.services.workout_recommendation import oneri_uret, oneri_uret_batch
from app.services.groq_service import groq_ai_insight, groq_ai_chat

router = APIRouter()


class GroqInsightRequest(BaseModel):
    workouts: List[dict] = []
    nutrition: dict = {}
    measurements: List[dict] = []


@router.post("/workout-recommendation")
def workout_recommendation_batch(req: AIWorkoutRequest):
    """Tüm antrenman için egzersiz bazlı AI önerileri döner."""
    oneriler = oneri_uret_batch(req.exercises)
    return {"oneriler": oneriler}


@router.post("/workout-recommendation/single")
def workout_recommendation_single(log: PerformanceLog):
    """Tekil egzersiz için öneri (geriye uyumluluk)."""
    oneri = oneri_uret(log.model_dump())
    return {"hareket": log.hareket_adi, "oneri": oneri}


class ChatRequest(BaseModel):
    message: str
    history: List[dict] = []
    context: dict = {}


@router.post("/chat")
def ai_chat_endpoint(req: ChatRequest):
    """Dashboard AI Koç chatbox — Groq ile konuşma."""
    try:
        reply = groq_ai_chat(req.message, req.history, req.context)
        return {"reply": reply, "success": True}
    except Exception as e:
        return {"reply": f"AI koç şu an yanıt veremiyor: {str(e)}", "success": False}


@router.post("/groq-insight")
def groq_insight_endpoint(req: GroqInsightRequest):
    """Groq Llama 3 ile kişisel fitness analizi."""
    try:
        insight = groq_ai_insight(req.workouts, req.nutrition, req.measurements)
        return {"insight": insight, "success": True}
    except Exception as e:
        return {"insight": f"AI koç şu an kullanılamıyor: {str(e)}", "success": False}
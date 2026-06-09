from pydantic import BaseModel
from typing import Optional, List


# ── Tekil egzersiz kaydı ─────────────────────────────────
class ExerciseLog(BaseModel):
    id:      int
    ad:      str
    kas:     str
    ekipman: str
    sets:    str
    reps:    str
    weight:  str
    rpe:     int = 7
    note:    Optional[str] = ""


# ── Tam antrenman kaydı (frontend'den gelir) ─────────────
class WorkoutRecord(BaseModel):
    dateKey:   str           # "2026-05-04"
    date:      str           # "4 Mayıs 2026 14:30"
    exercises: List[ExerciseLog]


# ── AI öneri isteği ──────────────────────────────────────
class AIWorkoutRequest(BaseModel):
    exercises: List[ExerciseLog]


# ── Eski şemalar (geriye uyumluluk) ──────────────────────
class PerformanceLog(BaseModel):
    hareket_adi:             str
    set_sayisi:              int
    tekrar:                  int
    agirlik:                 float
    rpe:                     int = 7
    hedef_tekrar_tamamlandi: bool = True
    not_:                    Optional[str] = None

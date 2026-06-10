from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from db_models import WorkoutRecord, ExerciseLog, User
from schemas.workout import WorkoutRecord as WorkoutSchema, PerformanceLog
from services.workout_recommendation import oneri_uret
from routes.auth import get_current_user

router = APIRouter()


def _serialize(w: WorkoutRecord) -> dict:
    return {
        "id":        w.id,
        "dateKey":   w.date_key,
        "date":      w.date_str,
        "exercises": [
            {
                "id":      e.id,
                "ad":      e.ad,
                "kas":     e.kas,
                "ekipman": e.ekipman,
                "sets":    e.sets,
                "reps":    e.reps,
                "weight":  e.weight,
                "rpe":     e.rpe,
                "note":    e.note,
            }
            for e in w.exercises
        ],
    }


@router.post("/record")
def save_workout_record(
    record: WorkoutSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_workout = WorkoutRecord(
        user_id=current_user.id,
        date_key=record.dateKey,
        date_str=record.date,
    )
    db.add(db_workout)
    db.flush()

    for ex in record.exercises:
        db.add(ExerciseLog(
            workout_id=db_workout.id,
            ad=ex.ad, kas=ex.kas, ekipman=ex.ekipman,
            sets=ex.sets, reps=ex.reps, weight=ex.weight,
            rpe=ex.rpe, note=ex.note or "",
        ))

    db.commit()
    db.refresh(db_workout)
    return {
        "mesaj":           "Antrenman kaydedildi",
        "id":              db_workout.id,
        "egzersiz_sayisi": len(record.exercises),
    }


@router.get("/records")
def get_workout_records(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    workouts = (
        db.query(WorkoutRecord)
        .filter(WorkoutRecord.user_id == current_user.id)
        .order_by(WorkoutRecord.id.desc())
        .all()
    )
    return [_serialize(w) for w in workouts]


@router.get("/records/{date_key}")
def get_workout_by_date(
    date_key: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    workouts = (
        db.query(WorkoutRecord)
        .filter(
            WorkoutRecord.user_id == current_user.id,
            WorkoutRecord.date_key == date_key,
        )
        .all()
    )
    return [_serialize(w) for w in workouts]


@router.get("/stats")
def get_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    total_workouts = (
        db.query(WorkoutRecord)
        .filter(WorkoutRecord.user_id == current_user.id)
        .count()
    )
    total_exercises = (
        db.query(ExerciseLog)
        .join(WorkoutRecord)
        .filter(WorkoutRecord.user_id == current_user.id)
        .count()
    )
    return {
        "toplam_antrenman": total_workouts,
        "toplam_egzersiz":  total_exercises,
    }


@router.post("/performance")
def log_performance(
    log: PerformanceLog,
    current_user: User = Depends(get_current_user),
):
    return {"mesaj": "Performans kaydedildi", "oneri": oneri_uret(log.model_dump())}
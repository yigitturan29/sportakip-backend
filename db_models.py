from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base


# ── YENİ: Kullanıcı tablosu ───────────────────────────────
class User(Base):
    __tablename__ = "users"

    id              = Column(Integer, primary_key=True, index=True)
    username        = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at      = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    workouts  = relationship("WorkoutRecord", back_populates="user", cascade="all, delete-orphan")
    nutrition = relationship("NutritionLog",  back_populates="user", cascade="all, delete-orphan")


class WorkoutRecord(Base):
    __tablename__ = "workouts"

    id         = Column(Integer, primary_key=True, index=True)
    user_id    = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)  # ← EKLENDİ
    date_key   = Column(String, index=True)
    date_str   = Column(String)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user      = relationship("User", back_populates="workouts")
    exercises = relationship("ExerciseLog", back_populates="workout", cascade="all, delete-orphan")


class ExerciseLog(Base):
    __tablename__ = "exercise_logs"

    id         = Column(Integer, primary_key=True, index=True)
    workout_id = Column(Integer, ForeignKey("workouts.id"), nullable=False)
    ad         = Column(String)
    kas        = Column(String)
    ekipman    = Column(String)
    sets       = Column(String)
    reps       = Column(String)
    weight     = Column(String)
    rpe        = Column(Integer, default=7)
    note       = Column(String, default="")

    workout = relationship("WorkoutRecord", back_populates="exercises")


class NutritionLog(Base):
    __tablename__ = "nutrition_logs"

    id         = Column(Integer, primary_key=True, index=True)
    user_id    = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)  # ← EKLENDİ
    date_key   = Column(String, index=True)
    food_id    = Column(Integer)
    ad         = Column(String)
    grams      = Column(Float)
    birim      = Column(String)
    kalori     = Column(Integer)
    protein    = Column(Float)
    karb       = Column(Float)
    yag        = Column(Float)
    tip        = Column(String)
    zaman      = Column(String)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="nutrition")
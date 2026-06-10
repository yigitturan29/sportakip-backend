from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from db_models import NutritionLog
from schemas.nutrition import MealEntry

router = APIRouter()


def _serialize(m: NutritionLog) -> dict:
    return {
        "id":      m.id,
        "foodId":  m.food_id,
        "ad":      m.ad,
        "grams":   m.grams,
        "birim":   m.birim,
        "kalori":  m.kalori,
        "protein": m.protein,
        "karb":    m.karb,
        "yag":     m.yag,
        "tip":     m.tip,
        "zaman":   m.zaman,
    }


@router.post("/meal")
def add_meal(entry: MealEntry, date_key: str, db: Session = Depends(get_db)):
    meal = NutritionLog(
        date_key=date_key,
        food_id=entry.foodId,
        ad=entry.ad,
        grams=entry.grams,
        birim=entry.birim,
        kalori=entry.kalori,
        protein=entry.protein,
        karb=entry.karb,
        yag=entry.yag,
        tip=entry.tip,
        zaman=entry.zaman,
    )
    db.add(meal)
    db.commit()
    db.refresh(meal)
    return {"id": meal.id, "mesaj": f"{entry.ad} kaydedildi"}


@router.get("/day/{date_key}")
def get_daily_meals(date_key: str, db: Session = Depends(get_db)):
    meals = (
        db.query(NutritionLog)
        .filter(NutritionLog.date_key == date_key)
        .order_by(NutritionLog.id)
        .all()
    )
    return [_serialize(m) for m in meals]


@router.delete("/meal/{meal_id}")
def delete_meal(meal_id: int, db: Session = Depends(get_db)):
    meal = db.query(NutritionLog).filter(NutritionLog.id == meal_id).first()
    if not meal:
        raise HTTPException(status_code=404, detail="Öğün bulunamadı")
    db.delete(meal)
    db.commit()
    return {"mesaj": "Silindi"}


@router.get("/summary/{date_key}")
def get_daily_summary(date_key: str, db: Session = Depends(get_db)):
    meals = db.query(NutritionLog).filter(NutritionLog.date_key == date_key).all()
    totals = {
        "kalori":  sum(m.kalori  for m in meals),
        "protein": sum(m.protein for m in meals),
        "karb":    sum(m.karb    for m in meals),
        "yag":     sum(m.yag     for m in meals),
    }
    return {"date_key": date_key, "meal_count": len(meals), **totals}

from fastapi import APIRouter, Query
from typing import Optional
from schemas.exercise import ExerciseResponse

router = APIRouter()

# Frontend data/exercises.json ile senkronize — 54 egzersiz
EXERCISES = [
  {"id": 1,  "ad": "Bench Press",           "kas": "Göğüs",     "ekipman": "Barbell",    "image_url": ""},
  {"id": 2,  "ad": "Incline Dumbbell Press", "kas": "Göğüs",     "ekipman": "Dumbbell",   "image_url": ""},
  {"id": 3,  "ad": "Cable Fly",             "kas": "Göğüs",     "ekipman": "Cable",      "image_url": ""},
  {"id": 4,  "ad": "Push Up",               "kas": "Göğüs",     "ekipman": "Bodyweight", "image_url": ""},
  {"id": 5,  "ad": "Decline Bench Press",   "kas": "Göğüs",     "ekipman": "Barbell",    "image_url": ""},
  {"id": 6,  "ad": "Dumbbell Fly",          "kas": "Göğüs",     "ekipman": "Dumbbell",   "image_url": ""},
  {"id": 7,  "ad": "Lat Pulldown",          "kas": "Sırt",      "ekipman": "Cable",      "image_url": ""},
  {"id": 8,  "ad": "Pull Up",               "kas": "Sırt",      "ekipman": "Bodyweight", "image_url": ""},
  {"id": 9,  "ad": "Barbell Row",           "kas": "Sırt",      "ekipman": "Barbell",    "image_url": ""},
  {"id": 10, "ad": "Seated Cable Row",      "kas": "Sırt",      "ekipman": "Cable",      "image_url": ""},
  {"id": 11, "ad": "T-Bar Row",             "kas": "Sırt",      "ekipman": "Barbell",    "image_url": ""},
  {"id": 12, "ad": "Deadlift",              "kas": "Sırt",      "ekipman": "Barbell",    "image_url": ""},
  {"id": 13, "ad": "Shoulder Press",        "kas": "Omuz",      "ekipman": "Dumbbell",   "image_url": ""},
  {"id": 14, "ad": "Lateral Raise",         "kas": "Omuz",      "ekipman": "Dumbbell",   "image_url": ""},
  {"id": 15, "ad": "Rear Delt Fly",         "kas": "Omuz",      "ekipman": "Dumbbell",   "image_url": ""},
  {"id": 16, "ad": "Front Raise",           "kas": "Omuz",      "ekipman": "Dumbbell",   "image_url": ""},
  {"id": 17, "ad": "Arnold Press",          "kas": "Omuz",      "ekipman": "Dumbbell",   "image_url": ""},
  {"id": 18, "ad": "Military Press",        "kas": "Omuz",      "ekipman": "Barbell",    "image_url": ""},
  {"id": 19, "ad": "Barbell Curl",          "kas": "Biceps",    "ekipman": "Barbell",    "image_url": ""},
  {"id": 20, "ad": "Dumbbell Curl",         "kas": "Biceps",    "ekipman": "Dumbbell",   "image_url": ""},
  {"id": 21, "ad": "Hammer Curl",           "kas": "Biceps",    "ekipman": "Dumbbell",   "image_url": ""},
  {"id": 22, "ad": "Preacher Curl",         "kas": "Biceps",    "ekipman": "Barbell",    "image_url": ""},
  {"id": 23, "ad": "Cable Bicep Curl",      "kas": "Biceps",    "ekipman": "Cable",      "image_url": ""},
  {"id": 24, "ad": "Tricep Pushdown",       "kas": "Triceps",   "ekipman": "Cable",      "image_url": ""},
  {"id": 25, "ad": "Skull Crusher",         "kas": "Triceps",   "ekipman": "Barbell",    "image_url": ""},
  {"id": 26, "ad": "Dips",                  "kas": "Triceps",   "ekipman": "Bodyweight", "image_url": ""},
  {"id": 27, "ad": "Overhead Tricep Ext.",  "kas": "Triceps",   "ekipman": "Dumbbell",   "image_url": ""},
  {"id": 28, "ad": "Close Grip Bench",      "kas": "Triceps",   "ekipman": "Barbell",    "image_url": ""},
  {"id": 29, "ad": "Crunch",               "kas": "Karın",     "ekipman": "Bodyweight", "image_url": ""},
  {"id": 30, "ad": "Hanging Leg Raise",    "kas": "Karın",     "ekipman": "Bodyweight", "image_url": ""},
  {"id": 31, "ad": "Plank",               "kas": "Karın",     "ekipman": "Bodyweight", "image_url": ""},
  {"id": 32, "ad": "Cable Crunch",         "kas": "Karın",     "ekipman": "Cable",      "image_url": ""},
  {"id": 33, "ad": "Russian Twist",        "kas": "Karın",     "ekipman": "Bodyweight", "image_url": ""},
  {"id": 34, "ad": "Squat",               "kas": "Ön Bacak",  "ekipman": "Barbell",    "image_url": ""},
  {"id": 35, "ad": "Front Squat",         "kas": "Ön Bacak",  "ekipman": "Barbell",    "image_url": ""},
  {"id": 36, "ad": "Leg Press",           "kas": "Ön Bacak",  "ekipman": "Machine",    "image_url": ""},
  {"id": 37, "ad": "Leg Extension",       "kas": "Ön Bacak",  "ekipman": "Machine",    "image_url": ""},
  {"id": 38, "ad": "Hack Squat",          "kas": "Ön Bacak",  "ekipman": "Machine",    "image_url": ""},
  {"id": 39, "ad": "Bulgarian Split Squat","kas": "Ön Bacak",  "ekipman": "Dumbbell",   "image_url": ""},
  {"id": 40, "ad": "Romanian Deadlift",   "kas": "Arka Bacak","ekipman": "Barbell",    "image_url": ""},
  {"id": 41, "ad": "Leg Curl",            "kas": "Arka Bacak","ekipman": "Machine",    "image_url": ""},
  {"id": 42, "ad": "Good Morning",        "kas": "Arka Bacak","ekipman": "Barbell",    "image_url": ""},
  {"id": 43, "ad": "Stiff Leg Deadlift",  "kas": "Arka Bacak","ekipman": "Barbell",    "image_url": ""},
  {"id": 44, "ad": "Hip Thrust",          "kas": "Kalça",     "ekipman": "Barbell",    "image_url": ""},
  {"id": 45, "ad": "Glute Bridge",        "kas": "Kalça",     "ekipman": "Bodyweight", "image_url": ""},
  {"id": 46, "ad": "Cable Kickback",      "kas": "Kalça",     "ekipman": "Cable",      "image_url": ""},
  {"id": 47, "ad": "Standing Calf Raise", "kas": "Baldır",    "ekipman": "Machine",    "image_url": ""},
  {"id": 48, "ad": "Seated Calf Raise",   "kas": "Baldır",    "ekipman": "Machine",    "image_url": ""},
  {"id": 49, "ad": "Barbell Shrug",       "kas": "Trapez",    "ekipman": "Barbell",    "image_url": ""},
  {"id": 50, "ad": "Face Pull",           "kas": "Trapez",    "ekipman": "Cable",      "image_url": ""},
  {"id": 51, "ad": "Rack Pull",           "kas": "Trapez",    "ekipman": "Barbell",    "image_url": ""},
  {"id": 52, "ad": "Wrist Curl",          "kas": "Ön Kol",    "ekipman": "Barbell",    "image_url": ""},
  {"id": 53, "ad": "Reverse Wrist Curl",  "kas": "Ön Kol",    "ekipman": "Barbell",    "image_url": ""},
  {"id": 54, "ad": "Farmer's Walk",       "kas": "Ön Kol",    "ekipman": "Dumbbell",   "image_url": ""},
]


@router.get("/", response_model=list[ExerciseResponse])
def get_exercises(kas: Optional[str] = Query(None, description="Göğüs | Sırt | Omuz | ...")):
    if kas:
        return [e for e in EXERCISES if e["kas"] == kas]
    return EXERCISES


@router.get("/{exercise_id}", response_model=ExerciseResponse)
def get_exercise(exercise_id: int):
    ex = next((e for e in EXERCISES if e["id"] == exercise_id), None)
    if not ex:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Egzersiz bulunamadı")
    return ex

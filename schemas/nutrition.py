from pydantic import BaseModel


class MealEntry(BaseModel):
    foodId:  int
    ad:      str
    grams:   float
    birim:   str
    kalori:  int
    protein: float
    karb:    float
    yag:     float
    tip:     str
    zaman:   str

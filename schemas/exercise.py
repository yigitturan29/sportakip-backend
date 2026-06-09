from pydantic import BaseModel
from typing import Optional


class ExerciseResponse(BaseModel):
    id:        int
    ad:        str
    kas:       str       # kas grubu (Göğüs, Sırt, Omuz, ...)
    ekipman:   str
    image_url: Optional[str] = ""

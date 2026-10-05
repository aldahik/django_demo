from pydantic import BaseModel
from decimal import Decimal
from datetime import date

class AnalysisResult(BaseModel):
    material: str | None = None
    quantity: int | None = None
    thickness_mm: float | None = None
    width_mm: float | None = None    
    height_mm: float | None = None
    deadline: date | None = None

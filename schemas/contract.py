from pydantic import BaseModel
from typing import Optional
from datetime import date
from schemas.streak import Streak
from schemas.penalty import Penalty

class Contract(BaseModel):
    id: Optional[int] = None
    task_id: str
    habit: str
    penalty: str
    start: date
    end: date
    supervisor_name: str
    supervisor_email: str
    status: Optional[int] = 0
    is_completed: Optional[int] = 0
    streaks: Optional[Streak] = None
    penalties: Optional[Penalty] = None
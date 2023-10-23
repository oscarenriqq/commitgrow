from pydantic import BaseModel
from typing import Optional
from datetime import date

class Contract(BaseModel):
    id: Optional[int] = None
    user_id: str
    task_id: str
    habit: str
    description: str
    penalty: str
    start: date
    end: date
    supervisor_name: str
    supervisor_email: str
    status: Optional[int] = 0
from pydantic import BaseModel
from typing import Optional
from datetime import date

class ContractUpdate(BaseModel):
    id: Optional[int] = None
    user_id: Optional[str] = None
    task_id: Optional[str] = None
    habit: Optional[str] = None
    description: Optional[str] = None
    penalty: Optional[str] = None
    start: Optional[date] = None
    end: Optional[date] = None
    supervisor_name: Optional[str] = None
    supervisor_email: Optional[str] = None
    status: Optional[int] = 0
    responsible_name: Optional[str] = None
    responsible_email: Optional[str] = None
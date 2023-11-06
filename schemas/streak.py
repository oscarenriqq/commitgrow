from pydantic import BaseModel
from typing import Optional

class Streak(BaseModel):
    id: Optional[int] = 0
    contract_id: int
from pydantic import BaseModel
from typing import Optional

class Penalty(BaseModel):
    id: Optional[int] = 0
    contract_id: int
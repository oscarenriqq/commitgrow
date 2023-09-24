from typing import Optional
from pydantic import BaseModel

class User(BaseModel):
    id: Optional[int] = 0
    name: str
    email: str
    password: str
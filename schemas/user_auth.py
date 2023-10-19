from typing import Optional
from pydantic import BaseModel

class UserAuth(BaseModel):
    id: Optional[str] = None
    name: str
    email: str
    password: str
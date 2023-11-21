from enum import Enum
from typing import Optional
from pydantic import BaseModel

class UserRole(str, Enum):
    admin = "admin"
    user = "user"

class User(BaseModel):
    id: Optional[int] = 0
    name: str
    email: str
    password: str
    secret_string: str
    todoist_access_token: Optional[str] = ""
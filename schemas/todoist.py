from pydantic import BaseModel

class Todoist(BaseModel):
    secret_string: str
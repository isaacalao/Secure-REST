from pydantic import BaseModel

class User(BaseModel): # inherits from PyDantic BaseModel
    username: str
    password: str
    access: str | None = None
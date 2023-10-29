from pydantic import BaseModel

class Demo(BaseModel): #inherits from PyDantic BaseModel
    title: str
    body: str
    description: str

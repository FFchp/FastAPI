from pydantic import BaseModel

#request field

class User(BaseModel):
    id: int
    name: str
    email: str
    password: int
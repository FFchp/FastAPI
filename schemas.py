from pydantic import BaseModel

#request field

class User(BaseModel):
    name: str
    email: str
    password: str

class Update_User(BaseModel):
    id: int
    name: str
    email: str
    password: str


class ShowUser(BaseModel):
    name: str
    email: str
    
    class Config():
        orm_mode = True

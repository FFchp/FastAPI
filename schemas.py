from pydantic import BaseModel

#request field

class User(BaseModel):
    username: str
    email: str
    password: str

class Update_User(BaseModel):
    id: int
    username: str
    email: str
    password: str

class ShowUser(BaseModel):
    username: str
    email: str
    
    class Config():
        orm_mode = True

class Login(BaseModel):
    username: str
    password: str
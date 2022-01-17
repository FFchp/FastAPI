from fastapi import FastAPI
import models
from database import engine
import user, authentication
app = FastAPI()

models.Base.metadata.create_all(engine)

app.include_router(user.router)
app.include_router(authentication.router)

# Home
@app.get('/')
def index():
    return {'msg' : 'Hello FastAPI!!'}

from fastapi import FastAPI
import models, user
from database import engine, get_db

app = FastAPI()

models.Base.metadata.create_all(engine)

app.include_router(user.router)

# Home
@app.get('/')
def index():
    return {'msg' : 'Hello FastAPI!!'}

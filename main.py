from os import stat
from threading import stack_size
from fastapi import FastAPI, Depends, responses, status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from starlette.responses import Response
import schemas, models
from database import SessionLocal, engine

app = FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/')
def index():
    return {'msg' : 'Hello FastAPI!!'}

@app.post('/user', status_code = status.HTTP_201_CREATED)
def create(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(id = request.id, name = request.name, email = request.email, password = request.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.delete('/user/{id}', status_code = status.HTTP_204_NO_CONTENT)
def delete(id, db: Session = Depends(get_db)):
    db.query(models.User).filter(models.User.id == id).delete(synchronize_session=False)
    db.commit()
    return 'done'

@app.put('/user/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_id(id, request: schemas.User, db : Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id)
    if not user.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f'User with id {id} not found')
    user.update(request)
    db.commit()
    return 'done'

@app.get('/user')
def querry(db : Session = Depends(get_db)):
    users = db.query(models.User).order_by(models.User.id).all()
    return users

@app.get('/user/{id}', status_code=status.HTTP_200_OK)
def show(id, response : Response, db : Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'detail' : f'blog with the id {id} is not aviavle'}
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f'blog with the id {id} is not aviavle')
    return user

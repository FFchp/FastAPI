from fastapi import FastAPI, Depends, status, Response
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
import schemas, models, api_router
from database import engine, get_db
from hashing import Hash

app = FastAPI()

models.Base.metadata.create_all(engine)

app.include_router(api_router.router)


# Home
@app.get('/')
def index():
    return {'msg' : 'Hello FastAPI!!'}

# Register
@app.post('/user', status_code = status.HTTP_201_CREATED, tags = ['user'])
def create(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(name = request.name, email = request.email, password = Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Delete User
#@app.delete('/user/{id}', status_code = status.HTTP_204_NO_CONTENT, tags = ['user'])
#def delete(id, db: Session = Depends(get_db)):
#    db.query(models.User).filter(models.User.id == id).delete(synchronize_session=False)
#    db.commit()
#    return 'done'

# Update User
@app.put('/user/{id}', status_code=status.HTTP_202_ACCEPTED, tags = ['user'])
def update_id(id, request: schemas.Update_User, db : Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id)
    if not user.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f'User with id {id} not found')
    user.update(request.dict())
    db.commit()
    return 'done'

# Qurry all User
#@app.get('/user', status_code= status.HTTP_200_OK, response_model = schemas.ShowUser, tags = ['user'])
#def querry(db : Session = Depends(get_db)):
#    users = db.query(models.User).order_by(models.User.id).all()
#    return users

# Querry User By id
#@app.get('/user/{id}', status_code=status.HTTP_200_OK, response_model = schemas.ShowUser, tags = ['user'])
#def show(id, response : Response, db : Session = Depends(get_db)):
#    user = db.query(models.User).filter(models.User.id == id).first()
#    if not user:
#        # response.status_code = status.HTTP_404_NOT_FOUND
#        # return {'detail' : f'blog with the id {id} is not aviavle'}
#        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
#                            detail = f'user with the id {id} is not aviable')
#    return user

# 

from fastapi import APIRouter, status, Depends, Response
from fastapi.exceptions import HTTPException
from typing import List
from sqlalchemy.orm import Session
import database, schemas, models
from hashing import Hash

router = APIRouter(
    prefix = '/user',
    tags = ['User']
)

get_db = database.get_db

# Query all User
@router.get('/', status_code= status.HTTP_200_OK, response_model = List[schemas.ShowUser])
def query_all(db : Session = Depends(get_db)):
    users = db.query(models.User).order_by(models.User.id).all()
    return users

# Query User by ID
@router.get('/{id}', status_code=status.HTTP_200_OK, response_model = schemas.ShowUser)
def query_user_by_id(id, response : Response, db : Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'detail' : f'blog with the id {id} is not aviavle'}
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f'user with the id {id} is not aviable')
    return user

# Register
@router.post('/', status_code = status.HTTP_201_CREATED)
def create(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(name = request.name, email = request.email, password = Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# Delete User Ref by ID
@router.delete('/{id}', status_code = status.HTTP_204_NO_CONTENT)
def delete(id, db: Session = Depends(get_db)):
    db.query(models.User).filter(models.User.id == id).delete(synchronize_session=False)
    db.commit()
    return 'done'

# Update User
@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_by_id(id, request: schemas.Update_User, db : Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id)
    if not user.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f'User with id {id} not found')
    user.update(request.dict())
    db.commit()
    return 'done'
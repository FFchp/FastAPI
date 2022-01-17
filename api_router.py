from fastapi import APIRouter, status, Depends, Response
from fastapi.exceptions import HTTPException
from typing import List
import schemas, database, models
from sqlalchemy.orm import Session

router = APIRouter()

get_db = database.get_db

# Query all User
@router.get('/user', status_code= status.HTTP_200_OK, response_model = List[schemas.ShowUser], tags = ['user_router'])
def all(db : Session = Depends(get_db)):
    users = db.query(models.User).order_by(models.User.id).all()
    return users

# Query User by ID
@router.get('/user/{id}', status_code=status.HTTP_200_OK, response_model = schemas.ShowUser, tags = ['user_router'])
def show(id, response : Response, db : Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'detail' : f'blog with the id {id} is not aviavle'}
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f'user with the id {id} is not aviable')
    return user

# Delete User Ref by ID
@router.delete('/user/{id}', status_code = status.HTTP_204_NO_CONTENT, tags = ['user_router'])
def delete(id, db: Session = Depends(get_db)):
    db.query(models.User).filter(models.User.id == id).delete(synchronize_session=False)
    db.commit()
    return 'done'



from fastapi import APIRouter, status, Depends, Response
import schemas, database, models
from sqlalchemy.orm import Session

router = APIRouter()

# Qurry all User
@router.get('/user', status_code= status.HTTP_200_OK, response_model = schemas.ShowUser, tags = ['user'])
def querry(db : Session = Depends(database.get_db)):
    users = db.query(models.User).order_by(models.User.id).all()
    return users
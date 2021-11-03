from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from app import models, schemas, utils
from app.database import get_db

router = APIRouter()


@router.post('/users', status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(data: schemas.UserCreate, db: Session = Depends(get_db)):
    # hash password
    password = utils.hash(data.password)
    data.password = password
    user = models.User(**data.dict())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.get('/users/{pk}', response_model=schemas.UserResponse)
def retrieve_user(pk: int, db: Session = Depends(get_db)):
    # hash password
    user = db.query(models.User).filter(models.User.id == pk).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id:{pk} was not found")
    return user

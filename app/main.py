from typing import List

from fastapi import FastAPI, status, HTTPException, Response, Depends
from sqlalchemy.orm import Session

from app.database import engine, get_db
from . import models, schemas, utils

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "HelloWorld !"}


@app.get("/posts", response_model=List[schemas.Post])
def post_retrieve(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@app.post('/posts', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def post_create(data: schemas.CreatePostSchema, db: Session = Depends(get_db)):
    post = models.Post(**data.dict())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


@app.get('/posts/{pk}', response_model=schemas.Post)
def post_get_post(pk: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == pk).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{pk} was not found")
    return post


@app.delete('/posts/{pk}', status_code=status.HTTP_204_NO_CONTENT)
def post_destroy(pk: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == pk)
    if post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{pk} does not exist")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put('/posts/{pk}', status_code=status.HTTP_202_ACCEPTED, response_model=schemas.Post)
def update(pk: int, data: schemas.CreatePostSchema, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == pk)
    if post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{pk} does not exist")
    post.update(data.dict(), synchronize_session=False)
    db.commit()
    return post.first()


@app.post('/users', status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(data: schemas.UserCreate, db: Session = Depends(get_db)):
    # hash password
    password = utils.hash(data.password)
    data.password = password
    user = models.User(**data.dict())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@app.get('/users/{pk}', response_model=schemas.UserResponse)
def retrieve_user(pk: int, db: Session = Depends(get_db)):
    # hash password
    user = db.query(models.User).filter(models.User.id == pk).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id:{pk} was not found")
    return user

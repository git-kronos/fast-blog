from fastapi import FastAPI, status, HTTPException, Response, Depends
from sqlalchemy.orm import Session

from app.database import engine, get_db
from . import models
from .schemas import CreatePostSchema

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "HelloWorld !"}


@app.get("/posts")
def post_retrieve(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}


@app.post('/posts', status_code=status.HTTP_201_CREATED)
def post_create(data: CreatePostSchema, db: Session = Depends(get_db)):
    post = models.Post(**data.dict())
    db.add(post)
    db.commit()
    db.refresh(post)
    return {"message": "Post created", "data": post}


@app.get('/posts/{pk}')
def post_get_post(pk: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == pk).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id:{pk} was not found")
    return {"data": post}


@app.delete('/posts/{pk}', status_code=status.HTTP_204_NO_CONTENT)
def post_destroy(pk: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == pk)
    if post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id:{pk} does not exist")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put('/posts/{pk}', status_code=status.HTTP_202_ACCEPTED)
def update(pk: int, data: CreatePostSchema, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == pk)
    if post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id:{pk} does not exist")
    post.update(data.dict(), synchronize_session=False)
    db.commit()
    return {"message": "Post Updated", "data": post.first()}

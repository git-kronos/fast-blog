from typing import List

from fastapi import status, HTTPException, Response, Depends, APIRouter
from sqlalchemy.orm import Session

from app import models, schemas, oauth2
from app.database import get_db

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


@router.get("/", response_model=List[schemas.Post])
def post_retrieve(
        db: Session = Depends(get_db),
        current_user: int = Depends(oauth2.get_current_user)
):
    posts = db.query(models.Post).all()
    return posts


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def post_create(
        data: schemas.CreatePostSchema,
        db: Session = Depends(get_db),
        current_user: int = Depends(oauth2.get_current_user)
):
    post = models.Post(**data.dict())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


@router.get('/{pk}', response_model=schemas.Post)
def post_get_post(
        pk: int,
        db: Session = Depends(get_db),
        current_user: int = Depends(oauth2.get_current_user)
):
    post = db.query(models.Post).filter(models.Post.id == pk).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{pk} was not found")
    return post


@router.delete('/{pk}', status_code=status.HTTP_204_NO_CONTENT)
def post_destroy(
        pk: int,
        db: Session = Depends(get_db),
        current_user: int = Depends(oauth2.get_current_user)
):
    post = db.query(models.Post).filter(models.Post.id == pk)
    if post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{pk} does not exist")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{pk}', status_code=status.HTTP_202_ACCEPTED, response_model=schemas.Post)
def update(
        pk: int,
        data: schemas.CreatePostSchema,
        db: Session = Depends(get_db),
        current_user: int = Depends(oauth2.get_current_user)
):
    post = db.query(models.Post).filter(models.Post.id == pk)
    if post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{pk} does not exist")
    post.update(data.dict(), synchronize_session=False)
    db.commit()
    return post.first()

from typing import List

from fastapi import status, HTTPException, Response, Depends, APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import Optional

from app import models, schemas, oauth2
from app.database import get_db

router = APIRouter(
    prefix="/posts",
    tags=['Posts'])

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create(
        data: schemas.CreatePostSchema,
        db: Session = Depends(get_db),
        current_user: int = Depends(oauth2.get_current_user)
):
    post = models.Post(owner_id=current_user.id, **data.dict())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


@router.get("/", response_model=List[schemas.PostOut])
def list_all(
        db: Session = Depends(get_db),
        current_user: int = Depends(oauth2.get_current_user),
        limit: int = 10,
        skip: int = 0,
        search: Optional[str] = ""
):
    object_list = db.query(
        models.Post,
        func.count(models.Vote.post_id).label('votes')
    ).join(
        models.Vote,
        models.Vote.post_id == models.Post.id,
        isouter=True
    ).group_by(models.Post.id).filter(
        models.Post.owner_id == current_user.id,
        models.Post.title.contains(search)
    ).offset(skip).limit(limit).all()

    return object_list


# @router.get('/{pk}', response_model=schemas.Post)
@router.get('/{pk}', response_model=schemas.PostOut)
def retrieve(
        pk: int,
        db: Session = Depends(get_db),
        current_user: int = Depends(oauth2.get_current_user)
):

    obj = db.query(
        models.Post,
        func.count(models.Vote.post_id).label('votes')
    ).join(
        models.Vote,
        models.Vote.post_id == models.Post.id,
        isouter=True
    ).group_by(models.Post.id).filter(models.Post.id == pk).first()

    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{pk} was not found")
    return obj


@router.put('/{pk}', status_code=status.HTTP_202_ACCEPTED, response_model=schemas.Post)
def update(
        pk: int,
        data: schemas.CreatePostSchema,
        db: Session = Depends(get_db),
        current_user: int = Depends(oauth2.get_current_user)
):
    object_list = db.query(models.Post).filter(models.Post.id == pk)
    if object_list.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{pk} does not exist")

    if object_list.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorised access")

    object_list.update(data.dict(), synchronize_session=False)
    db.commit()
    return object_list.first()


@router.delete('/{pk}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(
        pk: int,
        db: Session = Depends(get_db),
        current_user: int = Depends(oauth2.get_current_user)
):
    object_list = db.query(models.Post).filter(models.Post.id == pk)

    if object_list.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{pk} does not exist")

    if object_list.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorised access")

    object_list.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app import oauth2, schemas, database, models

router = APIRouter(
    prefix='/vote',
    tags=['Vote']
)


@router.post('/', status_code=status.HTTP_201_CREATED)
def submit_vote(
        vote: schemas.Vote,
        db: Session = Depends(database.get_db),
        current_user: int = Depends(oauth2.get_current_user)
):
    if not db.query(models.Post).filter(models.Post.id == vote.post_id).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post id {vote.post_id} not found")

    queryset = db.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)

    if vote.dir == 1:
        if queryset.first():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"Vote already submitted on post {vote.post_id}")
        data = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(data)
        db.commit()
        return {'message': 'vote successfully added'}
    else:
        if not queryset.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Vote doesn't exist")
        queryset.delete(synchronize_session=False)
        db.commit()
        return {'message': 'vote successfully deleted'}

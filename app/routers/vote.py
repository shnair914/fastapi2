from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from app.schemas import Vote
from sqlalchemy.orm import Session
from app.database import get_db
from app.oath2 import get_current_user
from app import models

router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: Vote, db: Session = Depends(get_db), get_user: int = Depends(get_current_user)):
    post_exist = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post_exist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {vote.post_id} does not exist")
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == get_user.id)
    found_vote = vote_query.first()
    if(vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {get_user.id} has already voted on the post {vote.post_id}") 
        new_vote = models.Vote(post_id = vote.post_id, user_id = get_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")
        
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "successfully deleted vote"}
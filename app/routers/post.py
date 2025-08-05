from typing import List, Optional
from fastapi import Depends, status, HTTPException
from sqlalchemy.orm import Session, aliased
from app import models
from app.database import get_db
from app.schemas import PostCreate
from app import schemas
from fastapi.routing import APIRouter
from app.oath2 import get_current_user
from sqlalchemy import func

router = APIRouter(
    prefix='/posts',
    tags=["Posts"]
    )

@router.get('/', response_model=List[schemas.Post])
async def get_posts(db: Session = Depends(get_db), get_user: str = Depends(get_current_user), limit: int = 10, skip: int = 0, search: Optional[str]= ""):
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def create_post(post: PostCreate, db: Session = Depends(get_db), get_user: str = Depends(get_current_user)):
    post_dict = post.dict()
    new_post = models.Post(owner_id=get_user.id, **post_dict)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post
   

@router.get('/{id}', response_model=schemas.PostOut)
async def get_post(id: int, db: Session = Depends(get_db), get_user: str = Depends(get_current_user)):
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} was not found")
    return post

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db), get_user: str = Depends(get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} was not found")
    if post.owner_id != get_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post_query.delete(synchronize_session=False)
    db.commit()

@router.put('/{id}', response_model=schemas.Post)
async def update_post(id: int, post: PostCreate, db: Session = Depends(get_db), get_user: str = Depends(get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    a_post = post_query.first()
    if a_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id {id} was not found')
    if a_post.owner_id != get_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
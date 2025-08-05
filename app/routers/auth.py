from fastapi import HTTPException, Depends, APIRouter, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import schemas
from app import models
from app.utilities import verify_password
from app.oath2 import create_access_token
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(tags=["Authentication"])

@router.post('/login', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Invalid Credentials')
    if not verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Invalid Credentials')
    access_token = create_access_token(data={"id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}

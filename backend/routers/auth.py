from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from schemas import schemas
from models import models
from database import database
import utils, oauth2

router = APIRouter()

@router.post("/login", response_model=schemas.Token)
def login(user_credentials: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(user_credentials.username == models.User.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Invalid credentials"
        )
    if not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Invalid credentials"
        )
    access_token = oauth2.create_access_token({"id": user.id})
    return schemas.Token(access_token=access_token, token_type="bearer")

@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    user.password = utils.get_password_hash(user.password)
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# current_user: schemas.UserOut = Depends(oauth2.get_current_user)
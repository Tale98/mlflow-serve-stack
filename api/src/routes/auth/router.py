from fastapi import APIRouter
from schemas.auth.user import UserRegister
from models.auth.user import User, timestamp
from schemas.auth.user import UserLogin, UserRegister, Token
from utils.auth.password import hash_password, verify_password, create_access_token, oauth2_scheme, decode_access_token
from fastapi import Depends, HTTPException, status
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from db.base import get_session
from sqlmodel import Session, select
router = APIRouter()

@router.post("/register")
def register(request: UserRegister, session: Session = Depends(get_session)):
    
    print(timestamp() )
    existing_user = session.exec(select(User).where(User.username == request.username)).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )
    existing_email = session.exec(select(User).where(User.email == request.email)).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    hashed_password = hash_password(request.password)
    new_user = User(username=request.username, email=request.email, hashed_password=hashed_password)
    
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    
    return {"message": f"User {new_user.username} registered successfully"}

@router.post("/token")
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.username == form_data.username)).first()
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user.username})
    return Token(access_token=access_token, token_type="bearer")
@router.get("/users/me")
def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    payload = decode_access_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = session.exec(select(User).where(User.username == payload["sub"])).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return {
        "username": user.username,
    }

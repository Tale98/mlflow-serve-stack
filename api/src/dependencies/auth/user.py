from utils.auth.password import oauth2_scheme, decode_access_token
from db.base import get_session
from fastapi import Depends, HTTPException, status
from models.auth.user import User
from sqlmodel import Session, select
def get_current_user(token: str = Depends(oauth2_scheme), session=Depends(get_session)):
    """
    Dependency to get the current user based on the provided OAuth2 token.
    This function decodes the token and retrieves the user from the database.
    """
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
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
from passlib.context import CryptContext
from typing import Optional
from jose import JWTError, jwt
import datetime
from typing import Optional
import os
from fastapi.security import OAuth2PasswordBearer
# Settings
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_SECONDS = 60*60  # 1 hour

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, seconds=ACCESS_TOKEN_EXPIRE_SECONDS):
    to_encode = data.copy()
    expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=seconds)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
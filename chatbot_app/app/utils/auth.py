from datetime import datetime, timedelta
from fastapi import HTTPException
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.models.user import User
from app.database.connection import get_db
from sqlalchemy.ext.asyncio import AsyncSession
import os

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
# Password hashing utility
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# JWT token generation utility
def create_access_token(data: dict, expires_delta: timedelta = timedelta(hours=1)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, key=SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Dependency to get current user
async def get_current_user(db: AsyncSession, username: str):
    user = await db.execute(f"SELECT * FROM users WHERE username = {username}")
    return user

def verify_token(token: str):
    try:
        # Decode the token and verify the validity
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        return username
    
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
import os
from datetime import datetime, timedelta
from typing import Annotated
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import bcrypt
from jose import JWTError, jwt
from sqlalchemy import select

from auth_server.database.db_config import db_dependency

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

if SECRET_KEY == "your-secret-key-change-this-in-production":
    raise RuntimeError("SECRET_KEY must be set in environment variables for production")


def hash_password(password: str) -> str:
    # Convert password to bytes
    pwd_bytes = password.encode("utf-8")
    # Generate salt and hash
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pwd_bytes, salt)
    # Return as string
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash"""
    # Convert to bytes
    pwd_bytes = plain_password.encode("utf-8")
    hashed_bytes = hashed_password.encode("utf-8")
    # Verify
    return bcrypt.checkpw(pwd_bytes, hashed_bytes)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Create JWT access token"""
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> int:
    """Verify and decode JWT token, returns user_id"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")

        if user_id is None:
            raise credentials_exception

        return int(user_id)

    except JWTError:
        raise credentials_exception


security = HTTPBearer()


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    db: db_dependency,
):
    """Get current authenticated user"""
    from auth_server.models import User

    token = credentials.credentials
    user_id = verify_token(token)

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user"
        )

    return user


# Type annotation for dependency injection
current_user_dependency = Annotated[object, Depends(get_current_user)]

from typing import Dict, Union, NoReturn
from datetime import datetime, timedelta
from pydantic import BaseModel

from jose import JWTError, jwt
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer

from app import schemas, models
from app.core.config import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Creates JWT access token
def create_jwt_token(content: Dict[str, str], expires_delta: timedelta) -> str:
    """
    content: {"sub": "username"}
    secret_key: for signing JWT
    expires_delta: lifetime of token
    """
    to_encode = content.copy()
    expire = datetime.utcnow() + expires_delta  # calculate expire time
    to_encode.update({"exp": expire})  # add expiration to JWT payload
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


# Creates JWT access token for given user
def create_user_access_token(user: schemas.User) -> str:
    return create_jwt_token(
        content={"sub": user.username},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRES_MINUTES)
    )


# Decrypt username from JWT access token
async def get_current_user(token: str = Depends(oauth2_scheme)) -> Union[schemas.User, NoReturn]:

    # Define HTTP exception for JWT
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    
    # Try to decode JWT and extract username from payload
    try:
        payload = jwt.decode(token, settings.SECRET_KEY)
        if (username := payload.get("sub")) is None:  # invalid access token
            raise credentials_exception

    except JWTError:  # invalid access token
        raise credentials_exception

    # Verify user with username: username exists in DB
    user = await models.User.get_or_none(username=username)
    if user is None:
        raise credentials_exception

    return schemas.User.from_orm(user)
    
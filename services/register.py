from fastapi import HTTPException, status
from typing import Union, NoReturn

from app import schemas, models
from app.core.security import get_password_hash


async def check_email_is_taken(email: str) -> bool:
    email = email.lower()
    return await models.User.filter(email=email).exists()


async def check_username_is_taken(username: str) -> bool:
    return await models.User.filter(username=username).exists()


async def register_user(new_user: schemas.UserCreate) -> Union[schemas.User, NoReturn]:
    
    # Check registering user's email not associated with another account
    user_exists = await check_email_is_taken(new_user.email)
    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="an account is already registered with this email"
        )

    # Check registering user's username not associated with another account
    user_exists = await check_username_is_taken(new_user.username)
    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="this username is not available"
        )
    
    # Hash plain-text password
    hashed_password = get_password_hash(new_user.password)

    # Force email to all lowercase for DB
    new_user.email = new_user.email.lower()

    # Create new user in DB
    user = await models.User.create(
        **new_user.dict(),
        hashed_password=hashed_password
    )

    return schemas.User.from_orm(user)

    
from typing import Union

from app import schemas, models
from app.core.security import verify_password

async def authenticate_user(
    username: str, 
    password: str
) -> Union[schemas.User, bool]:
    """
    Validates user with username: username exists in DB. Then validates the hash
    of the plain-text password matches the password hash in DB.
    """

    # Check is user with given username exists in DB
    user = await models.User.get_or_none(username=username)
    if user is None:
        return False

    # Check hash of password matches hashed password in DB
    if not verify_password(password, user.hashed_password):
        return False

    return schemas.User.from_orm(user)



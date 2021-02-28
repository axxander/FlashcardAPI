from typing import List

from fastapi import APIRouter, HTTPException, status

from app import schemas, models


router = APIRouter(
    prefix="/admin",
    tags=["admin"]
)


# Get all users
@router.get("/user", response_model=List[schemas.User])
async def get_users() -> List[schemas.User]:

    # fetch all users
    users = await models.User.all()
    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="no users are registered"
        )
    return [
        *map(
            lambda user: schemas.User.from_orm(user),
            users
        )
    ]


# Get specific user
@router.get("/user/{user_id}", response_model=schemas.User)
async def get_user(user_id: int) -> schemas.User:

    # fetch user
    user = await models.User.get_or_none(id=user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"flashcard does not exist"
        )
    
    return schemas.User.from_orm(user)
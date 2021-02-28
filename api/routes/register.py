from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from app import schemas, models
from app.services.register import register_user


router = APIRouter(
    prefix="/register",
    tags=["register"]
)

# Register new user
@router.post("/", response_model=schemas.User)
async def registration(
    form_data: schemas.RegistrationRequestForm = Depends()
) -> schemas.User:

    # Create UserCreat instance with form data
    new_user = schemas.UserCreate(
        **form_data.dict()
    )

    # Register new user
    user = await register_user(new_user)
    
    return schemas.User.from_orm(user)


    
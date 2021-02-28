from datetime import datetime, timedelta
from typing import Dict

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app import schemas
from app.services.authentication import authenticate_user
from app.services.jwt import create_user_access_token


router = APIRouter(
    tags=["authentication"]
)


# Endpoint for requesting access token
@router.post("/token", response_model=schemas.JWT)
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> Dict[str, str]:

    # Authenticate username and password
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token = create_user_access_token(
        user=user
    )

    return {"access_token": access_token, "token_type": "bearer"}
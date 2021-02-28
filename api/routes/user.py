from fastapi import APIRouter, Depends, HTTPException, status

from app import schemas, models
from app.services.jwt import get_current_user
from app.core.security import verify_password, get_password_hash


router = APIRouter(
    prefix="/user",
    tags=["user"]
)

# Update user details 
@router.put("/", response_model=schemas.User)
async def update_user_details(
    update_data: schemas.UserUpdate, 
    user: schemas.User = Depends(get_current_user)
) -> schemas.User:

    # Update user
    await models.User.filter(id=user.id).update(
        **update_data.dict()
    )

    # Return full user details
    return schemas.User.from_orm(
        await models.User.filter(id=user.id).get()
    )

# Update password
@router.patch("/password", response_model=int)
async def update_password(
    update: schemas.UserUpdatePassword,
    user: schemas.User = Depends(get_current_user)
) -> int:
    
    # Verify current password hash matches stored password hash
    userDB = await models.User.filter(id=user.id).get()
    verify = verify_password(
        update.current_password,
        userDB.hashed_password
    )
    if not verify:  # passwords don't match
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="password is incorrect"
        )

    # Confirm new password and confirm password match
    if update.new_password != update.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="new password does not match confirmed password"
        )

    # Store hash of new password in DB
    await models.User.filter(id=user.id).update(
        hashed_password=get_password_hash(update.new_password)
    )

    return status.HTTP_204_NO_CONTENT
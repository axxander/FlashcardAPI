from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from app import schemas, models
from app.services.jwt import get_current_user


router = APIRouter(
    prefix="/flashcard",
    tags=["flashcard"]
)


# Create new flashcard
@router.post("/", response_model=schemas.Flashcard)
async def create_flashcard(
    new_flashcard: schemas.FlashcardCreate, 
    user: schemas.User = Depends(get_current_user)
) -> schemas.Flashcard:
    
    # Create flashcard in DB with FK of user id
    flashcard = await models.Flashcard.create(
        **new_flashcard.dict(),
        user=await models.User.filter(id=user.id).get()
    )
    
    return schemas.Flashcard.from_orm(flashcard)


# List all flashcards
@router.get("/", response_model=List[schemas.Flashcard])
async def get_flashcards(
    user: schemas.User = Depends(get_current_user)
) -> List[schemas.Flashcard]:

    # Fetch user's flashcards
    flashcards = await models.Flashcard.filter(user_id=user.id)

    return [
        *map(
            lambda flashcard: schemas.Flashcard.from_orm(flashcard),
            flashcards
        )
    ]


# Get flashcards of specific category
@router.get("/{category}", response_model=List[schemas.Flashcard])
async def get_flashcards_specific_category(
    category: str, 
    user: schemas.User = Depends(get_current_user)
) -> List[schemas.Flashcard]:
    
    # Fetch user's flashcards with category: category
    flashcards = await models.Flashcard.filter(user_id=user.id, category=category)
    if not flashcards:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"the category '{category}' does not exist"
        )

    return [
        *map(
            lambda flashcard: schemas.Flashcard.from_orm(flashcard),
            flashcards
        )
    ]


# Get flashcard by ID
@router.get("/id/{flashcard_id}", response_model=schemas.Flashcard)
async def get_flashcard_by_id(
    flashcard_id: int, 
    user: schemas.User = Depends(get_current_user)
) -> schemas.Flashcard:

    # Fetch user's flashcard with flashcard ID: flashcard_id
    flashcard = await models.Flashcard.get_or_none(id=flashcard_id, user_id=user.id)
    if flashcard is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"flashcard does not exist"
        )

    return schemas.Flashcard.from_orm(flashcard)


# Update flashcard by ID
@router.put("/id/{flashcard_id}", response_model=schemas.Flashcard)
async def update_flashcard_by_id(
    flashcard_id: int, 
    updated_flashcard: schemas.FlashcardCreate, 
    user: schemas.User = Depends(get_current_user)
) -> schemas.Flashcard:

    # Update user's flashcard with flashcard ID: flashcard_id
    updated = await models.Flashcard.filter(id=flashcard_id, user_id=user.id).update(
        **updated_flashcard.dict()
    )
    if not updated:  # flashcard with ID: flashcard_id does not exist
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"flashcard does not exist"
        )
      
    return schemas.Flashcard.from_orm(
        await models.Flashcard.filter(
            id=flashcard_id,
            user_id=user.id
        ).get()
    )
    

# Bulk change category name
@router.put("/{category}", response_model=schemas.RenameFlashcardCategory)
async def update_category_name(
    category: str,
    new_category_name: str,
    user: schemas.User = Depends(get_current_user)
) -> schemas.RenameFlashcardCategory:
    
    # Update category name for user's set of flashcards
    updated = await models.Flashcard.filter(user_id=user.id, category=category).update(
        category=new_category_name
    )
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"category does not exist"
        )
    
    return schemas.RenameFlashcardCategory(
        current_category_name=category,
        new_category_name=new_category_name
    )


# Delete flashcard by ID
@router.delete("/id/{flashcard_id}", response_model=int)
async def delete_flashcard_by_id(
    flashcard_id: int, 
    user: schemas.User = Depends(get_current_user)
) -> int:

    # Delete flashcard with flashcard ID: flashcard_id
    await models.Flashcard.filter(id=flashcard_id, user_id=user.id).delete()
      
    return status.HTTP_204_NO_CONTENT


# Delete flashcard by category
@router.delete("/{category}", response_model=int)
async def delete_flashcards_by_category(
    category: str,
    user: schemas.User = Depends(get_current_user)
) -> int:
    
    # Delete all flashcards with category: category
    await models.Flashcard.filter(category=category, user_id=user.id).delete()

    return status.HTTP_204_NO_CONTENT
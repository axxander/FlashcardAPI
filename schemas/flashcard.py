from pydantic import BaseModel

# Shared properties
class FlashcardBase(BaseModel):
    category: str
    question: str
    answer: str

# Properties to recieve via API on creation
class FlashcardCreate(FlashcardBase):
    pass

class FlashcardInDBBase(FlashcardBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True

# Properties to return via API
class Flashcard(FlashcardInDBBase):
    pass


# Properties to recieve via API when changing flashcard category name
class RenameFlashcardCategory(BaseModel):
    current_category_name: str
    new_category_name: str
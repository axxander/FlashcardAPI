from pydantic import BaseModel, EmailStr
from fastapi import Form


# User registration form
class RegistrationRequestForm(BaseModel):
    firstname: str = Form(...)
    surname: str = Form(...)
    email: str = Form(...)
    username: str = Form(...)
    password: str = Form(...)


# Shared properties
class UserBase(BaseModel):
    firstname: str
    surname: str
    email: EmailStr


# Semi-shared properties
class UserUsername(BaseModel):
    username: str


# Properties to recieve via API on updating user details
class UserUpdate(UserBase):
    pass


# Properties to recieve via API on creation/registration
class UserCreate(UserBase, UserUsername):
    password: str


class UserInDBBase(UserBase, UserUsername):
    id: int

    class Config:
        orm_mode = True


# Properties to return via API
class User(UserInDBBase):
    pass


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password = True


# Properties to recieve via API on updating user password
class UserUpdatePassword(BaseModel):
    current_password: str
    new_password: str
    confirm_password: str
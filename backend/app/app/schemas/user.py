from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, validator


# Shared properties
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    nickname: Optional[str] = None

    @validator("nickname")
    def nickname_alphanumeric(cls, v):
        assert v.isalnum(), "must be alphanumeric"
        return v

    @validator("nickname")
    def nickname_length(cls, v):
        assert 3 <= len(v) <= 20, "must be between 3 and 20 characters"
        return v


# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr
    nickname: str
    password: str


# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None


class UserInDBBase(UserBase):
    id: Optional[int] = None
    date_joined: datetime
    email_verified: bool = False
    is_active: Optional[bool] = True
    is_superuser: bool = False

    class Config:
        orm_mode = True


# Additional properties to return via API
class User(UserInDBBase):
    pass


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str

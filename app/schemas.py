from datetime import datetime
from pydantic import BaseModel, EmailStr

from app.models import Base


# Base entity class for posts
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


# Base entity class for users
class UserBase(BaseModel):
    email: EmailStr


# Entity class for post creation and updation
class PostCreate(PostBase):
    pass


# Entity class for post response for APIs
class PostResponse(PostBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Entity class for user creation
class UserCreate(UserBase):
    password: str


# Entity class for user response for APIs
class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

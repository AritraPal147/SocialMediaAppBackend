from datetime import datetime
from pydantic import BaseModel

from app.models import Base


# Base entity class for posts
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


# Entity class for post creation and updation
class PostCreate(PostBase):
    pass


class PostResponse(PostBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

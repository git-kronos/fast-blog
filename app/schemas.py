from pydantic import BaseModel
from datetime import datetime


# schemas
class PostBaseSchema(BaseModel):
    title: str
    content: str
    is_published: bool


class CreatePostSchema(PostBaseSchema):
    is_published: bool = True


class Post(PostBaseSchema):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

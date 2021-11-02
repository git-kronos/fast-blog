from pydantic import BaseModel
from typing import Optional


# schemas
class PostSchema(BaseModel):
    title: str
    content: str
    is_published: bool = True
    rating: Optional[int] = None

from pydantic import BaseModel


# schemas
class PostBaseSchema(BaseModel):
    title: str
    content: str
    is_published: bool = True


class CreatePostSchema(PostBaseSchema):
    pass

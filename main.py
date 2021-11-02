from random import randrange

from fastapi import FastAPI, status, HTTPException

from schemas import PostSchema
from utils import find_post, my_post, ResponseMessage

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "HelloWorld !"}


@app.get("/posts")
def get_post():
    return {"data": my_post}


@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_posts(post: PostSchema):
    post_dict = post.dict()
    post_dict["id"] = randrange(0, 1000000000)
    my_post.append(post_dict)
    return {"message": ResponseMessage.post, "data": post_dict}


@app.get('/posts/{pk}')
def get_post(pk: int):
    post = find_post(pk)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id:{pk} was not found")
    return {"message": ResponseMessage.post, "data": post}

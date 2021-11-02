from random import randrange

from fastapi import FastAPI, status, HTTPException, Response

from .schemas import PostSchema
from .utils import (
    find_post,
    my_post,
    find_index_post
)

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
    return {"message": "Post created", "data": post_dict}


@app.get('/posts/{pk}')
def get_post(pk: int):
    post = find_post(pk)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id:{pk} was not found")
    return {"data": post}


@app.delete('/posts/{pk}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(pk: int):
    index = find_index_post(pk)
    my_post.pop(index)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id:{pk} does not exist")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put('/posts/{pk}', status_code=status.HTTP_202_ACCEPTED)
def update_post(pk: int, data: PostSchema):
    index = find_index_post(pk)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id:{pk} does not exist")
    post_dict = data.dict()
    post_dict['id'] = pk
    my_post[index] = post_dict
    return {"message": "Post Updated", "data": post_dict}

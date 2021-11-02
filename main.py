from fastapi import FastAPI
from schemas import PostSchema
from random import randrange

app = FastAPI()

message = {
    "post": "Created",
    "put": "Updated",
    "delete": "Deleted",
}

my_post = [
    {'id': 1, 'title': "Title 1", 'content': "Content 1"},
    {'id': 2, 'title': "Title 2", 'content': "Content 2"},
]


@app.get("/")
async def root():
    return {"message": "HelloWorld !"}


@app.get("/posts")
def get_post():
    return {"data": my_post}


@app.post('/posts')
def create_posts(post: PostSchema):
    post_dict = post.dict()
    post_dict["id"] = randrange(0, 1000000000)
    my_post.append(post_dict)
    return {"message": message["post"], "data": post_dict}

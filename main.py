from fastapi import FastAPI
from schemas import PostSchema

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "HelloWorld !"}


@app.get("/posts")
def get_post():
    return {"data": "Post Data"}


@app.post('/create-posts')
def create_posts(payload: PostSchema):
    print(payload.title)
    print(payload.content)
    print(payload.dict())
    return payload

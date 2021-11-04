from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import posts, users, base, auth, votes

# from app import models
# from app.database import engine

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# fetch('http://127.0.0.1:8000/').then(res => res.json()).then(console.log)
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(base.router)
app.include_router(posts.router)
app.include_router(users.router)
app.include_router(votes.router)

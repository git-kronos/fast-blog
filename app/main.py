from fastapi import FastAPI

from app.routers import posts, users, base, auth, votes

# from app import models
# from app.database import engine

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)
app.include_router(base.router)
app.include_router(posts.router)
app.include_router(users.router)
app.include_router(votes.router)

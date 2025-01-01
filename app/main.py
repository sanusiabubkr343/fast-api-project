from fastapi import FastAPI
from .database import engine
from .models import post, user

from app.routers.auth import router as AuthRouters
from app.routers.post import router as PostRouter


# create table
post.Base.metadata.create_all(bind=engine)
user.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(AuthRouters, prefix="/api/v1/auth")
app.include_router(PostRouter, prefix="/api/v1/posts")

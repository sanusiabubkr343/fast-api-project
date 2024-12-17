from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from app.routers import auth, post
from app.database import TORTOISE_ORM


app =FastAPI()

app.include_router(auth.router,prefix="/api/v1/auth")
app.include_router(post.router, prefix="/api/v1/posts")


register_tortoise(app,config=TORTOISE_ORM,generate_schemas=True)

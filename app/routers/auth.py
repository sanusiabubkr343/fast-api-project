from fastapi import APIRouter, HTTPException, Depends
from app.schemas.user import UserCreate, UserResponse
from app.models.user import User
from app.utils.auth import hash_password, verify_password, create_access_token
from tortoise.exceptions import DoesNotExist


router = APIRouter()


@router.post("/register/",response_model=UserResponse)
async def register(user:UserCreate):
    hashed_password = hash_password(user.password)
    user_obj = await User.create(username=user.username, hashed_password=hashed_password)
    return user_obj

@router.post("/login/")
async def login(user:UserCreate):
    try:
        db_user = await User.get(username=user.username)
    except DoesNotExist:
        raise HTTPException(status_code=401, detail="Authentication Failed")

    if not verify_password(user.password,db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Authentication Failed")
    
    access_token = create_access_token({"sub":db_user.username})
    return  {"access_token": access_token, "token_type": "bearer"}

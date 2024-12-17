from fastapi import APIRouter, HTTPException, Depends
from app.schemas.user import UserCreate, UserResponse
from app.models.user import User
from app.utils.auth import hash_password, verify_password, create_access_token
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from sqlalchemy.future import select

router = APIRouter()


@router.post("/register/",response_model=UserResponse)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    hashed_password = hash_password(user.password)
    new_user = User(username=user.username, password=hashed_password)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


@router.post("/login/")
async def login(user: UserCreate, db: AsyncSession = Depends(get_db)):

    result = await db.execute(select(User).where(User.username==user.username))
    db_user = result.scalars().first()

    if not db_user and verify_password(user.password,db_user.password):
        raise HTTPException(status_code=401, detail="Authentication Failed")

    access_token = create_access_token({"sub": db_user.username, "role": db_user})
    return  {"access_token": access_token, "token_type": "bearer"}

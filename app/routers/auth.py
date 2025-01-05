from fastapi import APIRouter, HTTPException, Depends, Query
from app.schemas.user import Login, PaginatedUserResponse, UserCreate, UserResponse, UserRole
from app.models.user import User
from app.utils.auth import hash_password, verify_password, create_access_token
from app.database import get_db
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from app.utils.pagination import PaginationMeta, paginate


router = APIRouter()


@router.post("/register/",response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already exisit")
    hashed_password = hash_password(user.password)
    new_user = User(username=user.username, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login/", response_model=dict)
def login(user: Login, db: Session = Depends(get_db)):

    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Authentication Failed")

    user_response = UserResponse.from_orm(db_user)
    access_token = create_access_token({"sub": db_user.username, "role": db_user.role.value})
    return {"access_token": access_token, "token_type": "Bearer", **user_response.dict()}


@router.get("/users/", response_model=PaginatedUserResponse)
def get_all_users(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
):
    # Query to fetch all users with optional filtering
    query = db.query(User).order_by(User.created_at.desc())
    paginated_users = paginate(query, page, page_size)

    # Return paginated response
    return PaginatedUserResponse(
        meta=PaginationMeta(
            current_page=paginated_users["current_page_number"],
            total_pages=paginated_users["total_page_number"],
            total_results=paginated_users["total_result"],
        ),
        users=paginated_users["data"],
    )


@router.get("/users/{user_id}/", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(404, "User not found")

    return user


@router.patch("/users/{user_id}/", response_model=UserResponse)
def update_user_role(user_id: int, role: UserRole, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(404, "User not found")
    user.role = role
    db.commit()
    db.refresh(user)
    return user


@router.delete("/users/{user_id}/", status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(404, "User not found")
    db.delete(user)
    db.commit()
    return {"detail": "user deleted successfully"}

from pydantic import BaseModel
from datetime import datetime
import enum


class UserRole(str, enum.Enum):
    admin = "admin"
    regular = "regular"


class UserCreate(BaseModel):
    username: str
    password: str
    role: UserRole


class UserResponse(BaseModel):
    id: int
    username: str
    created_at: datetime

    class Config:
        from_attributes = True

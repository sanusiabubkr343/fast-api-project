from typing import ClassVar
from pydantic import BaseModel, field_validator, ValidationError
from datetime import datetime
import enum
from sqlalchemy.orm import Session

from app.models.user import User

class UserRole(str, enum.Enum):
    admin = "admin"
    regular = "regular"


class UserCreate(BaseModel):
    username: str
    password: str
    role: UserRole


class Login(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    role: UserRole
    created_at: datetime

    class Config:
        from_attributes = True

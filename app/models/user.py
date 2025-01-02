from sqlalchemy import (
    Column,
    Integer,
    String,
    Enum,
    DateTime,
    Text,
    ForeignKey,
    func,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.database import Base


class UserRole(enum.Enum):
    admin = "admin"
    regular = "regular"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(128), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.regular, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)

    posts = relationship("Post", back_populates="author", cascade="all,delete")
    comments = relationship("Comment", back_populates="author", cascade="all,delete")
    votes = relationship("Vote", back_populates="user", cascade="all,delete")

    def __repr__(self):
        return f"<User(username='{self.username}', role='{self.role}')>"

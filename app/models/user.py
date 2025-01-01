from sqlalchemy import Column, Integer, String, Enum
import enum
from sqlalchemy.orm import relationship
from app.database import Base

class UserRole(enum.Enum):
    admin = "admin"
    regular = "regular"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.regular)

    posts = relationship("Post", back_populates="author")
    comments = relationship("Comment", back_populates="author")
    votes = relationship("vote", back_populates="user")

    def __repr__(self):
        return f"<User(username='{self.username}', role='{self.role}')>"

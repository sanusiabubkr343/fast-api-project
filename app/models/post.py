from sqlalchemy import Integer, Column, String, Text, ForeignKey, DateTime, func
from app.models.base import Base
from sqlalchemy.orm import relationship

USER_TABLE_REFERENCE = "users.id"
POST_TABLE_REFERENCE = "posts.id"


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
    author_id = Column(Integer, ForeignKey(USER_TABLE_REFERENCE), nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    author = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post", cascade="all,delete")
    votes = relationship("Vote", back_populates="post", cascade="all,delete")


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    post_id = Column(Integer, ForeignKey(POST_TABLE_REFERENCE), nullable=False)
    author_id = Column(Integer, ForeignKey(USER_TABLE_REFERENCE), nullable=False)
    created_at = Column(DateTime, default=func.now())

    post = relationship("Post", back_populates="comments")
    author = relationship("User", back_populates="comments")


# Vote Model
class Vote(Base):
    __tablename__ = "votes"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey(POST_TABLE_REFERENCE), nullable=False)
    user_id = Column(Integer, ForeignKey(USER_TABLE_REFERENCE), nullable=False)

    post = relationship("Post", back_populates="votes")
    user = relationship("User", back_populates="votes")

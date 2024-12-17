from datetime import datetime
from  pydantic import BaseModel
from enum import Enum

from app.schemas.user import UserResponse

class PostCreate(BaseModel):
    title: str
    content: str


class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    author_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class CommentCreate(BaseModel):
    content: str


class CommentRespond(BaseModel):
    id: int
    content: str
    author_id: int
    created_at: datetime


class VoteAction(str, Enum):
    vote = "vote"
    vote = "vote"


class VoteAction(BaseModel):
    post_id: int
    action: VoteAction


class VoteResponse(BaseModel):
    post_id: int
    user_id: int
    message: str


class PostWithCommentsandVoteDetail(BaseModel):

    id: int
    title: str
    content: str
    author_id: int
    author: UserResponse
    comments: list[CommentRespond]
    votes: list[VoteResponse]
    vote_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

from datetime import datetime
from pydantic import BaseModel
from enum import Enum
from typing import List

from app.schemas.user import UserResponse
from app.utils.pagination import PaginationMeta


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
        from_attributes = True


class PaginatedPostResponse(BaseModel):
    posts: List[PostResponse]
    meta: PaginationMeta


class CommentCreate(BaseModel):
    content: str


class CommentRespond(BaseModel):
    id: int
    content: str
    author_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class PaginatedCommentResponse(BaseModel):
    comments: List[CommentRespond]
    meta: PaginationMeta


class VoteAction(str, Enum):
    vote = "vote"
    unvote = "unvote"


class VoteAction(BaseModel):
    post_id: int
    action: VoteAction


class VoteResponse(BaseModel):
    post_id: int
    user_id: int


class PostWithCommentsandVoteDetail(BaseModel):

    id: int
    title: str
    content: str
    author: UserResponse
    comments: list[CommentRespond]
    votes: list[VoteResponse]
    vote_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

from datetime import datetime
from  pydantic import BaseModel

class PostCreate(BaseModel):
  title:str
  content :str

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
    content :str


class CommentRespond(BaseModel):
    id: int
    content: str
    author_id: int
    created_at: datetime
   


class PostComprehensiveResponse(BaseModel):
    id: int
    title: str
    content: str
    author_id: int
    votes_count: int  #
    comments:list[CommentRespond]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class VoteResponse(BaseModel):
    post_id: int
    user_id: int
    message:str


# Schema for the voting action (request)
class VoteAction(BaseModel):
    post_id: int
    action: str  # Can be "vote" or "unvote"

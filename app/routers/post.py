from fastapi import APIRouter, Depends, HTTPException, Query, requests
from app.schemas.post import (
    PostCreate,
    PostResponse,
    CommentCreate,
    CommentRespond,
    VoteAction,
    VoteResponse,
    PostWithCommentsandVoteDetail,
)
from app.models.post import Post, Comment, Vote
from app.utils.auth import decode_access_token, get_current_user
from app.models.user import User
from app.permission import is_admin
from app.database import get_db
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from app.utils.pagination import paginate
from sqlalchemy.orm import selectinload, joinedload

router = APIRouter()


@router.post("/create/", response_model=PostResponse)
def create_post(
    post: PostCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    post_obj = Post(title=post.title, content=post.content, author=user)

    db.add(post_obj)
    db.commit()
    db.refresh(post_obj)
    return post_obj


@router.get("/my-posts/", response_model=list[PostResponse])
def list_user_posts(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    posts = db.query(Post).filter(Post.author_id == user.id).all()

    return posts


@router.get("/list-all/", response_model=list[PostResponse])
def list_post(
    has_permission=Depends(is_admin),
    db: Session = Depends(get_db),
):
    posts = db.query(Post).all()
    return posts


@router.get("/{post_id}/detail/", response_model=PostWithCommentsandVoteDetail)
def get_comprehensive_post(
    post_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    post = (
        db.query(Post)
        .filter(Post.id == post_id)
        .options(joinedload(Post.author), selectinload(Post.comments), selectinload(Post.votes))
        .first()
    )

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    vote_count = len(post.votes)

    return {
        "id": post.id,
        "title": post.title,
        "content": post.content,
        "author": post.author,
        "comments": post.comments,
        "votes": post.votes,
        "vote_count": vote_count,
        "created_at": post.created_at,
        "updated_at": post.updated_at,
    }


@router.put("/{post_id}/", response_model=PostResponse)
def update_post(
    post_id: int,
    updated_data: PostCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    post = db.query(Post).filter(Post.id == post_id, Post.author_id == user.id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found or unauthorized")

    post.title = updated_data.title

    post.content = updated_data.content

    db.commit()
    db.refresh(post)

    return post


@router.delete("/{post_id}/", response_model=dict)
def delete_post(
    post_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    post = db.query(Post).filter(Post.id == post_id).first()
    db.delete(post)
    db.commit()
    return {"detail": "post deleted successfully"}


@router.post("/vote/", response_model=VoteResponse)
async def vote_action(
    vote: VoteAction, db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    query = select(Post).where(Post.id == vote.post_id)
    result = await db.execute(query)
    post = result.scalars().first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    existing_vote = await db.execute(
        select(Vote).where(Vote.post_id == post.id, Vote.user_id == user.id)
    )
    existing_vote = existing_vote.scalars().first()

    if vote.action == "vote":
        if existing_vote:
            raise HTTPException(status_code=400, detail="You have already voted")
        new_vote = Vote(post_id=post.id, user_id=user.id)
        db.add(new_vote)
        await db.commit()
        return {"post_id": post.id, "user_id": user.id, "message": "voted successfully"}

    elif vote.action == "unvote":
        if not existing_vote:
            raise HTTPException(status_code=400, detail="No vote to remove")
        await db.delete(existing_vote)
        await db.commit()
        return {"post_id": post.id, "user_id": user.id, "message": "unvoted successfully"}


# Add a comment to a post
@router.post("/{post_id}/comments/", response_model=dict)
async def comment_on_post(
    post_id: int,
    comment: CommentCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    result = await db.execute(select(Post).where(Post.id == post_id))
    post = result.scalar_one_or_none()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    new_comment = Comment(content=comment.content, post_id=post.id, author_id=user.id)
    db.add(new_comment)
    await db.commit()
    return {"detail": "Comment added successfully"}


# List comments for a specific post
@router.get("/{post_id}/comments/", response_model=list[CommentRespond])
async def list_comments(post_id: int, db: Session = Depends(get_db)):

    result = await db.execute(select(Post).where(Post.id == post_id))
    post = result.scalar_one_or_none()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    result = await db.execute(
        select(Comment).where(Comment.post_id == post_id).options(joinedload(Comment.author))
    )
    comments = result.scalars().all()

    return [
        {
            "id": comment.id,
            "content": comment.content,
            "author": comment.author.id,
            "created_at": comment.created_at,
        }
        for comment in comments
    ]


# Update a comment
@router.put("/comments/{comment_id}/", response_model=CommentRespond)
async def update_comment(
    comment_id: int,
    updated_comment: CommentCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    result = await db.execute(
        select(Comment).where(Comment.id == comment_id, Comment.author_id == user.id)
    )
    comment = result.scalar_one_or_none()

    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found or unauthorized")

    comment.content = updated_comment.content
    await db.commit()
    return comment


@router.delete("/comments/{comment_id}/", response_model=dict)
async def delete_comment(
    comment_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    # Fetch the comment and check ownership
    result =  db.execute(
        select(Comment).where(Comment.id == comment_id, Comment.author_id == user.id)
    )
    comment = result.scalar_one_or_none()

    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found for the user")

    await db.delete(comment)
    await db.commit()
    return {"detail": "Comment deleted successfully"}

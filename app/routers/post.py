from fastapi import APIRouter, Depends, HTTPException, Query, requests
from app.schemas.post import (
    PaginatedCommentResponse,
    PaginatedPostResponse,
    PaginationMeta,
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


@router.get("/my-posts/", response_model=PaginatedPostResponse)
def list_user_posts(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
):
    query = db.query(Post).filter(Post.author_id == user.id).order_by(Post.updated_at.desc())
    paginated_posts = paginate(query, page, page_size)

    return PaginatedPostResponse(
        meta=PaginationMeta(
            current_page=paginated_posts["current_page_number"],
            total_pages=paginated_posts["total_page_number"],
            total_results=paginated_posts["total_result"],
        ),
        posts=paginated_posts["data"],
    )


@router.get("/list-all/", response_model=PaginatedPostResponse)
def list_post(
    has_permission=Depends(is_admin),
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
):
    # Query all posts
    query = db.query(Post).order_by(Post.updated_at.desc())
    paginated_posts = paginate(query, page, page_size)

    # Return paginated data
    return PaginatedPostResponse(
        meta=PaginationMeta(
            current_page=paginated_posts["current_page_number"],
            total_pages=paginated_posts["total_page_number"],
            total_results=paginated_posts["total_result"],
        ),
        posts=paginated_posts["data"],
    )


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
    print(post)

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
def vote_action(
    vote: VoteAction, db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    post = db.query(Post).filter(Post.id == vote.post_id).first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    existing_vote = db.query(Vote).filter(Vote.post_id == post.id, Vote.user_id == user.id).first()

    if vote.action == "vote":
        if existing_vote:
            raise HTTPException(status_code=400, detail="You have already voted")
        new_vote = Vote(post_id=post.id, user_id=user.id)
        db.add(new_vote)
        db.commit()
        return {"post_id": post.id, "user_id": user.id, "message": "voted successfully"}

    elif vote.action == "unvote":
        if not existing_vote:
            raise HTTPException(status_code=400, detail="No vote to remove")
        db.delete(existing_vote)
        db.commit()
        return {"post_id": post.id, "user_id": user.id, "message": "unvoted successfully"}


# Add a comment to a post
@router.post("/{post_id}/comments/", response_model=dict)
def comment_on_post(
    post_id: int,
    comment: CommentCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    post = db.query(Post).filter(Post.id == post_id).first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    new_comment = Comment(content=comment.content, post_id=post.id, author_id=user.id)
    db.add(new_comment)
    db.commit()
    return {"detail": "Comment added successfully"}


# List comments for a specific post
@router.get("/{post_id}/comments/", response_model=PaginatedCommentResponse)
def list_comments(
    post_id: int,
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    query = db.query(Comment).filter(Comment.post_id == post_id).order_by(Comment.created_at.desc())
    paginated_comments = paginate(query, page, page_size)

    return PaginatedCommentResponse(
        meta=PaginationMeta(
            current_page=paginated_comments["current_page_number"],
            total_pages=paginated_comments["total_page_number"],
            total_results=paginated_comments["total_result"],
        ),
        comments=paginated_comments["data"],
    )


# Update a comment
@router.put("/comments/{comment_id}/", response_model=CommentRespond)
def update_comment(
    comment_id: int,
    updated_comment: CommentCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    comment = (
        db.query(Comment).filter(Comment.id == comment_id, Comment.author_id == user.id).first()
    )

    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found or unauthorized")

    comment.content = updated_comment.content
    db.commit()
    return comment


@router.delete("/comments/{comment_id}/", response_model=dict)
def delete_comment(
    comment_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    # Fetch the comment and check ownership
    comment = (
        db.query(Comment).filter(Comment.id == comment_id, Comment.author_id == user.id).first()
    )

    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found for the user")

    db.delete(comment)
    db.commit()
    return {"detail": "Comment deleted successfully"}

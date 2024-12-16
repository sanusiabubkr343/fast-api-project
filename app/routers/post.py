from fastapi import APIRouter, Depends, HTTPException
from app.schemas.post import (
    CommentRespond,
    PostComprehensiveResponse,
    PostCreate,
    PostResponse,
    CommentCreate,
    VoteAction,
    VoteResponse,
)
from app.models.post import Post, Comment, Vote
from app.utils.auth import decode_access_token
from app.models.user import User
from tortoise.exceptions import DoesNotExist

router = APIRouter()


# Utility to get the current user
async def get_current_user(token: str):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Authentication Required or Invalid Token")
    return await User.get(username=payload["sub"])


# Create a post
@router.post("/create/", response_model=PostResponse)
async def create_post(post: PostCreate, user: User = Depends(get_current_user)):
    post_obj = await Post.create(title=post.title, content=post.content, author=user)
    return post_obj


# List all posts
@router.get("/list/", response_model=list[PostResponse])
async def list_post():
    return await Post.all().select_related('author')


# Get a specific post
@router.get("/{post_id}/", response_model=dict)
async def get_post(post_id: int):
    post = await Post.filter(id=post_id).select_related("author").first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return {
        "id": post.id,
        "title": post.title,
        "content": post.content,
        "author_id": post.author.id,
        "author_username": post.author.username,  
        "created_at": post.created_at,
        "updated_at": post.updated_at,
    }

# Update a post
@router.put("/{post_id}/", response_model=PostResponse)
async def update_post(
    post_id: int, updated_data: PostCreate, user: User = Depends(get_current_user)
):
    post = await Post.get_or_none(id=post_id, author=user)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found or unauthorized")

    post.title = updated_data.title
    post.content = updated_data.content
    await post.save()
    return post


# Delete a post
@router.delete("/{post_id}/", response_model=dict)
async def delete_post(post_id: int, user: User = Depends(get_current_user)):
    post = await Post.get_or_none(id=post_id, author=user)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found or unauthorized")
    await post.delete()
    return {"detail": "Post deleted successfully"}


# Add a comment to a post
@router.post("/{post_id}/comments/", response_model=dict)
async def comment_on_post(
    post_id: int, comment: CommentCreate, user: User = Depends(get_current_user)
):
    try:
        post = await Post.get(id=post_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Post not found")

    await Comment.create(content=comment.content, post=post, author=user)
    return {"detail": "Comment added successfully"}


# List comments for a specific post
@router.get("/{post_id}/comments/", response_model=list[CommentRespond])
async def list_comments(post_id: int):
    post = await Post.get_or_none(id=post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    comments = await Comment.filter(post=post).select_related("author")
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
    comment_id: int, updated_comment: CommentCreate, user: User = Depends(get_current_user)
):
    comment = await Comment.get_or_none(id=comment_id, author=user)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found or unauthorized")

    comment.content = updated_comment.content
    await comment.save()
    return comment


# Delete a comment
@router.delete("/comments/{comment_id}/", response_model=dict)
async def delete_comment(comment_id: int, user: User = Depends(get_current_user)):
    comment = await Comment.get_or_none(id=comment_id, author=user)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found for the user")

    await comment.delete()
    return {"detail": "Comment deleted successfully"}


# Vote on a post
@router.post("/vote/", response_model=VoteResponse)
async def vote_action(vote: VoteAction, user: User = Depends(get_current_user)):
    post = await Post.get_or_none(id=vote.post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    existing_vote = await Vote.get_or_none(post=post, user=user)

    if vote.action == "vote":
        if existing_vote:
            raise HTTPException(status_code=400, detail="You have already voted for this post")
        await Vote.create(post=post, user=user)
        return {"post_id": post.id, "user_id": user.id,"message":"voted successfully"}

    elif vote.action == "unvote":
        if not existing_vote:
            raise HTTPException(status_code=400, detail="You haven't voted for this post")
        await existing_vote.delete()
        return {"post_id": post.id, "user_id": user.id,"message":"unvoted_successfully"}

    else:
        raise HTTPException(status_code=400, detail="Invalid action. Use 'vote' or 'unvote'.")


# Get comprehensive post data with vote count and comments
@router.get("/{post_id}/comprehensive/", response_model=PostComprehensiveResponse)
async def get_comprehensive_post(post_id: int):
    post = await Post.filter(id=post_id).prefetch_related("comments", "votes", "author").first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    comments = await Comment.filter(post=post).select_related("author")

    comments_data = [
        CommentRespond(
            id=comment.id,
            content=comment.content,
            author_id=comment.author.id,
            created_at=comment.created_at,
        )
        for comment in comments
    ]

    # Count the votes for the post
    vote_count = await Vote.filter(post=post).count()

    return {
        "id": post.id,
        "title": post.title,
        "content": post.content,
        "author_id": post.author.id,
        "votes_count": vote_count,
        "comments": comments_data,  # List of CommentRespond objects
        "created_at": post.created_at,
        "updated_at": post.updated_at,
    }

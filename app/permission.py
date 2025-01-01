from fastapi import HTTPException
from app.utils.auth import decode_access_token
from fastapi import Depends, HTTPException, Query, APIRouter, Request


def get_token_from_request(request: Request) -> str:
    """
    Extracts the token from the Authorization header in the request.
    """
    authorization: str = request.headers.get("Authorization")
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authorization token missing or invalid")

    # Return the token part after "Bearer "
    return authorization.split(" ")[1]


def is_admin(token: str = Depends(get_token_from_request)) -> bool:
    """
    Dependency to check if the user is an admin.
    """
    try:
        decoded = decode_access_token(token)
        role = decoded.get("role")
        if role != "admin":
            raise HTTPException(status_code=403, detail="Only Admin can access this endpoint")
    except Exception as e:
        raise HTTPException(status_code=403, detail="Invalid token or access forbidden")
    return True


def is_regular_user(token: str = Depends(get_token_from_request)) -> bool:
    """
    Dependency to check if the user is an regular user.
    """
    try:
        decoded = decode_access_token(token)
        role = decoded.get("role")
        if role != "regular":
            raise HTTPException(
                status_code=403, detail="Only Regular User can access this endpoint"
            )
    except Exception as e:
        raise HTTPException(status_code=403, detail="Invalid token or access forbidden")
    return True

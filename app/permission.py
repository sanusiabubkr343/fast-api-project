from fastapi import HTTPException
from app.utils.auth import decode_access_token, get_current_user
from fastapi import Depends, HTTPException, Query, APIRouter, Request


def is_admin(token: str):
    """
    Dependency to check if the user is an admin.
    """
    try:
        decoded = decode_access_token(token)
        role = decoded.get("role")
        print(role)
        if role != "admin":
            raise HTTPException(status_code=403, detail="Only Admin can access this endpoint")

        return
    except Exception as e:
        print(e)
        raise HTTPException(status_code=403, detail=str(e))


def is_regular_user(token: str):
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

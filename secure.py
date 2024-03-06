from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from firebase import jwt_decode_by_fb_auth, jwt_decode

http_bearer = HTTPBearer()


async def dget_user(header=Depends(http_bearer)):
    """
    token decode by direct(jose)
    """
    user = await jwt_decode(header.credentials)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Unauthorized",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_user(header=Depends(http_bearer)):
    """
    token decode by firebase admin
    """
    user = await jwt_decode_by_fb_auth(header.credentials)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Unauthorized",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

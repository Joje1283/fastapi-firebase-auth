from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from firebase import jwt_decode

http_bearer = HTTPBearer()


async def get_user(header=Depends(http_bearer)):
    user = await jwt_decode(header.credentials)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Unauthorized",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

from fastapi import Depends, FastAPI
from secure import get_user, dget_user


app = FastAPI()


@app.get("/verify")
async def get_user(token: str = Depends(get_user)):
    """
    token decode by firebase admin
    """
    return {"token": token}


@app.get("/verify/direct")
async def dget_user(token: str = Depends(dget_user)):
    """
    token decode by direct(jose)
    """
    return {"token": token}

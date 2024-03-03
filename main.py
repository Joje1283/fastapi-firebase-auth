import time
from fastapi import Depends, FastAPI, Request
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


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """
    add process time header
    ref: https://fastapi.tiangolo.com/tutorial/middleware/
    """
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

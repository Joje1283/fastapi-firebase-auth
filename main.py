from fastapi import Depends, FastAPI
from secure import get_user


app = FastAPI()


@app.get("/")
async def auth_firebase(token: str = Depends(get_user)):
    return {"token": token}

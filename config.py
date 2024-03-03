import os
from dotenv import load_dotenv
import requests
import aiohttp
import json

load_dotenv()


def get_fb_public_key():
    res = requests.get(
        "https://www.googleapis.com/robot/v1/metadata/x509/securetoken@system.gserviceaccount.com"
    )
    if res.status_code == 200:
        return res.json()
    else:
        raise Exception("Firebase public key fetch failed.")


async def aget_fb_public_key(
    certificate_url="https://www.googleapis.com/robot/v1/metadata/x509/securetoken@system.gserviceaccount.com",
):
    async with aiohttp.ClientSession() as session:
        async with session.get(certificate_url) as response:
            if response.status == 200:
                certs = await response.read()
                certs = json.loads(certs)
                return certs
            else:
                raise Exception("Firebase public key fetch failed.")


class Configs:
    FB_API_KEY: str = os.getenv(
        "FB_API_KEY"
    )  # Firebase Console > Settings > General > Web API Key
    FB_CERTS: dict = get_fb_public_key()


config = Configs()
res = requests.get(
    "https://www.googleapis.com/robot/v1/metadata/x509/securetoken@system.gserviceaccount.com"
)

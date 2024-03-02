import os
from dotenv import load_dotenv

load_dotenv()


class Configs:
    FB_API_KEY: str = os.getenv(
        "FB_API_KEY"
    )  # Firebase Console > Settings > General > Web API Key


config = Configs()

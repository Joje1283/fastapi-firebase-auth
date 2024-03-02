import json
from firebase_admin import auth, credentials, initialize_app
from firebase_admin.auth import UserRecord
from config import config
import requests

# Firebase Console > Settings > Service Accounts > Generate New Private key
cred = credentials.Certificate("serviceAccountKey.json")

# Firebase Console > Settings > General > Web API Key
API_KEY = config.FB_API_KEY
initialize_app(cred)


async def decode_fb_jwt(token: str) -> dict:
    """
    Firebase JWT 디코딩
    """
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception as e:
        return {}


def generate_token_by_uid(uid):
    """Return a Firebase ID token dict from a user id (UID).
    ref: https://github.com/jewang/firebase-id-token-generator-python/blob/master/firebase_token_generator.py

    Returns:
      dict: Keys are "kind", "idToken", "refreshToken", and "expiresIn".
      "expiresIn" is in seconds.

      The return dict matches the response payload described in
      https://firebase.google.com/docs/reference/rest/auth/#section-verify-custom-token

      The actual token is at get_token(uid)["idToken"].
    """
    token = auth.create_custom_token(uid)
    data = {"token": token.decode(), "returnSecureToken": True}

    url = (
        "https://www.googleapis.com/identitytoolkit/v3/relyingparty"
        "/verifyCustomToken?key={}".format(API_KEY)
    )

    req = requests.post(url, json.dumps(data), {"Content-Type": "application/json"})
    response = req.text

    return json.loads(response)


if __name__ == "__main__":
    import asyncio

    async def main():
        user: UserRecord = auth.get_user_by_email("test@test.test")
        uid = user.uid
        token = generate_token_by_uid(uid)
        id_token = token.get("idToken")
        print(id_token)
        decoded = await decode_fb_jwt(id_token)
        print(decoded)

    asyncio.run(main())

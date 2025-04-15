from fastapi import FastAPI, Query, HTTPException, Depends, Header
from pydantic import BaseModel
import requests
import os
app = FastAPI()


GITEE_CLIENT_ID = "19e3fc7ea81056e9abb2351ef76e0bf49f756346be1e1891bcc5d09e2edddb8e"
GITEE_CLIENT_SECRET = "30f6649b73043796e2130822e98ef870b99d595edd11357711407f4d7b94eaf7"
GITEE_REDIRECT_URI = "http://localhost:8000/callback"
class ProviderToken(BaseModel):
    id: int
    client_id: str
    redirect_url: str
    code: str
    client_secret: str
    state: str
class UserInfo(BaseModel):
    id: int
    login: str
    name: str
    avatar_url: str

@app.get("/callback")
def callback(code: str = Query(..., description="The code received from the OAuth provider")):
    token_url = "https://gitee.com/oauth/token"
    token_params = {
        "grant_type": "authorization_code",
        "code": code,
        "client_id": GITEE_CLIENT_ID,
        "redirect_uri": GITEE_REDIRECT_URI,
        "client_secret": GITEE_CLIENT_SECRET
    }
    token_headers = {
        "Content-Type": "application/json"
    }
    token_response = requests.post(token_url, json=token_params, headers=token_headers)
    if token_response.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to get access token")
    token_data = token_response.json()
    access_token = token_data.get("access_token")
    if not access_token:
        raise HTTPException(status_code=400, detail="Access token not found")

    # Step 2: Get user information
    user_url = "https://gitee.com/api/v5/user"
    user_headers = {
        "Authorization": f"token {access_token}"
    }
    user_response = requests.get(user_url, headers=user_headers)
    if user_response.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to get user information")
    user_data = user_response.json()
    user_info = UserInfo(**user_data)
    return {
        "access_token": access_token,
        "user_info": user_info
    }

# Step 3: Implement token dependency for route protection
async def get_token(Authorization: str = Header(..., description="Bearer token for authentication")):
    if not Authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    token = Authorization.split(" ")[1]
    return token


@app.get("/protected")
def protected_route(token: str = Depends(get_token)):
    # You can use the token to fetch user information or perform other checks
    user_url = "https://gitee.com/api/v5/user"
    user_headers = {
        "Authorization": f"token {token}"
    }
    user_response = requests.get(user_url, headers=user_headers)
    if user_response.status_code != 200:
        raise HTTPException(status_code=401, detail="Invalid token")
    user_data = user_response.json()
    user_info = UserInfo(**user_data)

    return {
        "message": "This is a protected route",
        "user_info": user_info
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
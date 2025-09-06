import os
import secrets
from dotenv import load_dotenv
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import RedirectResponse
import httpx
import urllib.parse

load_dotenv()

client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
redirect_uri = os.getenv("SPOTIFY_CLIENT_REDIRECT_URI")


class StateMismatchError(Exception):
    pass


api = FastAPI()

active_states = set()


@api.get("/login")
def login():
    state = secrets.token_urlsafe(32)
    active_states.add(state)

    redirect_uri = "http://127.0.0.1:8080/callback"
    scope = "playlist-modify-private"
    params = {
        "response_type": "code",
        "client_id": client_id,
        "scope": scope,
        "redirect_uri": redirect_uri,
        "state": state,
    }
    url = "https://accounts.spotify.com/authorize?" + urllib.parse.urlencode(params)
    return RedirectResponse(url)


@api.get("/callback")
def get_data(request: Request):
    returned_state = request.query_params.get("state")
    code = request.query_params.get("code")
    error = request.query_params.get("error")

    if error:
        raise HTTPException(status_code=400, detail=f"Authorization error: {error}")

    if not code:
        raise HTTPException(status_code=400, detail="Authorization code missing")

    if not returned_state:
        raise HTTPException(status_code=400, detail="State parameter missing")

    if returned_state not in active_states:
        raise StateMismatchError("Invalid or expired state")

    active_states.remove(returned_state)

    auth_endpoint = "https://accounts.spotify.com/api/token"

    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri,
        "client_id": client_id,
        "client_secret": client_secret,
    }

    try:
        response = httpx.post(
            auth_endpoint,
            data=data,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        response.raise_for_status()
        token_data = response.json()
        return token_data
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=400, detail=f"Token exchange failed: {e}")

    except StateMismatchError:
        raise HTTPException(status_code=400, detail="State mismatch")

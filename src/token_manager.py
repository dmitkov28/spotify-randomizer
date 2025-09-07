from base64 import b64encode
import os
from pathlib import Path
from typing import Protocol
from dotenv import set_key
import httpx


class TokenManager(Protocol):
    user_id: str
    user_access_token: str
    user_refresh_token: str
    client_secret: str
    client_id: str

    def refresh_token(self): ...


class SpotifyTokenManager:
    token_endpoint = "https://accounts.spotify.com/api/token"

    client_secret_env_key = "SPOTIFY_CLIENT_SECRET"
    client_id_env_key = "SPOTIFY_CLIENT_ID"
    user_id_env_key = "SPOTIFY_USER_ID"
    user_access_token_env_key = "SPOTIFY_USER_ACCESS_TOKEN"
    user_refresh_token_env_key = "SPOTIFY_USER_REFRESH_TOKEN"

    def __init__(self) -> None:
        self.user_access_token = self._get_token_from_env(
            self.user_access_token_env_key
        )
        self.user_refresh_token = self._get_token_from_env(
            self.user_refresh_token_env_key
        )

        self.client_id = self._get_token_from_env(self.client_id_env_key)
        self.client_secret = self._get_token_from_env(self.client_secret_env_key)

        self.user_id = self._get_token_from_env(self.user_id_env_key)

    def _get_token_from_env(self, token_name):
        token = os.environ[token_name]
        return token

    def set_token_to_env(self, token_name, token):
        script_dir = Path(__file__).parent
        dotenv_path = script_dir.parent / ".env"
        dotenv_path = str(dotenv_path.absolute())
        if os.path.exists(dotenv_path):
            set_key(
                dotenv_path, self.user_access_token_env_key, token, quote_mode="never"
            )
        os.environ[token_name] = token

    def _is_user_access_token_valid(self):
        url = "https://api.spotify.com/v1/me"
        headers = {"Authorization": f"Bearer {self.user_access_token}"}
        response = httpx.get(url, headers=headers)
        return response.status_code == 200

    def _get_new_user_access_token(self):
        url = "https://accounts.spotify.com/api/token"
        headers = {
            "Authorization": "Basic "
            + b64encode(f"{self.client_id}:{self.client_secret}".encode()).decode(),
            "Content-Type": "application/x-www-form-urlencoded",
        }
        data = {"grant_type": "refresh_token", "refresh_token": self.user_refresh_token}
        response = httpx.post(url, headers=headers, data=data)
        response.raise_for_status()
        return response.json().get("access_token")

    def refresh_token(self):
        if self._is_user_access_token_valid():
            return
        new_token = self._get_new_user_access_token()
        self.set_token_to_env(self.user_access_token_env_key, new_token)
        self.user_access_token = new_token

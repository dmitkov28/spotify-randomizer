import os
from dotenv import load_dotenv, set_key
import httpx


class SpotifyTokenManager:
    check_endpoint = "https://api.spotify.com/v1/search?q=test&type=artist&limit=1"
    token_endpoint = "https://accounts.spotify.com/api/token"

    env_key = "SPOTIFY_API_TOKEN"
    client_secret_key = "SPOTIFY_CLIENT_SECRET"
    client_id_key = "SPOTIFY_CLIENT_ID"

    def __init__(self) -> None:
        self.token = self._get_token_from_env()
        self.client_id = self._get_client_id_from_env()
        self.client_secret = self._get_secret_from_env()

    def _get_token_from_env(self):
        load_dotenv()
        token = os.getenv(self.env_key)
        if not token:
            raise ValueError("No API TOKEN set")
        return token

    def _get_secret_from_env(self):
        load_dotenv()
        secret = os.getenv(self.client_secret_key)
        if not secret:
            raise ValueError("No Client Secrent set")
        return secret

    def _get_client_id_from_env(self):
        load_dotenv()
        client_id = os.getenv(self.client_id_key)
        if not client_id:
            raise ValueError("No Client Id set")
        return client_id

    def set_token_to_env(self, token):
        set_key(".env", "SPOTIFY_API_TOKEN", token)

    def _is_token_valid(self):
        res = httpx.get(
            self.check_endpoint, headers={"Authorization": f"Bearer {self.token}"}
        )
        return res.status_code == 200

    def _get_new_token(self):
        new_token_res = httpx.post(
            self.token_endpoint,
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
            },
            data={
                "grant_type": "client_credentials",
                "client_id": self.client_id,
                "client_secret": self.client_secret,
            },
        )
        
        if new_token_res.status_code != 200:
            raise Exception("Failed fetching token")

        return new_token_res.json().get("access_token")

    def validate_token(self):
        if self._is_token_valid():
            return
        new_token = self._get_new_token()
        self.set_token_to_env(new_token)

from base64 import b64encode
from dotenv import get_key, set_key
import httpx


class SpotifyTokenManager:
    check_endpoint = "https://api.spotify.com/v1/search?q=test&type=artist&limit=1"
    token_endpoint = "https://accounts.spotify.com/api/token"

    app_token_env_key = "SPOTIFY_API_TOKEN"
    client_secret_env_key = "SPOTIFY_CLIENT_SECRET"
    client_id_env_key = "SPOTIFY_CLIENT_ID"

    user_id_env_key = "SPOTIFY_USER_ID"
    user_access_token_env_key = "SPOTIFY_USER_ACCESS_TOKEN"
    user_refresh_token_env_key = "SPOTIFY_USER_REFRESH_TOKEN"

    dotenv_path = "../.env"

    def __init__(self) -> None:
        self.app_token = self._get_token_from_env(self.app_token_env_key)
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
        token = get_key(".env", token_name)
        return token

    def set_token_to_env(self, token_name, token):
        set_key(".env", token_name, token)

    def _is_app_token_valid(self):
        res = httpx.get(
            self.check_endpoint, headers={"Authorization": f"Bearer {self.app_token}"}
        )
        return res.status_code == 200

    def _is_user_access_token_valid(self):
        url = "https://api.spotify.com/v1/me"
        headers = {"Authorization": f"Bearer {self.user_access_token}"}
        response = httpx.get(url, headers=headers)
        return response.status_code == 200

    def _get_new_app_token(self):
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

    def validate_app_token(self):
        if self._is_app_token_valid():
            return
        new_token = self._get_new_app_token()
        self.set_token_to_env(self.app_token_env_key, new_token)

    def validate_user_token(self):
        if self._is_user_access_token_valid():
            return
        new_token = self._get_new_user_access_token()
        self.set_token_to_env(self.user_access_token, new_token)

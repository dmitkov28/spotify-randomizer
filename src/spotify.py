import random
from typing import List

import httpx

from model import Item
from token_manager import SpotifyTokenManager, TokenManager

SPOTIFY_API = "https://api.spotify.com/v1"
SEARCH_ENDPOINT = "/search"


def generate_random_offsets(n_offsets: int = 5) -> List[int]:
    return list(set([random.randint(0, 1000) for _ in range(n_offsets)]))


def generate_random_years(from_year: int, to_year: int, n_years: int = 5) -> List[int]:
    return list(set([random.randint(from_year, to_year) for _ in range(n_years)]))


def get_random_tracks(
    spotify_token: str,
    offsets: List[int] = generate_random_offsets(),
    years: List[int] = generate_random_years(from_year=1950, to_year=2025),
):
    requests = []
    for idx in range(min(len(offsets), len(years))):
        logical_q = f"year:{years[idx]} genre:rock"
        q_type = "track"

        params = {"q": logical_q, "type": q_type, "offset": offsets[idx]}

        req = httpx.Request(
            "GET",
            SPOTIFY_API + SEARCH_ENDPOINT,
            headers={"Authorization": f"Bearer {spotify_token}"},
            params=params,
        )
        requests.append(req)

    all_tracks = []

    with httpx.Client() as client:
        for req in requests:
            res = client.send(req)
            if res.status_code == 200:
                tracks = res.json().get("tracks", {}).get("items")
                all_tracks.extend(tracks)

    return all_tracks


def process_fetched_tracks(tracks: List) -> List[Item]:
    processed_tracks = []
    for track in tracks:
        try:
            processed_tracks.append(Item(**track))
        except Exception:
            pass
    return processed_tracks


def get_track_ids(tracks: List[Item]) -> List[str]:
    return [track.id for track in tracks]


def create_spotify_playlist(
    user_id, playlist_name, access_token, public=False, description=""
):
    url = f"https://api.spotify.com/v1/users/{user_id}/playlists"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    data = {"name": playlist_name, "public": public, "description": description}
    response = httpx.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()


def add_to_playlist(playlist_id: str, track_ids: List[str], access_token: str):
    endpoint = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    data = {"uris": [f"spotify:track:{track_id}" for track_id in track_ids]}

    response = httpx.post(endpoint, headers=headers, json=data)
    response.raise_for_status()
    return response.json()


class SpotifyClient:
    def __init__(self, token_manager: TokenManager = SpotifyTokenManager()) -> None:
        self.token_manager = token_manager
        self.token_manager.refresh_token()

    def create_playlist_with_random_tracks(self, playlist_name: str):
        playlist = create_spotify_playlist(
            self.token_manager.user_id,
            playlist_name,
            access_token=self.token_manager.user_access_token,
        )

        playlist_id = playlist.get("id")
        tracks = get_random_tracks(self.token_manager.user_access_token)
        processed_tracks = process_fetched_tracks(tracks)
        track_ids = get_track_ids(processed_tracks)
        add_to_playlist(
            playlist_id, track_ids, access_token=self.token_manager.user_access_token
        )

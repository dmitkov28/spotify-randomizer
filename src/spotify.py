import os
import random
from typing import List

import httpx

from model import Item

SPOTIFY_API = "https://api.spotify.com/v1"
SEARCH_ENDPOINT = "/search"


def get_token() -> str:
    token = os.getenv("SPOTIFY_API_TOKEN")
    if not token:
        raise ValueError("Missing Spotify API Key")
    return token


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

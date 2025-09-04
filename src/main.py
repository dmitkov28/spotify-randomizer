import json
from spotify import get_random_tracks, get_track_ids, process_fetched_tracks
from token_check import SpotifyTokenManager

if __name__ == "__main__":
    token_manager = SpotifyTokenManager()
    token_manager.validate_token()

    tracks = get_random_tracks(spotify_token=token_manager.token)
    processed_tracks = process_fetched_tracks(tracks)
    track_ids = get_track_ids(processed_tracks)

    result = {
        "track_ids": json.dumps(track_ids),
    }
    print(json.dumps(result))

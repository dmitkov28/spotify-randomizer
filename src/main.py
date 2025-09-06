from dotenv import load_dotenv
from spotify import (
    add_to_playlist,
    create_spotify_playlist,
    get_random_tracks,
    get_track_ids,
    process_fetched_tracks,
)
from token_check import SpotifyTokenManager

if __name__ == "__main__":
    load_dotenv()
    
    playlist_name = "Test"

    sm = SpotifyTokenManager()
    sm.validate_app_token()
    sm.validate_user_token()
    
    breakpoint()
    
    playlist = create_spotify_playlist(
        sm.user_id, playlist_name=playlist_name, access_token=sm.user_access_token
    )
    playlist_id = playlist.get("id")
    tracks = get_random_tracks(str(sm.app_token))
    processed_tracks = process_fetched_tracks(tracks)
    track_ids = get_track_ids(processed_tracks)

    add_to_playlist(playlist_id, track_ids, access_token=str(sm.user_access_token))

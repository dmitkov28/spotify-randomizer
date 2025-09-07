from dotenv import load_dotenv
from spotify import (
    SpotifyClient,
)


if __name__ == "__main__":
    load_dotenv()
    client = SpotifyClient()
    client.create_playlist_with_random_tracks(playlist_name="Test Playlist #3")

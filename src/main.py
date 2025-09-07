from dotenv import load_dotenv
from spotify import (
    SpotifyClient,
)
from utils import generate_datetime_str


if __name__ == "__main__":
    load_dotenv()
    client = SpotifyClient()
    playlist_name = f"Random Playlist {generate_datetime_str()}"
    client.create_playlist_with_random_tracks(playlist_name=playlist_name)
    print("✅ Successfully created playlist.")

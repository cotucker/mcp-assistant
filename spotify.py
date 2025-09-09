import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')


scope = "user-top-read"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth())

results = sp.current_user_top_tracks()
for item in results['items']:
    print(item['name'])


query = input("\nQuery: ").strip()
track_name = sp.search(query, 1, type='track')

for track in track_name['tracks']['items']:
    print(f"{track['name']} by {track['artists'][0]['name']}")

from pydantic.errors import DEV_ERROR_DOCS_URL
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv


load_dotenv()

CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')
DEVICE_ID = '807cea9a26b8f1dd602ccc6f8279939e47a9d2bc'


scope = "user-modify-playback-state user-read-currently-playing"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

def play_track(name: str):
    track_name = sp.search(name, 1, type='track')
    for track in track_name['tracks']['items']:
        track_uri = track['uri']
        reply = f"Playing {track['name']} by {track['artists'][0]['name']}"
        sp.start_playback(device_id=DEVICE_ID, uris=[track_uri])
        return reply

def pause_playback():
    sp.pause_playback(device_id=DEVICE_ID)

def start_playback():
    sp.start_playback(device_id=DEVICE_ID)

def play_next_track():
    sp.next_track(device_id=DEVICE_ID)

def get_currently_playing_track():
    current_track = sp.currently_playing()
    if current_track is not None:
        track_name = current_track['item']['name']
        artist_name = current_track['item']['artists'][0]['name']
        return f"Currently playing: {track_name} by {artist_name}"
    else:
        return "No track is currently playing."

if __name__ == "__main__":
    res = sp.search('track:A million artist:Lil Wayne', 1, type='track')
    print(res)


import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

load_dotenv()
CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
PLAYLIST_ID = os.getenv('SPOTIFY_PLAYLIST_ID')

if not CLIENT_ID or not CLIENT_SECRET or not PLAYLIST_ID:
    raise SystemExit('Preencha SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET e SPOTIFY_PLAYLIST_ID no .env')

auth_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)

def fetch_playlist_tracks(playlist_id, limit=100):
    results = sp.playlist_items(playlist_id, additional_types=['track'], limit=limit)
    tracks = []
    for item in results['items']:
        track = item.get('track')
        if not track: continue
        track_info = {
            'track_id': track['id'],
            'name': track['name'],
            'artists': ', '.join([a['name'] for a in track['artists']]),
            'album': track['album']['name'],
            'duration_ms': track['duration_ms'],
            'popularity': track.get('popularity'),
            'explicit': track.get('explicit'),
        }
        tracks.append(track_info)
    return pd.DataFrame(tracks)

if __name__ == '__main__':
    df = fetch_playlist_tracks(PLAYLIST_ID, limit=100)
    os.makedirs('data', exist_ok=True)
    df.to_csv('data/spotify_tracks_raw.csv', index=False)
    print(f'Exported {len(df)} tracks to data/spotify_tracks_raw.csv')

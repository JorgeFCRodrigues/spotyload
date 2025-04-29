import os, re, spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv

load_dotenv()

SPOTIFY_CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")

def extract_playlist_id(url):
        match = re.search(r'playlist/([a-zA-Z0-9]+)', url)
        return match.group(1) if match else None

def get_spotify_tracks(playlist_id):
    """Obtém os nomes das músicas do Spotify no formato 'Artista - Título'."""
    auth = SpotifyClientCredentials(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET
    )
    sp = spotipy.Spotify(client_credentials_manager=auth)
    
    tracks = []
    try:
        results = sp.playlist_tracks(playlist_id)
        while results:
            for item in results['items']:
                track = item['track']
                if track:
                    artist = track['artists'][0]['name']
                    tracks.append(f"{artist} - {track['name']}")
            results = sp.next(results) if results['next'] else None
        return tracks
    except Exception as e:
        print(f"Erro no Spotify: {e}")
        return []

def get_playlist_name(playlist_id):
    """Obtém o nome da playlist do Spotify."""
    try:
        auth = SpotifyClientCredentials(
            client_id=SPOTIFY_CLIENT_ID,
            client_secret=SPOTIFY_CLIENT_SECRET
        )
        sp = spotipy.Spotify(client_credentials_manager=auth)
        playlist_data = sp.playlist(playlist_id)
        return playlist_data.get('name', 'playlist_downloads')
    except Exception as e:
        print(f"Não foi possível obter o nome da playlist: {e}")
        return 'playlist_downloads'

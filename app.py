from flask import Flask, render_template
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, render_template


app = Flask(__name__)

# Set up your Spotify API credentials
client_id = os.getenv('SPOTIPY_CLIENT_ID')
client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')
redirect_uri = os.getenv('SPOTIPY_REDIRECT_URI')

# Set up Spotify API authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope='user-read-playback-state', show_dialog=True, cache_path=".token.cache"))

@app.route('/')
def index():
    try:
        current_playback = sp.current_playback()

        if current_playback is not None and 'item' in current_playback:
            track = current_playback['item']
            track_name = track['name']
            artists = ', '.join([artist['name'] for artist in track['artists']])
            album_name = track['album']['name']
            track_uri = track['uri']
            duration_ms = track['duration_ms']
            release_date = track['album']['release_date']

            # Get recommendations based on the currently playing song
            recommendations = sp.recommendations(seed_tracks=[track_uri], limit=5)

            return render_template('index.html', track_name=track_name, artists=artists, album_name=album_name,
                                   duration_ms=duration_ms, release_date=release_date, recommendations=recommendations)

        else:
            return render_template('no_song.html')

    except spotipy.oauth2.SpotifyOauthError as e:
        return f"Authentication error: {e}"

if __name__ == '__main__':
    app.run(debug=True)

import os
import pandas as pd
from flask import Flask, render_template, render_template_string, request, flash
import spotipy
import re
from spotipy.oauth2 import SpotifyClientCredentials

app = Flask(__name__)

# Set up Spotify API credentials
client_id = "600220c413d049ee8a0ec07e593db803"
client_secret = "846b7e6a86834dbd81e282b043cc8fe0"

client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_track_info(song_link):
    track_id = re.search(r"track/(\w+)", song_link)
    if track_id:
        track_id = track_id.group(1)
    else:
        raise ValueError("Invalid song link")

    track = sp.track(track_id)
    audio_features = sp.audio_features(track_id)[0]
    audio_analysis = sp.audio_analysis(track_id)

    artist = track['artists'][0]['name']
    track_name = track['name']
    album = track['album']['name']
    release_date = track['album']['release_date']
    popularity = track['popularity']
    duration_ms = track['duration_ms']
    album_cover_url = track['album']['images'][0]['url'] if track['album']['images'] else None
    preview_url = track['preview_url']

    return {
        'artist': artist,
        'track_name': track_name,
        'album': album,
        'release_date': release_date,
        'popularity': popularity,
        'duration_ms': duration_ms,
        'album_cover_url': album_cover_url,
        'preview_url': preview_url,
        'audio_features': audio_features,
        'audio_analysis': audio_analysis
    }



@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            song_link = request.form["song_link"]
            print(f"Song link received: {song_link}")
            track_info = get_track_info(song_link)
            print(f"Track info: {track_info}")
            return render_template("dashboard.html", track_info=track_info)
        except Exception as e:
            print(f"Error: {e}")
            flash(f"Error: {e}")
    return render_template("index.html")

if __name__ == "__main__":
    app.secret_key = "test"  # Replace with your own secret key
    app.run(debug=True)

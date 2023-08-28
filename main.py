from bs4 import BeautifulSoup
import requests
from pprint import pprint
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# ------ SPOTIFY AUTHENTICATION ------ #
SPOTIPY_CLIENT_ID = os.environ.get("SPOTIFY_ID")
SPOTIPY_CLIENT_SECRET = os.environ.get("SPOTIFY_TOKEN")
SPOTIPY_REDIRECT_URI = "http://example.com"

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri=SPOTIPY_REDIRECT_URI,
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt",
    )
)

# .current_user()["id"] method retrieves user id
user_id = sp.current_user()["id"]

# ------ SCRAPING BILLBOARD 100  ------ #
date = input("Enter desired time travel date (YYYY-MM-DD): ")
URL = f"https://www.billboard.com/charts/hot-100/{date}/"

response = requests.get(URL)
web_data = response.text
soup = BeautifulSoup(web_data, "html.parser")

title_search = soup.find_all("h3", id="title-of-a-story", class_="u-max-width-230@tablet-only")
top_chart = []
song_uris = []
year = date.split("-")[0]

song_titles = [top_chart.append(song.text.strip("\t\n")) for song in title_search]

for track in top_chart:
    result = sp.search(q=f"track:{track}=", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{track} does not exist in Spotify. Skipped.")

# ----- CREATES PLAYLIST AND ADDs SONGS ----- #
playlist = sp.user_playlist_create(user="thebriantapia", name=f"{date} Billboard 100", public=False)
sp.user_playlist_add_tracks(user=user_id, playlist_id=playlist["id"], tracks=song_uris)

# --- Notify of Completion --- # 
print('Playlist created, time travel complete.')






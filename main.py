import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

URL = "https://www.billboard.com/charts/hot-100/"
REDIRECT = "https://example.com/"
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
spotify_uris = []

user_date = input("Enter the date you want to travel to in format YYYY-MM-DD: ")

# Web scraping the titles of the songs from the BillBoard Website
res = requests.get(URL+f"{user_date}")
soup = BeautifulSoup(res.text, "html.parser")
data = soup.find_all(name="h3", class_="a-no-trucate")
songs = [" ".join(song.getText().split()) for song in data]
# print(songs)

# Creating a Spotipy Client and creating a playlist
scope = "playlist-modify-private"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT))
current_user = sp.current_user()
playlist = sp.user_playlist_create(user=current_user['id'], name=f'{user_date} Billboard 100', public=False,
                                   collaborative=False, description="")

# Getting URI's for each song
for song in songs:
    uri = sp.search(q=f'track:{song}', type='track')['tracks']['items'][0]['uri']
    spotify_uris.append(uri)
# print(spotify_uris)

# Adding the tracks to the created playlist
add_tracks = sp.playlist_add_items(playlist_id=playlist['id'], items=spotify_uris)
# print(add_tracks)

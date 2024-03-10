from bs4 import BeautifulSoup
import lxml
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

date = input("Enter the date you want to travel to? Type the date in YYYY-MM-DD format")

billboard_url = f"https://www.billboard.com/charts/hot-100/{date}"
print(billboard_url)
response = requests.get(url = billboard_url)
data = response.text
soup = BeautifulSoup(data,"lxml") # here lxml is the parser
"""
<h3 id="title-of-a-story" class="c-title  a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 u-font-size-23@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-245 u-max-width-230@tablet-only u-letter-spacing-0028@tablet">

	
	
		
					Rockin' Around The Christmas Tree		
	
</h3>
"""
song_titles = soup.select("li ul li h3")

song_names =[]
for songs in song_titles:
    song_names.append(songs.getText().strip())
print(song_names)

# spotify part
client_id ="6f88cf6331194a8dbd6a001b3ef358b2"
client_secret = "e9dba71f54184ddea19821b72997a710"
OAUTH_AUTHORIZE_URL= 'https://accounts.spotify.com/authorize'
OAUTH_TOKEN_URL= 'https://accounts.spotify.com/api/token'

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=client_id,
        client_secret=client_secret,
        show_dialog=True,
        cache_path="token.txt",
        username="Dev_User_Acc",
    )
)
user_id = sp.current_user()["id"]
song_uris = []
year = date.split("-")[0]
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
# print(playlist)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)

import spotipy
import spotipy.util as util
import urllib.request as request
import json
from Kaspa.config import Config
import os


class Spotify:
    client_id = ''
    client_secret = ''
    username = ''
    token = ''
    spotipy = None
    scope = "playlist-read-private user-library-read playlist-modify-private playlist-modify-public " \
            "user-read-currently-playing "

    def __init__(self):
        config = Config.get_instance()
        self.client_id = config.get("spotify", "client_id")
        self.client_secret = config.get("spotify", "client_secret")
        self.username = config.get("spotify", "username")
        os.environ["SPOTIPY_CLIENT_ID"] = "self.client_id"
        os.environ["SPOTIPY_CLIENT_SECRET"] = "self.client_secret"
        os.environ["SPOTIPY_REDIRECT_URI"] = "http://localhost/'"
        self.token = util.prompt_for_user_token(self.username, self.scope, client_id=self.client_id,
                                                client_secret=self.client_secret, redirect_uri='http://localhost/')
        self.spotipy = spotipy.Spotify(auth=self.token)

    def get_currently_playing(self):
        url = "https://api.spotify.com/v1/me/player/currently-playing"
        req = request.Request(url)
        req.add_header("Authorization", " Bearer " + self.token)
        response = request.urlopen(req)
        res = response.read().decode()
        if res is "":
            return None
        else:
            res = json.loads(res)
            return res

    def search(self, search_str):
        results = self.spotipy.search(search_str)["tracks"]["items"]
        most_popular = results[0]
        return most_popular

    def get_saved(self, min_length=50, start_song=None):
        saved = self.spotipy.current_user_saved_tracks(limit=50)
        id_list = []
        for item in saved["items"]:
            id_list.append(item["track"]["uri"])
        i = 1
        new = self.spotipy.current_user_saved_tracks(limit=50, offset=i * 50)
        while 1 < len(new["items"]) <= min_length:
            for item in new["items"]:
                id_list.append(item["track"]["uri"])
            i = i + 1
            new = self.spotipy.current_user_saved_tracks(limit=50, offset=i * 50)
        if start_song is not None:
            start_index = 0
            for id in id_list:
                if id == start_song:
                    start_index = id_list.index(id) + 1
            id_list = id_list[start_index:]
        return id_list

    def get_artist_id(self, name):
        result = self.spotipy.search(q='artist:' + name, type='artist')
        uri = result['artists']['items'][0]['uri']
        return uri

    def show_recommendations_for_artist(self, artist):
        results = self.spotipy.recommendations(seed_artists=[self.get_artist_id(artist)])
        for track in results['tracks']:
            print(track['name'], '-', track['artists'][0]['name'])
        return results['tracks']

    def get_artist_songs(self, artist, start_song=None):
        response = self.spotipy.artist_top_tracks(artist)
        tracks = response["tracks"]
        ids = list()
        add_song = True
        for track in tracks:
            if start_song is not None:
                if track["uri"] == start_song:
                    # TODO somehow the two uri for the same song are not identical
                    add_song = True
                    continue
                if add_song:
                    ids.append(track["uri"])
            else:
                ids.append(track["uri"])
        return ids

    def get_artist(self, name):
        results = self.spotipy.search(q='artist:' + name, type='artist')
        items = results['artists']['items']
        if len(items) > 0:
            return items[0]
        else:
            return None

    def get_album_tracks(self, album, start_song=None):
        tracks = []
        results = self.spotipy.album_tracks(album)
        tracks.extend(results['items'])
        while results['next']:
            results = self.spotipy.next(results)
            tracks.extend(results['items'])
        ids = list()
        add_song = False
        for track in tracks:
            if start_song is not None:
                if track["uri"] == start_song:
                    add_song = True
                    continue
                if add_song:
                    ids.append(track["uri"])
            else:
                ids.append(track["uri"])
        return ids

    def show_artist_albums(self, artist):
        albums = []
        results = self.spotipy.artist_albums(artist, album_type='album')
        albums.extend(results['items'])
        while results['next']:
            results = self.spotipy.next(results)
            albums.extend(results['items'])
        unique = set()  # skip duplicate albums
        for album in albums:
            name = album['name'].lower()
            ids = []
            if not name in unique:
                ids.append(album["uri"])
                unique.add(name)
        return ids

    def get_artist_albums(self, name):
        artist = self.get_artist(name)
        self.show_artist(artist)
        self.show_artist_albums(artist)
        # TODO return value?

    @staticmethod
    def show_artist(artist):
        print('====', artist['name'], '====')
        print('Popularity: ', artist['popularity'])
        if len(artist['genres']) > 0:
            print('Genres: ', ','.join(artist['genres']))

    def get_user_playlists(self):
        playlists = self.spotipy.user_playlists(self.username)
        return playlists['items']

    def add_to_playlist(self, playlist_id, tids):
        self.spotipy.user_playlist_add_tracks(self.username, playlist_id, tids[:20])
        tids = tids[20:]
        while len(tids) > 19:
            print(len(tids))
            self.spotipy.user_playlist_add_tracks(self.username, playlist_id, tids[:20])
            tids = tids[20:]
        self.spotipy.user_playlist_add_tracks(self.username, playlist_id, tids)
        return

    def create_playlist(self, playlist_name, tids=None):
        playlists = self.spotipy.user_playlist_create(self.username, playlist_name)
        if tids is not None:
            self.add_to_playlist(playlists["uri"], tids)
        return playlists

    def read_playlist(self, uri, start_song=None):
        username = uri.split(':')[2]
        playlist_id = uri.split(':')[4]
        results = self.spotipy.user_playlist(username, playlist_id)
        ids = []
        for result in results["tracks"]["items"]:
            ids.append(result["track"]["uri"])
        if start_song is not None:
            start_index = 0
            for id in ids:
                if id == start_song:
                    start_index = ids.index(id) + 1
            ids = ids[start_index:]
        return ids

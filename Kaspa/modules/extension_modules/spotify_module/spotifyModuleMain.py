from Kaspa.modules.exceptions.moduleError import ModuleError
from Kaspa.modules.extension_modules.helper.spotify import Spotify
from Kaspa.modules.abstract_modules.abstractMediaModule import AbstractMediaModule
from Kaspa.modules.extension_modules.helper.mpdController import MpdController
from Kaspa.modules.extension_modules.spotify_module.spotifyModuleDe import SpotifyModuleDe
from Kaspa.modules.extension_modules.spotify_module.spotifyModuleEn import SpotifyModuleEn


class SpotifyModuleMain(AbstractMediaModule):

    module_name = "Spotify"

    # TODO config

    def __init__(self):
        super(SpotifyModuleMain, self).__init__()
        self.add_submodule(SpotifyModuleEn())
        self.add_submodule(SpotifyModuleDe())

    @staticmethod
    def continue_playback():
        spotify = Spotify()
        mpd_controller = MpdController.get_instance()
        song = spotify.get_currently_playing()
        if song is None:
            raise ModuleError("Spotify", "There is currently no song playing!")
        else:
            time = song["progress_ms"] // 1000
            mpd_controller.play_tid(song["item"]["uri"], time)
            if song["context"] is not None:
                if song["context"]["type"] == "playlist":
                    # fetch rest of the playlist
                    mpd_controller.add_to_current(spotify.read_playlist(song["context"]["uri"], song["item"]["uri"]))
                    return

                if song["context"]["type"] == "album":
                    # fetch rest of the album
                    mpd_controller.add_to_current(spotify.get_album_tracks(song["context"]["uri"], song["item"]["uri"]))
                    return

                if song["context"]["type"] == "artist":
                    # fetch rest of the artist songs
                    mpd_controller.add_to_current(spotify.get_artist_songs(song["context"]["uri"], song["item"]["uri"]))
                    return

                raise ModuleError("Spotify", "Cannot process current context: " + song["context"]["type"])
                    # TODO implement other contexts
            else:
                mpd_controller.add_to_current(spotify.get_saved(10, song["item"]["uri"]))

    @staticmethod
    def play_search(query):
        spotify = Spotify()
        song = spotify.search(query)
        MpdController.get_instance().play_tid(song["uri"])

    @staticmethod
    def play_saved():
        spotify = Spotify()
        tids = spotify.get_saved(min_length=49)
        MpdController.get_instance().play_tids(tids)

    @staticmethod
    def play_playlist(playlist):
        spotify = Spotify()
        tids = spotify.read_playlist(playlist)
        MpdController.get_instance().play_tids(tids, shuffle=True)
        return

    def play(self):
        mpd_controller = MpdController.get_instance()
        mpd_controller.play()

    def pause(self):
        mpd_controller = MpdController.get_instance()
        mpd_controller.pause()

    def is_playing(self):
        mpd_controller = MpdController.get_instance()
        if mpd_controller.get_state()["state"] == "play":
            return True

    def next(self):
        mpd_controller = MpdController.get_instance()
        mpd_controller.next()

    def current_song(self):
        mpd_controller = MpdController.get_instance()
        return mpd_controller.current_song()


from moduleException import ModuleException
from modules.helper.spotify import Spotify
from abstractModule import AbstractModule
from modules.helper.mpdController import MpdController


class SpotifyModule(AbstractModule):

    module_name = "Spotify"

    def continue_playback(self):
        song = Spotify.get_currently_playing()
        if song is None:
            raise ModuleException("Spotify", "There is currently no song playing!")
        else:
            time = song["progress_ms"]//1000
            MpdController.play_tid(song["item"]["uri"], time)
            if song["context"] is not None:
                if song["context"]["type"] == "playlist":
                    MpdController.add_to_current(Spotify.read_playlist(song["context"]["uri"], song["item"]["uri"]))
                else:
                    raise ModuleException("Spotify", "Cannot find current context")
                    # TODO implement other contexts
            else:
                MpdController.add_to_current(Spotify.get_saved(10, song["item"]["uri"]))

    def play_search(self, query):
        song = Spotify.search(query)
        MpdController.play_tid(song["uri"])

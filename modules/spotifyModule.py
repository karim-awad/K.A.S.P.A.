from moduleException import ModuleException
from modules.helper.spotify import Spotify
from abstractModule import AbstractModule
from modules.helper.mpdController import MpdController
from config import Config


class SpotifyModule(AbstractModule):
    key_regexes = ['(?i).*?(?=continue)+.+?(?=playback)+.', '(?i).*?(?=pause)+.', '(?i).*?(?=play)+.',
                   '(?i).*?(?=next)+.', '(?i).*?(?=stop)+.', '(?i).*?(?=what)+.+?(?=song)+.']

    module_name = "Spotify"

    def continue_playback(self):
        spotify = Spotify()
        mpd_controller = MpdController.get_instance()
        song = spotify.get_currently_playing()
        if song is None:
            raise ModuleException("Spotify", "There is currently no song playing!")
        else:
            time = song["progress_ms"] // 1000
            mpd_controller.play_tid(song["item"]["uri"], time)
            if song["context"] is not None:
                if song["context"]["type"] == "playlist":
                    mpd_controller.add_to_current(spotify.read_playlist(song["context"]["uri"], song["item"]["uri"]))
                else:
                    raise ModuleException("Spotify", "Cannot find current context")
                    # TODO implement other contexts
            else:
                mpd_controller.add_to_current(spotify.get_saved(10, song["item"]["uri"]))

    def play_search(self, query):
        spotify = Spotify()
        song = spotify.search(query)
        MpdController.get_instance().play_tid(song["uri"])

    def play_saved(self):
        spotify = Spotify()
        tids = spotify.get_saved()
        MpdController.get_instance().play_tids(tids)

    def action(self, query):
        text = query.get_text()
        communicator = query.get_communicator()
        mpd_controller = MpdController.get_instance()

        if "continue" in text and "playback" in text:
            communicator.say("I am now continuing your music playback.")
            self.continue_playback()
            return

        if "pause" in text or "stop" in text:
            mpd_controller.pause()
            communicator.say("Music paused.")
            return

        # TODO implement playlist playing
        # playlists = Config.get_instance().get_section_content('playlists')
        # for playlist in playlists:
        #     if playlist[0] in text:
        #        mpd_controller.play_playlist(playlist[1])
        #        communicator.say("Okay, playing " + playlist[0])
        #        return

        if "play" in text:
            if mpd_controller.current_song() is None:
                self.play_saved()
            mpd_controller.play()
            communicator.say("Okay")
            return

        if "next" in text:
            mpd_controller.next()
            communicator.say("Okay")
            return

        if "what" in text and "song" in text:
            if mpd_controller.current_song():
                communicator.say(mpd_controller.current_song())
            else:
                communicator.say("There is no music loaded right now.")

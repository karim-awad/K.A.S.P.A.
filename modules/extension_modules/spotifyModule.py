from modules.moduleException import ModuleException
from modules.extension_modules.helper.spotify import Spotify
from modules.abstract_modules.abstractMediaModule import AbstractMediaModule
from modules.extension_modules.helper.mpdController import MpdController
from config import Config


class SpotifyModule(AbstractMediaModule):
    key_regexes = ['(?i).*?(?=continue)+.+?(?=playback)+.', '(?i).*?(?=pause)+.', '(?i).*?(?=play)+.',
                   '(?i).*?(?=next)+.', '(?i).*?(?=stop)+.', '(?i).*?(?=what)+.+?(?=song)+.']

    module_name = "Spotify"

    # TODO config

    @staticmethod
    def continue_playback():
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

                raise ModuleException("Spotify", "Cannot process current context: " + song["context"]["type"])
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

    def action(self, query):
        text = query.get_text()
        communicator = query.get_communicator()
        mpd_controller = MpdController.get_instance()
        spotify = Spotify()

        if "continue" in text and "playback" in text:
            communicator.say("I am now continuing your music playback.")
            self.continue_playback()
            return

        if "pause" in text or "stop" in text:
            mpd_controller.pause()
            communicator.say("Music paused.")
            return

        # fetch all playlist macros from config file and search for matches in the query
        playlists = Config.get_instance().get_section_content('playlists')
        for playlist in playlists:
            if playlist[0] in text:
                tids = spotify.read_playlist(playlist[1])
                mpd_controller.play_tids(tids, shuffle=True)
                communicator.say("Okay, playing " + playlist[0])
                return

        if "play" in text:
            if mpd_controller.current_song() is None:
                self.play_saved()
                communicator.say("Okay, playing your last added songs.")
                return
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

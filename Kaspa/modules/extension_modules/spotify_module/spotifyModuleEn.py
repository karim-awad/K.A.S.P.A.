from Kaspa.modules.abstract_modules.abstractSubmodule import AbstractSubmodule
from Kaspa.modules.exceptions.impossibleActionError import ImpossibleActionError
from Kaspa.config import Config


class SpotifyModuleEn(AbstractSubmodule):
    module_name = "Spotify"

    language = "en"

    key_regexes = dict()

    def __init__(self):
        self.key_regexes = {'(?i).*?(?=continue)+.+?(?=playback)+.': self.action_continue_playback,
                            '(?i).*?(?=pause)+.': self.action_play,
                            '(?i).*?(?=play)+.': self.action_play,
                            '(?i).*?(?=next)+.': self.action_next,
                            '(?i).*?(?=stop)+.': self.action_pause,
                            '(?i).*?(?=what)+.+?(?=song)+.': self.action_song_info}

    def action_continue_playback(self, query):
        communicator = query.get_communicator()
        self.main_module.continue_playback()
        communicator.say("I am now continuing your music playback.")
        return

    def action_pause(self, query):
        communicator = query.get_communicator()
        self.main_module.pause()
        communicator.say("Music paused.")
        return

    def action_play(self, query):
        communicator = query.get_communicator()
        text = query.get_text()

        try:
            self.action_continue_playback(query)
            return
        except ImpossibleActionError:
            pass

        if self.main_module.current_song() is None:
            self.main_module.play_saved()
            communicator.say("Okay, playing your last added songs.")
            return

        # fetch all playlist macros from config file and search for matches in the query
        playlists = Config.get_instance().get_section_content('playlists')
        for playlist in playlists:
            if playlist[0].lower() in text.lower():
                self.main_module.play_playlist(playlist[1])
                communicator.say("Okay, I'll now play the playlist" + playlist[0] + ".")
                return

        self.main_module.play()
        communicator.say("Okay")
        return

    def action_next(self, query):
        communicator = query.get_communicator()
        self.main_module.next()
        communicator.say("Okay")
        return

    def action_song_info(self, query):
        communicator = query.get_communicator()
        if self.main_module.current_song():
            title, artist = self.main_module.current_song()
            communicator.say("The song is " + title + " by " + artist + ".")
        else:
            communicator.say("There is no music loaded right now.")

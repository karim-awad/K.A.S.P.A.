from Kaspa.modules.abstract_modules.abstractSubmodule import AbstractSubModule
from Kaspa.config import Config


class SpotifyModuleDe(AbstractSubModule):
    module_name = "Spotify"

    language = "de"

    key_regexes = dict()

    def __init__(self):
        self.key_regexes = {'(?i).*?(?=setze)+.+?(?=wiedergabe fort)+.': self.action_continue_playback,
                            '(?i).*?(?=pause)+.': self.action_pause,
                            '((?i).*?(?=wiedergabe)+.)|'
                            '((?i).*?(?=spiel)+.)|'
                            '((?i).*?(?=mach)+.+?(?=musik)+.)|'
                            '((?i).*?(?=musik)+.+?(?=anmachen)+.)': self.action_play,
                            '((?i).*?(?=weiter)+.) |'
                            '((?i).*?(?=nächste)+.+?(?=lied)+.)': self.action_next,
                            '(?i).*?(?=stop)+.': self.action_pause,
                            '(?i).*?(?=welches)+.+?(?=lied)+.': self.action_song_info}

    def action_continue_playback(self, query):
        communicator = query.get_communicator()
        self.main_module.continue_playback()
        communicator.say("Ich werde jetzt deine Musikwiedergabe fortsetzen.")
        return

    def action_pause(self, query):
        communicator = query.get_communicator()
        self.main_module.pause()
        communicator.say("Musik pausiert!")
        return

    def action_play(self, query):
        communicator = query.get_communicator()
        text = query.get_text()

        if self.main_module.current_song() is None:
            self.main_module.play_saved()
            communicator.say("Okay, ich spiele jetzt deine zuletzt hinzugefügten Lieder ab")
            return

        # fetch all playlist macros from config file and search for matches in the query
        playlists = Config.get_instance().get_section_content('playlists')
        for playlist in playlists:
            uri = playlist[1]
            playlist_name = playlist[0]
            if playlist_name.lower() in text.lower():
                self.main_module.play_playlist(uri)
                communicator.say("Ok, die Playlist " + playlist_name + " wird abgespielt")
                return
        self.main_module.play()
        communicator.say("Okay")
        return

    def action_next(self, query):
        communicator = query.get_communicator()
        self.main_module.next()
        communicator.say("Okay")[0]
        return

    def action_song_info(self, query):
        communicator = query.get_communicator()
        if self.main_module.current_song():
            title, artist = self.main_module.current_song()
            communicator.say("Gerade wird " + title + " von " + artist + " abgespielt.")
        else:
            communicator.say("Zurzeit ist keine Musik geladen.")

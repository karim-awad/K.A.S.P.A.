from Kaspa.modules.abstract_modules.abstractSubmodule import AbstractSubmodule
from Kaspa.modules.exceptions.impossibleActionError import ImpossibleActionError
from Kaspa.config import Config


class SpotifyModuleDe(AbstractSubmodule):
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
                            '((?i).*?(?=welches)+.+?(?=lied)+.)|'
                            '((?i).*?(?=was)+.+?(?=das)+.+?(?=lied)+.)|'
                            '((?i).*?(?=wie)+.+?(?=das)+.+?(?=lied)+.)': self.action_song_info,
                            '(?i).*?(?=wem)+.+?(?=lied)+.': self.action_current_artist}

    def action_continue_playback(self, query):
        communicator = query.get_communicator()
        self.main_module.continue_playback()
        communicator.say("Ich setze jetzt deine Musikwiedergabe fort.")
        return

    def action_pause(self, query):
        communicator = query.get_communicator()
        self.main_module.pause()
        communicator.say("Musik pausiert!")
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
            communicator.say("Okay, ich spiele jetzt deine zuletzt hinzugefügten Lieder ab")
            self.main_module.play_saved()
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

        communicator.say("Okay")
        self.main_module.play()
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
            communicator.say("Gerade wird " + title + " von " + artist + " abgespielt.")
        else:
            communicator.say("Zurzeit ist keine Musik geladen.")

    def action_current_artist(self, query):
        communicator = query.get_communicator()
        if self.main_module.current_song():
            title, artist = self.main_module.current_song()
            communicator.say("Das Lied " + title + " ist von " + artist + ".")
        else:
            communicator.say("Zurzeit ist keine Musik geladen.")

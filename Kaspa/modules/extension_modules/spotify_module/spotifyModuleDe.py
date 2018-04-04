from Kaspa.modules.abstract_modules.abstractSubmodule import AbstractSubModule


class SpotifyModuleDe(AbstractSubModule):

    module_name = "Spotify"

    language = "de"

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

        if self.main_module.current_song() is None:
            self.main_module.play_saved()
            communicator.say("Okay, ich spiele jetzt deine zuletzt hinzugefügten Lieder ab")
            return

        # # fetch all playlist macros from config file and search for matches in the query
        # playlists = Config.get_instance().get_section_content('playlists')
        # for playlist in playlists:
        #     if playlist[0] in text:
        #         tids = spotify.read_playlist(playlist[1])
        #         mpd_controller.play_tids(tids, shuffle=True)
        #         communicator.say("Okay, playing " + playlist[0])
        #         return

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
            communicator.say("Gerade wird " + title + " von " + artist + " abgespielt.")
        else:
            communicator.say("Zurzeit ist keine Musik geladen.")

    key_regexes = {'(?i).*?(?=setze)+.+?(?=wiedergabe fort)+.': action_continue_playback,
                   '(?i).*?(?=pause)+.': action_pause,
                   '((?i).*?(?=wiedergabe)+.)|'
                   '((?i).*?(?=spiele)+.+?(?=musik)+.)': action_play,
                   '((?i).*?(?=weiter)+.) |'
                   '((?i).*?(?=nächste)+.+?(?=lied)+.)': action_next,
                   '(?i).*?(?=stop)+.': action_pause,
                   '(?i).*?(?=welches)+.+?(?=lied)+.': action_song_info}




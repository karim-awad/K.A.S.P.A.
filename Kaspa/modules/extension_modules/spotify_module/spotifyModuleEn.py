from Kaspa.modules.abstract_modules.abstractSubmodule import AbstractSubModule


class SpotifyModuleEn(AbstractSubModule):

    module_name = "Spotify"

    language = "en"

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

        if self.main_module.current_song() is None:
            self.main_module.play_saved()
            communicator.say("Okay, playing your last added songs.")
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
            communicator.say("The song is " + title + " by " + artist + ".")
        else:
            communicator.say("There is no music loaded right now.")

    key_regexes = {'(?i).*?(?=continue)+.+?(?=playback)+.': action_continue_playback,
                   '(?i).*?(?=pause)+.': action_play,
                   '(?i).*?(?=play)+.': action_play,
                   '(?i).*?(?=next)+.': action_next,
                   '(?i).*?(?=stop)+.': action_pause,
                   '(?i).*?(?=what)+.+?(?=song)+.': action_song_info}




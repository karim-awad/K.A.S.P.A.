from mpd import MPDClient
import time
from Kaspa.config import Config


class MpdController:
    client = None
    instance = None
    VOLUME = 40

    class __MpdController:
        
        address = ''
        port = 0

        def __init__(self):
            config = Config.get_instance()
            self.address = config.get('mpd', 'address')
            self.port = config.get('mpd', 'port')
            self.client = MPDClient()
            self.client.connect(self.address, self.port)
            self.client.setvol(MpdController.VOLUME)
            self.client.disconnect()

        def play_beginning(self):
            self.client.connect(self.address, self.port)
            self.client.play(0)
            self.client.disconnect()
            return

        def play(self):
            self.client.connect(self.address, self.port)
            self.client.pause(0)
            self.client.disconnect()

        def pause(self):
            self.client.connect(self.address, self.port)
            self.client.pause(1)
            self.client.disconnect()

        def next(self):
            self.client.connect(self.address, self.port)
            self.client.next()
            self.client.disconnect()

        def stop(self):
            self.client.connect(self.address, self.port)
            self.client.stop()
            self.client.disconnect()

        def shuffle_on(self):
            self.client.connect(self.address, self.port)
            self.client.random(1)
            self.client.disconnect()

        def shuffle_off(self):
            self.client.connect(self.address, self.port)
            self.client.random(0)
            self.client.disconnect()

        def current_song(self):
            self.client.connect(self.address, self.port)
            song_dict = self.client.currentsong()
            if not bool(song_dict):
                self.client.disconnect()
                return None
            title = song_dict['title']
            artist = song_dict['artist']
            self.client.disconnect()
            return title, artist

        def play_playlist(self, playlist):
            self.client.connect(self.address, self.port)
            self.client.clear()
            self.client.load(playlist)
            self.client.shuffle()
            self.client.play(0)
            self.client.disconnect()

        def play_radio(self, uri):
            self.client.connect(self.address, self.port)
            self.client.clear()
            self.client.add(uri)
            self.client.play(0)
            self.client.disconnect()

        def get_state(self):
            self.client.connect(self.address, self.port)
            status = self.client.status()
            self.client.disconnect()
            return status

        def set_volume(self, volume):
            self.client.connect(self.address, self.port)
            self.client.setvol(volume)
            self.client.disconnect()

        def add_to_current(self, tids):
            self.client.connect(self.address, self.port)
            for tid in tids:
                self.client.findadd("Filename", tid)
            self.client.disconnect()

        def play_tids(self, tids, shuffle=False):
            self.client.connect(self.address, self.port)
            self.client.clear()
            self.client.disconnect()
            self.add_to_current(tids)
            self.client.connect(self.address, self.port)
            if shuffle:
                self.client.random(1)
                self.client.play(0)
                self.client.next()
            else:
                self.client.play(0)
            self.client.disconnect()

        def play_tid(self, tid, off=0):
            self.client.connect(self.address, self.port)
            self.client.clear()
            self.client.findadd("Filename", tid)
            self.client.seek(0, off)
            self.client.pause(0)
            self.client.disconnect()

        def set_sleep_timer(self, duration):
            # TODO implement non blocking waiting
            time.sleep(duration)
            self.client.connect(self.address, self.port)
            self.client.stop()
            self.client.disconnect()

    def __init__(self):
        pass

    @staticmethod
    def get_instance():
        if MpdController.instance is None:
            MpdController.instance = MpdController.__MpdController()
        return MpdController.instance

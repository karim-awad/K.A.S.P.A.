import wakeonlan
# from wakeonlan import wol
import time
import os
from Kaspa.config import Config


class PcControl(object):

    hostname = ''
    mac = ''
    user = ''

    def __init__(self):
        config = Config.get_instance()
        self.mac = config.get("pc", "mac")
        self.hostname = config.get("pc", "hostname")
        self.user = config.get("pc", "user")

    def on(self):
        # wol.send_magic_packet(self.mac)
        pass

    def off(self):
        os.system("ssh " + "root@" + self.hostname + " 'poweroff'")

    def ping(self):
        response = os.system("ping -q -c 1 " + self.hostname)

        if response == 0:
            return True
        else:
            return False

    def run_remote_command(self, command, force=True):
        self.on()
        if force:
            while not self.ping():
                time.sleep(1)
        remote_command = "ssh " + self.user + "@" + self.hostname + " '" + command + "' &"
        os.system(remote_command)

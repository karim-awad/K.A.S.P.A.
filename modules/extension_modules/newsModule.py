import urllib.request
from bs4 import BeautifulSoup as Bs
import subprocess
import threading
import os
from modules.abstract_modules.abstractBriefingModule import AbstractBriefingModule


class NewsModule(AbstractBriefingModule):
    key_regexes = ['(?i).*?(?=news)+.']

    module_name = "News"

    class Process(threading.Thread):
        def run(self):
            url = "https://www.tagesschau.de/100sekunden/"
            response = urllib.request.urlopen(url).read()
            soup = Bs(response, "lxml")
            videos = soup.find("div", "controls")
            href = videos.find_all("a")
            newest_url = href[0]['href']
            video = urllib.request.urlopen(newest_url).read()

            file = open("/tmp/tagesschau.mp4", "wb")
            file.write(video)
            file.close()

            command = "ffmpeg -i /tmp/tagesschau.mp4 -ab 160k -ac 2 -ar 44100 -vn /tmp/audio.wav"
            devnull = open(os.devnull, 'w')
            subprocess.call(command, shell=True, stderr=devnull, stdout=devnull, stdin=devnull)
            devnull.close()

    def action(self, query):
        communicator = query.get_communicator()
        t = self.Process()
        t.start()
        communicator.say("I'll now play today's latest episode of Tagesschau in 100 Sekunden")
        t.join()
        devnull = open(os.devnull, 'w')
        subprocess.call("play /tmp/audio.wav", shell=True, stderr=devnull, stdout=devnull, stdin=devnull)
        subprocess.call("rm -f /tmp/audio.wav /tmp/tagesschau.mp4", shell=True, stderr=devnull, stdout=devnull,
                        stdin=devnull)
        devnull.close()

from Kaspa.modules.abstract_modules.abstractBriefingSubmodule import AbstractBriefingSubmodule
from bs4 import BeautifulSoup as Bs
import subprocess
import threading
import os
import urllib.request


class NewsModuleDe(AbstractBriefingSubmodule):
    module_name = "News"

    language = "de"

    key_regexes = dict()

    def __init__(self):
        self.key_regexes = {'((?i).*?(?=nachrichten)+.)|'
                            '((?i).*?(?=was)+.+?(?=gibt)+.+?(?=neues)+.)': self.action}

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
        if communicator.is_text_based():
            communicator.say(
                "Hier sind die neusten Spiegel Online Nachrichten: \n\n" + self.main_module.read_rss(
                    "http://www.spiegel.de/schlagzeilen/tops/index.rss"))
        else:
            t = self.Process()
            t.start()
            communicator.say("Ich spiele jetzt die neuste Ausgabe der Tagesschau in 100 Sekunden.")
            t.join()
            devnull = open(os.devnull, 'w')
            subprocess.call("play /tmp/audio.wav", shell=True, stderr=devnull, stdout=devnull, stdin=devnull)
            subprocess.call("rm -f /tmp/audio.wav /tmp/tagesschau.mp4", shell=True, stderr=devnull, stdout=devnull,
                            stdin=devnull)
            devnull.close()

    def briefing_action(self, query):
        self.action(query)
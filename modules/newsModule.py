import urllib.request
from bs4 import BeautifulSoup as Bs
import subprocess
import threading
from abstractModule import AbstractModule


class NewsModule(AbstractModule):

    key_regexes = ['(?i).*?(?=news)+.']

    module_name = "News"

    class Process(threading.Thread):
        def run(self):
            url = "https://www.tagesschau.de/100sekunden/"
            response = urllib.request.urlopen(url).read()
            soup = Bs(response)
            videos = soup.find("div", "controls")
            href = videos.find_all("a")
            newest_url = href[0]['href']
            video = urllib.request.urlopen(newest_url).read()

            file = open("/tmp/tagesschau.mp4", "wb")
            file.write(video)
            file.close()

            command = "ffmpeg -i /tmp/tagesschau.mp4 -ab 160k -ac 2 -ar 44100 -vn /tmp/audio.wav"
            subprocess.call(command, shell=True)

    def action(self, query):
        communicator = query.get_communicator()
        t = self.Process()
        t.start()
        communicator.say("I'll now play today's latest news briefing:")
        t.join()
        subprocess.call("play audio.wav", shell=True)




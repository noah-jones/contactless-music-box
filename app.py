#!/usr/bin/env python3

import nfc
import os
import time
import subprocess
from urllib.parse import urlparse



class Reader():
    def __init__(self):
        self.music_controller = MusicController()

    def on_connect(self, tag):
        print(tag)
        self.music_controller.play(tag.ndef.records[0].uri)
        return True

    def on_disconnect(self):
        print('tag removed')
        self.music_controller.stop()

class MusicController:

    def __init__(self):
        print('music')

        self.p = None

    def play(self, url):
        print('playing')
        print(url)

        youtube_code = urlparse(url).path[1:].split('/')[-1]
        print(youtube_code)
        folder = '/var/lib/youtube'
        for file_ in os.listdir(folder):
            if youtube_code in file_:
                filename = file_
                break
        else:
            print('downloading')
            subprocess.run(['youtube-dl', '-o', folder+'/%(id)s.%(ext)s', '-x', youtube_code])
            for file_ in os.listdir(folder):
                if youtube_code in file_:
                    filename = file_
                    break

        print('playing')
        print(url)

        self.p = subprocess.Popen(['mplayer', os.path.join(folder, filename)],
                stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

    def stop(self):
        print('stopping')

        self.p.kill()

clf = nfc.ContactlessFrontend('tty:S0')

reader = Reader()

while True:
    print('listening')

    connection = clf.connect(rdwr={'on-connect': reader.on_connect})

    reader.on_disconnect()

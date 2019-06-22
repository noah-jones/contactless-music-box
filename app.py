#!/usr/bin/env python3

import os
import time
import subprocess
from urllib.parse import urlparse

from smartcard.CardConnectionObserver import ConsoleCardConnectionObserver
from smartcard.CardMonitoring import CardMonitor, CardObserver
from smartcard.util import toHexString


GET_UID = [0xFF, 0xCA, 0x00, 0x00, 0x00]
LOAD_KEY = [0xFF, 0x82, 0x00, 0x00, 0x06, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
AUTHENTICATE = [0xFF, 0x86, 0x00, 0x00, 0x05, 0x01, 0x00, 0x04, 0x60, 0x00]     # block 4
GET_BLOCK_4 = [0xFF, 0xB0, 0x00, 0x04, 0x10]
GET_BLOCK_5 = [0xFF, 0xB0, 0x00, 0x05, 0x10]
GET_BLOCK_6 = [0xFF, 0xB0, 0x00, 0x06, 0x10]

class MusicController:

    def __init__(self):
        print('music')

        self.p = None

    def play(self, url):
        print('playing')
        print(url)

        youtube_code = urlparse(url).path[1:]
        print(youtube_code)
        print('playing')
        print(url)

        self.p = subprocess.Popen(['mplayer', 'brothers.opus'])

    def stop(self):
        print('stopping')

        self.p.kill()

class PrintObserver(CardObserver):

    def __init__(self, controller):
        self.observer = ConsoleCardConnectionObserver()
        self.controller = controller

    def update(self, observable, actions):
        (addedcards, removedcards) = actions
        for card in addedcards:
            print('+++++', toHexString(card.atr))

            card.connection = card.createConnection()
            card.connection.connect()
            print('connected')
            card.connection.addObserver(self.observer)

            apdu = LOAD_KEY
            response, sw1, sw2 = card.connection.transmit(apdu)

            apdu = AUTHENTICATE
            response, sw1, sw2 = card.connection.transmit(apdu)

            payload = ''
            apdu = GET_BLOCK_4
            response, sw1, sw2 = card.connection.transmit(apdu)
            payload += ''.join([str(chr(_)) for _ in response])
            apdu = GET_BLOCK_5
            response, sw1, sw2 = card.connection.transmit(apdu)
            payload += ''.join([str(chr(_)) for _ in response])
            apdu = GET_BLOCK_6
            response, sw1, sw2 = card.connection.transmit(apdu)
            payload += ''.join([str(chr(_)) for _ in response])
            print('payload')
            print(payload)
            self.controller.play(payload)

        for card in removedcards:
            print('-----', toHexString(card.atr))
            self.controller.stop()

if __name__ == '__main__':

    controller = MusicController()

    card_monitor = CardMonitor()
    card_observer = PrintObserver(controller)
    card_monitor.addObserver(card_observer)

    try:
        while True:
            time.sleep(1)
    except Exception as e:
        card_monitor.deleteObserver(card_observer)
        raise e

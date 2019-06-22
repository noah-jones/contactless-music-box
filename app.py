#!/usr/bin/env python3

import time

from smartcard.CardConnectionObserver import ConsoleCardConnectionObserver
from smartcard.CardMonitoring import CardMonitor, CardObserver
from smartcard.util import toHexString


GET_UID = [0xFF, 0xCA, 0x00, 0x00, 0x00]
LOAD_KEY = [0xFF, 0x82, 0x00, 0x00, 0x06, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
AUTHENTICATE = [0xFF, 0x86, 0x00, 0x00, 0x05, 0x01, 0x00, 0x04, 0x60, 0x00]     # block 4
GET_BLOCK_4 = [0xFF, 0xB0, 0x00, 0x04, 0x10]
GET_BLOCK_5 = [0xFF, 0xB0, 0x00, 0x05, 0x10]
GET_BLOCK_6 = [0xFF, 0xB0, 0x00, 0x06, 0x10]


class PrintObserver(CardObserver):

    def __init__(self):
        self.observer = ConsoleCardConnectionObserver()

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
            print(response)

            apdu = AUTHENTICATE
            response, sw1, sw2 = card.connection.transmit(apdu)
            print(response)

            apdu = GET_BLOCK_4
            response, sw1, sw2 = card.connection.transmit(apdu)
            print(response)
            apdu = GET_BLOCK_5
            response, sw1, sw2 = card.connection.transmit(apdu)
            print(response)
            apdu = GET_BLOCK_6
            response, sw1, sw2 = card.connection.transmit(apdu)
            print(response)

        for card in removedcards:
            print('-----', toHexString(card.atr))

if __name__ == '__main__':

    card_monitor = CardMonitor()
    card_observer = PrintObserver()
    card_monitor.addObserver(card_observer)

    try:
        while True:
            time.sleep(1)
    except Exception as e:
        card_monitor.deleteObserver(card_observer)
        raise e

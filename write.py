#!/usr/bin/env python3

import nfc
import ndef
import sys

assert sys.argv[1]

clf = nfc.ContactlessFrontend('tty:S0')

tag = clf.connect(rdwr={'on-connect': lambda tag: False})

print('before')
for record in tag.ndef.records:
    print(record)
    print(record.uri)

print('after')
tag.ndef.records = [ndef.UriRecord('https://youtu.be/'+sys.argv[1])]

clf.close()

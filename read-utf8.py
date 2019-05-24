#!/usr/bin/env python
import fileinput
import math
import sys
import unicodedata
JUSTIFICATION = 6 # right-justified
UTF8 = "utf-8"
CONTROL_CHARACTER_DICT = {
    "\r": "CARRIAGE RETURN",
    "\n": "LINE FEED",
    "\t": "TAB",
    "\0": "NULL",
}

character_count = 1
for line in fileinput.input(openhook=fileinput.hook_encoded(UTF8)):
    for char in line:
        if char in CONTROL_CHARACTER_DICT:
            name = CONTROL_CHARACTER_DICT[char]
            length = 1
        else:
            byte_representation = bytes(char, UTF8)
            name = unicodedata.name(char, byte_representation)
            length = len(byte_representation)
        print(str(character_count+1).rjust(JUSTIFICATION) + ". {name} ({length} byte)".format(**locals()))
        character_count += 1

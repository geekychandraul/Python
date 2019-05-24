#!/usr/bin/env python
import base64
import fileinput
import os
import sys
UTF8 = "utf-8"

s = "".join([line for line in fileinput.input()])
bytes_ = bytes(s, UTF8)
base64_bytes = base64.b64decode(bytes_)
print(base64_bytes.decode(UTF8))

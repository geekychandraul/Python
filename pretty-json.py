#!/usr/bin/env python
import json
import sys

if len(sys.argv) > 1:
    data = json.loads(open(sys.argv[1]).read())
else:
    data = json.loads(sys.stdin.read())

print(json.dumps(data, sort_keys=True, indent=4))

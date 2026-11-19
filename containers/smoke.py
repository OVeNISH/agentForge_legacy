"""Trivial CP0 runtime smoke script, compatible with Python 2.7 and 3.12."""
from __future__ import print_function

import json
import sys

print(json.dumps({"python": sys.version, "message": "runtime ready"}, sort_keys=True))

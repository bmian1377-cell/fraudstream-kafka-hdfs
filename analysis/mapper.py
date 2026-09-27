#!/usr/bin/env python3
import sys
import json

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    try:
        record = json.loads(line)
    except json.JSONDecodeError:
        continue
    label = record.get("Class")
    amount = record.get("Amount")
    if label is None or amount is None:
        continue
    print(f"{int(label)}\t{amount}")
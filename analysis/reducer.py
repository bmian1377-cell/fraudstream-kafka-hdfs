#!/usr/bin/env python3
import sys

counts = {0: 0, 1: 0}
sums = {0: 0.0, 1: 0.0}

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    label_str, amount_str = line.split("\t")
    label = int(label_str)
    amount = float(amount_str)
    counts[label] += 1
    sums[label] += amount

for label in sorted(counts.keys()):
    count = counts[label]
    total = sums[label]
    avg = total / count if count > 0 else 0
    name = "Fraud" if label == 1 else "Normal"
    print(f"{name}\tcount={count}\ttotal_amount={total:.2f}\tavg_amount={avg:.2f}")
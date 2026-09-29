#!/bin/sh
cd "$(dirname "$0")"
for c in sg3524_buck sg3524_boost sg3524_inversor sg3524_pushpull; do
  python3 fra_ngspice.py configs/$c.py > /tmp/claude-0/-home-user-LTSpice-behavioral-IC-lib/782f8df8-45b1-5aa5-b3e8-e444247c9888/scratchpad/fra_$c.log 2>&1
done

#!/bin/sh
# roda as configs dadas (ou todas do SG3524), log em $LOGDIR
cd "$(dirname "$0")"
LOGDIR=${LOGDIR:-/tmp}
for c in ${@:-sg3524_buck sg3524_boost sg3524_inversor sg3524_pushpull}; do
  python3 fra_ngspice.py configs/$c.py > $LOGDIR/fra_$c.log 2>&1
done

#!/bin/sh
# Regression tests for the UC3854 behavioural model.
#
# The model itself (../UC3854.lib) is written for LTspice.  ngspice needs the
# PSpice-style "PARAMS:" keyword on the .subckt line before the default
# parameter list, so the runner generates uc3854_ng.lib from it.  That one
# keyword is the only difference between the two.
#
# Usage:  cd tests && ./run_tests.sh
set -e
cd "$(dirname "$0")"
command -v ngspice >/dev/null || { echo "ngspice not found"; exit 1; }
sed 's/^\.SUBCKT UC3854 \(.*\)$/.SUBCKT UC3854 \1 PARAMS:/' ../UC3854.lib > uc3854_ng.lib
fail=0
for f in 0*.cir; do
  out=$(ngspice -b "$f" 2>&1 | tr '\r' '\n')
  echo "$out" | grep -aE '^(--- test|PASS |FAIL )' || true
  n=$(echo "$out" | grep -ac '^FAIL' || true)
  fail=$((fail + n))
  if ! echo "$out" | grep -aq '^PASS'; then
    echo "FAIL $f produced no results"; fail=$((fail + 1))
  fi
done
echo
if [ "$fail" -eq 0 ]; then
  echo "ALL TESTS PASSED"
else
  echo "$fail TEST(S) FAILED"
  exit 1
fi

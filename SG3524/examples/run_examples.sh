#!/bin/sh
# Roda todos os exemplos no ngspice e confere o resultado.
# (Os .cir sao escritos para LTspice; a unica diferenca e a palavra PARAMS:
#  na linha .subckt, que ../tests/run_tests.sh gera em sg3524_ng.lib.)
set -e
cd "$(dirname "$0")"
command -v ngspice >/dev/null || { echo "ngspice nao encontrado"; exit 1; }
sed 's/^\.SUBCKT SG3524 \(.*\)$/.SUBCKT SG3524 \1 PARAMS:/' ../SG3524.lib > ../tests/sg3524_ng.lib
mkdir -p .run
fail=0
for f in *.cir; do
  sed 's|\.include \.\./SG3524\.lib|.include ../../tests/sg3524_ng.lib|' "$f" > ".run/$f"
  cat "checks/${f%.cir}.ctl" >> ".run/$f" 2>/dev/null || echo ".end" >> ".run/$f"
  out=$(cd .run && ngspice -b "$f" 2>&1 | tr '\r' '\n')
  echo "=== $f ==="
  echo "$out" | grep -aE '^(PASS|FAIL|RESULT)' || true
  if echo "$out" | grep -qai "timestep too small"; then
    echo "FAIL  simulacao abortou (timestep too small)"; fail=$((fail+1))
  fi
  fail=$((fail + $(echo "$out" | grep -ac '^FAIL' || true)))
done
echo
[ "$fail" -eq 0 ] && echo "TODOS OS EXEMPLOS OK" || { echo "$fail FALHA(S)"; exit 1; }

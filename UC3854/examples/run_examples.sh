#!/bin/sh
# Roda todos os exemplos no ngspice e confere o resultado.
# (Os .cir sao escritos para LTspice; a unica diferenca e a palavra PARAMS:
#  na linha .subckt, que o script gera em ../tests/uc3854_ng.lib.)
# Os dois PFC de 250 W levam alguns minutos cada.
set -e
cd "$(dirname "$0")"
command -v ngspice >/dev/null || { echo "ngspice nao encontrado"; exit 1; }
sed 's/^\.SUBCKT UC3854 \(.*\)$/.SUBCKT UC3854 \1 PARAMS:/' ../UC3854.lib > ../tests/uc3854_ng.lib
mkdir -p .run
fail=0
for f in ${1:-*.cir}; do
  sed 's|\.include \.\./UC3854\.lib|.include ../../tests/uc3854_ng.lib|' "$f" | sed '/^\.end$/d' > ".run/$f"
  cat "checks/${f%.cir}.ctl" >> ".run/$f" 2>/dev/null || echo ".end" >> ".run/$f"
  out=$(cd .run && ngspice -b "$f" 2>&1 | tr '\r' '\n')
  echo "=== $f ==="
  echo "$out" | grep -aE '^(PASS|FAIL|RESULT)|^[a-z0-9_]+ += ' | grep -avE ' at= | from= | targ= ' || true
  if echo "$out" | grep -qai "timestep too small"; then
    echo "FAIL  simulacao abortou (timestep too small)"; fail=$((fail+1))
  fi
  if ! echo "$out" | grep -qa '^PASS'; then
    [ -f "checks/${f%.cir}.ctl" ] && { echo "FAIL  sem resultado"; fail=$((fail+1)); }
  fi
  fail=$((fail + $(echo "$out" | grep -ac '^FAIL' || true)))
done
echo
[ "$fail" -eq 0 ] && echo "TODOS OS EXEMPLOS OK" || { echo "$fail FALHA(S)"; exit 1; }

.control
set noaskquit
run
let vo = v(vout)-v(rtn)
meas tran vdc AVG vo from=7m to=8.9m
meas tran vnd AVG vo from=12.5m to=13.9m
echo "RESULT buck"
print vdc vnd
if (abs(vdc/5.0-1) < 0.05) & (abs(vnd/5.0-1) < 0.06)
  echo "PASS  regula 5 V com 1 A e mantem apos o degrau para 2 A"
else
  echo "FAIL  regulacao do buck"
end
quit
.endc
.end

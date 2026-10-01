.control
set noaskquit
run
let vo = v(vout)-v(rtn)
meas tran vdc AVG vo from=16m to=19.9m
echo "RESULT boost"
print vdc
if (abs(vdc/24.0-1) < 0.06)
  echo "PASS  eleva 12 V para 24 V em malha fechada"
else
  echo "FAIL  regulacao do boost"
end
quit
.endc
.end

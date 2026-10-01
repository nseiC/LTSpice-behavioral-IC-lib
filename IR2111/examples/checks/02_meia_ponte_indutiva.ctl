.control
set noaskquit
run
let vh = v(ho)-v(sw)
let vbs = v(vb)-v(sw)
meas tran ipk MAX i(L1) from=0.8m to=1m
meas tran ivl MIN i(L1) from=0.8m to=1m
* tempo morto no no de comutacao: LO cai -> sw sobe -> HO sobe
meas tran tlo WHEN v(lo)=7.5 FALL=LAST
meas tran tsw WHEN v(sw)=100 RISE=LAST
meas tran tho WHEN vh=7.5 RISE=LAST
meas tran vbsm MIN vbs from=0.8m to=1m
echo "RESULT corrente na carga de $&ivl a $&ipk A; VBS min $&vbsm V"
echo "RESULT LO desliga em $&tlo, o no de comutacao vira em $&tsw (diodo de corpo), HO liga em $&tho"
if (ipk > 0.5) & (abs(ipk+ivl) < 0.1) & (tsw > tlo) & (tho > tsw) & (vbsm > 12)
  echo "PASS  meia-ponte: o no vira durante o tempo morto, antes do outro MOSFET ligar"
else
  echo "FAIL  meia-ponte indutiva"
end
quit
.endc
.end

.control
set noaskquit
save v(out) i(Vio) i(Vbus) v(lvg) v(css) v(isen)
run
* janela de medida: o ultimo 1 ms
let ta = 79m
let tb = 80m
meas tran vo AVG v(out) from=$&ta to=$&tb
meas tran io AVG i(Vio) from=$&ta to=$&tb
meas tran ib AVG i(Vbus) from=$&ta to=$&tb
let po = vo*io
let pin = -400*ib
let eta = po/pin*100
meas tran t1 WHEN v(lvg)=6 RISE=1 from=$&ta
meas tran t2 WHEN v(lvg)=6 RISE=101 from=$&ta
let fsw = 100/(t2-t1)
meas tran f1 WHEN v(lvg)=6 RISE=2
meas tran f2 WHEN v(lvg)=6 RISE=12
let fst = 10/(f2-f1)
meas tran vis MAX v(isen) from=$&ta to=$&tb
echo "RESULT LLC 150 W"
print vo io po pin eta fsw fst vis
if (vo > 11.9) & (vo < 12.3) & (fsw > 105k) & (fsw < 140k) & (eta > 90) & (fst > 200k) & (vis < 0.8)
  echo "PASS  12 V / 12.5 A, ~120 kHz (AN3233: 'about 120 kHz'), soft-start a partir de ~250 kHz, sem OCP"
else
  echo "FAIL  LLC 150 W"
end
quit
.endc
.end

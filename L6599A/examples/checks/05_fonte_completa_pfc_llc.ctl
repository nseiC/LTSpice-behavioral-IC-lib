.control
set noaskquit
save v(line) v(lr) i(Vline) v(bus) v(out) i(Vio)
run
* janela: os dois ultimos ciclos da rede (60 Hz)
let tb = 76m
let ta = tb-2/60
meas tran vb AVG v(bus) from=$&ta to=$&tb
meas tran vo AVG v(out) from=$&ta to=$&tb
meas tran io AVG i(Vio) from=$&ta to=$&tb
let vl = v(line)-v(lr)
let il = -i(Vline)
let pinst = vl*il
let i2 = il*il
let v2 = vl*vl
meas tran pin AVG pinst from=$&ta to=$&tb
meas tran ims AVG i2 from=$&ta to=$&tb
meas tran vms AVG v2 from=$&ta to=$&tb
let irms = sqrt(ims)
let pf = pin/(sqrt(vms)*irms)
let is = il*sin(2*pi*60*time)
let ic = il*cos(2*pi*60*time)
meas tran ia AVG is from=$&ta to=$&tb
meas tran ib AVG ic from=$&ta to=$&tb
let i1rms = sqrt(2*(ia*ia+ib*ib))
let h2 = 0
let n = 2
while n <= 40
  let sn = il*sin(2*pi*60*n*time)
  let cn = il*cos(2*pi*60*n*time)
  meas tran an AVG sn from=$&ta to=$&tb
  meas tran bn AVG cn from=$&ta to=$&tb
  let h2 = h2 + 2*(an*an+bn*bn)
  let n = n + 1
end
let thd = sqrt(h2)/i1rms*100
let po = vo*io
let eta = po/pin*100
echo "RESULT fonte completa"
print vb vo io po pin eta pf thd
if (vb > 380) & (vb < 420) & (vo > 11.9) & (vo < 12.3) & (pf > 0.97) & (thd < 10) & (eta > 85)
  echo "PASS  115 VCA -> 400 V -> 12 V / 150 W com FP > 0.97"
else
  echo "FAIL  fonte completa"
end
quit
.endc
.end

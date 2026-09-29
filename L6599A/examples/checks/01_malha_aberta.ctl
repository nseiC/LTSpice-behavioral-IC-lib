.control
set noaskquit
save v(cf) v(lvg) v(hvg) v(css) v(rfmin) i(Vrf)
run
* frequencia no inicio do soft-start, em regime (fmin) e com 400 uA do opto
meas tran a1 WHEN v(cf)=2 RISE=2
meas tran a2 WHEN v(cf)=2 RISE=6
let fst = 4/(a2-a1)
meas tran b1 WHEN v(cf)=2 RISE=1 from=7.5m
meas tran b2 WHEN v(cf)=2 RISE=21 from=7.5m
let fmn = 20/(b2-b1)
meas tran c1 WHEN v(cf)=2 RISE=1 from=11.9m
meas tran c2 WHEN v(cf)=2 RISE=11 from=11.9m
let fmx = 10/(c2-c1)
let fsteq = 1/(3*470p*(12k*6.2k/18.2k))
let fmneq = 1/(3*470p*12k)
let fmxeq = fmneq*(2/12k+400u)/(2/12k)
* tempo morto e duty
meas tran l1 WHEN v(lvg)=6.65 RISE=1 from=7m
meas tran l2 WHEN v(lvg)=6.65 FALL=1 from=$&l1
meas tran h1 WHEN v(hvg)=6.65 RISE=1 from=$&l2
meas tran h2 WHEN v(hvg)=6.65 FALL=1 from=$&h1
let td = h1-l2
let d = (l2-l1)/((l2-l1)+(h2-h1))*100
echo "RESULT malha aberta"
print fst fsteq fmn fmneq fmx fmxeq td d
if (abs(fst/fsteq-1) < 0.06) & (abs(fmn/fmneq-1) < 0.03) & (abs(fmx/fmxeq-1) < 0.06) & (td > 0.25u) & (td < 0.35u) & (abs(d-50) < 1)
  echo "PASS  fstart, fmin e fmax seguem as Eq. 1/4; tempo morto 0.3 us; duty 50 %"
else
  echo "FAIL  malha aberta"
end
quit
.endc
.end

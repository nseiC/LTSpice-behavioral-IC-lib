.control
set noaskquit
save v(out) v(delay) v(lvg) v(isen) v(css) v(pfcstop) i(Vio)
run
meas tran vpre AVG v(out) from=69m to=70m
meas tran t35 WHEN v(delay)=3.5 RISE=1 from=70m
meas tran t2  WHEN v(delay)=2.05 RISE=1 from=70m
let ta = t35+0.1m
let tb = t35+20m
meas tran lof MAX v(lvg) from=$&ta to=$&tb
meas tran pfs MAX v(pfcstop) from=$&ta to=$&tb
meas tran trs WHEN v(lvg)=6 RISE=1 from=$&tb
let tstop = trs-t35
let tstopc = 220k*47n*ln(3.5/0.33)
let tsh = t35-15m
echo "RESULT sobrecarga"
print vpre t2 t35 tsh lof pfs tstop tstopc
if (vpre > 11.5) & (lof < 0.5) & (pfs < 0.5) & (abs(tstop/tstopc-1) < 0.1)
  echo "PASS  sobrecarga: OCP, DELAY chega a 3.5 V, CI para (PFC_STOP baixo) e reparte em TSTOP = RC ln(3.5/0.33)"
else
  echo "FAIL  sobrecarga"
end
quit
.endc
.end

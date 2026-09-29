.control
set noaskquit
run
meas tran per  TRIG v(ct) VAL=3 RISE=3 TARG v(ct) VAL=3 RISE=4
meas tran dead TRIG v(x1.n_blk) VAL=0.5 RISE=3 TARG v(x1.n_blk) VAL=0.5 FALL=3
let csum = v(ca)+v(cb)
meas tran ovl MIN csum from=0.1m to=3.9m
if (abs(per/100e-6-1) < 0.05) & (abs(dead/0.5e-6-1) < 0.15) & (ovl > 20)
  echo "PASS  periodo RT*CT, tempo morto 0.5 us, saidas nunca sobrepostas"
else
  echo "FAIL  oscilador/blanking"
end
quit
.endc
.end

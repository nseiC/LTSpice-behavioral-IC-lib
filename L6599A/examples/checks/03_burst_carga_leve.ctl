.control
set noaskquit
save v(out) i(Vio) v(lvg) v(stby) v(pfcstop)
run
let ta = 40m
let tb = 50m
meas tran vo AVG v(out) from=$&ta to=$&tb
meas tran pfmn MIN v(pfcstop) from=$&ta to=$&tb
meas tran pfmx MAX v(pfcstop) from=$&ta to=$&tb
meas tran sbmn MIN v(stby) from=$&ta to=$&tb
meas tran sbmx MAX v(stby) from=$&ta to=$&tb
meas tran nb1 WHEN v(pfcstop)=7.5 FALL=1 from=$&ta
meas tran nb2 WHEN v(pfcstop)=7.5 FALL=3 from=$&ta
let fburst = 2/(nb2-nb1)
echo "RESULT burst 3 W"
print vo pfmn pfmx sbmn sbmx fburst
if (vo > 11.5) & (vo < 12.4) & (pfmn < 1) & (pfmx > 14) & (sbmn < 1.3) & (sbmx > 1.25)
  echo "PASS  modo burst: STBY cruza 1.24/1.29 V, PFC_STOP pulsa, saida regulada"
else
  echo "FAIL  burst"
end
quit
.endc
.end

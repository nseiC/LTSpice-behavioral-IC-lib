.control
set noaskquit
save v(ct) v(gtdrv) v(mult) v(caout) i(Viac)
run
meas tran t1 WHEN v(ct)=3 RISE=100
meas tran t2 WHEN v(ct)=3 RISE=150
let f = 50/(t2-t1)
meas tran g0 MAX v(gtdrv) from=0.1m to=0.25m
meas tran g1 WHEN v(gtdrv)=7 RISE=1 from=4.05m
let g1b = g1+10n
meas tran g2 WHEN v(gtdrv)=7 FALL=1 from=$&g1b
meas tran g3 WHEN v(gtdrv)=7 RISE=1 from=$&g1b
let dmax = (g2-g1)/(g3-g1)*100
meas tran imo MAX v(mult) from=4.2m to=8.4m
let imou = imo*1e6/1e3
echo "RESULT malha aberta"
print f g0 dmax imou
if (abs(f/55e3-1) < 0.05) & (g0 < 0.5) & (abs(dmax-95) < 2) & (abs(imou-250) < 5)
  echo "PASS  55 kHz, duty 0 % com CA Out < 1.1 V, ~95 % no maximo, Imo limitado em 3.75 V/RSET = 250 uA"
else
  echo "FAIL  malha aberta"
end
quit
.endc
.end

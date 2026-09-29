.control
set noaskquit
run
meas tran vcm AVG v(vc) from=3m to=4m
meas tran pv TRIG v(vco) VAL=2.5 RISE=300 TARG v(vco) VAL=2.5 RISE=380
meas tran tr WHEN v(ref)=2.5 RISE=1 TD=3.5m
meas tran tv WHEN v(vco)=2.5 RISE=1 TD=$&tr
let fv = 80/pv
let ph = 360*(tv-tr)*100k
echo "RESULT VCO = $&fv Hz, V(vc) = $&vcm V, atraso de fase = $&ph graus"
if (abs(fv/100k-1) < 0.002) & (abs(vcm-3.5) < 0.05) & ((abs(ph-126) < 5) | (abs(ph-234) < 5))
  echo "PASS  PLL travado em 100 kHz, V(vc) = 3,5 V, defasagem 126 graus"
else
  echo "FAIL  PLL nao travou"
end
quit
.endc
.end

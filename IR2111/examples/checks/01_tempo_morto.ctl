.control
set noaskquit
run
let vh = v(ho)-v(vs)
meas tran ton TRIG v(in) VAL=7.5 RISE=1 TARG vh VAL=1.5 RISE=1
meas tran toff TRIG v(in) VAL=7.5 FALL=1 TARG vh VAL=13.5 FALL=1
meas tran tr  TRIG vh VAL=1.5 RISE=1 TARG vh VAL=13.5 RISE=1
meas tran tf  TRIG vh VAL=13.5 FALL=1 TARG vh VAL=1.5 FALL=1
meas tran dt1 TRIG v(lo) VAL=13.5 FALL=1 TARG vh VAL=1.5 RISE=1
meas tran dt2 TRIG vh VAL=13.5 FALL=1 TARG v(lo) VAL=1.5 RISE=1
meas tran hshort MAX vh from=12u to=16u
echo "RESULT ton $&ton  toff $&toff  tr $&tr  tf $&tf"
echo "RESULT tempo morto LO->HO $&dt1 s, HO->LO $&dt2 s; HO no pulso de 400 ns: $&hshort V"
if (abs(ton/850n-1) < 0.01) & (abs(toff/150n-1) < 0.02) & (abs(dt1/700n-1) < 0.02) & (abs(dt2/700n-1) < 0.02) & (hshort < 0.1)
  echo "PASS  tipicos do datasheet (850 / 150 / 80 / 40 ns, DT 700 ns); pulso curto engolido"
else
  echo "FAIL  tempos / tempo morto"
end
quit
.endc
.end

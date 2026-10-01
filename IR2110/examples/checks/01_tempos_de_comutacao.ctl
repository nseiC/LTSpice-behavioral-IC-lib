.control
set noaskquit
run
let vh = v(ho)-v(vs)
let vh2 = v(ho2)-v(vs2)
meas tran ton TRIG v(in) VAL=7.5 RISE=1 TARG vh VAL=1.5 RISE=1
meas tran tr  TRIG vh VAL=1.5 RISE=1 TARG vh VAL=13.5 RISE=1
meas tran toff TRIG v(in) VAL=7.5 FALL=1 TARG vh VAL=13.5 FALL=1
meas tran tf  TRIG vh VAL=13.5 FALL=1 TARG vh VAL=1.5 FALL=1
meas tran tonl TRIG v(in) VAL=7.5 RISE=1 TARG v(lo) VAL=1.5 RISE=1
meas tran toffl TRIG v(in) VAL=7.5 FALL=1 TARG v(lo) VAL=13.5 FALL=1
meas tran ton2 TRIG v(in) VAL=7.5 RISE=1 TARG vh2 VAL=1.5 RISE=1
echo "RESULT HO: ton $&ton  toff $&toff  tr $&tr  tf $&tf"
echo "RESULT LO: ton $&tonl  toff $&toffl;  HO a 400 V: ton $&ton2"
if (abs(ton/120n-1) < 0.02) & (abs(toff/94n-1) < 0.02) & (abs(tr/25n-1) < 0.02) & (abs(tf/17n-1) < 0.02) & (abs(ton-tonl) < 10n) & (abs(ton2-ton) < 1n)
  echo "PASS  tipicos do datasheet: 120 / 94 / 25 / 17 ns, MT < 10 ns, igual com VS = 400 V"
else
  echo "FAIL  tempos de comutacao"
end
quit
.endc
.end

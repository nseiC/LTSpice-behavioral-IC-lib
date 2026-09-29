.control
set noaskquit
run
meas tran per5 TRIG v(y1) VAL=2.5 RISE=5 TARG v(y1) VAL=2.5 RISE=6
meas tran dev AVG v(y1) from=7u to=9u
meas tran tpd TRIG v(y1) VAL=2.5 RISE=5 TARG v(y2) VAL=2.5 FALL=5
let f5 = 1/per5
let parou = (dev lt 0.1) | (dev gt 4.9)
* guarda os resultados de 5 V antes de trocar de plot
set f5v = "$&f5"
set tpv = "$&tpd"
set parv = "$&parou"
alterparam vc = 3
reset
run
meas tran per3 TRIG v(y1) VAL=1.5 RISE=5 TARG v(y1) VAL=1.5 RISE=6
let f3 = 1/per3
echo "RESULT 5 V: f = $f5v Hz (tpd por estagio $tpv s);  3 V: f = $&f3 Hz"
if ($f5v > 5e6) & ($f5v < 20e6) & (f3 < $f5v/2) & ($parv > 0.5)
  echo "PASS  oscila com EN=1, para com EN=0, frequencia cai com VCC"
else
  echo "FAIL  oscilador em anel"
end
quit
.endc
.end

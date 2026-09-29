.control
set noaskquit
run
meas tran p1 TRIG v(y) VAL=2.5 RISE=3 TARG v(y) VAL=2.5 RISE=4
meas tran w1 TRIG v(y) VAL=2.5 RISE=3 TARG v(y) VAL=2.5 FALL=3
echo "RESULT periodo na saida $&p1 s, largura do pulso $&w1 s"
if (abs(p1/500n-1) < 0.02) & (w1 > 40n) & (w1 < 150n)
  echo "PASS  1 MHz na entrada -> 2 MHz na saida, um pulso por borda"
else
  echo "FAIL  dobrador"
end
quit
.endc
.end

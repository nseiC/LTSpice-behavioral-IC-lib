.control
set noaskquit
run
let vh = v(ho)-v(vs)
* pulsos de HIN: 2-7, 12-17, 22-27, 32-37, 42-47, 52-57, 62-67, 72-77 us
meas tran p1 FIND vh AT=5u
meas tran p2a FIND vh AT=13.5u
meas tran p2b MAX vh from=14.3u to=17u
meas tran p3 MAX vh from=22u to=27u
meas tran p4 MAX vh from=25.3u to=27u
meas tran p5 FIND vh AT=34u
meas tran p6a FIND vh AT=53.5u
meas tran p6b MAX vh from=54.5u to=57u
meas tran p7 FIND vh AT=64u
meas tran l4 MAX v(lo) from=25.3u to=27u
echo "RESULT HO nos pulsos 1, 2 (antes e depois do SD), 3, 4, 6 (antes e depois), 7: $&p1 , $&p2a , $&p2b , $&p3 , $&p5 , $&p6a , $&p6b , $&p7 V"
if (p1 > 14.9) & (p2a > 14.9) & (p2b < 0.1) & (p3 < 0.1) & (l4 < 0.1) & (p5 > 14.9) & (p6a > 14.9) & (p6b < 0.1) & (p7 > 14.9)
  echo "PASS  SD corta o pulso, segura enquanto alto, e a saida so volta na borda seguinte"
else
  echo "FAIL  desligamento ciclo a ciclo"
end
quit
.endc
.end

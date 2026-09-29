.control
set noaskquit
let nerr = 0
foreach ph 0 30 60 90 120 150 180
  alterparam fase = $ph
  reset
  run
  meas tran vm AVG v(med) from=6m to=8m
  let esp = 5*$ph/180
  echo "RESULT fase=$ph graus  V(med)=$&vm V  (ideal $&esp V)"
  if abs(vm - esp) > 0.06
    let nerr = nerr + 1
  end
end
if nerr = 0
  echo "PASS  V(med) = VCC*fase/180 em 0..180 graus (erro < 60 mV)"
else
  echo "FAIL  detector de fase ($&nerr pontos fora)"
end
quit
.endc
.end

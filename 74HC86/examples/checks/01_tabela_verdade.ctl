.control
set noaskquit
run
* amostra 400 ns depois de cada borda (saidas ja assentadas) e compara cada
* saida com A xor B calculado a partir das entradas no mesmo instante
let nerr = 0
let t = 0.65u
while t < 4.4u
  meas tran va FIND v(a) AT=$&t
  meas tran vb FIND v(b) AT=$&t
  meas tran w1 FIND v(y1) AT=$&t
  meas tran w2 FIND v(y2) AT=$&t
  meas tran w3 FIND v(y3) AT=$&t
  meas tran w4 FIND v(y4) AT=$&t
  let x = abs((va gt 2.5) - (vb gt 2.5))
  let e = 5*x
  if (abs(w1-e) > 0.1) | (abs(w2-e) > 0.1) | (abs(w3-e) > 0.1) | (abs(w4-e) > 0.1)
    let nerr = nerr + 1
  end
  echo "RESULT t=$&t A=$&va B=$&vb -> Y1=$&w1 Y2=$&w2 Y3=$&w3 Y4=$&w4"
  let t = t + 0.5u
end
if nerr = 0
  echo "PASS  Y = A xor B em LL, HL, LH, HH, nas quatro portas"
else
  echo "FAIL  tabela verdade ($&nerr amostras erradas)"
end
quit
.endc
.end

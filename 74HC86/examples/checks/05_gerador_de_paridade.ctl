.control
set noaskquit
run
let nerr = 0
let t = 0.65u
while t < 16.4u
  meas tran a0 FIND v(d0) AT=$&t
  meas tran a1 FIND v(d1) AT=$&t
  meas tran a2 FIND v(d2) AT=$&t
  meas tran a3 FIND v(d3) AT=$&t
  meas tran pp FIND v(p) AT=$&t
  let n = (a0 gt 2.5) + (a1 gt 2.5) + (a2 gt 2.5) + (a3 gt 2.5)
  let e = 5*(n - 2*floor(n/2))
  if abs(pp - e) > 0.1
    let nerr = nerr + 1
  end
  let t = t + 0.5u
end
if nerr = 0
  echo "PASS  paridade correta nas 16 combinacoes de D3..D0"
else
  echo "FAIL  paridade ($&nerr estados errados)"
end
quit
.endc
.end

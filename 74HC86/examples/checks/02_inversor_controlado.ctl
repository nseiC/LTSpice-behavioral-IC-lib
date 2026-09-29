.control
set noaskquit
run
meas tran b1 FIND v(y) AT=2.4u
meas tran b2 FIND v(y) AT=2.9u
meas tran i1 FIND v(y) AT=7.4u
meas tran i2 FIND v(y) AT=7.9u
* clk em 2.4u = alto, 2.9u = baixo (idem 7.4u / 7.9u)
if (b1 > 4.9) & (b2 < 0.1) & (i1 < 0.1) & (i2 > 4.9)
  echo "PASS  CTRL = 0 -> buffer, CTRL = 1 -> inversor"
else
  echo "FAIL  inversor controlado"
end
quit
.endc
.end

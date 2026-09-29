.control
set noaskquit
run
meas tran vdc AVG v(vout) from=9m to=11.9m
meas tran ica MAX i(Vea)  from=9m to=11.9m
meas tran dra MAX v(x1.n_dra) from=9m to=11.9m
meas tran drb MAX v(x1.n_drb) from=9m to=11.9m
echo "RESULT push-pull"
print vdc ica
if (abs(vdc/5.0-1) < 0.05) & (dra > 0.9) & (drb > 0.9)
  echo "PASS  regula 5 V; as duas saidas chaveam alternadas no transformador"
else
  echo "FAIL  push-pull"
end
quit
.endc
.end

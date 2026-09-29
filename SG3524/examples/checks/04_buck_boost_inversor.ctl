.control
set noaskquit
run
meas tran vdc AVG v(vout) from=12m to=14.9m
meas tran vni AVG v(ni)   from=12m to=14.9m
echo "RESULT buck-boost inversor"
print vdc vni
if (vdc < -11.0) & (vdc > -12.6) & (abs(vni-2.5) < 0.1)
  echo "PASS  inverte para tensao negativa, amplificador de erro em 2.5 V"
else
  echo "FAIL  regulacao do buck-boost"
end
quit
.endc
.end

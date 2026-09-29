.control
set noaskquit
run
meas tran p20 TRIG v(ct) VAL=3 RISE=4 TARG v(ct) VAL=3 RISE=24
let per = p20/20
meas tran vr   AVG v(vref) from=1m to=1.9m
meas tran icc  AVG i(Vis)  from=1m to=1.9m
meas tran vni  AVG v(ni)   from=1m to=1.9m
meas tran vcmp AVG v(comp) from=1m to=1.9m
meas tran vsat MIN v(ca)   from=1m to=1.9m
meas tran vosc MAX v(osc)  from=1m to=1.9m
echo "RESULT circuito de teste do datasheet (Figura 4)"
print per vr icc vni vcmp vsat vosc
if (abs(per/103.4e-6-1) < 0.06) & (abs(vr-5) < 0.02) & (abs(vcmp-vni) < 0.02) & (vsat < 1.1)
  echo "PASS  ~9.7 kHz, VREF 5 V, amp de erro em ganho unitario, Vce(sat) < 1.1 V"
else
  echo "FAIL  circuito de teste"
end
quit
.endc
.end

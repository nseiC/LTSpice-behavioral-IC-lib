.control
set noaskquit
save v(vout) v(sw) v(vb) v(comp)
run
let vbs = v(vb)-v(sw)
meas tran v1 AVG v(vout) from=5m to=6m
meas tran vpp PP v(vout) from=5m to=6m
meas tran vmx MAX v(vout) from=6m to=8m
meas tran v2 AVG v(vout) from=7.5m to=8m
meas tran vbsm MIN vbs from=5m to=6m
echo "RESULT Vout = $&v1 V com 4 A (ondulacao $&vpp V pp), $&v2 V com 2 A; pico no degrau $&vmx V; VBS min $&vbsm V"
if (abs(v1-12) < 0.05) & (abs(v2-12) < 0.05) & (vpp < 0.1) & (vmx < 12.5) & (vbsm > 13)
  echo "PASS  buck sincrono regula 12 V, partida suave e degrau de carga sem perder o bootstrap"
else
  echo "FAIL  buck sincrono"
end
quit
.endc
.end

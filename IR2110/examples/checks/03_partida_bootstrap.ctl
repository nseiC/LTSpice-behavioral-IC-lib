.control
set noaskquit
run
let vbs = v(vb)-v(sw)
let vh = v(ho)-v(sw)
meas tran th1 WHEN vh=7.5 RISE=1
meas tran vbs1 FIND vbs AT=th1
meas tran tuv WHEN vbs=8.6 RISE=1
meas tran vbsmax MAX vbs from=300u to=400u
meas tran vbsmin MIN vbs from=300u to=400u
meas tran vsw AVG v(sw) from=300u to=400u
echo "RESULT VBS passa de 8,6 V em $&tuv s; primeiro pulso de HO em $&th1 s (VBS = $&vbs1 V)"
echo "RESULT regime: VBS de $&vbsmin a $&vbsmax V, media do no de comutacao $&vsw V"
meas tran h0 MAX vh from=0.2u to=10u
if (h0 < 0.1) & (tuv > 10u) & (th1 > 20u) & (th1 < 20.5u) & (vbsmin > 13) & (vbsmax - vbsmin < 0.6) & (abs(vsw-24) < 1)
  echo "PASS  1o pulso de HIN bloqueado (UVLO do lado alto), HO sai na borda seguinte; VBS em regime ~14 V"
else
  echo "FAIL  partida do bootstrap"
end
quit
.endc
.end

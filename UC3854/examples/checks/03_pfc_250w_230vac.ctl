.control
set noaskquit
save v(out) v(vaout) v(line) v(lr) i(Vline)
run
* janela de medida: os ultimos ciclos da rede (50 Hz)
let ta = 60m
let tb = 100m
let tp = tb-ta
meas tran vo AVG v(out) from=$&ta to=$&tb
meas tran vamx MAX v(vaout) from=$&ta to=$&tb
meas tran vamn MIN v(vaout) from=$&ta to=$&tb
let vl = v(line,lr)
let il = -i(Vline)
let pinst = vl*il
let i2 = il*il
let v2 = vl*vl
let is = il*sin(2*pi*50*time)
let ic = il*cos(2*pi*50*time)
meas tran pin AVG pinst from=$&ta to=$&tb
meas tran ims AVG i2 from=$&ta to=$&tb
meas tran vms AVG v2 from=$&ta to=$&tb
meas tran ia AVG is from=$&ta to=$&tb
meas tran ib AVG ic from=$&ta to=$&tb
let irms = sqrt(ims)
let i1rms = sqrt(2*(ia*ia+ib*ib))
let pf = pin/(sqrt(vms)*irms)
let desloc = atan(ib/ia)*180/pi
* THD da corrente de linha: harmonicos 2 a 40 da rede (a THD calculada com
* Irms total incluiria o ripple de chaveamento, que o filtro de entrada
* remove e que nao e distorcao harmonica)
let h2 = 0
let n = 2
while n <= 40
  let sn = il*sin(2*pi*50*n*time)
  let cn = il*cos(2*pi*50*n*time)
  meas tran an AVG sn from=$&ta to=$&tb
  meas tran bn AVG cn from=$&ta to=$&tb
  let h2 = h2 + 2*(an*an+bn*bn)
  let n = n + 1
end
let thd = sqrt(h2)/i1rms*100
* FP so com a corrente de baixa frequencia (fundamental + harmonicos ate o 40o),
* como mediria um analisador depois do filtro de EMI
let pf40 = pin/(sqrt(vms)*sqrt(i1rms*i1rms+h2))
echo "RESULT PFC 250 W em 230 VCA"
print vo pin pf pf40 thd desloc vamn vamx
if (vo > 390) & (vo < 410) & (pf > 0.97) & (thd < 5) & (pin > 240) & (pin < 290)
  echo "PASS  regula ~400 V com FP > 0.97 e THD (harmonicos 2-40) < 5 % (datasheet: FP 0.99, distorcao < 5 %)"
else
  echo "FAIL  PFC"
end
quit
.endc
.end

# L6599A: LLC 12 V da AN3233 (L6599A/examples/02_llc_150w_an3233.cir), a 100 W
# Injecao em serie entre a saida (baixa impedancia) e a realimentacao do
# TSM1014: o divisor R49 e o ramo do LED do opto (R43), que saem ambos do
# +12 V.
# 100 W, nao 150 W: a plena carga o exemplo trabalha EM CIMA do limiar de
# OCP (ISEN chega a 0,80 V = VISX), o OCP fica descarregando o CSS e quem
# segura a saida e o limite de corrente, nao a malha de tensao (o opto U3
# fica praticamente apagado).  Medir a malha de tensao ali nao faz sentido.
title = "L6599A - LLC 12 V / 100 W (AN3233)"
deck = "../../../L6599A/examples/02_llc_150w_an3233.cir"
libs = [("../../../L6599A/L6599A.lib", "l6599a_ng.lib", "L6599A")]
replace = [(".include ../L6599A.lib", ".include l6599a_ng.lib"),
           (".param RLOAD=0.96", ".param RLOAD=1.44"),
           ("R43  out n36 51", "Vinj nfb out 0\nR43  nfb n36 51"),
           ("R49  out cvm 91k", "R49  nfb cvm 91k")]
inj, out, ret = "Vinj", "nfb", "out"
save_extra = ["v(isen)", "v(css)", "i(Vled3)"]
tsettle = 60e-3
freqs = [300, 700, 1500, 3000]
settle_cycles, meas_cycles = 4, 8
amp, maxstep = 20e-3, 40e-9
plot = "../../../L6599A/docs/fra_llc.png"

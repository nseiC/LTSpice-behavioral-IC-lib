# L6599A: LLC 12 V / 150 W da AN3233 (L6599A/examples/02_llc_150w_an3233.cir)
# Injecao em serie entre a saida (baixa impedancia) e a realimentacao do
# TSM1014: o divisor R49 e o ramo do LED do opto (R43), que saem ambos do
# +12 V - e o ponto que a AN3233 usa para medir a malha.
title = "L6599A - LLC 12 V / 150 W (AN3233)"
deck = "../../../L6599A/examples/02_llc_150w_an3233.cir"
libs = [("../../../L6599A/L6599A.lib", "l6599a_ng.lib", "L6599A")]
replace = [(".include ../L6599A.lib", ".include l6599a_ng.lib"),
           ("R43  out n36 51", "Vinj nfb out 0\nR43  nfb n36 51"),
           ("R49  out cvm 91k", "R49  nfb cvm 91k")]
inj, out, ret = "Vinj", "nfb", "out"
tsettle = 60e-3
freqs = [300, 700, 1500, 3000, 6000]
settle_cycles, meas_cycles = 3, 5
amp, maxstep = 20e-3, 40e-9
plot = "../../../L6599A/docs/fra_llc.png"

# SG3524: buck 20 V -> 5 V / 1 A (SG3524/examples/02_buck.cir)
title = "SG3524 - buck 20 V -> 5 V / 1 A"
deck = "../../../SG3524/examples/02_buck.cir"
libs = [("../../../SG3524/SG3524.lib", "sg3524_ng.lib", "SG3524")]
replace = [(".include ../SG3524.lib", ".include sg3524_ng.lib"),
           # injecao em serie entre a saida e o divisor de realimentacao
           ("Rfb1 vout inv 10k", "Vinj nfb vout 0\nRfb1 nfb inv 10k"),
           ("Cff  vout inv 3.3n", "Cff  nfb inv 3.3n"),
           # sem degrau de carga durante a medida
           ("Vstp nstpc 0 PWL(0 0 9m 0 9.002m 10 20m 10)", "Vstp nstpc 0 0")]
inj, out, ret = "Vinj", "nfb", "vout"
uic = "uic"
tsettle = 8e-3
freqs = [1000, 2000, 3000, 4000, 5000, 7000, 10000, 15000]
settle_cycles, meas_cycles = 6, 12
amp, maxstep = 20e-3, 200e-9
plot = "../../../SG3524/docs/fra_buck.png"
settle_time, meas_time = 2e-3, 2e-3

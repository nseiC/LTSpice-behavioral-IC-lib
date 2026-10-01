# SG3524: buck-boost inversor 12 V -> -12 V (SG3524/examples/04_buck_boost_inversor.cir)
title = "SG3524 - buck-boost inversor 12 V -> -12 V"
deck = "../../../SG3524/examples/04_buck_boost_inversor.cir"
libs = [("../../../SG3524/SG3524.lib", "sg3524_ng.lib", "SG3524")]
replace = [(".include ../SG3524.lib", ".include sg3524_ng.lib"),
           ("Rb vout ni 57.6k", "Vinj nfb vout 0\nRb nfb ni 57.6k"),
           ("Cff vout ni 4.7n", "Cff nfb ni 4.7n")]
inj, out, ret = "Vinj", "nfb", "vout"
uic = "uic"
tsettle = 12e-3
freqs = [500, 1000, 1500, 2000, 3000, 4000, 6000]
settle_cycles, meas_cycles = 6, 12
amp, maxstep = 30e-3, 500e-9
plot = "../../../SG3524/docs/fra_inversor.png"
settle_time, meas_time = 4e-3, 2e-3

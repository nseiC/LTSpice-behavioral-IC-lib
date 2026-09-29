# SG3524: buck-boost inversor 12 V -> -12 V (SG3524/examples/04_buck_boost_inversor.cir)
title = "SG3524 - buck-boost inversor 12 V -> -12 V"
deck = "../../../SG3524/examples/04_buck_boost_inversor.cir"
libs = [("../../../SG3524/SG3524.lib", "sg3524_ng.lib", "SG3524")]
replace = [(".include ../SG3524.lib", ".include sg3524_ng.lib"),
           ("Rb vout ni 57.6k", "Vinj nfb vout 0\nRb nfb ni 57.6k")]
inj, out, ret = "Vinj", "nfb", "vout"
uic = "uic"
tsettle = 12e-3
freqs = [300, 600, 1000, 1500, 2000, 3000, 5000]
settle_cycles, meas_cycles = 6, 12
amp, maxstep = 30e-3, 500e-9
plot = "../../../SG3524/docs/fra_inversor.png"

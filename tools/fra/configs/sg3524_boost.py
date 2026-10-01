# SG3524: boost 12 V -> 24 V (SG3524/examples/03_boost.cir)
title = "SG3524 - boost 12 V -> 24 V"
deck = "../../../SG3524/examples/03_boost.cir"
libs = [("../../../SG3524/SG3524.lib", "sg3524_ng.lib", "SG3524")]
replace = [(".include ../SG3524.lib", ".include sg3524_ng.lib"),
           ("Rfb1 vout inv 86k", "Vinj nfb vout 0\nRfb1 nfb inv 86k"),
           ("Cff  vout inv 4.7n", "Cff  nfb inv 4.7n")]
inj, out, ret = "Vinj", "nfb", "vout"
uic = "uic"
tsettle = 12e-3
freqs = [300, 500, 800, 1200, 1600, 2000, 3000, 5000]
settle_cycles, meas_cycles = 6, 12
amp, maxstep = 50e-3, 500e-9
plot = "../../../SG3524/docs/fra_boost.png"
settle_time, meas_time = 3e-3, 2e-3

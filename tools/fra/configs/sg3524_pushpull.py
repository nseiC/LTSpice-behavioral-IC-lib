# SG3524: push-pull 24 V -> 5 V / 2 A (SG3524/examples/05_push_pull.cir)
title = "SG3524 - push-pull 24 V -> 5 V / 2 A"
deck = "../../../SG3524/examples/05_push_pull.cir"
libs = [("../../../SG3524/SG3524.lib", "sg3524_ng.lib", "SG3524")]
replace = [(".include ../SG3524.lib", ".include sg3524_ng.lib"),
           ("Rfb1 vout inv 10k", "Vinj nfb vout 0\nRfb1 nfb inv 10k"),
           ("Cff  vout inv 10n", "Cff  nfb inv 10n")]
inj, out, ret = "Vinj", "nfb", "vout"
uic = "uic"
tsettle = 10e-3
freqs = [700, 1000, 1500, 2000, 2600, 3500, 5000, 8000]
settle_cycles, meas_cycles = 6, 12
amp, maxstep = 50e-3, 100e-9
plot = "../../../SG3524/docs/fra_pushpull.png"
settle_time, meas_time = 3e-3, 5e-3

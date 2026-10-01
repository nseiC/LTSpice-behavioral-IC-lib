# SG3524: boost 12 V -> 24 V / 1 A (SG3524/examples/03_boost.cir)
title = "SG3524 - boost 12 V -> 24 V / 1 A"
deck = "../../../SG3524/examples/03_boost.cir"
libs = [("../../../SG3524/SG3524.lib", "sg3524_ng.lib", "SG3524")]
replace = [(".include ../SG3524.lib", ".include sg3524_ng.lib"),
           ("Rfb1 vout inv 86k", "Vinj nfb vout 0\nRfb1 nfb inv 86k"),
           ("Cff  vout inv 4.7n", "Cff  nfb inv 4.7n")]
inj, out, ret = "Vinj", "nfb", "vout"
uic = "uic"
tsettle = 16e-3
freqs = [300, 500, 800, 1000, 1300, 1700, 2500, 4000]
settle_cycles, meas_cycles = 6, 12
amp, maxstep = 25e-3, 500e-9
plot = "../../../SG3524/docs/fra_boost.png"
settle_time, meas_time = 3e-3, 2e-3
# 25 mV: perto do cruzamento a corrente do indutor varia ~0,45 A por 25 mV de
# injecao (capacitores de saida grandes).  Com 1 A de carga o vale da corrente
# e ~1,4 A, entao ate 50 mV (a rodada 2x) o conversor fica em CCM; muito mais
# que isso ele entra em DCM e a medida deixa de ser linear - com 0,5 A de
# carga isso ja acontecia com 25 mV.

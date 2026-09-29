# 74HC86: PLL com detector de fase XOR (74HC86/examples/07_pll.cir)
import math, cmath
title = "74HC86 - PLL, detector de fase XOR"
deck = "../../../74HC86/examples/07_pll.cir"
libs = [("../../../74HC86/74HC86.lib", "74hc86_ng.lib", "74HC86")]
replace = [(".include ../74HC86.lib", ".include 74hc86_ng.lib")]
inj, out, ret = "Vinj", "vc", "n1"
tsettle = 3e-3
freqs = [300, 500, 800, 1200, 1800, 2500, 4000, 6000]
settle_cycles, meas_cycles = 4, 6
amp, maxstep = 20e-3, 50e-9
plot = "../../../74HC86/docs/fra_pll.png"

def analytic(f):
    s = 2j * math.pi * f
    Kd, Kv = 5 / math.pi, 2 * math.pi * 10e3
    R1, R2, C1, C2 = 10e3, 1e3, 100e-9, 1e-9
    Z2 = 1 / (1 / (R2 + 1 / (s * C1)) + s * C2)
    return Kd * Kv / s * Z2 / (R1 + Z2)

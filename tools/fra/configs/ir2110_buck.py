# IR2110: buck sincrono 48 V -> 12 V / 4 A, 100 kHz (IR2110/examples/04_buck_sincrono.cir)
# Injecao em serie entre a saida (baixa impedancia) e o divisor / rede tipo
# III do amplificador de erro.  O IR2110 esta dentro da malha: PWM -> HIN /
# LIN -> HO / LO -> gates da meia-ponte.
import math
title = "IR2110 - buck sincrono 48 V -> 12 V / 4 A"
deck = "../../../IR2110/examples/04_buck_sincrono.cir"
libs = [("../../../IR2110/IR2110.lib", "ir2110_ng.lib", "IR2110")]
replace = [(".include ../IR2110.lib", ".include ir2110_ng.lib"),
           # sem degrau de carga durante a medida
           ("Vstep nstc 0 PWL(0 0 6m 0 6.001m 1)", "Vstep nstc 0 0")]
inj, out, ret = "Vinj", "nfb", "vout"
uic = "uic"
tsettle = 4e-3
freqs = [1500, 2500, 4000, 6000, 8000, 12000, 18000, 25000]
settle_cycles, meas_cycles = 4, 8
amp, maxstep = 30e-3, 20e-9
plot = "../../../IR2110/docs/fra_buck.png"

def analytic(f):
    """Media do estagio de potencia + rede tipo III + amp. op. de 100 dB / 10 MHz"""
    s = 2j * math.pi * f
    par = lambda a, b: a * b / (a + b)
    R1, Rb, R3, C3, R2, C2, C1 = 10e3, 2.632e3, 435, 10e-9, 3e3, 47e-9, 1e-9
    Zin = par(R1, R3 + 1 / (s * C3))
    Zf = par(R2 + 1 / (s * C2), 1 / (s * C1))
    A = 1e5 / (1 + s * 100e6 * 15.9e-12)
    Y = 1 / Zin + 1 / Zf + 1 / Rb
    Gc = A / (Zin * Y + A * Zin / Zf)
    # modulador: Vin / Vrampa; estagio: Rs = Rds(on) (12m + canal 2,8m) + DCR
    Fm = 48 / 3.0
    Rs, L, C, Resr, R = 0.0148 + 0.020, 47e-6, 220e-6, 0.020, 3.0
    Zp = par(R, Resr + 1 / (s * C))
    return Gc * Fm * Zp / (Zp + Rs + s * L)

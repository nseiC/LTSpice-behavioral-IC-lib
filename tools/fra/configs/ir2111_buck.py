# IR2111: buck sincrono 48 V -> 12 V / 3 A, 50 kHz (IR2111/examples/03_buck_sincrono.cir)
# Injecao em serie entre a saida (baixa impedancia) e o divisor / rede tipo
# III do amplificador de erro.  O IR2111 esta dentro da malha: PWM -> IN ->
# HO / LO com o tempo morto interno (~700 ns) -> gates da meia-ponte.
import math
title = "IR2111 - buck sincrono 48 V -> 12 V / 3 A"
deck = "../../../IR2111/examples/03_buck_sincrono.cir"
libs = [("../../../IR2111/IR2111.lib", "ir2111_ng.lib", "IR2111")]
replace = [(".include ../IR2111.lib", ".include ir2111_ng.lib"),
           # sem degrau de carga durante a medida (fica em 3 A)
           ("Vstep nstc 0 PWL(0 1 8m 1 8.001m 0)", "Vstep nstc 0 1")]
inj, out, ret = "Vinj", "nfb", "vout"
uic = "uic"
tsettle = 6e-3
freqs = [800, 1300, 2000, 3000, 4500, 6500, 10000, 15000]
settle_cycles, meas_cycles = 4, 8
amp, maxstep = 30e-3, 40e-9
plot = "../../../IR2111/docs/fra_buck.png"

def analytic(f):
    """Media do estagio de potencia + rede tipo III + amp. op. de 100 dB / 10 MHz"""
    s = 2j * math.pi * f
    par = lambda a, b: a * b / (a + b)
    R1, Rb, R3, C3, R2, C2, C1 = 10e3, 2.632e3, 523, 15e-9, 2.2e3, 100e-9, 2.7e-9
    Zin = par(R1, R3 + 1 / (s * C3))
    Zf = par(R2 + 1 / (s * C2), 1 / (s * C1))
    A = 1e5 / (1 + s * 100e6 * 15.9e-12)
    Y = 1 / Zin + 1 / Zf + 1 / Rb
    Gc = A / (Zin * Y + A * Zin / Zf)
    # modulador: Vin / Vrampa; estagio: Rs = Rds(on) (12m + canal 2,8m) + DCR
    Fm = 48 / 3.0
    Rs, L, C, Resr, R = 0.0148 + 0.030, 100e-6, 220e-6, 0.025, 4.0
    Zp = par(R, Resr + 1 / (s * C))
    return Gc * Fm * Zp / (Zp + Rs + s * L)

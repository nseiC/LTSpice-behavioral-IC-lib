#!/usr/bin/env python3
"""Plota o exemplo 05 (fonte completa PFC UC3854 + LLC L6599A).

Entrada: .raw binario do ngspice com  vl i(vline) v(bus) v(out) i(vio) i(lr)
Uso:  python3 plot_fonte.py <dados.raw> <saida.png>
"""
import sys

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from plot_llc_raw import read_raw

SURFACE, INK, INK2, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#e4e3df"
S1, S2, S3 = "#2a78d6", "#eb6834", "#1baf7a"

r = read_raw(sys.argv[1])
t = r["time"]
vl, il, vb, vo, io, ilr = r["vl"], -r["i(vline)"], r["v(bus)"], r["v(out)"], r["i(vio)"], r["i(lr)"]

T = 1 / 60
tf = t[-1]


def avg(x, t0, t1=tf):
    m = (t >= t0) & (t <= t1)
    return np.trapezoid(x[m], t[m]) / (t[m][-1] - t[m][0])


t0 = tf - 2 * T
pin = avg(vl * il, t0)
pf = pin / np.sqrt(avg(vl * vl, t0) * avg(il * il, t0))
po = avg(vo * io, t0)
vbm, vom = avg(vb, t0), avg(vo, t0)

# resample uniformly for the plots and the switching-period average
tu = np.arange(t[0], tf, 0.2e-6)
ilu = np.interp(tu, t, il)
n = int(round(10e-6 / 0.2e-6))
ilavg = np.convolve(ilu, np.ones(n) / n, mode="same")

plt.rcParams.update({
    "font.size": 10, "axes.edgecolor": INK2, "axes.labelcolor": INK2,
    "xtick.color": INK2, "ytick.color": INK2, "axes.titlecolor": INK,
    "axes.titlesize": 10.5, "axes.titleweight": "bold", "axes.titlelocation": "left",
})
fig, ax = plt.subplots(4, 1, figsize=(9, 11), sharex=True, facecolor=SURFACE,
                       gridspec_kw={"hspace": 0.62})
for a in ax:
    a.set_facecolor(SURFACE)
    a.grid(True, color=GRID, lw=0.8)
    a.spines[["top", "right"]].set_visible(False)
ms = t * 1e3
ax[0].plot(ms, vl, color=S1, lw=1.4, label="tensão da rede (V)")
ax[0].plot(tu * 1e3, ilavg * 50, color=S2, lw=1.4, label="corrente da rede × 50 (média por 10 µs)")
ax[0].set_title(f"Rede 115 VCA / 60 Hz — FP = {pf:.3f}, P_in = {pin:.0f} W")
ax[0].legend(frameon=False, loc="lower left", bbox_to_anchor=(0, 1.12), ncol=2, labelcolor=INK2, fontsize=9)
ax[1].plot(ms, vb, color=S1, lw=1.4)
ax[1].set_title(f"Barramento do PFC (UC3854) — {vbm:.0f} V; o LLC só parte acima de ~386 V (pino LINE)")
ax[1].set_ylabel("V")
ax[2].plot(ms, vo, color=S3, lw=1.6)
ax[2].set_title(f"Saída do LLC (L6599A) — {vom:.2f} V, {po:.0f} W")
ax[2].set_ylabel("V")
ax[3].plot(ms, ilr, color=S1, lw=0.4)
ax[3].set_title(f"Corrente no tanque ressonante — rendimento total {po/pin*100:.1f} %")
ax[3].set_ylabel("A")
ax[3].set_xlabel("tempo (ms)")
fig.suptitle("Fonte completa: PFC UC3854 + LLC L6599A, 115 VCA → 400 V → 12 V / 150 W",
             x=0.125, ha="left", color=INK, fontsize=13, fontweight="bold")
fig.savefig(sys.argv[2], dpi=110, facecolor=SURFACE, bbox_inches="tight")
print(f"{sys.argv[2]}: Vbus={vbm:.1f} V Vout={vom:.3f} V Pout={po:.1f} W Pin={pin:.1f} W "
      f"PF={pf:.4f} eta={po/pin*100:.1f} %")

#!/usr/bin/env python3
"""Plota o exemplo 01 (malha aberta).

Entrada: .raw binario do ngspice com  v(cf) v(lvg) v(hvg) v(css) i(Vrf)
Uso:  python3 plot_malha_aberta.py <dados.raw> <saida.png>
"""
import sys

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from plot_llc_raw import read_raw

SURFACE, INK, INK2, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#e4e3df"
S1, S2, S3, S4 = "#2a78d6", "#eb6834", "#1baf7a", "#8b5cf6"

r = read_raw(sys.argv[1])
t = r["time"]
cf, lvg, hvg, css, irf = (r[k] for k in ("v(cf)", "v(lvg)", "v(hvg)", "v(css)", "i(vrf)"))

i = np.nonzero((lvg[:-1] < 6) & (lvg[1:] >= 6))[0]
e = t[i]
fe = 1 / np.diff(e)

plt.rcParams.update({
    "font.size": 10, "axes.edgecolor": INK2, "axes.labelcolor": INK2,
    "xtick.color": INK2, "ytick.color": INK2, "axes.titlecolor": INK,
    "axes.titlesize": 10.5, "axes.titleweight": "bold", "axes.titlelocation": "left",
})
fig = plt.figure(figsize=(9, 11), facecolor=SURFACE)
gs = fig.add_gridspec(4, 1, hspace=0.6)
ax = [fig.add_subplot(gs[k]) for k in range(4)]
for a in ax:
    a.set_facecolor(SURFACE)
    a.grid(True, color=GRID, lw=0.8)
    a.spines[["top", "right"]].set_visible(False)

ms = t * 1e3
ax[0].plot(e[1:] * 1e3, fe / 1e3, color=S2, lw=1.8)
ax[0].set_title("Frequência — soft-start (Rss·Css) de 166 kHz a fmin = 60 kHz; depois o opto puxa 0→400 µA do RFMIN")
ax[0].set_ylabel("kHz")
ax[1].plot(ms, css, color=S3, lw=1.6, label="Css (pino 1)")
ax[1].plot(ms, irf * 1e3, color=S1, lw=1.6, label="corrente do RFMIN (mA)")
ax[1].set_ylabel("V / mA")
ax[1].set_title("Soft-start e corrente de referência IR")
ax[1].legend(frameon=False, loc="lower left", bbox_to_anchor=(0, 1.12), ncol=2, labelcolor=INK2, fontsize=9)
ax[1].set_xlabel("tempo (ms)")

# zoom: two cycles at fmin
k = np.searchsorted(e, 7.0e-3)
ta, tb = e[k], e[k + 2]
m = (t >= ta - 0.5e-6) & (t <= tb)
us = (t[m] - ta) * 1e6
ax[2].plot(us, cf[m], color=S1, lw=1.8)
ax[2].set_title("Rampa do CF — triângulo simétrico de ~0,85 a ~3,8 V")
ax[2].set_ylabel("V")
ax[3].plot(us, lvg[m], color=S3, lw=1.8, label="LVG")
ax[3].plot(us, hvg[m], color=S4, lw=1.8, label="HVG")
ax[3].set_title("LVG na subida da rampa, HVG na descida, 0,3 µs de tempo morto")
ax[3].set_ylabel("V")
ax[3].set_xlabel("tempo (µs) — dois ciclos em 7 ms (60 kHz)")
ax[3].legend(frameon=False, loc="lower left", bbox_to_anchor=(0, 1.12), ncol=2, labelcolor=INK2, fontsize=9)
fig.suptitle("L6599A — malha aberta (CF = 470 pF, RFmin = 12k)", x=0.125, ha="left",
             color=INK, fontsize=13, fontweight="bold")
fig.savefig(sys.argv[2], dpi=110, facecolor=SURFACE, bbox_inches="tight")
print(sys.argv[2])

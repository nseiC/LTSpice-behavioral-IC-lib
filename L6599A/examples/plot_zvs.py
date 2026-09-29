#!/usr/bin/env python3
"""Zoom nas duas comutacoes da meia-ponte (exemplo 02): mostra o ZVS.

Uso:  python3 plot_zvs.py <dados.raw> <saida.png>
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
t, hb, il, lvg = r["time"], r["v(hb)"], r["i(lr)"], r["v(lvg)"]
hvg = r["v(hvg)"] - hb


def cross(v, th, up):
    i = np.nonzero((v[:-1] < th) & (v[1:] >= th))[0] if up else np.nonzero((v[:-1] > th) & (v[1:] <= th))[0]
    return t[i] + (th - v[i]) * (t[i + 1] - t[i]) / (v[i + 1] - v[i])


# last complete cycle: LVG falls -> (dead time) -> HVG rises ; HVG falls -> LVG rises
lf = cross(lvg, 6.5, False)[-2]
hr = cross(hvg, 6.5, True)
hr = hr[hr > lf][0]
hf = cross(hvg, 6.5, False)
hf = hf[hf > hr][0]
lr = cross(lvg, 6.5, True)
lr = lr[lr > hf][0]

# gate "on" instant: gate above the MOSFET threshold region (3 V), and hb there
def at(x, tt):
    return np.interp(tt, t, x)

th_on = cross(hvg, 3.0, True)
th_on = th_on[th_on > lf][0]
tl_on = cross(lvg, 3.0, True)
tl_on = tl_on[tl_on > hf][0]
v_hs = 400 - at(hb, th_on)      # Vds of the high side when it turns on
v_ls = at(hb, tl_on)            # Vds of the low side when it turns on
print(f"Vds(high side) at turn-on = {v_hs:.2f} V, i(Lr) = {at(il, th_on):.2f} A")
print(f"Vds(low side)  at turn-on = {v_ls:.2f} V, i(Lr) = {at(il, tl_on):.2f} A")

plt.rcParams.update({
    "font.size": 10, "axes.edgecolor": INK2, "axes.labelcolor": INK2,
    "xtick.color": INK2, "ytick.color": INK2, "axes.titlecolor": INK,
    "axes.titlesize": 10.5, "axes.titleweight": "bold", "axes.titlelocation": "left",
})
fig, axs = plt.subplots(2, 2, figsize=(11, 7.5), facecolor=SURFACE,
                        gridspec_kw={"hspace": 0.45, "wspace": 0.35, "height_ratios": [2, 1]})
for col, (t0, name, von, ton) in enumerate(((lf, "LVG desliga → HVG liga", v_hs, th_on),
                                           (hf, "HVG desliga → LVG liga", v_ls, tl_on))):
    m = (t >= t0 - 0.25e-6) & (t <= t0 + 0.75e-6)
    ns = (t[m] - t0) * 1e9
    a = axs[0, col]
    a2 = a.twinx()
    a.plot(ns, hb[m], color=S1, lw=2)
    a2.plot(ns, il[m], color=S2, lw=2)
    a.axvline((ton - t0) * 1e9, color=INK2, lw=1, ls="--")
    a.set_ylabel("V (meia-ponte)", color=S1)
    a2.set_ylabel("i(Lr) (A)", color=S2)
    a2.tick_params(axis="y", colors=S2)
    a.set_title(f"{name}\nVds na entrada em condução: {von:.1f} V")
    b = axs[1, col]
    b.plot(ns, lvg[m], color=S3, lw=2, label="LVG")
    b.plot(ns, hvg[m], color=S4, lw=2, label="HVG − OUT")
    b.axvline((ton - t0) * 1e9, color=INK2, lw=1, ls="--")
    b.set_ylabel("V")
    b.set_xlabel("ns")
    b.legend(frameon=False, fontsize=9, labelcolor=INK2, loc="center right")
    for x in (a, b):
        x.set_facecolor(SURFACE)
        x.grid(True, color=GRID, lw=0.8)
        x.spines[["top"]].set_visible(False)
    a2.spines[["top"]].set_visible(False)
fig.suptitle("ZVS no LLC de 150 W: no tempo morto a corrente do tanque carrega/descarrega as Coss\n"
             "e o nó vira de trilho a trilho antes do gate ligar (linha tracejada = gate em 3 V)",
             x=0.08, y=0.99, ha="left", color=INK, fontsize=12, fontweight="bold")
fig.subplots_adjust(top=0.83)
fig.savefig(sys.argv[2], dpi=110, facecolor=SURFACE, bbox_inches="tight")
print(sys.argv[2])

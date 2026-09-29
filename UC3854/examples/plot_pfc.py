#!/usr/bin/env python3
"""Plota as formas de onda dos exemplos de PFC (02 e 03).

Entrada: arquivo gerado pelo ngspice com
    wrdata <arq> v(line,lr) i(Vline) v(out) i(L1) v(vaout)
(pares tempo/valor por vetor, como o wrdata escreve).

Uso:  python3 plot_pfc.py <dados.txt> <saida.png> <titulo> <f_rede> <Rload>
"""
import sys

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK2 = "#52514e"
GRID = "#e4e3df"
S1, S2, S3 = "#2a78d6", "#eb6834", "#1baf7a"   # blue, orange, aqua (fixed order)

src, out, title, fline, rload = sys.argv[1], sys.argv[2], sys.argv[3], float(sys.argv[4]), float(sys.argv[5])

d = np.loadtxt(src)
t = d[:, 0]
vline, iline, vout, il = d[:, 1], -d[:, 3], d[:, 5], d[:, 7]
iout = vout / rload

# last two line cycles
T = 1.0 / fline
m = t >= t[-1] - 2 * T
t, vline, iline, vout, il, iout = t[m], vline[m], iline[m], vout[m], il[m], iout[m]
tm = (t - t[0]) * 1e3

# line current averaged over one switching period: what an EMI filter passes
n = max(1, int(round(10e-6 / (t[1] - t[0]))))
iavg = np.convolve(iline, np.ones(n) / n, mode="same")

# metrics over the plotted window
p = np.mean(vline * iline)
pf = p / (np.sqrt(np.mean(vline**2)) * np.sqrt(np.mean(iline**2)))

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

ax[0].plot(tm, vline, color=S1, lw=2)
ax[0].set_title("Tensão da rede")
ax[0].set_ylabel("V")

ax[1].plot(tm, iline, color=S2, lw=0.6, alpha=0.35)
ax[1].plot(tm, iavg, color=S2, lw=2)
ax[1].plot([], [], color=S2, lw=0.6, alpha=0.5, label="instantânea (com ripple de chaveamento)")
ax[1].plot([], [], color=S2, lw=2, label="média por ciclo de chaveamento")
ax[1].set_title(f"Corrente da rede — FP = {pf:.3f}")
ax[1].legend(frameon=False, loc="lower left", bbox_to_anchor=(0, 1.1), ncol=2, labelcolor=INK2, fontsize=9)
ax[1].set_ylabel("A")

ax[2].plot(tm, vout, color=S1, lw=2)
ax[2].set_title(f"Tensão de saída — média {vout.mean():.1f} V, ripple de 2×f_rede {vout.max() - vout.min():.1f} V p-p")
ax[2].set_ylabel("V")

ax[3].plot(tm, il, color=S3, lw=0.6, alpha=0.5, label="corrente no indutor boost")
ax[3].plot(tm, iout, color=S2, lw=2, label=f"corrente de saída (carga {rload:.0f} Ω)")
ax[3].set_title(f"Correntes — saída média {iout.mean():.3f} A, P_out {np.mean(vout * iout):.0f} W, P_in {p:.0f} W")
ax[3].set_ylabel("A")
ax[3].set_xlabel("tempo (ms) — últimos dois ciclos da rede")
ax[3].legend(frameon=False, loc="lower left", bbox_to_anchor=(0, 1.1), ncol=2, labelcolor=INK2, fontsize=9)

fig.suptitle(title, x=0.125, ha="left", color=INK, fontsize=13, fontweight="bold")
fig.savefig(out, dpi=110, facecolor=SURFACE, bbox_inches="tight")
print(f"{out}: Vout={vout.mean():.2f} V  Iout={iout.mean():.4f} A  Pin={p:.1f} W  PF={pf:.4f}")

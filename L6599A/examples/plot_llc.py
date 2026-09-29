#!/usr/bin/env python3
"""Plota as formas de onda dos exemplos do LLC (02, 03, 04) e da fonte
completa (05).

Entrada: arquivo .raw binario do ngspice (set filetype=binary; write) com
os vetores v(out) v(hb) i(lr) v(cf) v(css) v(stby) v(isen) v(lvg) v(hvg)
i(vbus) i(vio) v(delay) v(pfcstop).

Uso:  python3 plot_llc.py <dados.raw> <saida_prefixo> <modo> <titulo>
      modo = partida | burst | curto
"""
import sys

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from plot_llc_raw import read_raw

SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK2 = "#52514e"
GRID = "#e4e3df"
S1, S2, S3, S4 = "#2a78d6", "#eb6834", "#1baf7a", "#8b5cf6"



src, prefix, mode, title = sys.argv[1:5]
r = read_raw(src)
t = r["time"]
ALIAS = {"out": "v(out)", "hb": "v(hb)", "ilr": "i(lr)", "cf": "v(cf)", "css": "v(css)",
         "stby": "v(stby)", "isen": "v(isen)", "lvg": "v(lvg)", "hvg": "v(hvg)",
         "ibus": "i(vbus)", "iout": "i(vio)", "delay": "v(delay)", "pfcstop": "v(pfcstop)"}
d = {k: r[v] for k, v in ALIAS.items() if v in r}
if "ibus" in d:
    d["ibus"] = -d["ibus"]

plt.rcParams.update({
    "font.size": 10, "axes.edgecolor": INK2, "axes.labelcolor": INK2,
    "xtick.color": INK2, "ytick.color": INK2, "axes.titlecolor": INK,
    "axes.titlesize": 10.5, "axes.titleweight": "bold", "axes.titlelocation": "left",
})


def figure(n, h=11):
    fig, ax = plt.subplots(n, 1, figsize=(9, h), sharex=True, facecolor=SURFACE,
                           gridspec_kw={"hspace": 0.55})
    for a in ax:
        a.set_facecolor(SURFACE)
        a.grid(True, color=GRID, lw=0.8)
        a.spines[["top", "right"]].set_visible(False)
    fig.suptitle(title, x=0.125, ha="left", color=INK, fontsize=13, fontweight="bold")
    return fig, ax


def save(fig, name):
    fig.savefig(f"{prefix}_{name}.png", dpi=110, facecolor=SURFACE, bbox_inches="tight")
    print(f"{prefix}_{name}.png")


def edges(v, th=6.0):
    """instants where v crosses th going up (linear interpolation)"""
    i = np.nonzero((v[:-1] < th) & (v[1:] >= th))[0]
    return t[i] + (th - v[i]) * (t[i + 1] - t[i]) / (v[i + 1] - v[i])


def fsw():
    e = edges(d["lvg"])
    if len(e) < 2:
        return np.array([]), np.array([])
    per = np.diff(e)
    ok = per < 50e-6          # ignore the gaps of burst / stop
    return e[1:][ok], 1 / per[ok]


def avg(x, t0, t1):
    m = (t >= t0) & (t <= t1)
    return np.trapezoid(x[m], t[m]) / (t[m][-1] - t[m][0])


tf = t[-1]
ms = t * 1e3

if mode == "partida":
    # ---------------- visao geral da partida ----------------
    te, fe = fsw()
    t0 = tf - 1e-3
    vo = avg(d["out"], t0, tf)
    io = avg(d["iout"], t0, tf)
    po = avg(d["out"] * d["iout"], t0, tf)
    pi = avg(400 * d["ibus"], t0, tf)
    ff = np.mean(fe[te > t0]) if len(fe) else 0
    fig, ax = figure(4)
    ax[0].plot(ms, d["out"], color=S1, lw=1.6)
    ax[0].set_title(f"Tensão de saída — {vo:.2f} V no fim, {io:.2f} A, P_out {po:.0f} W")
    ax[0].set_ylabel("V")
    ax[1].plot(te * 1e3, fe / 1e3, color=S2, lw=1.6)
    ax[1].axhline(107, color=INK2, lw=1, ls="--")
    ax[1].text(ms[-1], 109, "fr = 107 kHz (Lr, Cr)", ha="right", va="bottom", color=INK2, fontsize=9)
    ax[1].set_title(f"Frequência de chaveamento — soft-start a partir de ~{fe[:20].max()/1e3:.0f} kHz, {ff/1e3:.0f} kHz no fim")
    ax[1].set_ylabel("kHz")
    ax[2].plot(ms, d["css"], color=S3, lw=1.6, label="Css (pino 1)")
    ax[2].plot(ms, d["stby"], color=S4, lw=1.2, label="STBY (pino 5)")
    ax[2].plot(ms, d["isen"], color=S2, lw=1.2, label="ISEN (pino 6)")
    ax[2].axhline(0.8, color=S2, lw=0.8, ls=":")
    ax[2].set_title("Soft-start, STBY e sensor de corrente")
    ax[2].set_ylabel("V")
    ax[2].legend(frameon=False, loc="lower left", bbox_to_anchor=(0, 1.12), ncol=3, labelcolor=INK2, fontsize=9)
    ax[3].plot(ms, d["ilr"], color=S1, lw=0.5)
    ax[3].set_title("Corrente no tanque ressonante i(Lr)")
    ax[3].set_ylabel("A")
    ax[3].set_xlabel("tempo (ms)")
    save(fig, "partida")
    print(f"Vout={vo:.3f} V Iout={io:.3f} A Pout={po:.1f} W Pin={pi:.1f} W "
          f"eta={po/pi*100:.1f} % fsw={ff/1e3:.1f} kHz")

    # ---------------- detalhe em regime ----------------
    e = edges(d["lvg"])
    tb = e[-1]
    ta = e[-4]
    m = (t >= ta) & (t <= tb)
    us = (t[m] - ta) * 1e6
    fig, ax = figure(3, 9)
    ax[0].plot(us, d["hb"][m], color=S1, lw=1.6, label="nó da meia-ponte (OUT)")
    ax[0].set_ylabel("V")
    a2 = ax[0].twinx()
    a2.plot(us, d["ilr"][m], color=S2, lw=1.6)
    a2.set_ylabel("A", color=S2)
    a2.tick_params(axis="y", colors=S2)
    a2.spines[["top"]].set_visible(False)
    ax[0].set_title("Meia-ponte (azul, V) e corrente ressonante (laranja, A) — a corrente atrasa a tensão: ZVS")
    ax[1].plot(us, d["lvg"][m], color=S3, lw=1.6, label="LVG (GND)")
    ax[1].plot(us, (d["hvg"] - d["hb"])[m], color=S4, lw=1.6, label="HVG − OUT")
    ax[1].set_title("Saídas de gate — 50 % com 0,3 µs de tempo morto")
    ax[1].set_ylabel("V")
    ax[1].legend(frameon=False, loc="lower left", bbox_to_anchor=(0, 1.12), ncol=2, labelcolor=INK2, fontsize=9)
    ax[2].plot(us, d["cf"][m], color=S1, lw=1.6)
    ax[2].set_title("Rampa do oscilador (pino CF) — LVG na subida, HVG na descida")
    ax[2].set_ylabel("V")
    ax[2].set_xlabel("tempo (µs) — três ciclos de chaveamento no fim da simulação")
    save(fig, "regime")

elif mode == "burst":
    t0 = tf - 15e-3
    m = t >= t0
    tm = ms[m]
    fig, ax = figure(4)
    ax[0].plot(tm, d["out"][m], color=S1, lw=1.6)
    ax[0].set_title(f"Tensão de saída — média {avg(d['out'], t0, tf):.2f} V, "
                    f"{avg(d['out'] * d['iout'], t0, tf):.1f} W de carga")
    ax[0].set_ylabel("V")
    ax[1].plot(tm, d["stby"][m], color=S4, lw=1.4)
    ax[1].axhline(1.24, color=INK2, lw=0.8, ls="--")
    ax[1].axhline(1.29, color=INK2, lw=0.8, ls=":")
    ax[1].set_title("STBY (pino 5) — para em 1,24 V, volta em 1,29 V")
    ax[1].set_ylabel("V")
    ax[2].plot(tm, d["lvg"][m], color=S3, lw=0.6)
    ax[2].set_title("LVG — pacotes de ciclos separados por pausas")
    ax[2].set_ylabel("V")
    ax[3].plot(tm, d["pfcstop"][m], color=S2, lw=1.4)
    ax[3].set_title("PFC_STOP (pino 9, 100k para Vcc) — baixo durante as pausas: desliga o PFC")
    ax[3].set_ylabel("V")
    ax[3].set_xlabel("tempo (ms)")
    save(fig, "burst")
    pi = avg(400 * d["ibus"], t0, tf)
    po = avg(d["out"] * d["iout"], t0, tf)
    e = edges(d["lvg"])
    e = e[e > t0]
    gaps = np.diff(e)
    nb = np.sum(gaps > 50e-6)
    print(f"Pout={po:.2f} W Pin={pi:.2f} W bursts={nb} in {(tf-t0)*1e3:.0f} ms "
          f"fav={len(e)/(tf-t0):.0f} Hz")

elif mode == "curto":
    te, fe = fsw()
    fig, ax = figure(5, 13)
    ax[0].plot(ms, d["out"], color=S1, lw=1.6)
    ax[0].set_title("Tensão de saída — sobrecarga (0,3 Ω) a partir de 70 ms")
    ax[0].set_ylabel("V")
    ax[1].plot(ms, d["ilr"], color=S1, lw=0.4)
    ax[1].set_title("Corrente no tanque ressonante i(Lr)")
    ax[1].set_ylabel("A")
    ax[2].plot(te * 1e3, fe / 1e3, color=S2, lw=1.4)
    ax[2].set_title("Frequência de chaveamento")
    ax[2].set_ylabel("kHz")
    ax[3].plot(ms, d["isen"], color=S2, lw=1.2, label="ISEN (pino 6)")
    ax[3].plot(ms, d["css"], color=S3, lw=1.2, label="Css (pino 1)")
    ax[3].axhline(0.8, color=S2, lw=0.8, ls=":")
    ax[3].set_title("ISEN e soft-start — o OCP de 0,8 V descarrega o Css")
    ax[3].set_ylabel("V")
    ax[3].legend(frameon=False, loc="lower left", bbox_to_anchor=(0, 1.12), ncol=2, labelcolor=INK2, fontsize=9)
    ax[4].plot(ms, d["delay"], color=S4, lw=1.6, label="DELAY (pino 2)")
    ax[4].plot(ms, d["pfcstop"] / 15 * 4, color=INK2, lw=1, alpha=0.6, label="PFC_STOP (escala 4/15)")
    for y, s in ((2.05, "2,05 V: Css preso em 0"), (3.5, "3,5 V: para"), (0.33, "0,33 V: reparte")):
        ax[4].axhline(y, color=INK2, lw=0.8, ls="--")
        ax[4].text(ms[0], y + 0.05, s, color=INK2, fontsize=8, va="bottom")
    ax[4].set_title("Temporização do OLP no pino DELAY (Figura 29 do datasheet)")
    ax[4].set_ylabel("V")
    ax[4].set_xlabel("tempo (ms)")
    ax[4].legend(frameon=False, loc="lower left", bbox_to_anchor=(0, 1.12), ncol=2, labelcolor=INK2, fontsize=9)
    save(fig, "hiccup")

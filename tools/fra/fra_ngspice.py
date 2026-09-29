#!/usr/bin/env python3
"""Emulacao do .FRA do LTspice no ngspice / ngspice emulation of LTspice .FRA

O .FRA do LTspice mede o ganho de malha no dominio do tempo: um UNICO
transiente em que, depois de o circuito assentar, uma senoide pequena e
injetada em serie na malha (metodo de Middlebrook), um tom por vez, e a
resposta nos dois lados da injecao e extraida por transformada de Fourier.

Este script faz o mesmo no ngspice, para verificar se um modelo e "robusto
ao FRA":

  * o transiente com a injecao converge em todas as frequencias;
  * o resultado e LINEAR: com o dobro da amplitude de injecao, |T| e fase
    nao mudam (um modelo com zona morta, histerese ou quantizacao no ponto
    de operacao falha aqui);
  * o resultado NAO DEPENDE DO PASSO: com metade do passo maximo, |T| e
    fase nao mudam (um modelo cujas bordas caem na grade do passo falha).

Cada tom ocupa um numero inteiro de ciclos (a injecao comeca e termina em
zero), com ciclos de acomodacao antes da janela de medida.  A componente em
f e extraida com janela de Hann (o ripple de chaveamento nao vaza para o
tom).  SNR = sinal em V(out) no tom / o mesmo calculo num trecho sem
injecao; so os pontos com SNR >= snr_min (20 dB) entram no veredito - onde
|T| e muito alto o sinal em V(out) some no ripple, em qualquer FRA, inclusive
no do LTspice.

    T(f) = -V(ret)/V(out)       (Vinj: out = ret + injecao)
    margem de fase = 180 + fase(T) no cruzamento |T| = 1

Uso:  python3 fra_ngspice.py <config.py>      (ver configs/*.py)
"""
import math, os, re, subprocess, sys, concurrent.futures as cf
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))


def read_raw(path):
    """ngspice binary rawfile (real transient data) -> {name: array}"""
    with open(path, "rb") as f:
        data = f.read()
    k = data.index(b"Binary:\n")
    head = data[:k].decode("latin-1").splitlines()
    nvar = int(next(l for l in head if l.startswith("No. Variables")).split(":")[1])
    npt = int(next(l for l in head if l.startswith("No. Points")).split(":")[1])
    i = head.index("Variables:")
    names = [head[i + 1 + j].split()[1].lower() for j in range(nvar)]
    arr = np.frombuffer(data[k + 8:], dtype="<f8", count=nvar * npt).reshape(npt, nvar)
    return {n: arr[:, j].copy() for j, n in enumerate(names)}


def schedule(cfg):
    """[(f, t_start, t_meas0, t_end)] - each tone an integer number of cycles"""
    t = cfg["tsettle"]
    seg = []
    for f in cfg["freqs"]:
        ns = max(cfg.get("settle_cycles", 4), math.ceil(f * cfg.get("settle_time", 0)))
        nm = cfg.get("meas_cycles", 10)
        seg.append((f, t, t + ns / f, t + (ns + nm) / f))
        t += (ns + nm) / f
    return seg


def make_deck(cfg, amp, maxstep, tag, workdir):
    src = open(cfg["deck"]).read()
    for a, b in cfg.get("replace", []):
        if a not in src:
            sys.exit("replace: '%s' nao encontrado em %s" % (a, cfg["deck"]))
        src = src.replace(a, b)
    # ngspice needs PARAMS: on the model's .subckt line; generate the copy
    lines = []
    for l in src.splitlines():
        s = l.strip().lower()
        if s.startswith(".tran") or s == ".end" or s.startswith(".step") \
           or s.startswith(".control") or s.startswith(".endc") or s.startswith(".fra"):
            continue
        lines.append(l)
    seg = schedule(cfg)
    terms = []
    for f, t0, _, t1 in seg:
        terms.append("sin(%.9g*(time-%.9g))*u(time-%.9g)*u(%.9g-time)"
                     % (2 * math.pi * f, t0, t0, t1))
    inj = cfg["inj"]
    pat = re.compile(r"^\s*%s\s+(\S+)\s+(\S+)\s+.*$" % re.escape(inj), re.I | re.M)
    body = "\n".join(lines)
    m = pat.search(body)
    if not m:
        sys.exit("fonte de injecao %s nao encontrada" % inj)
    body = body[:m.start()] + "B%s %s %s V = %.6g*(%s)" % (
        inj, m.group(1), m.group(2), amp, " + ".join(terms)) + body[m.end():]
    tstop = seg[-1][3]
    raw = os.path.join(workdir, tag + ".raw")
    deck = body + "\n.tran %g %.9g 0 %g %s\n.control\nsave %s\nrun\nwrite %s %s\nquit\n.endc\n.end\n" % (
        maxstep, tstop, maxstep, cfg.get("uic", ""), " ".join(
            "v(%s)" % n for n in (cfg["out"], cfg["ret"])), raw,
        " ".join("v(%s)" % n for n in (cfg["out"], cfg["ret"])))
    path = os.path.join(workdir, tag + ".cir")
    open(path, "w").write(deck)
    return path, raw


def dft(t, v, f, ta, tb):
    """Fourier component (peak amplitude) at f over [ta, tb], Hann-windowed.
    The window keeps the switching ripple (not a multiple of f) from leaking
    into the measurement - with a rectangular window, 70 mV of 100 kHz ripple
    puts tenths of a mV on every tone, and that is all the signal there is
    where the loop gain is high."""
    k = (t >= ta) & (t <= tb)
    tt, vv = t[k], v[k]
    win = 0.5 - 0.5 * np.cos(2 * math.pi * (tt - ta) / (tb - ta))
    w = (vv - np.mean(vv)) * win * np.exp(-2j * math.pi * f * tt)
    integ = np.trapezoid if hasattr(np, "trapezoid") else np.trapz
    return 2 * integ(w, tt) / (0.5 * (tb - ta))


def run_variant(cfg, name, amp, maxstep, workdir):
    deck, raw = make_deck(cfg, amp, maxstep, name, workdir)
    if os.environ.get("FRA_REUSE") and os.path.exists(raw):
        log = ""          # re-analyse an existing run (FRA_REUSE=1)
    else:
        p = subprocess.run(["ngspice", "-b", os.path.basename(deck)], cwd=os.path.dirname(deck),
                           capture_output=True, text=True)
        log = p.stdout + p.stderr
    if "too small" in log.lower() or not os.path.exists(raw):
        return name, None, log[-3000:]
    d = read_raw(raw)
    t = d["time"]
    x, y = d["v(%s)" % cfg["out"].lower()], d["v(%s)" % cfg["ret"].lower()]
    res = []
    t0 = cfg["tsettle"]
    for f, _, ta, tb in schedule(cfg):
        X, Y = dft(t, x, f, ta, tb), dft(t, y, f, ta, tb)
        T = -Y / X
        # noise floor: the same analysis on a quiet stretch before injection
        L = min(tb - ta, 0.5 * t0)
        nx = abs(dft(t, x, f, t0 - L, t0))
        res.append((f, 20 * math.log10(abs(T)), math.degrees(np.angle(T)),
                    20 * math.log10(abs(X) / max(nx, 1e-15))))
    return name, res, ""


def crossover(res):
    for (f1, g1, p1, *_), (f2, g2, p2, *_) in zip(res, res[1:]):
        if g1 >= 0 > g2:
            a = g1 / (g1 - g2)
            lf = math.log10(f1) + a * (math.log10(f2) - math.log10(f1))
            dp = (p2 - p1 + 180) % 360 - 180
            return 10 ** lf, 180 + (p1 + a * dp)
    return None, None


def main(cfgfile):
    cfg = {}
    exec(open(cfgfile).read(), cfg)
    base = os.path.dirname(os.path.abspath(cfgfile))
    cfg["deck"] = os.path.normpath(os.path.join(base, cfg["deck"]))
    workdir = os.path.join(os.path.dirname(cfg["deck"]), ".fra")
    os.makedirs(workdir, exist_ok=True)
    # ngspice copy of the model(s)
    for lib, ng, sub in cfg.get("libs", []):
        lib = os.path.normpath(os.path.join(base, lib))
        s = open(lib).read()
        s = re.sub(r"^(\.SUBCKT %s .*)$" % re.escape(sub), r"\1 PARAMS:", s, count=1, flags=re.M)
        open(os.path.join(workdir, ng), "w").write(s)
    A, dt = cfg["amp"], cfg["maxstep"]
    variants = [("base", A, dt), ("amp2", 2 * A, dt), ("step2", A, dt / 2)]
    out = {}
    with cf.ThreadPoolExecutor(max_workers=3) as ex:
        stem = os.path.splitext(os.path.basename(cfgfile))[0]
        futs = [ex.submit(run_variant, cfg, stem + "_" + n, a, s, workdir) for n, a, s in variants]
        for (n, _, _), fu in zip(variants, futs):
            _, r, log = fu.result()
            out[n] = r
            if r is None:
                print("FAIL  %s: simulacao abortou\n%s" % (n, log))
    title = cfg.get("title", os.path.basename(cfgfile))
    print("=== FRA: %s ===" % title)
    if any(r is None for r in out.values()):
        print("FAIL  %s: transiente com injecao nao completou" % title)
        return 1
    ana = cfg.get("analytic")
    hdr = "%10s %9s %8s %6s | %7s %6s | %7s %6s" % ("f (Hz)", "|T| dB", "fase", "SNR", "d(2A)", "dfase", "d(dt/2)", "dfase")
    if ana: hdr += " | %9s %8s" % ("analit dB", "fase")
    print(hdr)
    worst_g = worst_p = 0
    judged = 0
    snr_min = cfg.get("snr_min", 20)
    for i, (f, g, p, snr) in enumerate(out["base"]):
        ga, pa = out["amp2"][i][1:3]
        gs, ps = out["step2"][i][1:3]
        dpa = (pa - p + 180) % 360 - 180
        dps = (ps - p + 180) % 360 - 180
        line = "%10.4g %9.2f %8.1f %6.1f | %7.2f %6.1f | %7.2f %6.1f" % (f, g, p, snr, ga - g, dpa, gs - g, dps)
        if ana:
            Ta = ana(f)
            line += " | %9.2f %8.1f" % (20 * math.log10(abs(Ta)), math.degrees(np.angle(Ta)))
        print(line)
        if snr >= snr_min:
            judged += 1
            worst_g = max(worst_g, abs(ga - g), abs(gs - g))
            worst_p = max(worst_p, abs(dpa), abs(dps))
    fc, pm = crossover(out["base"])
    if fc:
        print("RESULT cruzamento %.4g Hz, margem de fase %.1f graus" % (fc, pm))
    else:
        print("RESULT sem cruzamento de 0 dB na faixa medida")
    tol_g, tol_p = cfg.get("tol_db", 1.0), cfg.get("tol_deg", 5.0)
    ok = worst_g <= tol_g and worst_p <= tol_p and judged >= 3
    msg = "linear (2x amplitude) e independente do passo (dt/2): pior desvio %.2f dB / %.1f graus nos %d pontos com SNR >= %g dB" % (
        worst_g, worst_p, judged, snr_min)
    if ana and fc:
        ga = [abs(20 * math.log10(abs(ana(r[0]))) - r[1]) for r in out["base"] if r[3] >= snr_min]
        msg += "; vs analitico ate %.2f dB" % max(ga)
        ok = ok and max(ga) <= cfg.get("tol_analytic_db", 1.5)
    print(("PASS  " if ok else "FAIL  ") + msg)
    if cfg.get("plot"):
        try:
            import matplotlib; matplotlib.use("Agg")
            import matplotlib.pyplot as plt
            fig, (a1, a2) = plt.subplots(2, 1, sharex=True, figsize=(7, 6))
            for n, st in (("base", "o-"), ("amp2", "x--"), ("step2", "+:")):
                fs = [r[0] for r in out[n]]
                a1.semilogx(fs, [r[1] for r in out[n]], st, label=n)
                a2.semilogx(fs, [r[2] for r in out[n]], st, label=n)
            if ana:
                ff = np.logspace(math.log10(cfg["freqs"][0]), math.log10(cfg["freqs"][-1]), 200)
                a1.semilogx(ff, [20 * math.log10(abs(ana(f))) for f in ff], "k-", lw=0.8, label="analitico")
                a2.semilogx(ff, [math.degrees(np.angle(ana(f))) for f in ff], "k-", lw=0.8)
            a1.axhline(0, color="gray", lw=0.5); a1.set_ylabel("|T| (dB)"); a1.legend(); a1.grid(True, which="both", alpha=0.3)
            a2.set_ylabel("fase T (graus)"); a2.set_xlabel("f (Hz)"); a2.grid(True, which="both", alpha=0.3)
            a1.set_title("FRA (ngspice): " + title)
            fig.tight_layout()
            png = os.path.normpath(os.path.join(base, cfg["plot"]))
            os.makedirs(os.path.dirname(png), exist_ok=True)
            fig.savefig(png, dpi=110)
            print("RESULT grafico: %s" % os.path.relpath(png, base))
        except ImportError:
            pass
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(max(main(c) for c in sys.argv[1:]))

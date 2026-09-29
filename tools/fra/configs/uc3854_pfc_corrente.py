# UC3854: malha de CORRENTE do PFC de 250 W (UC3854/examples/02_pfc_250w_u134.cir)
# Injecao em serie entre o shunt (rn, baixa impedancia) e Rmo (3.9k) - o
# caminho por onde o sinal de corrente entra no amplificador de corrente.
# O ganho da malha de corrente de um PFC varia ao longo do ciclo da rede; o
# FRA mede a media na janela, exatamente como o .FRA do LTspice faria.
title = "UC3854 - PFC 250 W, malha de corrente"
deck = "../../../UC3854/examples/02_pfc_250w_u134.cir"
libs = [("../../../UC3854/UC3854.lib", "uc3854_ng.lib", "UC3854")]
replace = [(".include ../UC3854.lib", ".include uc3854_ng.lib"),
           ("Rmo mult rn 3.9k", "Vinj nrm rn 0\nRmo mult nrm 3.9k")]
inj, out, ret = "Vinj", "nrm", "rn"
uic = "uic"
tsettle = 20e-3
freqs = [2000, 4000, 7000, 10000, 15000, 20000, 30000]
settle_cycles, meas_cycles = 4, 6
amp, maxstep = 20e-3, 100e-9
judge_db = 15
plot = "../../../UC3854/docs/fra_malha_corrente.png"

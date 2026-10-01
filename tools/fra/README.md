# tools/fra — emulação do `.FRA` do LTspice no ngspice

[Português](#português) · [English](#english)

## Português

O `.fra` do LTspice mede o ganho de malha **no domínio do tempo**: um único
transiente em que, depois de o circuito assentar, uma senoide pequena é
injetada em série na malha (método de Middlebrook), um tom por vez, e a
resposta dos dois lados da injeção é extraída por Fourier. Isso só funciona
se o modelo tem ponto de operação bem definido, responde de forma **linear**
a uma perturbação pequena e **não depende do passo de tempo**.

O LTspice não roda no ambiente de verificação deste repositório. Este script
faz a mesma medida no ngspice e roda cada malha **três vezes**:

| Rodada | Amplitude | Passo máximo | O que pega |
|---|---|---|---|
| nominal | A | dt | — |
| `2A` | 2·A | dt | não linearidade no ponto de operação (zona morta, histerese, DCM…) |
| `dt/2` | A | dt/2 | bordas presas na grade do passo, latches metaestáveis, quantização |

```
python3 fra_ngspice.py configs/sg3524_buck.py      # um
python3 fra_ngspice.py configs/*.py                # todos (horas)
FRA_REUSE=1 python3 fra_ngspice.py configs/x.py    # reanalisa sem simular
```

Requer `ngspice` e `numpy` (`matplotlib` para o gráfico). As simulações
ficam em `<pasta do exemplo>/.fra/`.

### Como a medida é feita

* **Injeção:** a fonte de 0 V `Vinj` do exemplo (em série entre um ponto de
  baixa impedância e um de alta) vira uma cadeia de fontes SIN
  independentes: cada tom é um par +A a partir de t0 e −A a partir de
  t1 = t0 + N/f, que se cancelam dali em diante. Cada tom tem um número
  inteiro de ciclos e começa e termina em zero. (Uma fonte comportamental
  com `time` e funções degrau fazia o ngspice perder a equação da fonte no
  LLC, e a simulação abortava.)
* **T(f) = −V(ret)/V(out)**, com `out = ret + injeção`. Margem de fase
  = 180° + fase(T) no cruzamento |T| = 1.
* **Extração:** tendência quadrática removida, janela de Hann, componente
  em f. Antes de cada janela há um tempo de acomodação; cada tom começa de
  forma abrupta e excita os modos lentos da malha.
* **Ruído:** o RMS da mesma análise de 3 a 8 bins de cada lado, na mesma
  janela. SNR = |V(out)| no tom / esse ruído. Um conversor chaveado tem
  mais ruído *com* o tom presente do que sem ele, então estimar o ruído num
  trecho sem injeção dá um SNR otimista.

### Veredito

Só entram os pontos com SNR ≥ 20 dB. Em cada um, os desvios das rodadas `2A`
e `dt/2` em relação à nominal têm de caber na tolerância do ponto: o maior
entre **1 dB / 5°** e **3σ** do que o ruído medido permite. Um ponto em que
a nominal fica fora, mas `2A` e `dt/2` concordam entre si, é contado como
excursão de ruído da nominal. Essas duas rodadas diferem entre si em
amplitude *e* em passo: uma não linearidade isolaria a `2A`, uma dependência
do passo isolaria a `dt/2`.

### Configurações (`configs/*.py`)

| Chave | Significado |
|---|---|
| `deck`, `libs`, `replace` | o exemplo, o modelo (gera a cópia com `PARAMS:`) e as substituições de texto — em geral, inserir `Vinj` em série na realimentação |
| `inj`, `out`, `ret` | a fonte de injeção e os dois nós em volta dela |
| `tsettle`, `uic` | quanto esperar antes do primeiro tom; `uic` se o exemplo usa |
| `freqs` | os tons, em ordem |
| `settle_cycles`/`settle_time`, `meas_cycles`/`meas_time` | acomodação e janela de cada tom: o maior entre N ciclos e o tempo |
| `amp`, `maxstep` | amplitude e passo da rodada nominal |
| `step_factor` | (opcional) passo da terceira rodada = `maxstep`·fator; 0,5 por padrão. Só para um circuito que não roda com metade do passo — e o config tem de dizer por quê |
| `save_extra` | (opcional) outros vetores para salvar (para conferir o ponto de operação) |
| `analytic` | (opcional) ganho de malha teórico para comparar |
| `plot` | onde salvar o gráfico de Bode |

### Lições que valem para qualquer FRA de conversor chaveado

* **Chave ideal + trapezoidal** faz o nó de comutação "tocar" numericamente
  e injetar corrente falsa no indutor. Use `.options method=gear` ou uma
  chave de transição suave.
* **Passo máximo pequeno o bastante** para não quantizar a borda do PWM: a
  perturbação do tempo ligado tem de ser bem maior que o passo.
* **Amplitude de injeção:** pequena o bastante para não tirar o conversor do
  modo de condução (um boost perto da fronteira CCM/DCM muda de ganho com a
  amplitude) e grande o bastante para ficar acima do ruído.
* **Comece a medir depois do soft-start.**

## English

LTspice's `.fra` measures loop gain in the time domain: one transient, a
small sine injected in series with the loop one tone at a time (Middlebrook),
the response on both sides of the injection extracted by Fourier transform.
LTspice does not run in this repository's verification environment, so this
script does the same in ngspice and runs every loop three times: nominal,
**twice the injection amplitude** (catches nonlinearity at the operating
point) and **half the maximum step** (catches step-size dependence, latch
metastability, edge quantisation).

The injection is a chain of paired independent SIN sources (each tone a
whole number of cycles), the tone is extracted with a quadratic detrend and
a Hann window, and the noise is the RMS of the same analysis 3–8 bins either
side, in the same window. A point is judged only if SNR ≥ 20 dB, and every
deviation must fit the larger of 1 dB / 5° and 3σ of the measured noise. A
point where only the nominal run sits apart, while the 2× and dt/2 runs
(which differ from each other in both amplitude and step) agree, counts as a
noise excursion of the nominal run.

```
python3 fra_ngspice.py configs/sg3524_buck.py
```

<p align="center">
  <img src="docs/utfpr.png" alt="UTFPR – Universidade Tecnológica Federal do Paraná" width="360">
</p>

# LTSpice-behavioral-IC-lib

[Português](#português) · [English](#english)

![LLC de 150 W / 150 W LLC: ZVS](L6599A/docs/llc_zvs.png)

---

## Português

Biblioteca de **modelos SPICE comportamentais** de controladores de fontes
chaveadas, drivers de gate, conversores D/A e CIs lógicos, para **LTspice**
(e ngspice).

Este repositório é destinado a apoiar o **kit educacional de LTspice**
desenvolvido pela **Universidade Tecnológica Federal do Paraná (UTFPR) –
Campus Campo Mourão**, sob a coordenação dos professores **André Regis** e
**Márcio Cunha**, do curso de Engenharia Eletrônica.

Cada modelo é um único `.subckt` comentado, construído bloco a bloco a partir
do datasheet e das notas de aplicação do fabricante, com:

* uma **suíte de testes** que confere o modelo contra as tabelas do datasheet;
* **exemplos em malha fechada** reproduzindo projetos publicados;
* o **símbolo** (`.asy`) do LTspice com a pinagem do CI.

Não são modelos em nível de transistor: cada bloco do diagrama do datasheet é
reproduzido pelo seu comportamento nos terminais. O objetivo é simular o
conversor inteiro em malha fechada — rápido, convergente e fiel às
especificações que importam no projeto.

### Modelos

| CI | Função | Validação | Exemplos |
|---|---|---|---|
| [**SG3524**](SG3524/) | controlador PWM | datasheets Philips, ST e TI cruzados | malha aberta, buck, boost, buck-boost inversor, push-pull, circuito de teste do datasheet |
| [**UC3854**](UC3854/) | PFC boost por corrente média | 57 verificações (datasheet 6/98) | malha aberta; PFC de 250 W da U-134 em 120 V e 230 V (FP 0,995 / 0,980) |
| [**L6599A**](L6599A/) (L6599AD / L6599AN) | controlador ressonante LLC meia-ponte | 47 verificações (datasheet Rev 7) | LLC 12 V / 150 W da AN3233 (ZVS, burst, hiccup); fonte completa UC3854 + L6599A, 115 VCA → 12 V, FP 0,985 |
| [**74HC86**](74HC86/) | 4 portas XOR de 2 entradas, CMOS HC | 30 verificações (ON Semi 74HC86/D Rev. 1), no limite garantido a 25 °C | tabela verdade, inversor controlado, detector de fase, dobrador de frequência, paridade, oscilador em anel, PLL |
| [**IR2110**](IR2110/) (IR2113) | driver de meia-ponte, lados alto e baixo independentes | 26 verificações (IR PD60147 rev.V), valores típicos e curvas de V<sub>DD</sub> / V<sub>BIAS</sub> | tempos de comutação, shutdown ciclo a ciclo, partida do bootstrap, buck síncrono 48 V → 12 V em malha fechada |
| [**IR2111**](IR2111/) | driver de meia-ponte de uma entrada, tempo morto interno | 22 verificações (IR PD-6.028C), valores típicos | tempo morto, meia-ponte com carga indutiva, buck síncrono 48 V → 12 V em malha fechada |
| [**DAC0800**](DAC0800/) (DAC0802) | DAC multiplicador de 8 bits, saídas em corrente complementares | 34 verificações (TI SNAS538C), Tabelas 1–3 | Tabelas 1, 2 e 3, rampa em escada, gerador de senoide, multiplicador / atenuador digital |

Cada pasta tem o próprio README com a pinagem, como cada bloco foi modelado,
a tabela de verificação, os resultados dos exemplos e o que **não** foi
modelado.

### Como usar no LTspice

1. Copie o `.lib` e o `.asy` do CI que quiser para a pasta do seu esquemático
   (ou para `Documents\LTspiceXVII\lib\sub` e `...\lib\sym`).
2. Coloque o símbolo com **F2 → (sua pasta) → nome do CI**. O símbolo já
   carrega o `ModelFile`, então o LTspice inclui o modelo sozinho.
3. Use um `.tran` com passo máximo pequeno (o README de cada CI diz quanto).

### Testes e exemplos (ngspice)

A única diferença para o LTspice é a palavra `PARAMS:` na linha `.subckt`, que
os scripts geram sozinhos:

```
cd SG3524/tests && ./run_tests.sh
cd UC3854/tests && ./run_tests.sh
cd L6599A/tests && ./run_tests.sh
cd 74HC86/tests && ./run_tests.sh
cd IR2110/tests && ./run_tests.sh
cd IR2111/tests && ./run_tests.sh
cd DAC0800/tests && ./run_tests.sh
cd L6599A/examples && ./run_examples.sh 01_malha_aberta.cir
cd 74HC86/examples && ./run_examples.sh
cd DAC0800/examples && ./run_examples.sh
```

Os exemplos de conversores completos levam de alguns minutos (SG3524) a ~1 h
cada (LLC e PFC + LLC).

### Robustez ao FRA do LTspice

O `.fra` do LTspice mede o ganho de malha no domínio do tempo: um único
transiente em que, depois de o circuito assentar, uma senoide pequena é
injetada em série na malha, um tom por vez, e a resposta é extraída por
Fourier. Para isso dar certo, o modelo precisa ter um ponto de operação bem
definido, responder de forma **linear** a uma perturbação pequena e **não
depender do passo de tempo**.

O LTspice não roda no ambiente de verificação deste repositório, então
`tools/fra/fra_ngspice.py` emula o `.fra` no ngspice (mesmo método:
injeção de Middlebrook, um tom por vez, número inteiro de ciclos, DFT com
janela de Hann) e roda cada malha três vezes: nominal, com o **dobro da
amplitude** e com **metade do passo**. O modelo é considerado robusto se as
três rodadas concordam dentro do maior entre **1 dB / 5°** e 3σ do ruído
medido ao lado do tom, em todo ponto com SNR ≥ 20 dB (ver
[`tools/fra/README.md`](tools/fra/README.md)).

```
python3 tools/fra/fra_ngspice.py tools/fra/configs/*.py     # todas (horas)
python3 tools/fra/fra_ngspice.py tools/fra/configs/74hc86_pll.py
```

| Malha | Cruzamento | MF | Pior desvio (2× amplitude / passo/2) | Situação |
|---|---|---|---|---|
| 74HC86 — PLL com detector de fase XOR | 1,88 kHz | 53° | 0,26 dB / 1,1°; bate com o ganho de malha teórico (≤ 0,06 dB) | **passa** |
| SG3524 — buck 20 → 5 V / 1 A | 4,76 kHz | 65° | 0,8 dB / 3,8° de 2 kHz para cima (2,4 dB a 1 kHz, onde \|T\| = 18 dB e o ruído admite 3,2 dB) | **passa** |
| SG3524 — boost 12 → 24 V / 1 A | 1,16 kHz | 55° | 0,16 dB / 1,2° | **passa** |
| SG3524 — buck-boost inversor 12 → −12 V / 1 A | 1,18 kHz | 46° | 0,10 dB / 1,4° | **passa** |
| SG3524 — push-pull 24 → 5 V / 2 A | 2,73 kHz | 61° | 0,43 dB / 2,1° | **passa** |
| UC3854 — malha de corrente do PFC de 250 W | 17,5 kHz | 45° | 0,34 dB / 2,2° | **passa** |
| L6599A — LLC 12 V da AN3233, a 100 W | — | — | — | **não medida**: a 150 W o exemplo trabalha em cima do limiar de sobrecorrente e não há malha de tensão para medir (ver o README do L6599A); a medida a 100 W foi interrompida |
| IR2110 — buck síncrono 48 → 12 V, 100 kHz | 7,68 kHz | 65° | 0,18 dB / 1,6°; bate com o ganho de malha médio (≤ 0,48 dB) | **passa** |
| IR2111 — buck síncrono 48 → 12 V, 50 kHz, uma entrada | 4,14 kHz | 58° | 0,18 dB / 1,0°; bate com o ganho de malha médio (≤ 0,42 dB) | **passa** (versão anterior da ferramenta) |
| DAC0800 | — | — | — | não se aplica (não fica dentro de uma malha nos exemplos; `.ac` funciona) |

O que precisou mudar para chegar aqui (detalhes no README de cada CI):

* **SG3524:** o latch de descarga do oscilador foi refeito como célula
  integradora sem realimentação positiva instantânea. O latch regenerativo
  antigo podia ficar no ponto de equilíbrio instável com passos longos do
  integrador implícito: pulsos perdidos ou 1,7 µs mais curtos em alguns
  passos e não em outros. Os exemplos foram recompensados (boost e inversor
  a 1 A, longe da fronteira CCM/DCM; push-pull com chaves externas e
  transformador de 1 mH).
* **L6599A:** a célula de direção do oscilador passou a se manter por uma
  cópia atrasada (2 ns) do próprio estado. Com a realimentação instantânea, o
  ngspice perdia o passo bem no meio da comutação dessa célula, durante o
  soft-start, e o exemplo do LLC abortava com passo máximo de 10, 20 ou
  25 ns. Com a correção, 10 e 25 ns rodam até 4 ms (o trecho onde
  abortava) e as 47 verificações do datasheet passam; os exemplos completos e o
  FRA ainda não foram re-rodados com ela.
* **Exemplos de conversor:** `.options method=gear` (ver a dica abaixo).

As medidas do SG3524 foram feitas antes do último ajuste do oscilador
(`GDIS` 72 m → 74,3 m, tempo morto 0,516 → 0,50 µs); os exemplos foram
re-rodados com o ajuste e passam, o FRA não.

Dica que vale para qualquer esquemático com chave ideal (`S`) no LTspice ou
no ngspice: se o FRA sair ruidoso, veja primeiro se o nó de comutação não
está "tocando" numericamente na abertura da chave. `method=gear`, ou uma
chave com transição suave, resolve. Com os drivers de gate (IR2110, IR2111)
no ngspice, mais duas: diodo de bootstrap sem tempo de trânsito (`TT`) e
MOSFET em subcircuito (nível 1 + capacitâncias) em vez de `VDMOS` — os dois
causavam "timestep too small" raros em simulações longas (ver o README do
IR2110).

### Licença

Domínio público / CC0. Sem garantia — confira em bancada qualquer coisa que
envolva segurança.

---

## English

A library of **behavioural SPICE models** of switch-mode power supply
controllers, gate drivers, D/A converters and logic ICs, for **LTspice**
(and ngspice).

This repository is intended to support the **LTspice educational kit**
developed at the **Federal University of Technology – Paraná (UTFPR),
Campo Mourão Campus**, under the coordination of professors **André Regis**
and **Márcio Cunha** of the Electronic Engineering program.

Each model is a single, heavily commented `.subckt`, built block by block from
the manufacturer's datasheet and application notes, and comes with:

* a **test suite** that checks the model against the datasheet tables;
* **closed-loop examples** that reproduce published designs;
* the LTspice **symbol** (`.asy`) with the IC pinout.

These are not transistor-level models: every block of the datasheet block
diagram is reproduced by its terminal behaviour. The goal is to simulate the
whole converter in closed loop — fast, convergent, and faithful to the specs
that matter when you design around the part.

### Models

| IC | Function | Validation | Examples |
|---|---|---|---|
| [**SG3524**](SG3524/) | PWM controller | Philips, ST and TI datasheets cross-checked | open loop, buck, boost, inverting buck-boost, push-pull, datasheet test circuit |
| [**UC3854**](UC3854/) | average-current-mode boost PFC | 57 checks (datasheet 6/98) | open loop; U-134 250 W PFC at 120 V and 230 V (PF 0.995 / 0.980) |
| [**L6599A**](L6599A/) (L6599AD / L6599AN) | resonant LLC half-bridge controller | 47 checks (datasheet Rev 7) | AN3233 12 V / 150 W LLC (ZVS, burst, hiccup); complete UC3854 + L6599A supply, 115 VAC → 12 V, PF 0.985 |
| [**74HC86**](74HC86/) | quad 2-input XOR gate, HC CMOS | 30 checks (ON Semi 74HC86/D Rev. 1), at the 25 °C guaranteed limit | truth table, controlled inverter, phase detector, frequency doubler, parity, ring oscillator, PLL |
| [**IR2110**](IR2110/) (IR2113) | half-bridge driver, independent high and low side | 26 checks (IR PD60147 rev.V), typical values and V<sub>DD</sub> / V<sub>BIAS</sub> curves | switching times, cycle-by-cycle shutdown, bootstrap start-up, closed-loop 48 V → 12 V synchronous buck |
| [**IR2111**](IR2111/) | single-input half-bridge driver, internal dead time | 22 checks (IR PD-6.028C), typical values | dead time, half-bridge with inductive load, closed-loop 48 V → 12 V synchronous buck |
| [**DAC0800**](DAC0800/) (DAC0802) | 8-bit multiplying DAC, complementary current outputs | 34 checks (TI SNAS538C), Tables 1–3 | Tables 1, 2 and 3, staircase ramp, sine generator, multiplier / digital attenuator |

Each folder has its own README with the pinout, how each block is modelled,
the verification table, the example results and what is **not** modelled.
(Parts of those READMEs — mainly the example sections — are in Portuguese.)

### Using the models in LTspice

1. Copy the `.lib` and `.asy` of the IC you want next to your schematic
   (or into `Documents\LTspiceXVII\lib\sub` and `...\lib\sym`).
2. Place the symbol with **F2 → (your folder) → IC name**. The symbol already
   carries its `ModelFile`, so LTspice pulls the model in by itself.
3. Use a `.tran` with a small maximum step (each IC's README says how small).

### Tests and examples (ngspice)

The only difference from LTspice is the `PARAMS:` keyword on the `.subckt`
line, which the scripts generate automatically:

```
cd SG3524/tests && ./run_tests.sh
cd UC3854/tests && ./run_tests.sh
cd L6599A/tests && ./run_tests.sh
cd 74HC86/tests && ./run_tests.sh
cd IR2110/tests && ./run_tests.sh
cd IR2111/tests && ./run_tests.sh
cd DAC0800/tests && ./run_tests.sh
cd L6599A/examples && ./run_examples.sh 01_malha_aberta.cir
cd 74HC86/examples && ./run_examples.sh
cd DAC0800/examples && ./run_examples.sh
```

The complete-converter examples take from a few minutes (SG3524) to about an
hour each (LLC and PFC + LLC).

### Robustness to LTspice .FRA

LTspice's `.fra` measures loop gain in the time domain: one transient in
which, once the circuit has settled, a small sine is injected in series with
the loop, one tone at a time, and the response is extracted by Fourier
transform. That only works if the model has a well-defined operating point,
responds **linearly** to a small perturbation and does **not depend on the
time step**.

LTspice does not run in this repository's verification environment, so
`tools/fra/fra_ngspice.py` emulates `.fra` in ngspice (same method:
Middlebrook injection, one tone at a time, whole cycles, Hann-windowed DFT)
and runs every loop three times — nominal, **twice the injection
amplitude**, **half the time step**. A model passes when the three agree
within the larger of **1 dB / 5°** and 3σ of the noise measured next to the
tone, at every point with SNR ≥ 20 dB (see
[`tools/fra/README.md`](tools/fra/README.md)).

| Loop | Crossover | PM | Worst deviation (2× amplitude / half step) | Status |
|---|---|---|---|---|
| 74HC86 — XOR phase-detector PLL | 1.88 kHz | 53° | 0.26 dB / 1.1°; matches the textbook loop gain (≤ 0.06 dB) | **passes** |
| SG3524 — buck 20 → 5 V / 1 A | 4.76 kHz | 65° | 0.8 dB / 3.8° from 2 kHz up (2.4 dB at 1 kHz, where \|T\| = 18 dB and the noise allows 3.2 dB) | **passes** |
| SG3524 — boost 12 → 24 V / 1 A | 1.16 kHz | 55° | 0.16 dB / 1.2° | **passes** |
| SG3524 — inverting buck-boost 12 → −12 V / 1 A | 1.18 kHz | 46° | 0.10 dB / 1.4° | **passes** |
| SG3524 — push-pull 24 → 5 V / 2 A | 2.73 kHz | 61° | 0.43 dB / 2.1° | **passes** |
| UC3854 — 250 W PFC current loop | 17.5 kHz | 45° | 0.34 dB / 2.2° | **passes** |
| L6599A — AN3233 12 V LLC, at 100 W | — | — | — | **not measured**: at 150 W the example runs right on the over-current threshold and there is no voltage loop to measure (see the L6599A README); the 100 W run was stopped |
| IR2110 — 48 → 12 V synchronous buck, 100 kHz | 7.68 kHz | 65° | 0.18 dB / 1.6°; matches the averaged loop gain (≤ 0.48 dB) | **passes** |
| IR2111 — 48 → 12 V synchronous buck, 50 kHz, single input | 4.14 kHz | 58° | 0.18 dB / 1.0°; matches the averaged loop gain (≤ 0.42 dB) | **passes** (earlier version of the tool) |
| DAC0800 | — | — | — | not applicable (not inside a loop in the examples; `.ac` works) |

What had to change to get here (details in each IC's README):

* **SG3524:** the oscillator's discharge latch was rebuilt as an integrating
  cell with no instantaneous positive feedback. The old regenerative latch
  could be left at its unstable equilibrium by an implicit integrator taking
  long steps: lost or 1.7 µs-short pulses at some step sizes and not others.
  The examples were recompensated (boost and inverter at 1 A, away from the
  CCM/DCM boundary; push-pull with external switches and a 1 mH
  transformer).
* **L6599A:** the oscillator's direction cell now holds itself through a
  2 ns-delayed copy of its own state. With the instantaneous feedback,
  ngspice lost the time step right in the middle of that cell's transition
  during the soft-start, and the LLC example aborted with a 10, 20 or 25 ns
  maximum step. With the fix, 10 and 25 ns run through 4 ms (past where it
  aborted) and the 47 datasheet checks pass; the full examples and the FRA
  have not been re-run with it yet.
* **Converter examples:** `.options method=gear` (see the tip in the
  Portuguese section: an ideal switch with the trapezoidal integrator makes
  the switch node ring numerically and inject spurious inductor current).

The SG3524 loops were measured before the oscillator's last trim (`GDIS`
72 m → 74.3 m, dead time 0.516 → 0.50 µs); the examples were re-run with
it and pass, the FRA was not.

### Licence

Public domain / CC0. No warranty — check anything safety-critical on the
bench.

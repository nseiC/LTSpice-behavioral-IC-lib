# LTSpice-behavioral-IC-lib

[Português](#português) · [English](#english)

![LLC de 150 W / 150 W LLC: ZVS](L6599A/docs/llc_zvs.png)

---

## Português

Biblioteca de **modelos SPICE comportamentais** de controladores de fontes
chaveadas, para **LTspice** (e ngspice).

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
| [**L6599A**](L6599A/) (L6599AD / L6599AN) | controlador ressonante LLC meia-ponte | 49 verificações (datasheet Rev 7) | LLC 12 V / 150 W da AN3233 (ZVS, burst, hiccup); fonte completa UC3854 + L6599A, 115 VCA → 12 V, FP 0,985 |

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
cd L6599A/examples && ./run_examples.sh 01_malha_aberta.cir
```

Os exemplos de conversores completos levam de alguns minutos (SG3524) a ~1 h
cada (LLC e PFC + LLC).

### Licença

Domínio público / CC0. Sem garantia — confira em bancada qualquer coisa que
envolva segurança.

---

## English

A library of **behavioural SPICE models** of switch-mode power supply
controllers, for **LTspice** (and ngspice).

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
| [**L6599A**](L6599A/) (L6599AD / L6599AN) | resonant LLC half-bridge controller | 49 checks (datasheet Rev 7) | AN3233 12 V / 150 W LLC (ZVS, burst, hiccup); complete UC3854 + L6599A supply, 115 VAC → 12 V, PF 0.985 |

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
cd L6599A/examples && ./run_examples.sh 01_malha_aberta.cir
```

The complete-converter examples take from a few minutes (SG3524) to about an
hour each (LLC and PFC + LLC).

### Licence

Public domain / CC0. No warranty — check anything safety-critical on the
bench.

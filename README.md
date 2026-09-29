# LTSpice-behavioral-IC-lib

Biblioteca de **modelos SPICE comportamentais** de controladores de fontes
chaveadas, para **LTspice** (e ngspice). Cada modelo é um único `.subckt`
comentado, construído bloco a bloco a partir do datasheet e das notas de
aplicação do fabricante, com:

* uma **suíte de testes** que confere o modelo contra as tabelas do datasheet;
* **exemplos em malha fechada** reproduzindo projetos publicados;
* o **símbolo** (`.asy`) do LTspice com a pinagem do CI.

Não são modelos em nível de transistor: cada bloco do diagrama do datasheet é
reproduzido pelo seu comportamento nos terminais. O objetivo é simular o
conversor inteiro em malha fechada — rápido, convergente e fiel às
especificações que importam no projeto.

## Modelos

| CI | Função | Validação | Exemplos |
|---|---|---|---|
| [**SG3524**](SG3524/) | controlador PWM | datasheets Philips, ST e TI cruzados | malha aberta, buck, boost, buck-boost inversor, push-pull, circuito de teste do datasheet |
| [**UC3854**](UC3854/) | PFC boost por corrente média | 57 verificações (datasheet 6/98) | malha aberta; PFC de 250 W da U-134 em 120 V e 230 V (FP 0,995 / 0,980) |
| [**L6599A**](L6599A/) (L6599AD / L6599AN) | controlador ressonante LLC meia-ponte | 49 verificações (datasheet Rev 7) | LLC 12 V / 150 W da AN3233 (ZVS, burst, hiccup); fonte completa UC3854 + L6599A, 115 VCA → 12 V, FP 0,985 |

Cada pasta tem o próprio README com a pinagem, como cada bloco foi modelado,
a tabela de verificação, os resultados dos exemplos e o que **não** foi
modelado.

![LLC de 150 W: ZVS](L6599A/docs/llc_zvs.png)

## Como usar no LTspice

1. Copie o `.lib` e o `.asy` do CI que quiser para a pasta do seu esquemático
   (ou para `Documents\LTspiceXVII\lib\sub` e `...\lib\sym`).
2. Coloque o símbolo com **F2 → (sua pasta) → nome do CI**. O símbolo já
   carrega o `ModelFile`, então o LTspice inclui o modelo sozinho.
3. Use um `.tran` com passo máximo pequeno (o README de cada CI diz quanto).

## Testes e exemplos (ngspice)

Os testes e exemplos rodam no **ngspice** (a única diferença para o LTspice é
a palavra `PARAMS:` na linha `.subckt`, que os scripts geram sozinhos):

```
cd SG3524/tests && ./run_tests.sh
cd UC3854/tests && ./run_tests.sh
cd L6599A/tests && ./run_tests.sh
cd L6599A/examples && ./run_examples.sh 01_malha_aberta.cir
```

Os exemplos de conversores completos levam de alguns minutos (SG3524) a
~1 h cada (LLC e PFC + LLC).

## Origem

Esta biblioteca reúne o conteúdo dos repositórios `SG3524-spice-model`,
`UC3854-spice-model` e `L6599AD-spice-model`, sem alterações nos modelos.

## Licença

Domínio público / CC0. Sem garantia — confira em bancada qualquer coisa que
envolva segurança.

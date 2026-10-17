# Layout escolhido — Editorial suíço

Escolhido pelo aluno em 17/10/2026 (resumo de ultrassom transvaginal), direto em HTML, sem passar pelo Paper.
Mood: estilo tipográfico internacional — grade rígida, sans-serif, muito branco, preto e um único vermelho.

## Como gerar

```
python3 templates/gerar_html.py resumos/<tema> editorial-suico
```

CSS em `templates/editorial-suico.css`. Para trocar o texto do cabeçalho, coloque no topo do `rascunho.md`:
`<!-- kicker: Ultrassom Transvaginal · ISUOG -->` (sem isso, sai "Sistemas de Informação · CESMAC").

## Origem dos valores

Cores, fontes e medidas copiadas do design feito pelo designer no Paper (arquivo "Resumo – Ultrassom
Transvaginal (ISUOG)", capa e página de roteiro). Seção 9 e exemplos foram estendidos no mesmo sistema.

## Grade

- Largura máxima de 960 px; coluna da margem de 120 px (números de seção e subseção) + 24 px + texto.
- Texto corrido limitado a ~44em. Abaixo de 760 px vira coluna única (celular). Na impressão A4, margem de 90 px.

## Cores

| Papel | Hex | Uso |
|---|---|---|
| Tinta | `#111111` | texto, réguas (1 px no cabeçalho, 6 px sob títulos), selo [Outra fonte] |
| Papel | `#FFFFFF` | fundo |
| Azul-cobalto | `#1F3FD1` | destaque principal: números de seção/subseção, numeração "01", selos [ISUOG] e [Consenso], resultado |
| Alerta | `#E5391B` | só avisos: selo "⚠ VER SEÇÃO N" e faixa da seção de limitações |
| Alerta-claro | `#FDEEEA` | fundo das caixas de aviso e da seção de limitações |
| Texto 2 / cinza | `#333333` / `#5A5A5A` | introdução, rótulos em mono, conferências |
| Linha | `#DADADA` | divisórias de tabela e listas |

## Tipografia

- **Inter** (texto e títulos, até peso 900) + **JetBrains Mono** (cabeçalho corrido, rótulos, selos, numeração).
- Título: 80 px / 900 / −0,045em; complemento após "—" em 30 px regular.
- Seção: número 132 px / 900 azul + título 34 px / 800. Subseção: número 26 px / 900 azul na margem + título 20 px / 700.
- Rótulos em mono 10,5–11 px, caixa-alta, +0,12em.

## Elementos especiais

- **Selos de origem** (mono, caixa-alta, raio 2 px): [ISUOG] azul cheio; [Consenso] contorno azul; [Outra fonte] preto cheio; [Prática/ensino] tracejado cinza.
- **Avisos** "⚠ ver seção N": selo vermelho que leva à seção.
- **"Para quem"**: rótulo na margem ao lado do subtítulo, sob a régua de 6 px.
- **Seção cujo nome contém "conferir"**: faixa vermelha no título e fundo alerta-claro; página nova na impressão.
- **Exemplos e gabarito**: caixa cinza com régua preta de 6 px no topo; resultado com barra azul.

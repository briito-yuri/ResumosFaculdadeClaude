# Layout escolhido — Editorial suíço

Escolhido pelo aluno em 17/10/2026 (resumo de ultrassom transvaginal), direto em HTML, sem passar pelo Paper.
Mood: estilo tipográfico internacional — grade rígida, sans-serif, muito branco, preto e um único vermelho.

## Como gerar

```
python3 templates/gerar_html.py resumos/<tema> editorial-suico
```

CSS em `templates/editorial-suico.css`. Para trocar o texto do cabeçalho, coloque no topo do `rascunho.md`:
`<!-- kicker: Ultrassom Transvaginal · ISUOG -->` (sem isso, sai "Sistemas de Informação · CESMAC").

## Grade

- Largura máxima de 1040 px; duas colunas: margem de 152 px (números de seção) + 32 px de respiro + texto.
- Texto corrido limitado a ~44em para a linha não ficar longa demais.
- Abaixo de 760 px de largura vira coluna única (celular).
- Na impressão (A4), a coluna da margem cai para 96 px.

## Cores

| Papel | Hex | Uso |
|---|---|---|
| Tinta | `#141414` | texto, réguas, selo [ISUOG] |
| Papel | `#FFFFFF` | fundo |
| Vermelho | `#E2231A` | único destaque: números de seção, numeração de listas, resultado, avisos "⚠ ver seção N", faixa da seção de limitações |
| Vermelho-claro | `#FDECEB` | fundo da seção "não conseguiu conferir" |
| Cinza-claro | `#F2F2F2` | fundo dos exemplos e do gabarito |
| Cinza-texto | `#5C5C5C` | introdução, conferências, selos secundários |

## Tipografia

- **Inter** (texto e títulos, pesos 400–800) + **IBM Plex Mono** (subnúmeros, selos de origem, células de tabela).
- Título: 64 px / peso 800 / −0,035em. Seção: número em 88 px vermelho + título 34 px.

## Elementos especiais

- **Selos de origem**: [ISUOG] preto cheio; [Consenso ISUOG/UOG] contorno preto; [Outra fonte] contorno cinza; [Prática/ensino] contorno cinza tracejado.
- **Avisos** "⚠ ver seção N": link vermelho sublinhado para a seção.
- **Seção cujo nome contém "conferir"**: faixa vermelha no título e fundo vermelho-claro; começa em página nova na impressão.
- **Exemplos e gabarito**: caixa cinza com régua preta grossa no topo; resultado com barra vermelha à esquerda.

# Layout escolhido — Sinalização

Escolhido pelo aluno em 16/10/2026 (resumo de conversão de bases), entre 3 opções desenhadas no Paper.
Mood: placa de sinalização — tinta preta, papel branco e um único amarelo-cromo.

## Página

- A4 retrato: 794 × 1123 px (96 dpi).
- Margens: 48 px em cima e embaixo, 64 px nas laterais (largura útil: 666 px).
- Fundo: branco `#FFFFFF`. Elementos empilhados em coluna, com 24 px entre blocos.

## Cores

| Papel | Hex | Uso |
|---|---|---|
| Tinta | `#111111` | texto principal, fios, bordas, etiquetas, cabeçalho de tabela |
| Papel | `#FFFFFF` | fundo; texto sobre a tinta |
| Amarelo-cromo | `#FFD21F` | único destaque: marca-texto do resultado, etiqueta "OPÇÃO/tema", coluna-chave no cabeçalho da tabela |
| Cinza-claro | `#F3F3F3` | fundo dos blocos de bits/código e linhas alternadas da tabela |
| Cinza-texto | `#555555` | subtítulo e rótulos secundários |
| Texto de conferência | `#333333` | linhas da conferência |

Regra: o amarelo aparece pouco — um destaque forte por bloco, nunca como fundo de área grande.

## Tipografia

- **Space Grotesk** (texto e títulos) + **JetBrains Mono** (bits, números de tabela, etiquetas).

| Elemento | Fonte | Peso | Tamanho / entrelinha | Extra |
|---|---|---|---|---|
| Título do resumo | Space Grotesk | 700 | 42 / 46 px | tracking −0.03em |
| Subtítulo | Space Grotesk | 400 | 15 / 22 px | cor `#555555` |
| Etiqueta do topo | JetBrains Mono | 700 | 11 px | caixa alta, tracking 0.08em, fundo amarelo, padding 4×8 |
| Título de seção (##) | Space Grotesk | 700 | 23 / 28 px | tracking −0.01em, precedido da etiqueta numérica |
| Etiqueta numérica da seção | JetBrains Mono | 700 | 16 / 22 px | branco sobre `#111111`, padding 4×10 |
| Subtítulo (####, título de exemplo) | Space Grotesk | 700 | 17 / 22 px | |
| Corpo | Space Grotesk | 400 | 15 / 24 px | |
| Texto dentro do exemplo | Space Grotesk | 400 | 14 / 20 px | |
| Bits / código | JetBrains Mono | 400 | 12 / 19 px | `white-space: pre`, fundo `#F3F3F3`, padding 10×12 |
| Conferência | Space Grotesk | 400 | 14 / 22 px | cor `#333333`; rótulo em 600, 13 px |

## Componentes

- **Cabeçalho da página 1:** etiqueta amarela + rótulo, título, subtítulo e fio inferior de **8 px** `#111111` (padding-bottom 20 px).
- **Seção:** etiqueta preta com o número (ex.: `3.5`) ao lado do título, gap 12 px; corpo logo abaixo, gap 12 px.
- **Exemplo resolvido:** caixa com borda **2 px** `#111111`, sem preenchimento, padding 18×22, gap 10 px. Passos em texto normal; bits em blocos cinza.
- **Resultado:** marca-texto — fundo `#FFD21F`, Space Grotesk 700 19/26 px, padding 3×8, largura do conteúdo.
- **Tabela:** borda externa 2 px `#111111`; cabeçalho com fundo `#111111`, texto branco 700 13 px (a coluna-chave em amarelo); linhas com padding 6×14, separadas por fio 1 px `#111111`, alternando branco e `#F3F3F3`; valores em JetBrains Mono 13 px (coluna-chave em 700). Colunas com largura fixa para alinhar.
- **Destaque "Importante":** faixa com borda esquerda 6 px `#FFD21F` sobre fundo `#F3F3F3`, padding 12×16.
- **Listas:** marcador "•" ou número, Space Grotesk 15/24 px, gap 6 px.

## Impressão / HTML

- `@media print`: A4, margens equivalentes, manter fundos (`print-color-adjust: exact`), evitar quebrar exemplos e tabelas no meio (`break-inside: avoid`).
- Celular: coluna única com 16 px de margem; blocos de bits com rolagem horizontal própria (a página não rola de lado).

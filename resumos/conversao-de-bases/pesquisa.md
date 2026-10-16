# Conversão de Bases Numéricas — Pesquisa

Público: aluno de 1º período de Sistemas de Informação (CESMAC).

---

## 1. Objetivo

Ao final deste resumo, o aluno deve saber:

1. Explicar o que é uma **base numérica** e a **notação posicional** (valor do dígito = dígito × base^posição), e reconhecer quais dígitos são válidos em cada base.
2. Converter **qualquer base → decimal** (soma de potências) e **decimal → qualquer base** (divisões sucessivas).
3. Converter **binário ↔ octal** e **binário ↔ hexadecimal** por agrupamento direto de bits (3 e 4 bits).
4. Converter **octal ↔ hexadecimal** usando **sempre o binário como pivô**, e **outras bases entre si** (ex.: base 5 → base 7) usando **o decimal como pivô**.
5. **Conferir** qualquer resultado convertendo de volta, e evitar os erros mais comuns de prova.

---

## 2. Conceitos (do básico ao avançado)

### 2.1 Base (ou raiz)

**Definição:** a base de um sistema de numeração é a quantidade de dígitos diferentes que ele usa. Na base *b*, os dígitos vão de 0 até *b* − 1.

**Exemplo:** na base 10 usamos 10 dígitos (0 a 9); na base 2, só 2 dígitos (0 e 1).

### 2.2 Dígitos válidos em cada base

| Base | Nome | Dígitos válidos |
|---|---|---|
| 2 | binária | 0, 1 |
| 3 | ternária | 0, 1, 2 |
| 5 | quinária | 0, 1, 2, 3, 4 |
| 7 | — | 0 a 6 |
| 8 | octal | 0 a 7 |
| 10 | decimal | 0 a 9 |
| 12 | duodecimal | 0 a 9, A (=10), B (=11) |
| 16 | hexadecimal | 0 a 9, A (=10), B (=11), C (=12), D (=13), E (=14), F (=15) |

Regra prática: **nenhum dígito pode ser maior ou igual à base**. Por isso, `19₈` não existe (9 ≥ 8) e `102₂` não existe (2 ≥ 2).

Nas bases maiores que 10, usamos letras para representar valores de 10 em diante, porque cada posição precisa de **um único símbolo**.

### 2.3 Notação de índice

**Definição:** escrevemos a base como índice (subscrito) à direita do número para não haver confusão.

**Exemplo:** `1011₂` (binário), `17₈` (octal), `2F₁₆` (hexadecimal), `25₁₀` (decimal). Note que `10₂`, `10₈`, `10₁₀` e `10₁₆` são números diferentes (valem 2, 8, 10 e 16 em decimal).

Outras notações que aparecem em programação: `0b1011` (binário), `0o17` ou `017` (octal), `0x2F` (hexadecimal).

### 2.4 Notação posicional

**Definição:** o valor de cada dígito depende da **posição** em que ele está. As posições são numeradas **da direita para a esquerda, começando em 0**. O valor de cada dígito é:

> **valor do dígito = dígito × base^posição**

e o valor do número é a **soma** dos valores de todos os dígitos.

**Exemplo (base 10):**

```
  3   5   7      ← dígitos
  2   1   0      ← posições
357₁₀ = 3×10² + 5×10¹ + 7×10⁰ = 300 + 50 + 7 = 357
```

**Exemplo (base 2):**

```
  1   0   1   1  ← dígitos
  3   2   1   0  ← posições
1011₂ = 1×2³ + 0×2² + 1×2¹ + 1×2⁰ = 8 + 0 + 2 + 1 = 11₁₀
```

O "peso" de cada posição é uma potência da base: na base 2 os pesos são 1, 2, 4, 8, 16...; na base 16 são 1, 16, 256, 4096...

### 2.5 Tabela de potências úteis

| Expoente | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2^n | 1 | 2 | 4 | 8 | 16 | 32 | 64 | 128 | 256 | 512 | 1024 |
| 3^n | 1 | 3 | 9 | 27 | 81 | 243 | | | | | |
| 5^n | 1 | 5 | 25 | 125 | 625 | | | | | | |
| 7^n | 1 | 7 | 49 | 343 | 2401 | | | | | | |
| 8^n | 1 | 8 | 64 | 512 | 4096 | | | | | | |
| 12^n | 1 | 12 | 144 | 1728 | | | | | | | |
| 16^n | 1 | 16 | 256 | 4096 | 65536 | | | | | | |

Lembrete: **qualquer número elevado a 0 vale 1** (por isso o dígito mais à direita sempre vale "ele mesmo").

### 2.6 Tabela de referência 0 a 15

| Decimal | Binário (4 bits) | Octal | Hexadecimal |
|---|---|---|---|
| 0 | 0000 | 0 | 0 |
| 1 | 0001 | 1 | 1 |
| 2 | 0010 | 2 | 2 |
| 3 | 0011 | 3 | 3 |
| 4 | 0100 | 4 | 4 |
| 5 | 0101 | 5 | 5 |
| 6 | 0110 | 6 | 6 |
| 7 | 0111 | 7 | 7 |
| 8 | 1000 | 10 | 8 |
| 9 | 1001 | 11 | 9 |
| 10 | 1010 | 12 | A |
| 11 | 1011 | 13 | B |
| 12 | 1100 | 14 | C |
| 13 | 1101 | 15 | D |
| 14 | 1110 | 16 | E |
| 15 | 1111 | 17 | F |

Para o octal, só interessam as linhas 0 a 7, usando os **3 últimos bits**: 0=000, 1=001, 2=010, 3=011, 4=100, 5=101, 6=110, 7=111.

Dica para montar a tabela de cabeça: os pesos de 4 bits são **8 4 2 1**. Ex.: 1101 = 8 + 4 + 0 + 1 = 13 = D.

### 2.7 Por que binário, octal e hexadecimal "conversam" direto

**Definição:** como **8 = 2³**, cada dígito octal corresponde a exatamente **3 bits**; como **16 = 2⁴**, cada dígito hexadecimal corresponde a exatamente **4 bits**.

Justificativa: com 3 bits formamos 2³ = 8 combinações (000 a 111 = 0 a 7), que são exatamente os 8 dígitos octais. Com 4 bits formamos 2⁴ = 16 combinações (0000 a 1111 = 0 a 15), exatamente os 16 dígitos hexadecimais. Além disso, cada grupo de 3 bits tem peso 8^k (pois 2^(3k) = 8^k) e cada grupo de 4 bits tem peso 16^k (pois 2^(4k) = 16^k). Por isso podemos converter **grupo a grupo**, sem fazer nenhuma conta grande.

**Exemplo:** `101 011₂` → 5 e 3 → `53₈`. Conferindo: 101011₂ = 32 + 8 + 2 + 1 = 43; 53₈ = 5×8 + 3 = 43. ✔

### 2.8 Estratégia de pivô (qual caminho usar)

**Definição:** "pivô" é a base intermediária pela qual passamos quando não convertemos direto.

| De → Para | Caminho |
|---|---|
| Binário → octal / hexadecimal | Agrupamento direto (3 ou 4 bits, da direita para a esquerda) |
| Octal / hexadecimal → binário | Cada dígito vira 3 ou 4 bits |
| **Octal ↔ hexadecimal** | **Sempre pelo binário:** octal → binário (3 bits por dígito) → reagrupa de 4 em 4 → hexadecimal (e o inverso) |
| Qualquer base → decimal | Soma de potências (notação posicional) |
| Decimal → qualquer base | Divisões sucessivas pela base de destino, restos lidos de baixo para cima |
| **Todas as outras** (ex.: base 5 → base 7, base 3 → base 16) | **Pelo decimal:** origem → decimal (soma de potências) → destino (divisões sucessivas) |

**Exemplo:** para levar `1234₅` à base 7, primeiro calculamos `1234₅ = 194₁₀`, depois dividimos 194 sucessivamente por 7.

### 2.9 Parte fracionária (avançado)

**Definição:** depois da vírgula, as posições continuam com **expoentes negativos**: −1, −2, −3... Assim, 0,1₂ = 1×2⁻¹ = 0,5.

**Exemplo:** 0,101₂ = 1×2⁻¹ + 0×2⁻² + 1×2⁻³ = 0,5 + 0 + 0,125 = 0,625₁₀.

Para ir do decimal para outra base, a parte inteira usa divisões sucessivas e a parte fracionária usa **multiplicações sucessivas** pela base (ver método 3.7).

---

## 3. Métodos (passo a passo com exemplos resolvidos)

### 3.1 Qualquer base → decimal (soma de potências)

1. Escreva os dígitos e, embaixo de cada um, sua posição (da direita para a esquerda, começando em 0).
2. Troque letras pelo seu valor (A=10, B=11, ..., F=15).
3. Multiplique cada dígito por base^posição.
4. Some tudo. O resultado está em decimal.

#### Exemplo 1 — Binário → decimal: 110101₂

```
dígitos:   1   1   0   1   0   1
posições:  5   4   3   2   1   0
```

| Dígito | Potência | Conta | Valor |
|---|---|---|---|
| 1 | 2⁵ = 32 | 1 × 32 | 32 |
| 1 | 2⁴ = 16 | 1 × 16 | 16 |
| 0 | 2³ = 8 | 0 × 8 | 0 |
| 1 | 2² = 4 | 1 × 4 | 4 |
| 0 | 2¹ = 2 | 0 × 2 | 0 |
| 1 | 2⁰ = 1 | 1 × 1 | 1 |

Soma: 32 + 16 + 0 + 4 + 0 + 1 = **53**. Logo, **110101₂ = 53₁₀**.

**Verificação (volta para binário):**

```
53 ÷ 2 = 26, resto 1
26 ÷ 2 = 13, resto 0
13 ÷ 2 =  6, resto 1
 6 ÷ 2 =  3, resto 0
 3 ÷ 2 =  1, resto 1
 1 ÷ 2 =  0, resto 1
```

Restos de baixo para cima: 1 1 0 1 0 1 → 110101₂. ✔

#### Exemplo 2 — Hexadecimal → decimal: 2AF₁₆

```
dígitos:   2   A   F       (A = 10, F = 15)
posições:  2   1   0
```

| Dígito | Potência | Conta | Valor |
|---|---|---|---|
| 2 | 16² = 256 | 2 × 256 | 512 |
| A = 10 | 16¹ = 16 | 10 × 16 | 160 |
| F = 15 | 16⁰ = 1 | 15 × 1 | 15 |

Soma: 512 + 160 + 15 = **687**. Logo, **2AF₁₆ = 687₁₀**.

**Verificação:**

```
687 ÷ 16 = 42, resto 15 → F    (42 × 16 = 672; 687 − 672 = 15)
 42 ÷ 16 =  2, resto 10 → A    ( 2 × 16 =  32;  42 −  32 = 10)
  2 ÷ 16 =  0, resto  2 → 2
```

Restos de baixo para cima: 2 A F → 2AF₁₆. ✔

### 3.2 Decimal → qualquer base (divisões sucessivas)

1. Divida o número decimal pela base de destino (divisão inteira). Anote o **quociente** e o **resto**.
2. Divida o quociente novamente pela base. Anote quociente e resto.
3. Repita até o **quociente ser 0**.
4. Se algum resto for ≥ 10, troque pela letra (10=A, 11=B, ..., 15=F).
5. Leia os restos **de baixo para cima** (do último para o primeiro). Esse é o resultado.

Por que funciona: cada divisão pela base "retira" o dígito da posição 0 (o resto) e "desloca" o resto do número uma posição para a direita (o quociente). O primeiro resto é o dígito menos significativo, por isso ele fica no final.

#### Exemplo 3 — Decimal → binário: 45₁₀

```
45 ÷ 2 = 22, resto 1    (22 × 2 = 44; 45 − 44 = 1)
22 ÷ 2 = 11, resto 0
11 ÷ 2 =  5, resto 1
 5 ÷ 2 =  2, resto 1
 2 ÷ 2 =  1, resto 0
 1 ÷ 2 =  0, resto 1    ← quociente 0: para
```

Restos de baixo para cima: 1 0 1 1 0 1 → **45₁₀ = 101101₂**.

**Verificação:** 101101₂ = 1×32 + 0×16 + 1×8 + 1×4 + 0×2 + 1×1 = 32 + 8 + 4 + 1 = 45. ✔

#### Exemplo 4 — Decimal → hexadecimal: 1000₁₀

```
1000 ÷ 16 = 62, resto  8         (62 × 16 = 992;  1000 − 992 = 8)
  62 ÷ 16 =  3, resto 14 → E     ( 3 × 16 =  48;    62 −  48 = 14)
   3 ÷ 16 =  0, resto  3         ← quociente 0: para
```

Restos de baixo para cima: 3 E 8 → **1000₁₀ = 3E8₁₆**.

**Verificação:** 3E8₁₆ = 3×256 + 14×16 + 8×1 = 768 + 224 + 8 = 1000. ✔

#### Exemplo 5 (generalização) — Decimal → base 12: 143₁₀

```
143 ÷ 12 = 11, resto 11 → B     (11 × 12 = 132; 143 − 132 = 11)
 11 ÷ 12 =  0, resto 11 → B
```

Resultado: **143₁₀ = BB₁₂**.

**Verificação:** BB₁₂ = 11×12 + 11×1 = 132 + 11 = 143. ✔

### 3.3 Binário ↔ octal (agrupamento de 3 bits)

**Binário → octal:**

1. Separe os bits em grupos de **3, da direita para a esquerda**.
2. Se o grupo mais à esquerda ficar incompleto, **complete com zeros à esquerda** (zeros à esquerda não mudam o valor).
3. Troque cada grupo pelo dígito octal correspondente (000=0 ... 111=7).

**Octal → binário:**

1. Troque cada dígito octal por **exatamente 3 bits** (ex.: 2 vira 010, não "10").
2. Junte tudo. Zeros à esquerda do número final podem ser removidos.

#### Exemplo 6 — Binário → octal: 1011101₂

```
1011101  →  1 | 011 | 101       (da direita para a esquerda)
         → 001 | 011 | 101      (completa com zeros à esquerda)
            1     3     5
```

Resultado: **1011101₂ = 135₈**.

**Verificação (pelo decimal):**
- 1011101₂ = 64 + 0 + 16 + 8 + 4 + 0 + 1 = 93
- 135₈ = 1×64 + 3×8 + 5×1 = 64 + 24 + 5 = 93 ✔

#### Exemplo 7 — Octal → binário: 472₈

```
 4     7     2
100   111   010
```

Resultado: **472₈ = 100111010₂**.

**Verificação (pelo decimal):**
- 472₈ = 4×64 + 7×8 + 2×1 = 256 + 56 + 2 = 314
- 100111010₂ = 256 + 0 + 0 + 32 + 16 + 8 + 0 + 2 + 0 = 314 ✔

### 3.4 Binário ↔ hexadecimal (agrupamento de 4 bits)

**Binário → hexadecimal:**

1. Separe os bits em grupos de **4, da direita para a esquerda**.
2. Complete o grupo da esquerda com zeros à esquerda, se precisar.
3. Troque cada grupo pelo dígito hexadecimal (0000=0 ... 1111=F).

**Hexadecimal → binário:**

1. Troque cada dígito hexadecimal por **exatamente 4 bits**.
2. Junte tudo.

#### Exemplo 8 — Binário → hexadecimal: 1101011110₂

```
1101011110  →  11 | 0101 | 1110
            → 0011 | 0101 | 1110      (completa com zeros)
                3      5      E
```

Resultado: **1101011110₂ = 35E₁₆**.

**Verificação (pelo decimal):**
- 1101011110₂ = 512 + 256 + 0 + 64 + 0 + 16 + 8 + 4 + 2 + 0 = 862
- 35E₁₆ = 3×256 + 5×16 + 14×1 = 768 + 80 + 14 = 862 ✔

#### Exemplo 9 — Hexadecimal → binário: B7₁₆

```
  B      7
 1011   0111
```

Resultado: **B7₁₆ = 10110111₂**.

**Verificação (pelo decimal):**
- B7₁₆ = 11×16 + 7 = 176 + 7 = 183
- 10110111₂ = 128 + 0 + 32 + 16 + 0 + 4 + 2 + 1 = 183 ✔

### 3.5 Octal ↔ hexadecimal (SEMPRE com o binário como pivô)

**Octal → hexadecimal:**

1. Converta cada dígito octal em **3 bits**.
2. Junte os bits numa sequência só.
3. Reagrupe em blocos de **4 bits, da direita para a esquerda**, completando com zeros à esquerda.
4. Troque cada bloco de 4 bits pelo dígito hexadecimal.

**Hexadecimal → octal:**

1. Converta cada dígito hexadecimal em **4 bits**.
2. Junte os bits.
3. Reagrupe em blocos de **3 bits, da direita para a esquerda**, completando com zeros à esquerda.
4. Troque cada bloco de 3 bits pelo dígito octal.

Atenção: **não** dá para trocar dígito por dígito entre octal e hexadecimal (17₈ é 15₁₀ = F₁₆, e não 17₁₆). O binário é a "ponte" porque 8 e 16 são potências de 2.

Observação: nos exemplos abaixo, a "Verificação (pelo decimal)" é **só uma conferência** do resultado. A conversão em si **nunca** passa pelo decimal: o caminho é sempre octal → binário → hexadecimal (ou o inverso).

#### Exemplo 10 — Octal → hexadecimal: 765₈

Passo 1 — octal → binário (3 bits por dígito):

```
 7     6     5
111   110   101    →  111110101₂   (9 bits)
```

Passo 2 — reagrupar de 4 em 4, da direita para a esquerda:

```
111110101  →  1 | 1111 | 0101
           → 0001 | 1111 | 0101    (completa com zeros à esquerda)
               1      F      5
```

Resultado: **765₈ = 1F5₁₆**.

**Verificação (pelo decimal):**
- 765₈ = 7×64 + 6×8 + 5×1 = 448 + 48 + 5 = 501
- 1F5₁₆ = 1×256 + 15×16 + 5×1 = 256 + 240 + 5 = 501 ✔

#### Exemplo 11 — Hexadecimal → octal: 3AD₁₆

Passo 1 — hexadecimal → binário (4 bits por dígito):

```
  3      A      D
 0011   1010   1101    →  001110101101₂   (12 bits)
```

Passo 2 — reagrupar de 3 em 3, da direita para a esquerda:

```
001110101101  →  001 | 110 | 101 | 101
                  1     6     5     5
```

Resultado: **3AD₁₆ = 1655₈**.

(Se você tivesse removido os zeros da esquerda antes — 1110101101, 10 bits —, os grupos seriam 1 | 110 | 101 | 101 → 001 | 110 | 101 | 101, e o resultado é o mesmo.)

**Verificação (pelo decimal):**
- 3AD₁₆ = 3×256 + 10×16 + 13×1 = 768 + 160 + 13 = 941
- 1655₈ = 1×512 + 6×64 + 5×8 + 5×1 = 512 + 384 + 40 + 5 = 941 ✔

### 3.6 Outras bases entre si (SEMPRE com o decimal como pivô)

1. **Origem → decimal:** soma de potências da base de origem (método 3.1).
2. **Decimal → destino:** divisões sucessivas pela base de destino (método 3.2).
3. **Confira:** converta o resultado de volta para decimal.

#### Exemplo 12 — Base 5 → base 7: 1234₅

Passo 1 — 1234₅ → decimal:

```
dígitos:   1   2   3   4
posições:  3   2   1   0
```

| Dígito | Potência | Conta | Valor |
|---|---|---|---|
| 1 | 5³ = 125 | 1 × 125 | 125 |
| 2 | 5² = 25 | 2 × 25 | 50 |
| 3 | 5¹ = 5 | 3 × 5 | 15 |
| 4 | 5⁰ = 1 | 4 × 1 | 4 |

Soma: 125 + 50 + 15 + 4 = **194₁₀**.

Passo 2 — 194₁₀ → base 7:

```
194 ÷ 7 = 27, resto 5    (27 × 7 = 189; 194 − 189 = 5)
 27 ÷ 7 =  3, resto 6    ( 3 × 7 =  21;  27 −  21 = 6)
  3 ÷ 7 =  0, resto 3
```

Restos de baixo para cima: 3 6 5 → **1234₅ = 365₇**.

**Verificação:** 365₇ = 3×49 + 6×7 + 5×1 = 147 + 42 + 5 = 194 = 1234₅. ✔

#### Exemplo 13 — Base 3 → base 16: 2101₃

Passo 1 — 2101₃ → decimal:

```
dígitos:   2   1   0   1
posições:  3   2   1   0
```

| Dígito | Potência | Conta | Valor |
|---|---|---|---|
| 2 | 3³ = 27 | 2 × 27 | 54 |
| 1 | 3² = 9 | 1 × 9 | 9 |
| 0 | 3¹ = 3 | 0 × 3 | 0 |
| 1 | 3⁰ = 1 | 1 × 1 | 1 |

Soma: 54 + 9 + 0 + 1 = **64₁₀**.

Passo 2 — 64₁₀ → base 16:

```
64 ÷ 16 = 4, resto 0    (4 × 16 = 64; 64 − 64 = 0)
 4 ÷ 16 = 0, resto 4
```

Restos de baixo para cima: 4 0 → **2101₃ = 40₁₆**.

**Verificação:** 40₁₆ = 4×16 + 0×1 = 64 = 2101₃. ✔

### 3.7 Parte fracionária (decimal → outra base): multiplicações sucessivas

1. Separe a parte inteira e a parte fracionária. A parte inteira vai pelo método 3.2.
2. Multiplique a parte fracionária pela base de destino.
3. A **parte inteira** do resultado é o próximo dígito (depois da vírgula). Guarde só a parte fracionária.
4. Repita com a nova parte fracionária até ela virar **0** (ou até ter dígitos suficientes, se a fração for periódica).
5. Leia os dígitos **de cima para baixo** (ordem em que apareceram) — o contrário das divisões.

#### Exemplo 14 — Decimal → binário: 10,375₁₀

Parte inteira (10):

```
10 ÷ 2 = 5, resto 0
 5 ÷ 2 = 2, resto 1
 2 ÷ 2 = 1, resto 0
 1 ÷ 2 = 0, resto 1     → de baixo para cima: 1010
```

Parte fracionária (0,375):

```
0,375 × 2 = 0,75  → dígito 0, sobra 0,75
0,75  × 2 = 1,5   → dígito 1, sobra 0,5
0,5   × 2 = 1,0   → dígito 1, sobra 0     ← para
```

De cima para baixo: 0 1 1 → 0,011.

Resultado: **10,375₁₀ = 1010,011₂**.

**Verificação:** 1010,011₂ = 8 + 0 + 2 + 0 + 0×0,5 + 1×0,25 + 1×0,125 = 10 + 0,375 = 10,375. ✔

#### Exemplo 15 — Decimal → hexadecimal: 0,75₁₀

```
0,75 × 16 = 12,0 → dígito 12 = C, sobra 0  ← para
```

Resultado: **0,75₁₀ = 0,C₁₆**. **Verificação:** C × 16⁻¹ = 12/16 = 0,75. ✔

Observação: nem toda fração decimal "fecha" em binário. Ex.: 0,1₁₀:

```
0,1 × 2 = 0,2 → 0
0,2 × 2 = 0,4 → 0
0,4 × 2 = 0,8 → 0
0,8 × 2 = 1,6 → 1 (sobra 0,6)
0,6 × 2 = 1,2 → 1 (sobra 0,2)  ← 0,2 já apareceu: o ciclo se repete
```

0,1₁₀ = 0,0001100110011...₂ (dízima periódica). Nesses casos, pare depois do número de dígitos pedido no enunciado.

---

## 4. Atalhos e pegadinhas (erros comuns em prova)

1. **Ler os restos na ordem errada.** Nas divisões sucessivas, leia **de baixo para cima**. Ex.: 13₁₀ dá restos 1, 0, 1, 1 (nessa ordem); o correto é **1101₂** (= 13). Ler de cima para baixo dá 1011₂, que vale 11 — errado.
2. **Parar a divisão antes da hora.** Continue até o **quociente ser 0**; o último resto (o primeiro dígito do resultado) costuma ser esquecido.
3. **Inverter a regra na parte fracionária.** Nas multiplicações sucessivas, a leitura é **de cima para baixo** (o contrário das divisões).
4. **Agrupar bits a partir da esquerda.** Os grupos de 3 ou 4 bits começam **pela direita** (na parte inteira). Ex.: 1101011110₂ agrupado errado pela esquerda dá 1101 | 0111 | 10 → "D72" (errado); o certo é 0011 | 0101 | 1110 → **35E₁₆**. (Se houver parte fracionária, ela é agrupada a partir da vírgula **para a direita**, completando com zeros **à direita**: 0,11₂ → 0,110₂ → 0,6₈.)
5. **Esquecer de completar com zeros à esquerda** e, por exemplo, ler o grupo "11" como se fosse "110". Complete sempre com zeros **à esquerda** do grupo mais à esquerda: 11 → 0011.
6. **Escrever menos bits por dígito.** Na conversão octal/hexa → binário, cada dígito vira **exatamente** 3 (octal) ou 4 (hexa) bits. Ex.: 72₈ = 111 **010**, e não 111 10.
7. **Converter octal ↔ hexadecimal dígito a dígito.** 17₈ ≠ 17₁₆. 17₈ = 15₁₀ = F₁₆. Use o binário como pivô.
8. **Começar a contar posições em 1.** A posição mais à direita é a **0** (peso base⁰ = 1).
9. **Ignorar os dígitos zero na soma de potências.** Eles valem 0, mas **ocupam posição**: pular um zero desloca todas as potências seguintes.
10. **Dígito inválido.** Se aparecer 8 ou 9 num número octal, ou 2 num binário, o número está errado (ou a base foi lida errado). Na base 16, não existe "G".
11. **Esquecer de trocar resto ≥ 10 por letra.** Resto 14 na divisão por 16 é **E**, não "14" (escrever "14" geraria dois dígitos).
12. **Confundir o valor das letras.** A=10, B=11, C=12, D=13, E=14, F=15. Truque: F é o maior (15); conte para trás.

**Atalhos:**
- **Conferência rápida de paridade:** um número binário é par se e só se termina em 0. Em hexadecimal/octal/decimal, o número é par se e só se o último dígito for par (vale porque as bases 16, 8 e 10 são pares). Em hexadecimal, considere o **valor** da letra: A (10), C (12) e E (14) são pares; B, D e F são ímpares.
- **Pesos 8-4-2-1:** decore para converter qualquer grupo de 4 bits de cabeça (pesos 4-2-1 para 3 bits).
- **Decimal → binário por subtração de potências:** pegue a maior potência de 2 que cabe, subtraia e repita. Ex.: 45 = 32 + 8 + 4 + 1 → posições 5, 3, 2, 0 → 101101₂.
- **Decimal → octal/hexa grandes:** é mais rápido dividir direto por 8 ou 16 do que passar pelo binário.
- **Sempre confira** convertendo de volta (ou passando os dois lados para decimal).

---

## 5. Exercícios

1. Converta **77₁₀** para binário.
2. Converta **11100110₂** para decimal.
3. Converta **500₁₀** para hexadecimal.
4. Converta **C0DE₁₆** para decimal.
5. Converta **10110110101₂** para octal e para hexadecimal.
6. Converta **1750₈** para hexadecimal (use o binário como pivô).
7. Converta **4B₁₆** para octal (use o binário como pivô).
8. Converta **342₅** para a base 3 (use o decimal como pivô).

---

## Gabarito

**1. 77₁₀ = 1001101₂**

```
77 ÷ 2 = 38, resto 1
38 ÷ 2 = 19, resto 0
19 ÷ 2 =  9, resto 1
 9 ÷ 2 =  4, resto 1
 4 ÷ 2 =  2, resto 0
 2 ÷ 2 =  1, resto 0
 1 ÷ 2 =  0, resto 1
```

De baixo para cima: 1001101. Conferência: 64 + 0 + 0 + 8 + 4 + 0 + 1 = 77. ✔

**2. 11100110₂ = 230₁₀**

1×128 + 1×64 + 1×32 + 0×16 + 0×8 + 1×4 + 1×2 + 0×1 = 128 + 64 + 32 + 4 + 2 = 230.
Conferência: 230 ÷ 16 = 14, resto 6 (14×16 = 224); 14 ÷ 16 = 0, resto 14 = E → E6₁₆ = 1110 0110₂. ✔

**3. 500₁₀ = 1F4₁₆**

```
500 ÷ 16 = 31, resto  4        (31 × 16 = 496)
 31 ÷ 16 =  1, resto 15 → F    ( 1 × 16 =  16)
  1 ÷ 16 =  0, resto  1
```

Conferência: 1×256 + 15×16 + 4 = 256 + 240 + 4 = 500. ✔

**4. C0DE₁₆ = 49374₁₀**

12×4096 + 0×256 + 13×16 + 14×1 = 49152 + 0 + 208 + 14 = 49374.
Conferência:

```
49374 ÷ 16 = 3085, resto 14 → E   (3085 × 16 = 49360)
 3085 ÷ 16 =  192, resto 13 → D   ( 192 × 16 =  3072)
  192 ÷ 16 =   12, resto  0       (  12 × 16 =   192)
   12 ÷ 16 =    0, resto 12 → C
```

De baixo para cima: C0DE. ✔

**5. 10110110101₂ = 2665₈ = 5B5₁₆**

- Octal (grupos de 3 pela direita): 10 | 110 | 110 | 101 → 010 | 110 | 110 | 101 → 2 6 6 5.
- Hexadecimal (grupos de 4 pela direita): 101 | 1011 | 0101 → 0101 | 1011 | 0101 → 5 B 5.

Conferência pelo decimal:
- 10110110101₂ = 1024 + 256 + 128 + 32 + 16 + 4 + 1 = 1461
- 2665₈ = 2×512 + 6×64 + 6×8 + 5 = 1024 + 384 + 48 + 5 = 1461
- 5B5₁₆ = 5×256 + 11×16 + 5 = 1280 + 176 + 5 = 1461 ✔

**6. 1750₈ = 3E8₁₆**

- Octal → binário: 1 = 001, 7 = 111, 5 = 101, 0 = 000 → 001111101000.
- Reagrupando de 4 em 4: 0011 | 1110 | 1000 → 3 E 8.

Conferência: 1750₈ = 1×512 + 7×64 + 5×8 + 0 = 512 + 448 + 40 = 1000; 3E8₁₆ = 768 + 224 + 8 = 1000. ✔

**7. 4B₁₆ = 113₈**

- Hexa → binário: 4 = 0100, B = 1011 → 01001011 (sem zeros à esquerda: 1001011).
- Reagrupando de 3 em 3 pela direita: 1 | 001 | 011 → 001 | 001 | 011 → 1 1 3.

Conferência: 4B₁₆ = 4×16 + 11 = 75; 113₈ = 1×64 + 1×8 + 3 = 75. ✔

**8. 342₅ = 10121₃**

- 342₅ → decimal: 3×25 + 4×5 + 2×1 = 75 + 20 + 2 = 97.
- 97 → base 3:

```
97 ÷ 3 = 32, resto 1    (32 × 3 = 96)
32 ÷ 3 = 10, resto 2    (10 × 3 = 30)
10 ÷ 3 =  3, resto 1    ( 3 × 3 =  9)
 3 ÷ 3 =  1, resto 0
 1 ÷ 3 =  0, resto 1
```

De baixo para cima: 10121. Conferência: 1×81 + 0×27 + 1×9 + 2×3 + 1×1 = 81 + 9 + 6 + 1 = 97. ✔

---

## 6. Fontes (realmente consultadas)

- Wikipédia (pt). "Sistema de numeração hexadecimal". Disponível em: https://pt.wikipedia.org/wiki/Sistema_de_numeração_hexadecimal — conversão hexa ↔ binário (grupos de 4 bits), hexa → decimal por potências de 16, decimal → hexa por divisões sucessivas, tabela de equivalências.
- Wikipédia (pt). "Sistema octal". Disponível em: https://pt.wikipedia.org/wiki/Sistema_octal — octal → decimal por potências de 8 (ex.: 764₈ = 500₁₀), octal → binário (3 bits por dígito), octal → hexadecimal passando pelo binário.
- ARAUJO, Fernando. "<Direto ao Ponto 05> Conversão entre bases de numeração". DIO, 18 jan. 2024. Disponível em: https://www.dio.me/en/articles/direto-ao-ponto-05-conversao-entre-bases-de-numeracao — métodos gerais (soma de potências, divisões sucessivas, agrupamento de bits). Atenção: o artigo traz pelo menos um exemplo com erro (3C₁₆ deveria ser 00111100₂); os exemplos deste resumo foram todos refeitos e conferidos aqui.
- LOPES, Evelin. "Conversão de bases numéricas". Evelin DEV (Substack), 9 mar. 2022. Disponível em: https://evelindev.substack.com/p/conversao-de-bases-numericas — algoritmo de divisões sucessivas (restos invertidos ao final).

Todos os exemplos e exercícios deste arquivo são próprios e foram conferidos pela conversão inversa.

---

## Revisão QA

Não há nenhum erro numérico. Todas as contas dos Exemplos 1 a 15, das seções 2.4, 2.7 e 4 e do gabarito dos exercícios 1 a 8 foram refeitas de forma independente e conferidas com Python (`int(..., base)`, `format`, `hex`, `oct` e `fractions` para 0,1₁₀ em binário).

Ajustes de clareza e lacunas:

- **§3.5:** foi acrescentada uma observação explicando que a "Verificação (pelo decimal)" serve só para conferir o resultado. A conversão octal ↔ hexadecimal continua passando sempre pelo binário. Sem essa observação, o leitor poderia achar que a regra estava sendo quebrada.
- **Exemplo 13:** foi incluído o bloco "dígitos/posições", como nos Exemplos 1, 2 e 12, para não pular passo.
- **§4, pegadinha 4:** a nota sobre o agrupamento da parte fracionária foi completada. O agrupamento começa na vírgula e vai para a direita, completando com zeros à direita (ex.: 0,11₂ = 0,110₂ = 0,6₈ = 0,75₁₀).
- **§4, atalho de paridade:** antes estava escrito "par se o último dígito for par". Agora está "par se e só se o último dígito for par", com a explicação de que A, C e E são pares e B, D e F são ímpares.
- **§3.7, observação sobre 0,1₁₀:** "para depois do número de dígitos" virou "pare depois do número de dígitos".

O texto segue as regras do aluno. A tabela §2.8 e as seções 3.3 a 3.6 usam o agrupamento de 3 ou 4 bits entre binário e octal ou hexadecimal. Octal ↔ hexadecimal passa sempre pelo binário (Exemplos 10 e 11, exercícios 6 e 7). As outras bases passam pelo decimal: base 5 → base 7 (Ex. 12), base 3 → base 16 (Ex. 13) e base 5 → base 3 (exercício 8).

Fontes: as 4 URLs foram abertas e existem. O conteúdo citado também foi confirmado: o exemplo 764₈ = 500₁₀ na Wikipédia "Sistema octal" e o erro 3C₁₆ → 00111010₂ no artigo da DIO. O correto é 00111100₂.

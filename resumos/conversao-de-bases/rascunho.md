# Conversão de Bases Numéricas

Resumo para alunos do 1º período de Sistemas de Informação (CESMAC).

Aqui vamos trabalhar só com quatro bases: **2 (binária), 8 (octal), 10 (decimal) e 16 (hexadecimal)**.

---

## 1. O que você vai aprender

Ao terminar este resumo, você vai saber:

1. Explicar o que é uma **base numérica** e como funciona a **notação posicional** (valor do dígito = dígito × base^posição). Também vai reconhecer quais dígitos valem em cada base.
2. Converter **binário, octal ou hexadecimal → decimal** (soma de potências) e **decimal → binário, octal ou hexadecimal** (divisões sucessivas).
3. Converter **binário ↔ octal** e **binário ↔ hexadecimal** agrupando os bits de 3 em 3 ou de 4 em 4.
4. Converter **octal ↔ hexadecimal** passando **sempre pelo binário**.
5. Converter números **com parte fracionária** (com vírgula) do decimal para binário, octal ou hexadecimal (multiplicações sucessivas), e entender quanto vale cada posição depois da vírgula (expoentes negativos).
6. **Conferir** qualquer resultado fazendo a conversão de volta, e fugir dos erros mais comuns de prova.

---

## 2. Conceitos básicos

### 2.1 O que é a base

A base (ou raiz) de um sistema de numeração é a quantidade de dígitos diferentes que ele usa. Na base *b*, os dígitos vão de 0 até *b* − 1.

**Exemplo:** a base 10 usa 10 dígitos (0 a 9). A base 2 usa só 2 dígitos (0 e 1).

### 2.2 Dígitos válidos em cada base

| Base | Nome | Dígitos válidos |
|---|---|---|
| 2 | binária | 0, 1 |
| 8 | octal | 0 a 7 |
| 10 | decimal | 0 a 9 |
| 16 | hexadecimal | 0 a 9, A (=10), B (=11), C (=12), D (=13), E (=14), F (=15) |

Guarde esta regra: **nenhum dígito pode ser maior ou igual à base**. Por isso, `19₈` não existe (9 ≥ 8), e `102₂` também não (2 ≥ 2).

A base 16 passa de 10. Como cada posição precisa de **um único símbolo**, usamos letras para os valores de 10 em diante.

### 2.3 Como indicar a base

Escrevemos a base como um índice pequeno (subscrito) à direita do número. Assim ninguém se confunde.

**Exemplo:** `1011₂` (binário), `17₈` (octal), `2F₁₆` (hexadecimal), `25₁₀` (decimal).

Repare: `10₂`, `10₈`, `10₁₀` e `10₁₆` são números diferentes. Em decimal, eles valem 2, 8, 10 e 16.

Em programação, você também vai ver: `0b1011` (binário), `0o17` ou `017` (octal) e `0x2F` (hexadecimal).

### 2.4 Notação posicional

O valor de um dígito depende da **posição** em que ele está. Contamos as posições **da direita para a esquerda, começando em 0**. Cada dígito vale:

> **valor do dígito = dígito × base^posição**

O valor do número é a **soma** dos valores de todos os dígitos.

**Exemplo na base 10:**

```
  3   5   7      ← dígitos
  2   1   0      ← posições
357₁₀ = 3×10² + 5×10¹ + 7×10⁰ = 300 + 50 + 7 = 357
```

**Exemplo na base 2:**

```
  1   0   1   1  ← dígitos
  3   2   1   0  ← posições
1011₂ = 1×2³ + 0×2² + 1×2¹ + 1×2⁰ = 8 + 0 + 2 + 1 = 11₁₀
```

Cada posição tem um "peso", que é uma potência da base. Na base 2, os pesos são 1, 2, 4, 8, 16... Na base 16, são 1, 16, 256, 4096...

### 2.5 Tabela de potências

| Expoente | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2^n | 1 | 2 | 4 | 8 | 16 | 32 | 64 | 128 | 256 | 512 | 1024 |
| 8^n | 1 | 8 | 64 | 512 | 4096 | | | | | | |
| 16^n | 1 | 16 | 256 | 4096 | 65536 | | | | | | |

Lembre: **qualquer número elevado a 0 vale 1**. Por isso o dígito mais à direita sempre vale ele mesmo.

### 2.6 Tabela de referência de 0 a 15

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

Para o octal, use só as linhas de 0 a 7 e os **3 últimos bits**: 0=000, 1=001, 2=010, 3=011, 4=100, 5=101, 6=110, 7=111.

Quer montar a tabela de cabeça? Use os pesos **8 4 2 1** para os 4 bits. Exemplo: 1101 = 8 + 4 + 0 + 1 = 13 = D. Para 3 bits, os pesos são 4 2 1.

### 2.7 Por que binário, octal e hexadecimal conversam direto

Como **8 = 2³**, cada dígito octal corresponde a exatamente **3 bits**. Como **16 = 2⁴**, cada dígito hexadecimal corresponde a exatamente **4 bits**.

Veja por quê. Com 3 bits formamos 2³ = 8 combinações (000 a 111 = 0 a 7): são exatamente os 8 dígitos octais. Com 4 bits formamos 2⁴ = 16 combinações (0000 a 1111 = 0 a 15): são exatamente os 16 dígitos hexadecimais.

Além disso, cada grupo de 3 bits tem peso 8^k (pois 2^(3k) = 8^k), e cada grupo de 4 bits tem peso 16^k (pois 2^(4k) = 16^k). Por isso dá para converter **grupo a grupo**, sem nenhuma conta grande.

**Exemplo:** `101 011₂` → 5 e 3 → `53₈`. Conferindo: 101011₂ = 32 + 8 + 2 + 1 = 43; 53₈ = 5×8 + 3 = 43. ✔

### 2.8 Qual caminho usar em cada conversão

Às vezes não dá para converter direto. Aí passamos por uma base intermediária, que chamamos de **pivô**.

| De → Para | Caminho |
|---|---|
| Binário → octal / hexadecimal | Agrupamento direto (3 ou 4 bits, da direita para a esquerda) |
| Octal / hexadecimal → binário | Cada dígito vira 3 ou 4 bits |
| **Octal ↔ hexadecimal** | **Sempre pelo binário:** octal → binário (3 bits por dígito) → reagrupa de 4 em 4 → hexadecimal (e o inverso) |
| Binário / octal / hexadecimal → decimal | Soma de potências (notação posicional) |
| Decimal → binário / octal / hexadecimal | Divisões sucessivas pela base de destino (2, 8 ou 16), restos lidos de baixo para cima |

### 2.9 Parte fracionária (avançado)

Depois da vírgula, as posições continuam com **expoentes negativos**: −1, −2, −3... Assim, 0,1₂ = 1×2⁻¹ = 0,5.

**Exemplo:** 0,101₂ = 1×2⁻¹ + 0×2⁻² + 1×2⁻³ = 0,5 + 0 + 0,125 = 0,625₁₀.

Para sair do decimal e ir para outra base, a parte inteira usa divisões sucessivas. Já a parte fracionária usa **multiplicações sucessivas** pela base (veja a seção 3.6).

---

## 3. Métodos passo a passo

### 3.1 Binário, octal ou hexadecimal → decimal (soma de potências)

1. Escreva os dígitos. Embaixo de cada um, anote a posição (da direita para a esquerda, começando em 0).
2. Troque as letras pelo valor delas (A=10, B=11, ..., F=15).
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

**Conferência (volta para binário):**

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

**Conferência:**

```
687 ÷ 16 = 42, resto 15 → F    (42 × 16 = 672; 687 − 672 = 15)
 42 ÷ 16 =  2, resto 10 → A    ( 2 × 16 =  32;  42 −  32 = 10)
  2 ÷ 16 =  0, resto  2 → 2
```

Restos de baixo para cima: 2 A F → 2AF₁₆. ✔

### 3.2 Decimal → binário, octal ou hexadecimal (divisões sucessivas)

1. Divida o número decimal pela base de destino (divisão inteira). Anote o **quociente** e o **resto**.
2. Divida o quociente de novo pela base. Anote quociente e resto.
3. Repita até o **quociente dar 0**.
4. Se algum resto for ≥ 10, troque pela letra (10=A, 11=B, ..., 15=F).
5. Leia os restos **de baixo para cima** (do último para o primeiro). Esse é o resultado.

Por que funciona? Cada divisão pela base "tira" o dígito da posição 0 (é o resto) e "empurra" o restante do número uma posição para a direita (é o quociente). O primeiro resto é o dígito menos significativo. Por isso ele fica no final.

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

**Conferência:** 101101₂ = 1×32 + 0×16 + 1×8 + 1×4 + 0×2 + 1×1 = 32 + 8 + 4 + 1 = 45. ✔

#### Exemplo 4 — Decimal → hexadecimal: 1000₁₀

```
1000 ÷ 16 = 62, resto  8         (62 × 16 = 992;  1000 − 992 = 8)
  62 ÷ 16 =  3, resto 14 → E     ( 3 × 16 =  48;    62 −  48 = 14)
   3 ÷ 16 =  0, resto  3         ← quociente 0: para
```

Restos de baixo para cima: 3 E 8 → **1000₁₀ = 3E8₁₆**.

**Conferência:** 3E8₁₆ = 3×256 + 14×16 + 8×1 = 768 + 224 + 8 = 1000. ✔

### 3.3 Binário ↔ octal (grupos de 3 bits)

**Binário → octal:**

1. Separe os bits em grupos de **3, da direita para a esquerda**.
2. Se o grupo da ponta esquerda ficar incompleto, **complete com zeros à esquerda**. Zeros à esquerda não mudam o valor.
3. Troque cada grupo pelo dígito octal correspondente (000=0 ... 111=7).

**Octal → binário:**

1. Troque cada dígito octal por **exatamente 3 bits**. Exemplo: 2 vira 010, e não "10".
2. Junte tudo. Os zeros à esquerda do número final podem sair.

#### Exemplo 5 — Binário → octal: 1011101₂

```
1011101  →  1 | 011 | 101       (da direita para a esquerda)
         → 001 | 011 | 101      (completa com zeros à esquerda)
            1     3     5
```

Resultado: **1011101₂ = 135₈**.

**Conferência pelo decimal:**
- 1011101₂ = 64 + 0 + 16 + 8 + 4 + 0 + 1 = 93
- 135₈ = 1×64 + 3×8 + 5×1 = 64 + 24 + 5 = 93 ✔

#### Exemplo 6 — Octal → binário: 472₈

```
 4     7     2
100   111   010
```

Resultado: **472₈ = 100111010₂**.

**Conferência pelo decimal:**
- 472₈ = 4×64 + 7×8 + 2×1 = 256 + 56 + 2 = 314
- 100111010₂ = 256 + 0 + 0 + 32 + 16 + 8 + 0 + 2 + 0 = 314 ✔

### 3.4 Binário ↔ hexadecimal (grupos de 4 bits)

**Binário → hexadecimal:**

1. Separe os bits em grupos de **4, da direita para a esquerda**.
2. Se precisar, complete o grupo da esquerda com zeros à esquerda.
3. Troque cada grupo pelo dígito hexadecimal (0000=0 ... 1111=F).

**Hexadecimal → binário:**

1. Troque cada dígito hexadecimal por **exatamente 4 bits**.
2. Junte tudo.

#### Exemplo 7 — Binário → hexadecimal: 1101011110₂

```
1101011110  →  11 | 0101 | 1110
            → 0011 | 0101 | 1110      (completa com zeros)
                3      5      E
```

Resultado: **1101011110₂ = 35E₁₆**.

**Conferência pelo decimal:**
- 1101011110₂ = 512 + 256 + 0 + 64 + 0 + 16 + 8 + 4 + 2 + 0 = 862
- 35E₁₆ = 3×256 + 5×16 + 14×1 = 768 + 80 + 14 = 862 ✔

#### Exemplo 8 — Hexadecimal → binário: B7₁₆

```
  B      7
 1011   0111
```

Resultado: **B7₁₆ = 10110111₂**.

**Conferência pelo decimal:**
- B7₁₆ = 11×16 + 7 = 176 + 7 = 183
- 10110111₂ = 128 + 0 + 32 + 16 + 0 + 4 + 2 + 1 = 183 ✔

### 3.5 Octal ↔ hexadecimal (sempre pelo binário)

Não dá para trocar dígito por dígito entre octal e hexadecimal. Por exemplo, 17₈ vale 15₁₀ = F₁₆, e não 17₁₆. O binário serve de "ponte" porque 8 e 16 são potências de 2.

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

> **Importante:** nos exemplos abaixo, a "conferência pelo decimal" serve **só para checar** o resultado. A conversão em si **nunca** passa pelo decimal. O caminho é sempre octal → binário → hexadecimal (ou o inverso).

#### Exemplo 9 — Octal → hexadecimal: 765₈

Passo 1 — octal → binário (3 bits por dígito):

```
 7     6     5
111   110   101    →  111110101₂   (9 bits)
```

Passo 2 — reagrupe de 4 em 4, da direita para a esquerda:

```
111110101  →  1 | 1111 | 0101
           → 0001 | 1111 | 0101    (completa com zeros à esquerda)
               1      F      5
```

Resultado: **765₈ = 1F5₁₆**.

**Conferência pelo decimal (só para checar):**
- 765₈ = 7×64 + 6×8 + 5×1 = 448 + 48 + 5 = 501
- 1F5₁₆ = 1×256 + 15×16 + 5×1 = 256 + 240 + 5 = 501 ✔

#### Exemplo 10 — Hexadecimal → octal: 3AD₁₆

Passo 1 — hexadecimal → binário (4 bits por dígito):

```
  3      A      D
 0011   1010   1101    →  001110101101₂   (12 bits)
```

Passo 2 — reagrupe de 3 em 3, da direita para a esquerda:

```
001110101101  →  001 | 110 | 101 | 101
                  1     6     5     5
```

Resultado: **3AD₁₆ = 1655₈**.

E se você tivesse tirado os zeros da esquerda antes? Ficaria 1110101101 (10 bits). Os grupos seriam 1 | 110 | 101 | 101 → 001 | 110 | 101 | 101, e o resultado seria o mesmo.

**Conferência pelo decimal (só para checar):**
- 3AD₁₆ = 3×256 + 10×16 + 13×1 = 768 + 160 + 13 = 941
- 1655₈ = 1×512 + 6×64 + 5×8 + 5×1 = 512 + 384 + 40 + 5 = 941 ✔

### 3.6 Parte fracionária: decimal → binário, octal ou hexadecimal (multiplicações sucessivas)

1. Separe a parte inteira da parte fracionária. A parte inteira segue o método da seção 3.2.
2. Multiplique a parte fracionária pela base de destino.
3. A **parte inteira** do resultado é o próximo dígito depois da vírgula. Guarde só a parte fracionária.
4. Repita com a nova parte fracionária até ela virar **0**. Se a fração for periódica, pare quando tiver dígitos suficientes.
5. Leia os dígitos **de cima para baixo**, na ordem em que apareceram. É o contrário das divisões.

#### Exemplo 11 — Decimal → binário: 10,375₁₀

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

**Conferência:** 1010,011₂ = 8 + 0 + 2 + 0 + 0×0,5 + 1×0,25 + 1×0,125 = 10 + 0,375 = 10,375. ✔

#### Exemplo 12 — Decimal → octal: 25,6875₁₀

Parte inteira (25):

```
25 ÷ 8 = 3, resto 1    (3 × 8 = 24; 25 − 24 = 1)
 3 ÷ 8 = 0, resto 3     → de baixo para cima: 31
```

Parte fracionária (0,6875):

```
0,6875 × 8 = 5,5  → dígito 5, sobra 0,5
0,5    × 8 = 4,0  → dígito 4, sobra 0     ← para
```

De cima para baixo: 5 4 → 0,54.

Resultado: **25,6875₁₀ = 31,54₈**.

**Conferência:** 31,54₈ = 3×8 + 1×1 + 5×8⁻¹ + 4×8⁻² = 24 + 1 + 5/8 + 4/64 = 25 + 0,625 + 0,0625 = 25,6875. ✔

#### Exemplo 13 — Decimal → hexadecimal: 0,75₁₀

```
0,75 × 16 = 12,0 → dígito 12 = C, sobra 0  ← para
```

Resultado: **0,75₁₀ = 0,C₁₆**.

**Conferência:** C × 16⁻¹ = 12/16 = 0,75. ✔

#### Quando a fração não fecha

Nem toda fração decimal "fecha" em binário. Veja 0,1₁₀:

```
0,1 × 2 = 0,2 → 0
0,2 × 2 = 0,4 → 0
0,4 × 2 = 0,8 → 0
0,8 × 2 = 1,6 → 1 (sobra 0,6)
0,6 × 2 = 1,2 → 1 (sobra 0,2)  ← 0,2 já apareceu: o ciclo se repete
```

0,1₁₀ = 0,0001100110011...₂ (dízima periódica). Nesses casos, pare quando atingir o número de dígitos pedido no enunciado.

---

## 4. Erros comuns de prova

1. **Ler os restos na ordem errada.** Nas divisões sucessivas, leia **de baixo para cima**. Exemplo: 13₁₀ dá os restos 1, 0, 1, 1 (nessa ordem). O certo é **1101₂** (= 13). Lendo de cima para baixo, você teria 1011₂, que vale 11. Errado.
2. **Parar a divisão antes da hora.** Continue até o **quociente dar 0**. Muita gente esquece o último resto, que é o primeiro dígito do resultado.
3. **Inverter a regra na parte fracionária.** Nas multiplicações sucessivas, a leitura é **de cima para baixo** (o contrário das divisões).
4. **Agrupar os bits a partir da esquerda.** Na parte inteira, os grupos de 3 ou 4 bits começam **pela direita**. Exemplo: agrupando 1101011110₂ pela esquerda, você teria 1101 | 0111 | 10 → "D72" (errado). O certo é 0011 | 0101 | 1110 → **35E₁₆**. Na parte fracionária é diferente: agrupe a partir da vírgula **para a direita** e complete com zeros **à direita**. Exemplo: 0,11₂ → 0,110₂ → 0,6₈.
5. **Esquecer de completar com zeros à esquerda.** Aí você acaba lendo o grupo "11" como se fosse "110". Complete sempre com zeros **à esquerda** do grupo da ponta esquerda: 11 → 0011.
6. **Escrever menos bits por dígito.** Na conversão octal/hexa → binário, cada dígito vira **exatamente** 3 bits (octal) ou 4 bits (hexa). Exemplo: 72₈ = 111 **010**, e não 111 10.
7. **Converter octal ↔ hexadecimal dígito a dígito.** 17₈ ≠ 17₁₆. Na verdade, 17₈ = 15₁₀ = F₁₆. Use o binário como pivô.
8. **Começar a contar as posições em 1.** A posição mais à direita é a **0** (peso base⁰ = 1).
9. **Pular os zeros na soma de potências.** Um zero vale 0, mas **ocupa posição**. Se você pular um zero, todas as potências seguintes ficam deslocadas.
10. **Usar dígito inválido.** Se aparecer 8 ou 9 num número octal, ou 2 num binário, o número está errado (ou você leu a base errada). Na base 16, não existe "G".
11. **Esquecer de trocar resto ≥ 10 por letra.** Na divisão por 16, resto 14 vira **E**, e não "14". Escrever "14" geraria dois dígitos.
12. **Confundir o valor das letras.** A=10, B=11, C=12, D=13, E=14, F=15. Truque: F é a maior (15); conte para trás a partir dela.

---

## 5. Atalhos

- **Paridade rápida:** um número binário é par se, e somente se, termina em 0. Em hexadecimal, octal e decimal, o número é par se, e somente se, o último dígito for par. Isso vale porque as bases 16, 8 e 10 são pares. No hexadecimal, olhe o **valor** da letra: A (10), C (12) e E (14) são pares; B, D e F são ímpares.
- **Pesos 8-4-2-1:** decore e você converte qualquer grupo de 4 bits de cabeça (para 3 bits, use 4-2-1).
- **Decimal → binário por subtração de potências:** pegue a maior potência de 2 que cabe no número, subtraia e repita. Exemplo: 45 = 32 + 8 + 4 + 1 → posições 5, 3, 2, 0 → 101101₂.
- **Decimal → octal ou hexa com números grandes:** dividir direto por 8 ou 16 é mais rápido do que passar pelo binário.
- **Sempre confira:** converta de volta ou passe os dois lados para decimal.

---

## 6. Exercícios

1. Converta **77₁₀** para binário.
2. Converta **11100110₂** para decimal.
3. Converta **500₁₀** para hexadecimal.
4. Converta **C0DE₁₆** para decimal.
5. Converta **10110110101₂** para octal e para hexadecimal.
6. Converta **1750₈** para hexadecimal (use o binário como pivô).
7. Converta **4B₁₆** para octal (use o binário como pivô).

---

## 7. Gabarito

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

De baixo para cima: 1001101.
Conferência: 64 + 0 + 0 + 8 + 4 + 0 + 1 = 77. ✔

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

Conferência pelo decimal (só para checar): 1750₈ = 1×512 + 7×64 + 5×8 + 0 = 512 + 448 + 40 = 1000; 3E8₁₆ = 768 + 224 + 8 = 1000. ✔

**7. 4B₁₆ = 113₈**

- Hexa → binário: 4 = 0100, B = 1011 → 01001011 (sem zeros à esquerda: 1001011).
- Reagrupando de 3 em 3 pela direita: 1 | 001 | 011 → 001 | 001 | 011 → 1 1 3.

Conferência pelo decimal (só para checar): 4B₁₆ = 4×16 + 11 = 75; 113₈ = 1×64 + 1×8 + 3 = 75. ✔

---

## 8. Fontes consultadas

- Wikipédia (pt). "Sistema de numeração hexadecimal". Disponível em: https://pt.wikipedia.org/wiki/Sistema_de_numeração_hexadecimal — conversão hexa ↔ binário (grupos de 4 bits), hexa → decimal por potências de 16, decimal → hexa por divisões sucessivas, tabela de equivalências.
- Wikipédia (pt). "Sistema octal". Disponível em: https://pt.wikipedia.org/wiki/Sistema_octal — octal → decimal por potências de 8 (ex.: 764₈ = 500₁₀), octal → binário (3 bits por dígito), octal → hexadecimal passando pelo binário.
- ARAUJO, Fernando. "<Direto ao Ponto 05> Conversão entre bases de numeração". DIO, 18 jan. 2024. Disponível em: https://www.dio.me/en/articles/direto-ao-ponto-05-conversao-entre-bases-de-numeracao — métodos gerais (soma de potências, divisões sucessivas, agrupamento de bits). Atenção: o artigo traz pelo menos um exemplo com erro (3C₁₆ deveria ser 00111100₂). Todos os exemplos deste resumo foram refeitos e conferidos aqui.
- LOPES, Evelin. "Conversão de bases numéricas". Evelin DEV (Substack), 9 mar. 2022. Disponível em: https://evelindev.substack.com/p/conversao-de-bases-numericas — algoritmo de divisões sucessivas (restos invertidos no final).

Todos os exemplos e exercícios deste resumo são próprios e foram conferidos pela conversão inversa.

---

<!-- STATUS DO FLUXO: nota de trabalho, NÃO faz parte do resumo. Remover antes de gerar o resumo.html. -->

## Status do fluxo (nota de trabalho — não entra no resumo final)

Atualizado em 16/10/2026, na **etapa 4 (designer)**: resumo completo desenhado no Paper, **aguardando aprovação do aluno**.

- Concluído: pesquisa, revisão QA, rascunho, exemplo de fração em octal, 3 opções de layout no Paper.
- Layout escolhido pelo aluno: **Opção 3 — Sinalização**, especificado em `templates/layout-escolhido.md`.
- No Paper (arquivo "Resumos Faculdade", Page 1), páginas A4 "Resumo · p. 1" a "Resumo · p. 19", todas conferidas por screenshot.
  - p. 13: Exemplos 11 e 12; p. 14: Exemplo 13, "Quando a fração não fecha", início da seção 4;
  - p. 15: erros 4–12 e início da seção 5; p. 16: fim dos atalhos e seção 6;
  - p. 17–18: seção 7 (gabarito); p. 19: seção 8 (fontes).
- Próximos passos: aluno revisa e aprova no Paper → gerar `resumo.html` (arquivo único, CSS embutido, `@media print`) → commit.
- Lembrete: no Paper o negrito dentro de frases não aparece (limitação da ferramenta); no `resumo.html` ele deve voltar.

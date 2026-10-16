# ResumosFaculdadeClaude

Repositório de resumos de estudo do curso de Sistemas de Informação (CESMAC).
Cada resumo é produzido por uma squad de subagentes em `.claude/agents/`.

## Estrutura

- `resumos/<tema>/` — uma pasta por resumo (ex.: `resumos/conversao-de-bases/`)
  - `pesquisa.md` — saída do pesquisador
  - `rascunho.md` — conteúdo revisado (QA + polimento)
  - `resumo.html` — versão final diagramada
- `templates/layout-escolhido.md` — layout aprovado no Paper (o designer reutiliza nos próximos resumos)

## Fluxo de um resumo

Trabalhe sempre num branch próprio (`resumo/<tema>`), nunca direto na `main`.

1. **pesquisador** → cria `pesquisa.md` com conceitos, exemplos resolvidos e fontes.
2. **revisor-qa** → confere cada conceito, conta e exemplo; corrige erros em `pesquisa.md` e lista o que mudou.
3. **polidor-texto** → transforma em `rascunho.md`: linguagem didática, português correto, ordem lógica.
4. **designer** → no Paper, desenha 3 opções de layout, ESPERA o aluno escolher, desenha o resumo completo e, aprovado, gera `resumo.html`. Requer o app Paper Desktop aberto.

Ao fim de cada etapa: commit pequeno com mensagem clara (ex.: `pesquisa: conversão de bases`)
e **push imediato do branch para o GitHub** (`git push -u origin <branch>`), para o trabalho ficar salvo na nuvem.
Ao pausar o trabalho, também faça commit e push do que estiver pronto.
Pare e mostre o resultado ao aluno antes de passar para a próxima etapa.

## Regras gerais

- Português do Brasil.
- Público: aluno de 1º período. Explique do básico ao avançado, sem pular passos.
- Todo cálculo deve aparecer passo a passo e ser conferido.
- Nada de inventar fontes: cite só o que foi realmente consultado.

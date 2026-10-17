# Pesquisa — Como orquestrar agentes de IA com Claude Code, Orca e GitHub

> **Nota sobre o "Orca" (leia antes).** Existem vários projetos com o nome "Orca". Assumi o
> **Orca da Stably AI** (`github.com/stablyai/orca`, site `onorca.dev`): um aplicativo de desktop
> gratuito e de código aberto (licença MIT) para rodar vários agentes de código (Claude Code, Codex,
> Cursor CLI etc.) **em paralelo**, cada um no seu próprio *git worktree*. Isso foi confirmado no
> README oficial e na documentação oficial (`onorca.dev/docs`). Outros "Orca" achados na busca
> (forks como `MuathJ/orca` e projetos sem relação, como `orca-agent-ide`) **não** foram usados.
> Grau de confiança: **alto** para o que o Orca é e para o fluxo básico (Add Repo → criar worktree →
> escolher agente → revisar diff → commit/push). A CLI `orca worktree create` foi conferida no README
> e no `orca worktree create --help` de uma instalação real; as opções da CLI mudam rápido, então
> confira o `--help` da sua versão antes de usar.
>
> **Nota de versão.** Claude Code e Orca são atualizados com frequência. Tudo aqui foi conferido na
> documentação oficial em **outubro de 2026**.

---

## 1. Objetivo

Ao final, o aluno deve saber:

1. Explicar o que é um **agente de IA**, um **subagente** e um **orquestrador**, e por que vale dividir um trabalho grande em papéis (pesquisa → revisão → texto → design).
2. Instalar o **Claude Code**, escrever um **`CLAUDE.md`** de regras e criar **subagentes** em `.claude/agents/*.md` com `name`, `description` e `tools` corretos.
3. Usar **Git e GitHub** do jeito certo para agentes: um **branch por tema**, **commit pequeno por etapa**, **push**, **pull request**, revisão e **merge** — nunca trabalhar direto na `main`.
4. Rodar vários agentes **em paralelo** com **git worktrees**, pelo terminal (`git worktree`, `claude --worktree`) ou pelo **Orca**, sem um agente atropelar o outro.
5. Recriar do zero a estrutura deste repositório (`ResumosFaculdadeClaude`) e identificar os erros mais comuns (ferramentas demais, ferramentas de menos, pular a pausa humana, conflito entre worktrees).

---

## 2. Conceitos (do básico ao avançado)

### 2.1 Modelo de linguagem (LLM)
**Definição:** programa treinado com muito texto que recebe uma mensagem e gera uma resposta em texto. Sozinho, ele só "conversa": não lê seus arquivos nem roda comandos.
**Exemplo:** perguntar no chat "o que é base binária?" e receber uma explicação.

### 2.2 Agente de IA
**Definição:** um LLM que, além de responder, pode **usar ferramentas** (ler arquivo, escrever arquivo, buscar na web, rodar comando no terminal) em um ciclo: pensa → usa ferramenta → vê o resultado → decide o próximo passo, até terminar a tarefa.
**Exemplo:** o Claude Code recebe "crie `pesquisa.md` sobre conversão de bases", busca fontes na web (`WebSearch`), escreve o arquivo (`Write`) e faz commit (`Bash` com `git commit`).

### 2.3 Ferramentas (tools)
**Definição:** as ações que o agente tem permissão de fazer. No Claude Code, alguns nomes reais: `Read`, `Write`, `Edit`, `Glob` (achar arquivos por padrão), `Grep` (buscar texto), `Bash` (rodar comandos), `WebSearch`, `WebFetch`.
**Exemplo:** um agente só com `Read, Grep, Glob` consegue **ler** o projeto, mas **não consegue alterar** nada — é "somente leitura".

### 2.4 Contexto (janela de contexto)
**Definição:** tudo o que o modelo "tem na cabeça" naquela conversa: suas mensagens, arquivos lidos, resultados de busca. Tem tamanho limitado; se enche de lixo, a qualidade cai.
**Exemplo:** se o agente principal ler 40 páginas de documentação para pesquisar, essas páginas ocupam o contexto da conversa inteira, mesmo quando você já passou para o design.

### 2.5 Subagente
**Definição (doc oficial):** "assistentes de IA especializados que lidam com tipos específicos de tarefa". Cada um roda **na sua própria janela de contexto**, com **prompt de sistema próprio**, **ferramentas próprias** e **permissões próprias**. Ele começa "do zero" (não vê o histórico da conversa principal) e, ao terminar, **devolve só um resumo** para a conversa principal.
**Exemplo:** o subagente `pesquisador` lê dezenas de páginas, mas a conversa principal recebe só "criei `pesquisa.md` com X conceitos, Y exercícios".

### 2.6 Orquestrador
**Definição:** quem **coordena** os agentes: decide quem trabalha, em que ordem, passa a tarefa e recebe o resultado. No Claude Code, o orquestrador é a **conversa principal** (a sessão `claude` que você abriu). No Orca, o orquestrador é **você**, usando o app para controlar várias sessões ao mesmo tempo.
**Exemplo:** neste repositório, a sessão principal chama `pesquisador`, espera, mostra ao aluno, chama `revisor-qa`, e assim por diante.

### 2.7 Pipeline (esteira) e por que dividir em papéis
**Definição:** sequência fixa de etapas em que a saída de uma é a entrada da próxima.
**Por que dividir:**
- **Foco:** cada agente tem instruções curtas e específicas → segue melhor.
- **Contexto limpo:** a sujeira da pesquisa não contamina o design.
- **Segurança:** cada papel recebe só as ferramentas de que precisa (isso se chama **princípio do menor privilégio**).
- **Revisão:** um agente confere o trabalho do outro (o QA acha erro do pesquisador).
**Exemplo (este repo):** `pesquisador` → `pesquisa.md` → `revisor-qa` (corrige `pesquisa.md`) → `polidor-texto` → `rascunho.md` → `designer` → `resumo.html`.

### 2.8 `CLAUDE.md` (memória do projeto)
**Definição:** arquivo Markdown com **instruções permanentes** que o Claude Code carrega **no início de toda sessão**. Pode ficar em:
| Arquivo | Para quem vale | Vai para o Git? |
|---|---|---|
| `./CLAUDE.md` ou `./.claude/CLAUDE.md` | todo mundo do projeto | sim |
| `./CLAUDE.local.md` | só você, neste projeto | não (coloque no `.gitignore`) |
| `~/.claude/CLAUDE.md` | só você, em todos os projetos | não |

A doc recomenda **menos de 200 linhas** por arquivo e instruções **específicas e concisas**. O comando `/init` gera um `CLAUDE.md` inicial. Importante: o `CLAUDE.md` é **contexto, não trava** — o Claude tenta seguir, mas não é garantido (para bloquear algo de verdade, a doc indica *hooks*: scripts que o Claude Code roda automaticamente antes ou depois de cada ação e que podem barrar a ação).
**Exemplo:** o `CLAUDE.md` deste repo diz "Trabalhe sempre num branch próprio (`resumo/<tema>`), nunca direto na `main`" e "Pare e mostre o resultado ao aluno antes de passar para a próxima etapa".

### 2.9 Arquivo de subagente (`.claude/agents/<nome>.md`)
**Definição:** um arquivo Markdown com **frontmatter YAML** (o bloco entre `---`) e, abaixo, o **prompt de sistema** do agente.
- **Obrigatórios:** `name` (identificador único, sem `:`, sem começar com `-`, até 256 caracteres) e `description` (quando o Claude deve delegar para ele). Se faltar `description` ou se o `name` for inválido, o arquivo inteiro é **pulado**: o agente nem aparece.
- **Opcional mais importante:** `tools` (lista do que ele pode usar). **Se omitir, ele herda todas as ferramentas disponíveis.**
- Outros opcionais: `disallowedTools` (lista do que ele **não** pode usar), `model` (`sonnet`, `opus`, `haiku`, `inherit`...), `permissionMode`, `maxTurns`, `isolation: worktree`, entre outros.
- Campos com nome errado são **ignorados sem aviso** (ex.: `max_turns` em vez de `maxTurns`).

Onde ficam:
| Local | Escopo |
|---|---|
| `.claude/agents/` | só este projeto (vai para o Git; a doc recomenda versionar) |
| `~/.claude/agents/` | todos os seus projetos |
Se dois agentes tiverem o mesmo `name`, vale o de **maior prioridade** (projeto vence usuário).

**Exemplo (real, deste repo):**
```markdown
---
name: polidor-texto
description: Use depois do revisor-qa para transformar pesquisa.md em rascunho.md com texto claro, didático e gramaticalmente correto.
tools: Read, Write, Edit, Glob
---

Você é o editor de texto da squad.
...
```

### 2.10 Como um subagente é chamado
Três jeitos (doc oficial):
1. **Automático:** o Claude compara seu pedido com a `description` de cada agente. Frases como "use proactively" na descrição incentivam a delegação.
2. **Por linguagem natural:** "Use o subagente pesquisador para o tema conversão de bases".
3. **Por @-menção:** `@"pesquisador (agent)" tema: matrizes` — garante que **esse** agente rode.
Também dá para abrir a sessão inteira como um agente: `claude --agent pesquisador`.

### 2.11 O que o subagente vê e o que ele NÃO pode fazer
- Vê: o **próprio prompt de sistema** (o texto abaixo do frontmatter) + a tarefa que o orquestrador escreveu + os arquivos `CLAUDE.md` (a menos que `omitClaudeMd: true`) + um retrato do `git status`.
- **Não vê** o histórico da conversa principal.
- **Não pode perguntar nada ao usuário**: a ferramenta `AskUserQuestion` é removida de todo subagente. Por isso a **pausa humana** (ex.: "aluno, escolha o layout 1 a 6") acontece quando o subagente **termina e devolve** a pergunta; quem fala com o aluno é a conversa principal.
- Pode chamar outros subagentes (pela ferramenta `Agent`, que até a versão 2.1.63 se chamava `Task`), até **3 níveis** abaixo da conversa principal (padrão). Para impedir, tire `Agent` da lista de `tools` ou coloque-o em `disallowedTools`.

### 2.12 Git: repositório, commit, branch
- **Repositório (repo):** pasta cujo histórico é controlado pelo Git (pasta oculta `.git/`).
- **Commit:** "foto" salva do projeto com uma mensagem. **Commit pequeno** = uma mudança lógica só (ex.: `pesquisa: conversão de bases`). Facilita revisar e desfazer.
- **Branch:** linha de trabalho separada. A `main` é a versão "oficial". Cada tema ganha seu branch `resumo/<tema>`.
**Exemplo:** `git switch -c resumo/matrizes` cria e entra no branch do tema "matrizes".

### 2.13 GitHub: remoto, push, pull request, revisão, merge
- **Remoto (`origin`):** cópia do repositório no GitHub.
- **Push:** enviar seus commits locais para o GitHub (`git push -u origin resumo/matrizes`).
- **Pull request (PR):** "proposta para juntar mudanças" de um branch (o *head*, ex.: `resumo/matrizes`) em outro (a *base*, ex.: `main`). Tem aba de conversa e aba **Files changed** com o *diff* (a lista de linhas adicionadas e removidas em cada arquivo) para revisar.
- **PR em rascunho (draft):** não pode ser mergeado até ser marcado "pronto para revisão".
- **Merge:** aceitar o PR; as mudanças entram na `main`.
**Exemplo:** `gh pr create --base main --title "Resumo: matrizes" --body "pesquisa + QA + rascunho + html"`.

### 2.14 Git worktree
**Definição (doc do Git):** permite ter **várias pastas de trabalho ligadas ao mesmo repositório**, cada uma com um branch diferente "aberto" ao mesmo tempo. Elas compartilham o histórico (`.git`), mas cada uma tem seus próprios arquivos.
**Regra importante:** por padrão o Git **recusa** abrir o **mesmo branch** em dois worktrees.
**Exemplo:**
```bash
git worktree add -b resumo/matrizes ../resumos-matrizes main
```
cria a pasta `../resumos-matrizes` já no branch novo `resumo/matrizes`, que parte da `main`.

### 2.15 Agentes em paralelo
**Definição:** rodar várias sessões de agente ao mesmo tempo, cada uma em um worktree, para que uma não altere os arquivos da outra.
Formas confirmadas na doc:
- **Claude Code:** `claude --worktree <nome>` (ou `-w <nome>`) abre uma sessão isolada num worktree novo em `.claude/worktrees/<nome>/`, num branch novo chamado `worktree-<nome>`, que parte do branch padrão do remoto (normalmente `main`). O repo precisa ter pelo menos 1 commit.
- **Subagente:** `isolation: worktree` no frontmatter faz aquele subagente trabalhar numa cópia temporária (parte do branch padrão; é apagada se ele não mudar nada).
- **Orca:** app que cria um worktree por tarefa e abre um terminal com o agente escolhido.

### 2.16 Orca (Stably AI)
**Definição:** "ambiente de desenvolvimento de agentes" (*agent development environment*). App de desktop (macOS, Windows, Linux), gratuito, MIT, que junta worktrees, terminais, visualizador de diff, navegador e uma CLI. **Não traz modelo próprio**: você usa suas próprias assinaturas (ex.: Claude Code).
Recursos confirmados no README/site: worktrees paralelos ("mande um prompt para cinco agentes, compare e faça merge do vencedor"), anotar diffs da IA e devolver ao agente, integração com GitHub (ver PRs e issues no app) e Linear, worktrees via SSH, app de celular para acompanhar, CLI (ex.: `orca worktree create --name <nome> [--base-branch <ref>] [--agent <id>] [--prompt <texto>]`).
Instalação confirmada: download em onorca.dev / releases do GitHub, ou `brew install --cask stablyai/orca/orca` (macOS).
**Exemplo:** abrir 3 worktrees `resumo-matrizes`, `resumo-limites`, `resumo-logica` no Orca, cada um com Claude Code rodando a pipeline de um tema diferente.

### 2.17 Claude no GitHub Actions (opcional, avançado)
**Definição:** a action oficial `anthropics/claude-code-action@v1` roda o Claude Code dentro do GitHub. Quem tem permissão de escrita escreve `@claude ...` num comentário de issue ou PR e o Claude responde, podendo criar commits.
Configuração rápida: dentro do `claude`, rodar `/install-github-app` (precisa do `gh` instalado e logado, e ser admin do repo). A chave fica num **secret** (`ANTHROPIC_API_KEY` ou `CLAUDE_CODE_OAUTH_TOKEN`) — **nunca** commitada.
**Exemplo:** num PR do resumo, comentar `@claude confira se todos os exercícios de rascunho.md têm gabarito`.

---

## 3. Métodos (passo a passo com exemplos resolvidos)

### Método A — Instalar e preparar as ferramentas

1. **Git** instalado (`git --version` deve mostrar uma versão).
2. **Conta no GitHub** e, opcionalmente, a **GitHub CLI** (`gh`) logada com `gh auth login`.
3. **Claude Code** (precisa de plano Pro, Max, Team, Enterprise ou conta Console; o plano grátis não inclui):
   - macOS / Linux / WSL:
     ```bash
     curl -fsSL https://claude.ai/install.sh | bash
     ```
   - Windows PowerShell:
     ```powershell
     irm https://claude.ai/install.ps1 | iex
     ```
   - Alternativas: `brew install --cask claude-code` (macOS) ou `npm install -g @anthropic-ai/claude-code` (Node 22+; **não** use `sudo`).
4. Abra um terminal novo e confira: `claude --version` (deve imprimir um número de versão). Diagnóstico: `claude doctor`.
5. Rode `claude` dentro da pasta do projeto e faça login pelo navegador.
6. **(Opcional) Orca:** baixe em onorca.dev ou, no macOS, `brew install --cask stablyai/orca/orca`.

**Conferência (sentido inverso):** se `claude --version` falhar com "command not found", a pasta do programa não entrou no PATH (a lista de pastas onde o terminal procura comandos) → abra um terminal novo ou siga a página de troubleshooting.

---

### Método B — Recriar a estrutura deste repositório do zero (exemplo resolvido central)

**Meta:** chegar exatamente nesta árvore:
```
ResumosFaculdadeClaude/
├── .claude/
│   └── agents/
│       ├── pesquisador.md
│       ├── revisor-qa.md
│       ├── polidor-texto.md
│       └── designer.md
├── resumos/
│   └── .gitkeep
├── templates/
│   └── .gitkeep
├── .gitignore
└── CLAUDE.md
```

**Passo 1 — Criar a pasta e o repositório Git**
```bash
mkdir ResumosFaculdadeClaude
cd ResumosFaculdadeClaude
git init -b main
```

**Passo 2 — Criar as pastas** (o Git não guarda pasta vazia; o `.gitkeep` é um arquivo vazio só para a pasta existir no repo)
```bash
mkdir -p .claude/agents resumos templates
touch resumos/.gitkeep templates/.gitkeep
printf ".DS_Store\nnode_modules/\n" > .gitignore
```

**Passo 3 — Escrever o `CLAUDE.md`** (regras que valem para todos). Conteúdo usado neste repo:
```markdown
# ResumosFaculdadeClaude

Repositório de resumos de estudo do curso de Sistemas de Informação (CESMAC).
Cada resumo é produzido por uma squad de subagentes em `.claude/agents/`.

## Estrutura

- `resumos/<tema>/` — uma pasta por resumo (ex.: `resumos/conversao-de-bases/`)
  - `pesquisa.md` — saída do pesquisador
  - `rascunho.md` — conteúdo revisado (QA + polimento)
  - `resumo.html` — versão final diagramada
- `templates/` — layouts aprovados (o designer reutiliza o escolhido)

## Fluxo de um resumo

Trabalhe sempre num branch próprio (`resumo/<tema>`), nunca direto na `main`.

1. **pesquisador** → cria `pesquisa.md` com conceitos, exemplos resolvidos e fontes.
2. **revisor-qa** → confere cada conceito, conta e exemplo; corrige erros em `pesquisa.md` e lista o que mudou.
3. **polidor-texto** → transforma em `rascunho.md`: linguagem didática, português correto, ordem lógica.
4. **designer** → gera opções de layout, ESPERA o aluno escolher, e só então monta `resumo.html`.

Ao fim de cada etapa: commit pequeno com mensagem clara (ex.: `pesquisa: conversão de bases`).
Pare e mostre o resultado ao aluno antes de passar para a próxima etapa.

## Regras gerais

- Português do Brasil.
- Público: aluno de 1º período. Explique do básico ao avançado, sem pular passos.
- Todo cálculo deve aparecer passo a passo e ser conferido.
- Nada de inventar fontes: cite só o que foi realmente consultado.
```
Repare nos três ingredientes: **onde ficam as coisas**, **a ordem do fluxo** e **as regras de qualidade**.

**Passo 4 — Escrever os 4 subagentes.** Cada um em `.claude/agents/<nome>.md`. Arquivo completo do primeiro:
```markdown
---
name: pesquisador
description: Use no início de um resumo novo para levantar conceitos, exemplos resolvidos e fontes sobre o tema. Salva em resumos/<tema>/pesquisa.md.
tools: Read, Write, Edit, Glob, Grep, WebSearch, WebFetch
---

Você é o pesquisador da squad de resumos.

Tarefa: dado um tema da faculdade, produza `resumos/<tema>/pesquisa.md` com:

1. **Objetivo** — o que o aluno deve saber fazer ao final (3 a 5 itens).
2. **Conceitos** — do básico ao avançado, cada um com definição curta e um exemplo.
3. **Métodos** — passo a passo numerado, com exemplos resolvidos completos.
4. **Atalhos e pegadinhas** — erros comuns em prova.
5. **Exercícios** — 5 a 8, com gabarito no final.
6. **Fontes** — links ou livros realmente consultados.

Regras:
- Confira toda conta antes de escrever (refaça no sentido inverso).
- Não se preocupe com visual; só conteúdo em Markdown.
- Ao terminar, devolva (o commit fica com o orquestrador) um resumo de 3 linhas do que foi produzido.
```
Os outros três seguem o mesmo molde. Resumo dos papéis e ferramentas reais deste repo:

| Agente | Entrada → Saída | `tools` | Tem `Bash`? |
|---|---|---|---|
| `pesquisador` | tema → `pesquisa.md` | Read, Write, Edit, Glob, Grep, WebSearch, WebFetch | **não** |
| `revisor-qa` | `pesquisa.md` → `pesquisa.md` corrigido + seção "Revisão QA" | Read, Edit, Bash, Glob, Grep, WebSearch, WebFetch | sim |
| `polidor-texto` | `pesquisa.md` → `rascunho.md` | Read, Write, Edit, Glob | **não** |
| `designer` | `rascunho.md` → `opcoes.html` → (aluno escolhe) → `templates/<nome>.css` + `resumo.html` | Read, Write, Edit, Bash, Glob | sim |

Por que cada lista é assim:
- `revisor-qa` **não tem `Write`** (só `Edit`): ele corrige o arquivo existente, não cria outro. Tem `Bash` para conferir contas com `python3 -c ...`.
- `polidor-texto` não tem web: ele não deve trazer informação nova, só reescrever.
- `designer` não tem web: só diagrama, não altera conteúdo.

> **Atenção (inconsistência real que este repo já teve e corrigiu):** na primeira versão, os prompts do `pesquisador` e do `polidor-texto` mandavam "faça commit", mas a lista `tools` deles **não inclui `Bash`** — então eles **não conseguiam** rodar `git commit`. Havia duas correções possíveis:
> (a) adicionar `Bash` à lista desses dois; ou
> (b) trocar a instrução por "devolva o resultado; o orquestrador faz o commit".
> O repo escolheu a (b), que mantém o princípio do menor privilégio (commit `squad: commit do pesquisador e do polidor fica com o orquestrador`). Hoje os dois prompts dizem "devolva (o commit fica com o orquestrador) ...". Ver pegadinha 4.5.

**Passo 5 — Primeiro commit e envio ao GitHub**
```bash
git add .
git commit -m "Estrutura da squad de resumos com subagentes"
```
Crie um repositório **vazio** no site do GitHub (sem README, para não dar conflito) e conecte:
```bash
git remote add origin https://github.com/<seu-usuario>/ResumosFaculdadeClaude.git
git push -u origin main
```

**Passo 6 — Conferir que o Claude Code enxerga os agentes.** Abra `claude` na pasta e pergunte: "quais subagentes existem neste projeto?". Devem aparecer os 4 nomes. (Nas versões mais novas, `/agents` só lembra que os agentes ficam em `.claude/agents/`; em versões até a 2.1.197 ele abria um assistente interativo.)

**Conferência (sentido inverso):** liste o que foi criado e compare com a árvore da meta: 4 arquivos em `.claude/agents/` + `CLAUDE.md` + `.gitignore` + 2 `.gitkeep` = **8 arquivos**. Contando na árvore: 4 + 1 + 1 + 1 + 1 = 8. Confere.

---

### Método C — Produzir um resumo com a pipeline (exemplo resolvido: tema "conversão de bases")

1. **Criar o branch do tema** (nunca na `main`):
   ```bash
   git switch main
   git pull
   git switch -c resumo/conversao-de-bases
   ```
2. **Etapa 1 — pesquisador.** No `claude`:
   `Use o subagente pesquisador. Tema: conversão de bases. Pasta: resumos/conversao-de-bases/`
   Resultado: `resumos/conversao-de-bases/pesquisa.md`.
   Commit feito pelo **orquestrador** (a conversa principal), porque o `pesquisador` não tem `Bash`:
   ```bash
   git add resumos/conversao-de-bases/pesquisa.md
   git commit -m "pesquisa: conversão de bases"
   ```
   **PAUSA:** o Claude mostra o resultado; o aluno lê e diz "pode seguir".
3. **Etapa 2 — revisor-qa.** `Use o subagente revisor-qa em resumos/conversao-de-bases/pesquisa.md`.
   Ele refaz contas (ex.: 45₁₀ = 101101₂; conferência inversa: 32 + 8 + 4 + 1 = 45), corrige e adiciona "## Revisão QA". Commit `qa: conversão de bases`. **PAUSA.**
4. **Etapa 3 — polidor-texto.** Gera `rascunho.md` (sem a seção Revisão QA, sem mudar números). Commit `rascunho: conversão de bases`, feito pelo orquestrador (o `polidor-texto` também não tem `Bash`). **PAUSA.**
5. **Etapa 4 — designer.**
   - Se `templates/` não tem layout: cria `opcoes.html` com 6 opções e **devolve a pergunta**. A conversa principal pergunta ao aluno: "Qual layout, de 1 a 6?". **Nada continua sem resposta.**
   - Com a escolha: salva `templates/<nome>.css`, monta `resumo.html`. Commit `design: conversão de bases`.
6. **Publicar e revisar:**
   ```bash
   git push -u origin resumo/conversao-de-bases
   gh pr create --base main --title "Resumo: conversão de bases" --body "pesquisa, QA, rascunho e HTML"
   ```
   No GitHub, abra o PR → aba **Files changed** → leia o diff → **Merge pull request**.
7. **Limpar:** `git switch main && git pull` (agora a `main` tem o resumo) e, se quiser, `git branch -d resumo/conversao-de-bases`. (Se o PR foi mergeado com **Squash and merge**, o Git não reconhece o branch como mergeado e o `-d` recusa; aí, depois de conferir que o PR entrou, use `git branch -D`.)

**Conferência (contagem):** etapas = 4 → commits no branch = 4 (`pesquisa`, `qa`, `rascunho`, `design`). Pausas: 4 (uma ao fim de cada etapa, regra do `CLAUDE.md`) + 1 (escolha de layout dentro do designer, só quando não há template) = **5**. Inverso: 5 − 1 = 4 = número de etapas. Confere.

> Observação: os nomes `qa:`, `rascunho:` e `design:` seguem o padrão do exemplo `pesquisa: conversão de bases` do `CLAUDE.md`; o repositório só fixa o exemplo da pesquisa.

---

### Método D — Vários temas em paralelo com worktrees (terminal puro)

Cenário: produzir **matrizes** e **lógica proposicional** ao mesmo tempo.

1. Na pasta principal (na `main`, com pelo menos 1 commit), crie um worktree por tema, cada um com **branch próprio**:
   ```bash
   git worktree add -b resumo/matrizes ../resumos-matrizes main
   git worktree add -b resumo/logica-proposicional ../resumos-logica main
   ```
2. Abra **dois terminais**:
   ```bash
   # terminal 1
   cd ../resumos-matrizes && claude
   # terminal 2
   cd ../resumos-logica && claude
   ```
   Cada sessão roda a pipeline do Método C no seu tema. Como são pastas diferentes, um agente **não sobrescreve** os arquivos do outro.
   (Atalho do Claude Code: `claude --worktree matrizes` cria e abre o worktree isolado em um comando. Atenção: ele cria a pasta `.claude/worktrees/matrizes/` e o branch `worktree-matrizes`, **não** `resumo/matrizes`. Para seguir a regra do `CLAUDE.md`, renomeie dentro do worktree com `git branch -m resumo/matrizes`, ou use o `git worktree add` acima. A doc também recomenda pôr `.claude/worktrees/` no `.gitignore`.)
3. Ver o que existe: `git worktree list` (a pasta principal aparece primeiro).
4. Ao terminar cada tema: `git push -u origin resumo/matrizes`, abrir PR, revisar, merge.
5. Remover o worktree (só funciona se estiver limpo: sem mudanças pendentes nem arquivos não rastreados):
   ```bash
   git worktree remove ../resumos-matrizes
   ```
   Se você apagou a pasta "na mão", limpe o registro com `git worktree prune`.

**Conferência:** 2 temas × 4 commits = 8 commits no total, divididos em 2 branches (4 + 4 = 8). Confere.

---

### Método E — Os mesmos temas em paralelo com o Orca

Fluxo da documentação oficial ("Your first 3-agent session"), adaptado:

1. **Add Repo** (barra lateral) → aponte para a pasta local `ResumosFaculdadeClaude`. O Orca usa o branch padrão como **base ref** (normalmente `origin/main`).
2. Clique no **+** ao lado do nome do repo → nome da tarefa `resumo-matrizes`. Em **Advanced → Branch name** dá para forçar o nome `resumo/matrizes` (por padrão o Orca deriva o nome do branch do nome do workspace). Ponto de partida: a base ref.
3. Abre-se um terminal com seletor de agente → escolha **Claude Code**. Como o worktree é uma cópia do repo, o `CLAUDE.md` e os `.claude/agents/` **vêm junto** — a squad funciona igual.
4. Repita para `resumo-logica`.
5. Use **splits** (arraste a aba para a borda) para ver as duas sessões lado a lado.
6. Em cada worktree, abra o **diff**; use **Annotate AI Diff** para comentar linhas e mandar de volta ao agente (é uma forma de pausa humana).
7. **Commit & push** pelo Orca, depois abra o PR no GitHub (ou pelo próprio app, que mostra PRs e issues).
8. Ao terminar, **delete** o worktree no Orca (remove a pasta e o branch local, após confirmação; numa exclusão em lote, se o Git recusar apagar um branch com commits não mergeados, o Orca mantém esse branch e avisa).

Uso avançado ("corrida" de agentes): mandar **o mesmo prompt** a 3 worktrees, comparar os 3 resultados e ficar só com o melhor. Para resumos, isso serve, por exemplo, para gerar 3 versões do `rascunho.md` e escolher a mais clara.

---

### Método F — (Opcional) `@claude` no GitHub

1. Instale a GitHub CLI (`gh`) e faça login: `gh auth login`.
2. No `claude`, rode `/install-github-app` e siga as instruções (precisa ser admin do repo). Ele instala o app do Claude, salva o secret, envia um branch com o workflow `.github/workflows/claude.yml` e abre o navegador com o PR pronto para você criar.
3. Crie e faça merge desse PR.
4. Num PR de resumo, comente: `@claude verifique se rascunho.md manteve todos os números de pesquisa.md`.
5. Lembre: só quem tem **acesso de escrita** dispara; cada execução gasta minutos do GitHub Actions e tokens.

---

## 4. Atalhos e pegadinhas

4.1 **Commitar direto na `main`.** O `CLAUDE.md` proíbe. Antes de pedir qualquer etapa, rode `git branch --show-current`; deve mostrar `resumo/<tema>`. Lembre que o `CLAUDE.md` é **contexto, não trava**: o Claude pode errar; para bloquear de verdade, use proteção de branch no GitHub ou *hooks*.

4.2 **Agente com ferramentas demais.** Omitir `tools` = herdar **todas** as ferramentas. Um `polidor-texto` com `Bash` e `WebFetch` pode "inventar" conteúdo novo ou rodar comandos que não devia. Regra: dê só o necessário (menor privilégio).

4.3 **Nome de campo errado no frontmatter.** `max_turns`, `Tools`, `nome` etc. são **ignorados em silêncio**. Use exatamente `name`, `description`, `tools`, `model`, `maxTurns`.

4.4 **`description` vaga.** "Agente útil" não diz quando usar → o Claude não delega na hora certa. Diga **quando** ("Use depois do revisor-qa para...") e **o que entrega**.

4.5 **Agente com ferramentas de menos para o que o prompt pede.** Pedir "faça commit" a um agente sem `Bash` não funciona. Isso aconteceu de verdade neste repo com `pesquisador` e `polidor-texto`, e já foi corrigido: em vez de dar `Bash` a eles, o prompt passou a dizer "devolva (o commit fica com o orquestrador)", e quem roda `git commit` é a conversa principal. Confira sempre se o prompt e a lista `tools` combinam.

4.6 **Pular a pausa humana.** Encadear as 4 etapas sem parar faz um erro da pesquisa passar pelo QA, virar texto bonito e ir para o HTML. Além disso, **subagente não consegue perguntar ao usuário** (não tem `AskUserQuestion`): a pergunta "qual layout?" tem que ser devolvida à conversa principal.

4.7 **Achar que o subagente "lembra" da conversa.** Ele começa do zero. O que importa (tema, pasta, restrições) tem que ir **no prompt de delegação**.

4.8 **Mesmo branch em dois worktrees.** O Git recusa por padrão. Cada worktree = um branch diferente. Forçar com `--force` é pedir confusão.

4.9 **Conflitos entre worktrees.** Dois temas não conflitam (pastas `resumos/<tema>/` diferentes). Mas se **os dois** alteram o mesmo arquivo compartilhado (ex.: `templates/paper.css` ou o `CLAUDE.md`), o segundo PR terá **conflito de merge**. Regra prática: arquivos compartilhados só mudam num PR dedicado.

4.10 **`CLAUDE.local.md` e worktrees.** Ele fica no `.gitignore`, então **não existe** nos worktrees novos. Para levar preferências pessoais deste projeto a todos os worktrees, a doc indica guardar num arquivo da sua pasta pessoal e importá-lo (ex.: uma linha `@~/.claude/minhas-instrucoes.md`); se a preferência vale para todos os projetos, use `~/.claude/CLAUDE.md`.

4.11 **`claude --worktree` em repo sem commit.** Falha (`Failed to resolve base branch "HEAD"`). Faça o primeiro commit antes.

4.12 **Remover worktree com mudanças pendentes.** `git worktree remove` recusa (mensagem: `contains modified or untracked files, use --force to delete it`). Faça commit (ou descarte) antes.

4.13 **Chave de API no repositório.** Nunca. No GitHub Actions use **Secrets** (`${{ secrets.ANTHROPIC_API_KEY }}`).

4.14 **Orca não é modelo de IA.** Ele não "pensa"; ele organiza worktrees e terminais. Quem faz o trabalho é o agente (Claude Code) com a sua assinatura.

4.15 **`CLAUDE.md` gigante.** Acima de ~200 linhas, a adesão cai. Detalhes de um papel vão no arquivo do agente, não no `CLAUDE.md`.

---

## 5. Exercícios

**E1.** Escreva o arquivo completo `.claude/agents/verificador-fontes.md` para um agente que só **confere se os links da seção Fontes de `pesquisa.md` abrem**, sem alterar nenhum arquivo.

**E2.** Pela tabela do Método B, quais agentes deste repositório **conseguem** rodar `git commit` sozinhos? Quais não? Na primeira versão do repo, os que não conseguiam recebiam a ordem "faça commit". Quais eram as duas correções possíveis, qual o repo escolheu e por quê?

**E3.** Encontre os **4 erros** neste arquivo de agente:
```markdown
---
name: revisor:qa
Tools: Read, Edit
max_turns: 10
---
Você revisa resumos.
```

**E4.** Escreva, em ordem, os comandos para: (a) sair da `main` atualizada para um branch novo do tema "limites"; (b) depois da etapa de pesquisa, commitar só o arquivo da pesquisa; (c) enviar o branch para o GitHub.

**E5.** Você rodou:
```bash
git worktree add -b resumo/matrizes ../wt1 main
git worktree add ../wt2 resumo/matrizes
```
O que acontece no segundo comando? Por quê? Como corrigir?

**E6.** Três temas são produzidos **um depois do outro** pela pipeline. No início não há nenhum layout em `templates/`. Quantos **commits** e quantas **pausas humanas** acontecem no total? (Use: 1 commit por etapa; 1 pausa ao fim de cada etapa; +1 pausa de escolha de layout sempre que `templates/` estiver vazio.)

**E7.** A conversa principal chama o agente A, que chama B, que chama C, que tenta chamar D. Com a configuração padrão, quais chamadas funcionam? Como impedir que o `pesquisador` chame qualquer subagente?

**E8.** Você quer que o Claude sempre responda com frases curtas **em todos os seus projetos**, mas isso é preferência sua, não do grupo. Onde escreve essa instrução? E se fosse uma preferência só deste projeto e só sua?

---

### Gabarito

**E1.** Exemplo de resposta correta:
```markdown
---
name: verificador-fontes
description: Use depois do pesquisador para conferir se cada link da seção Fontes de resumos/<tema>/pesquisa.md abre e trata do tema. Não altera arquivos.
tools: Read, Grep, WebFetch
---

Você é o verificador de fontes da squad.

1. Leia a seção "Fontes" de `resumos/<tema>/pesquisa.md`.
2. Abra cada link com WebFetch.
3. Devolva uma lista: link → "ok" ou "problema: <motivo>".
Não edite nenhum arquivo.
```
Pontos que precisam estar presentes: `name` sem `:`; `description` dizendo **quando** usar; `tools` **sem** `Write`, `Edit` e `Bash` (somente leitura + web).

**E2.** Conseguem: `revisor-qa` e `designer` (têm `Bash`). Não conseguem: `pesquisador` e `polidor-texto` (sem `Bash`). Correções possíveis: (a) adicionar `Bash` ao `tools` deles, ou (b) mudar o prompt para "devolva o resultado; o orquestrador faz o commit". O repo escolheu a (b), pelo menor privilégio: os dois continuam sem `Bash` e o prompt atual diz "devolva (o commit fica com o orquestrador)". Conferência: 2 conseguem + 2 não = 4 agentes. Confere.

**E3.**
1. `name: revisor:qa` — `name` **não pode conter `:`** → `revisor-qa`.
2. Falta `description`, que é **obrigatória**.
3. `Tools` com T maiúsculo → nome de campo errado, **ignorado** → o agente herdaria **todas** as ferramentas. Correto: `tools`.
4. `max_turns` → ignorado. Correto: `maxTurns`.

Observação: por causa dos erros 1 e 2 (nome com `:` e falta de `description`), o Claude Code **pula o arquivo inteiro**: o agente nem chega a ser carregado. Os erros 3 e 4 só fariam efeito depois de corrigidos os dois primeiros.

**E4.**
```bash
# (a)
git switch main
git pull
git switch -c resumo/limites
# (b)
git add resumos/limites/pesquisa.md
git commit -m "pesquisa: limites"
# (c)
git push -u origin resumo/limites
```

**E5.** O segundo comando **falha** (`fatal: 'resumo/matrizes' is already used by worktree at '.../wt1'`): o branch `resumo/matrizes` já está aberto no worktree `../wt1`, e por padrão o Git recusa abrir o mesmo branch em dois worktrees. Correção: criar outro branch, por exemplo `git worktree add -b resumo/limites ../wt2 main`, ou trabalhar em `../wt1`.

**E6.**
- Commits: 3 temas × 4 etapas = **12**. Inverso: 12 ÷ 4 = 3 temas. Confere.
- Pausas: tema 1 = 4 + 1 (escolha de layout, `templates/` vazio) = 5. Depois disso o designer salva `templates/<nome>.css`, então os temas 2 e 3 pulam a escolha: 4 + 4. Total = 5 + 4 + 4 = **13**. Inverso: 13 − 1 = 12 = 3 × 4. Confere.

**E7.** Padrão: até **3 níveis abaixo** da conversa principal. A = nível 1, B = nível 2, C = nível 3 → as chamadas principal→A, A→B e B→C funcionam. D seria nível 4 → a chamada C→D é **bloqueada** (no limite, o Claude Code tira a ferramenta `Agent` de C). Inverso: 4 − 3 = 1 nível além do limite. Para impedir o `pesquisador` de chamar subagentes: **não** listar `Agent` no `tools` dele (como já acontece neste repo) ou colocá-lo em `disallowedTools`.

**E8.** Em todos os projetos e só para você: `~/.claude/CLAUDE.md`. Só neste projeto e só para você: `./CLAUDE.local.md` (e adicionar ao `.gitignore`). O `./CLAUDE.md` do projeto é para regras do **grupo** e vai para o Git.

---

## 6. Fontes (realmente consultadas, outubro de 2026)

**Este repositório (exemplo central):**
- `CLAUDE.md`, `.claude/agents/pesquisador.md`, `revisor-qa.md`, `polidor-texto.md`, `designer.md`, `.gitignore` — https://github.com/briito-yuri/ResumosFaculdadeClaude (lidos localmente)

**Anthropic — documentação oficial do Claude Code:**
- Subagentes: https://code.claude.com/docs/en/sub-agents
- Memória / `CLAUDE.md`: https://code.claude.com/docs/en/memory
- Instalação (Advanced setup): https://code.claude.com/docs/en/setup
- Fluxos comuns (worktrees paralelos, `claude --worktree`, subagentes de pesquisa): https://code.claude.com/docs/en/common-workflows
- Claude Code GitHub Actions: https://code.claude.com/docs/en/github-actions
- Worktrees (`claude --worktree`, pasta `.claude/worktrees/`, branch `worktree-<nome>`, `isolation: worktree`): https://code.claude.com/docs/en/worktrees (acrescentada na revisão QA)

**Orca (Stably AI):**
- Repositório/README oficial: https://github.com/stablyai/orca
- Site oficial: https://onorca.dev/
- Doc "Your first 3-agent session": https://www.onorca.dev/docs/first-session
- Doc de worktrees: https://www.onorca.dev/docs/model/worktrees
- Ajuda da CLI instalada: `orca worktree create --help` (conferida na revisão QA)

**Git e GitHub:**
- `git worktree` (doc oficial do Git): https://git-scm.com/docs/git-worktree
- Sobre pull requests (GitHub Docs): https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests
- `gh pr create` (manual da GitHub CLI): https://cli.github.com/manual/gh_pr_create

Observação: comandos básicos do Git (`git init`, `git add`, `git commit`, `git switch`, `git push`, `git remote add`) foram usados na forma padrão, sem consulta a uma página específica nesta pesquisa.

---

## Revisão QA

Conferido em outubro de 2026 contra a documentação oficial (Claude Code: sub-agents, memory, setup, common-workflows, worktrees, github-actions; Orca: README, onorca.dev, docs first-session e worktrees; GitHub Docs; manual do `gh`), contra os arquivos reais do repositório (`CLAUDE.md` idêntico ao do Passo 3; `.gitignore`; `.claude/agents/*.md`) e com testes locais (`git worktree` em pasta temporária, `claude --help` v2.1.302, `orca worktree create --help`).

O que mudou:

1. **Pesquisador e polidor-texto (mudança recente do repo).** Passo 4 do Método B agora mostra a linha real atual do `pesquisador.md` ("devolva (o commit fica com o orquestrador) ..."). O quadro "Atenção" virou histórico de um problema **já resolvido** pela opção (b). Método C: os commits das etapas 1 e 3 passam a ser do orquestrador. Pegadinha 4.5 e exercício E2 (enunciado e gabarito) reescritos como problema já resolvido.
2. **`claude --worktree` (2.15 e Método D):** faltava dizer que ele cria `.claude/worktrees/<nome>/` e o branch `worktree-<nome>` (não `resumo/<tema>`), partindo do branch padrão do remoto. Acrescentados o atalho `-w`, como renomear (`git branch -m resumo/matrizes`) e a dica de pôr `.claude/worktrees/` no `.gitignore`.
3. **CLI do Orca:** `orca worktree create` foi confirmado (README e `--help`). Nota inicial deixou de marcar como "confiança média" e 2.16 agora mostra a sintaxe real (`--name`, `--base-branch`, `--agent`, `--prompt`).
4. **Método E, passo 8:** "o Orca mantém o branch com commits não mergeados" vale, segundo a doc, para **exclusão em lote**. Texto ajustado.
5. **Método F:** o `/install-github-app` não abre o PR sozinho. Ele envia um branch e abre o navegador com o PR **pronto para você criar**. Passos 1 a 3 corrigidos.
6. **4.10 (`CLAUDE.local.md` e worktrees):** a doc indica **importar** um arquivo da pasta pessoal (`@~/.claude/...`) para levar preferências de um projeto a todos os worktrees. `~/.claude/CLAUDE.md` serve só quando a regra vale para todos os projetos.
7. **2.9 (frontmatter):** regras do `name` completadas (sem `:`, sem começar com `-`, até 256 caracteres). Explicado que o arquivo inteiro é **pulado** se faltar `description` ou o `name` for inválido. Acrescentado `disallowedTools`.
8. **E3, gabarito:** observação nova. Com `name: revisor:qa` e sem `description`, o agente **nem carrega**, então os erros 3 e 4 só teriam efeito depois de corrigidos os dois primeiros.
9. **2.11 e E7:** o subagente também vê o próprio prompt de sistema e um retrato do `git status`. Explicado que a ferramenta `Agent` se chamava `Task` até a versão 2.1.63. No E7, ficou claro quais **chamadas** funcionam (principal→A, A→B, B→C) e que C→D é bloqueada porque C perde a ferramenta `Agent`.
10. **Método C, passo 7:** com "Squash and merge", o `git branch -d` recusa. Acrescentado o aviso e a alternativa `-D`.
11. **Mensagens de erro reais** (testadas) acrescentadas ao E5 (`is already used by worktree`) e ao 4.12 (`contains modified or untracked files`). No Método D, a remoção também exige "sem arquivos não rastreados".
12. **Lacunas de vocabulário:** termos usados antes de serem explicados agora têm definição curta: *menor privilégio* (2.7), *hooks* (2.8), *diff* (2.13) e *PATH* (Método A).
13. **Fontes:** acrescentadas apenas páginas abertas nesta revisão (`code.claude.com/docs/en/worktrees` e o `--help` da CLI do Orca). Todas as outras fontes foram abertas e confirmadas.

Conferido e **sem erro**: comandos de instalação (curl, irm, `brew install --cask claude-code`, npm com Node 22+ e sem `sudo`), planos exigidos, `claude doctor`, `claude --agent`, sintaxe de @-menção, "use proactively", limite de 3 níveis, remoção de `AskUserQuestion` em subagentes, `omitClaudeMd`, `/agents` (até a 2.1.197), `isolation: worktree`, erro `Failed to resolve base branch "HEAD"`, limite de 200 linhas e `/init`, `brew install --cask stablyai/orca/orca`, recursos do Orca, action `anthropics/claude-code-action@v1`, nomes dos secrets, acesso de escrita para `@claude`, PR em rascunho não pode ser mergeado, flags do `gh pr create`. Contagens também conferidas: 8 arquivos no Método B, 4 commits e 5 pausas no Método C, 8 commits no Método D, E6 = 12 commits e 13 pausas.

# Como orquestrar agentes de IA com Claude Code, Orca e GitHub

Este guia usa o próprio repositório `ResumosFaculdadeClaude` como exemplo. Você vai ver como uma "squad" de agentes de IA produz um resumo de estudo, etapa por etapa, com Git e GitHub cuidando do histórico.

> **Antes de começar: qual "Orca"?** Existem vários projetos com esse nome. Aqui, "Orca" é o **Orca da Stably AI** (`github.com/stablyai/orca`, site `onorca.dev`). É um aplicativo de desktop gratuito e de código aberto (licença MIT). Ele roda vários agentes de código (Claude Code, Codex, Cursor CLI etc.) **em paralelo**, cada um no seu próprio *git worktree*. Confirmamos isso no README e na documentação oficial (`onorca.dev/docs`). Outros "Orca" que aparecem na busca (forks como `MuathJ/orca` e projetos sem relação, como `orca-agent-ide`) **não** entram aqui.
>
> O grau de confiança é **alto** para o que o Orca é e para o fluxo básico (Add Repo → criar worktree → escolher agente → revisar diff → commit/push). Conferimos a CLI `orca worktree create` no README e no `orca worktree create --help` de uma instalação real. Mas as opções da CLI mudam rápido: confira o `--help` da sua versão antes de usar.
>
> **Versão.** Claude Code e Orca mudam com frequência. Tudo aqui foi conferido na documentação oficial em **outubro de 2026**.

---

## 1. O que você vai aprender

Ao final, você deve conseguir:

1. Explicar o que é um **agente de IA**, um **subagente** e um **orquestrador**. E entender por que vale dividir um trabalho grande em papéis (pesquisa → revisão → texto → design).
2. Instalar o **Claude Code**, escrever um **`CLAUDE.md`** de regras e criar **subagentes** em `.claude/agents/*.md` com `name`, `description` e `tools` corretos.
3. Usar **Git e GitHub** do jeito certo com agentes: um **branch por tema**, **commit pequeno por etapa**, **push**, **pull request**, revisão e **merge**. Nunca trabalhar direto na `main`.
4. Rodar vários agentes **em paralelo** com **git worktrees**, pelo terminal (`git worktree`, `claude --worktree`) ou pelo **Orca**, sem um agente atropelar o outro.
5. Recriar do zero a estrutura deste repositório (`ResumosFaculdadeClaude`) e reconhecer os erros mais comuns: ferramentas demais, ferramentas de menos, pular a pausa humana e conflito entre worktrees.

---

## 2. Conceitos, do básico ao avançado

### 2.1 Modelo de linguagem (LLM)

Um LLM é um programa treinado com muito texto. Ele recebe uma mensagem e gera uma resposta em texto. Sozinho, ele só "conversa": não lê seus arquivos nem roda comandos.

**Exemplo:** você pergunta no chat "o que é base binária?" e recebe uma explicação.

### 2.2 Agente de IA

Um agente é um LLM que também pode **usar ferramentas**: ler arquivo, escrever arquivo, buscar na web, rodar comando no terminal. Ele trabalha em ciclo: pensa → usa uma ferramenta → vê o resultado → decide o próximo passo. E repete até terminar a tarefa.

**Exemplo:** o Claude Code recebe "crie `pesquisa.md` sobre conversão de bases". Ele busca fontes na web (`WebSearch`), escreve o arquivo (`Write`) e faz commit (`Bash` com `git commit`).

### 2.3 Ferramentas (tools)

Ferramentas são as ações que o agente tem permissão de fazer. No Claude Code, alguns nomes reais são: `Read`, `Write`, `Edit`, `Glob` (achar arquivos por padrão), `Grep` (buscar texto), `Bash` (rodar comandos), `WebSearch` e `WebFetch`.

**Exemplo:** um agente só com `Read, Grep, Glob` consegue **ler** o projeto, mas **não consegue alterar** nada. Ele é "somente leitura".

### 2.4 Contexto (janela de contexto)

O contexto é tudo o que o modelo "tem na cabeça" naquela conversa: suas mensagens, os arquivos lidos, os resultados de busca. O tamanho é limitado. Se o contexto enche de lixo, a qualidade cai.

**Exemplo:** se o agente principal ler 40 páginas de documentação para pesquisar, essas páginas ocupam o contexto da conversa inteira. Elas continuam lá mesmo quando você já passou para o design.

### 2.5 Subagente

A documentação oficial define subagentes como "assistentes de IA especializados que lidam com tipos específicos de tarefa". Cada um tem:

- **janela de contexto própria**;
- **prompt de sistema próprio**;
- **ferramentas próprias**;
- **permissões próprias**.

O subagente começa "do zero": não vê o histórico da conversa principal. Ao terminar, ele **devolve só um resumo** para a conversa principal.

**Exemplo:** o subagente `pesquisador` lê dezenas de páginas. A conversa principal recebe só "criei `pesquisa.md` com X conceitos, Y exercícios".

### 2.6 Orquestrador

O orquestrador **coordena** os agentes. Ele decide quem trabalha e em que ordem, passa a tarefa e recebe o resultado.

- No **Claude Code**, o orquestrador é a **conversa principal** (a sessão `claude` que você abriu).
- No **Orca**, o orquestrador é **você**, usando o app para controlar várias sessões ao mesmo tempo.

**Exemplo:** neste repositório, a sessão principal chama o `pesquisador`, espera, mostra o resultado ao aluno, chama o `revisor-qa`, e assim por diante.

### 2.7 Pipeline (esteira) e por que dividir em papéis

Uma pipeline é uma sequência fixa de etapas. A saída de uma etapa é a entrada da próxima.

Por que dividir o trabalho em papéis:

- **Foco:** cada agente recebe instruções curtas e específicas, e segue melhor.
- **Contexto limpo:** a sujeira da pesquisa não contamina o design.
- **Segurança:** cada papel recebe só as ferramentas de que precisa. Isso se chama **princípio do menor privilégio**.
- **Revisão:** um agente confere o trabalho do outro. O QA acha erro do pesquisador.

**Exemplo (este repo):** `pesquisador` → `pesquisa.md` → `revisor-qa` (corrige `pesquisa.md`) → `polidor-texto` → `rascunho.md` → `designer` → `resumo.html`.

### 2.8 `CLAUDE.md`: a memória do projeto

O `CLAUDE.md` é um arquivo Markdown com **instruções permanentes**. O Claude Code carrega esse arquivo **no início de toda sessão**. Ele pode ficar em três lugares:

| Arquivo | Para quem vale | Vai para o Git? |
|---|---|---|
| `./CLAUDE.md` ou `./.claude/CLAUDE.md` | todo mundo do projeto | sim |
| `./CLAUDE.local.md` | só você, neste projeto | não (coloque no `.gitignore`) |
| `~/.claude/CLAUDE.md` | só você, em todos os projetos | não |

Dicas da documentação:

- Mantenha cada arquivo com **menos de 200 linhas**.
- Escreva instruções **específicas e concisas**.
- O comando `/init` gera um `CLAUDE.md` inicial.

**Importante:** o `CLAUDE.md` é **contexto, não trava**. O Claude tenta seguir, mas não há garantia. Para bloquear algo de verdade, a documentação indica *hooks*: scripts que o Claude Code roda automaticamente antes ou depois de cada ação e que podem barrar essa ação.

**Exemplo:** o `CLAUDE.md` deste repo diz "Trabalhe sempre num branch próprio (`resumo/<tema>`), nunca direto na `main`" e "Pare e mostre o resultado ao aluno antes de passar para a próxima etapa".

### 2.9 O arquivo de um subagente (`.claude/agents/<nome>.md`)

Cada subagente é um arquivo Markdown com duas partes:

1. um **frontmatter YAML** no topo (o bloco entre `---`);
2. logo abaixo, o **prompt de sistema** do agente.

Campos do frontmatter:

- **Obrigatórios:**
  - `name`: identificador único. Não pode ter `:`, não pode começar com `-` e tem até 256 caracteres.
  - `description`: diz quando o Claude deve delegar para esse agente.
  - Se faltar `description` ou se o `name` for inválido, o arquivo inteiro é **pulado**. O agente nem aparece.
- **Opcional mais importante:** `tools`, a lista do que o agente pode usar. **Se você omitir, ele herda todas as ferramentas disponíveis.**
- **Outros opcionais:** `disallowedTools` (lista do que ele **não** pode usar), `model` (`sonnet`, `opus`, `haiku`, `inherit`...), `permissionMode`, `maxTurns`, `isolation: worktree`, entre outros.
- **Cuidado:** campos com nome errado são **ignorados sem aviso**. Por exemplo, `max_turns` em vez de `maxTurns`.

Onde os arquivos ficam:

| Local | Escopo |
|---|---|
| `.claude/agents/` | só este projeto (vai para o Git; a doc recomenda versionar) |
| `~/.claude/agents/` | todos os seus projetos |

Se dois agentes tiverem o mesmo `name`, vale o de **maior prioridade**: o do projeto vence o do usuário.

**Exemplo real deste repo:**
```markdown
---
name: polidor-texto
description: Use depois do revisor-qa para transformar pesquisa.md em rascunho.md com texto claro, didático e gramaticalmente correto.
tools: Read, Write, Edit, Glob
---

Você é o editor de texto da squad.
...
```

### 2.10 Como chamar um subagente

A documentação oficial mostra três jeitos:

1. **Automático:** o Claude compara seu pedido com a `description` de cada agente. Frases como "use proactively" na descrição incentivam a delegação.
2. **Por linguagem natural:** "Use o subagente pesquisador para o tema conversão de bases".
3. **Por @-menção:** `@"pesquisador (agent)" tema: matrizes`. Isso garante que **esse** agente rode.

Você também pode abrir a sessão inteira como um agente: `claude --agent pesquisador`.

### 2.11 O que o subagente vê e o que ele não pode fazer

**O que ele vê:**
- o **próprio prompt de sistema** (o texto abaixo do frontmatter);
- a tarefa que o orquestrador escreveu;
- os arquivos `CLAUDE.md` (a menos que `omitClaudeMd: true`);
- um retrato do `git status`.

**O que ele não vê:** o histórico da conversa principal.

**O que ele não pode fazer:**
- **Perguntar algo ao usuário.** A ferramenta `AskUserQuestion` é removida de todo subagente. Por isso a **pausa humana** (ex.: "aluno, escolha o layout 1 a 6") acontece quando o subagente **termina e devolve** a pergunta. Quem fala com o aluno é a conversa principal.
- **Descer mais de 3 níveis.** Um subagente pode chamar outros pela ferramenta `Agent` (que se chamava `Task` até a versão 2.1.63). O padrão permite até **3 níveis** abaixo da conversa principal. Para impedir que ele chame outros, tire `Agent` da lista de `tools` ou coloque-o em `disallowedTools`.

### 2.12 Git: repositório, commit e branch

- **Repositório (repo):** pasta cujo histórico o Git controla (pela pasta oculta `.git/`).
- **Commit:** uma "foto" salva do projeto, com uma mensagem. Um **commit pequeno** traz uma mudança lógica só (ex.: `pesquisa: conversão de bases`). Isso facilita revisar e desfazer.
- **Branch:** uma linha de trabalho separada. A `main` é a versão "oficial". Cada tema ganha seu branch `resumo/<tema>`.

**Exemplo:** `git switch -c resumo/matrizes` cria o branch do tema "matrizes" e já entra nele.

### 2.13 GitHub: remoto, push, pull request, revisão e merge

- **Remoto (`origin`):** a cópia do repositório no GitHub.
- **Push:** envia seus commits locais para o GitHub (`git push -u origin resumo/matrizes`).
- **Pull request (PR):** uma "proposta para juntar mudanças" de um branch (o *head*, ex.: `resumo/matrizes`) em outro (a *base*, ex.: `main`). O PR tem uma aba de conversa e a aba **Files changed**, com o *diff* para revisar. O diff é a lista de linhas adicionadas e removidas em cada arquivo.
- **PR em rascunho (draft):** não pode ser mergeado até ser marcado como "pronto para revisão".
- **Merge:** aceita o PR; as mudanças entram na `main`.

**Exemplo:** `gh pr create --base main --title "Resumo: matrizes" --body "pesquisa + QA + rascunho + html"`.

### 2.14 Git worktree

Segundo a documentação do Git, um worktree permite ter **várias pastas de trabalho ligadas ao mesmo repositório**. Cada pasta fica com um branch diferente "aberto" ao mesmo tempo. Elas compartilham o histórico (`.git`), mas cada uma tem seus próprios arquivos.

**Regra importante:** por padrão, o Git **recusa** abrir o **mesmo branch** em dois worktrees.

**Exemplo:**
```bash
git worktree add -b resumo/matrizes ../resumos-matrizes main
```
Esse comando cria a pasta `../resumos-matrizes` já no branch novo `resumo/matrizes`, que parte da `main`.

### 2.15 Agentes em paralelo

Rodar agentes em paralelo é abrir várias sessões ao mesmo tempo, cada uma em um worktree. Assim, uma sessão não altera os arquivos da outra. A documentação confirma três formas:

- **Claude Code:** `claude --worktree <nome>` (ou `-w <nome>`) abre uma sessão isolada num worktree novo.
  - A pasta fica em `.claude/worktrees/<nome>/`.
  - O branch novo se chama `worktree-<nome>` e parte do branch padrão do remoto (normalmente `main`).
  - O repo precisa ter pelo menos 1 commit.
- **Subagente:** `isolation: worktree` no frontmatter faz o subagente trabalhar numa cópia temporária. Ela parte do branch padrão e é apagada se ele não mudar nada.
- **Orca:** o app cria um worktree por tarefa e abre um terminal com o agente escolhido.

### 2.16 Orca (Stably AI)

O Orca se define como um "ambiente de desenvolvimento de agentes" (*agent development environment*). É um app de desktop para macOS, Windows e Linux, gratuito e com licença MIT. Ele junta worktrees, terminais, visualizador de diff, navegador e uma CLI.

O Orca **não traz modelo próprio**. Você usa suas próprias assinaturas (ex.: Claude Code).

Recursos confirmados no README e no site:
- worktrees paralelos ("mande um prompt para cinco agentes, compare e faça merge do vencedor");
- anotar diffs da IA e devolver ao agente;
- integração com GitHub (ver PRs e issues no app) e com Linear;
- worktrees via SSH;
- app de celular para acompanhar;
- CLI, por exemplo: `orca worktree create --name <nome> [--base-branch <ref>] [--agent <id>] [--prompt <texto>]`.

**Instalação:** baixe em onorca.dev ou nas releases do GitHub. No macOS, também dá para usar `brew install --cask stablyai/orca/orca`.

**Exemplo:** abrir 3 worktrees no Orca (`resumo-matrizes`, `resumo-limites`, `resumo-logica`), cada um com o Claude Code rodando a pipeline de um tema diferente.

### 2.17 Claude no GitHub Actions (opcional, avançado)

A action oficial `anthropics/claude-code-action@v1` roda o Claude Code dentro do GitHub. Quem tem permissão de escrita escreve `@claude ...` num comentário de issue ou PR. O Claude responde e pode até criar commits.

**Configuração rápida:** dentro do `claude`, rode `/install-github-app`. Você precisa do `gh` instalado e logado, e precisa ser admin do repo. A chave fica num **secret** (`ANTHROPIC_API_KEY` ou `CLAUDE_CODE_OAUTH_TOKEN`). **Nunca** faça commit da chave.

**Exemplo:** num PR do resumo, comente `@claude confira se todos os exercícios de rascunho.md têm gabarito`.

---

## 3. Métodos: passo a passo com exemplos resolvidos

### Método A — Instalar e preparar as ferramentas

1. **Git** instalado: `git --version` deve mostrar uma versão.
2. **Conta no GitHub** e, se quiser, a **GitHub CLI** (`gh`) logada com `gh auth login`.
3. **Claude Code.** Ele exige plano Pro, Max, Team, Enterprise ou conta Console; o plano grátis não inclui.
   - macOS / Linux / WSL:
     ```bash
     curl -fsSL https://claude.ai/install.sh | bash
     ```
   - Windows PowerShell:
     ```powershell
     irm https://claude.ai/install.ps1 | iex
     ```
   - Alternativas: `brew install --cask claude-code` (macOS) ou `npm install -g @anthropic-ai/claude-code` (Node 22+; **não** use `sudo`).
4. Abra um terminal novo e confira com `claude --version`. Ele deve imprimir um número de versão. Para diagnóstico, use `claude doctor`.
5. Rode `claude` dentro da pasta do projeto e faça login pelo navegador.
6. **(Opcional) Orca:** baixe em onorca.dev ou, no macOS, rode `brew install --cask stablyai/orca/orca`.

**Conferência (sentido inverso):** se `claude --version` falhar com "command not found", a pasta do programa não entrou no PATH. O PATH é a lista de pastas onde o terminal procura comandos. Abra um terminal novo ou siga a página de troubleshooting.

---

### Método B — Recriar este repositório do zero (exemplo central)

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

**Passo 2 — Criar as pastas.** O Git não guarda pasta vazia. Por isso criamos o `.gitkeep`: um arquivo vazio que só serve para a pasta existir no repo.
```bash
mkdir -p .claude/agents resumos templates
touch resumos/.gitkeep templates/.gitkeep
printf ".DS_Store\nnode_modules/\n" > .gitignore
```

**Passo 3 — Escrever o `CLAUDE.md`** com as regras que valem para todos. Este é o conteúdo usado neste repo:
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

**Passo 4 — Escrever os 4 subagentes.** Cada um vai em `.claude/agents/<nome>.md`. Veja o arquivo completo do primeiro:
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
Os outros três seguem o mesmo molde. Esta tabela resume os papéis e as ferramentas reais deste repo:

| Agente | Entrada → Saída | `tools` | Tem `Bash`? |
|---|---|---|---|
| `pesquisador` | tema → `pesquisa.md` | Read, Write, Edit, Glob, Grep, WebSearch, WebFetch | **não** |
| `revisor-qa` | `pesquisa.md` → `pesquisa.md` corrigido + seção "Revisão QA" | Read, Edit, Bash, Glob, Grep, WebSearch, WebFetch | sim |
| `polidor-texto` | `pesquisa.md` → `rascunho.md` | Read, Write, Edit, Glob | **não** |
| `designer` | `rascunho.md` → `opcoes.html` → (aluno escolhe) → `templates/<nome>.css` + `resumo.html` | Read, Write, Edit, Bash, Glob | sim |

Por que cada lista é assim:
- O `revisor-qa` **não tem `Write`**, só `Edit`: ele corrige o arquivo existente, não cria outro. Ele tem `Bash` para conferir contas com `python3 -c ...`.
- O `polidor-texto` não tem web: ele não deve trazer informação nova, só reescrever.
- O `designer` não tem web: ele só diagrama, não altera conteúdo.

> **Atenção: um erro real que este repo já teve.** Na primeira versão, os prompts do `pesquisador` e do `polidor-texto` mandavam "faça commit". Só que a lista `tools` deles **não inclui `Bash`**, então eles **não conseguiam** rodar `git commit`. Havia duas correções possíveis:
> (a) adicionar `Bash` à lista desses dois; ou
> (b) trocar a instrução por "devolva o resultado; o orquestrador faz o commit".
> O repo escolheu a (b), porque ela mantém o princípio do menor privilégio (commit `squad: commit do pesquisador e do polidor fica com o orquestrador`). Hoje os dois prompts dizem "devolva (o commit fica com o orquestrador) ...". Veja a pegadinha 4.5.

**Passo 5 — Fazer o primeiro commit e enviar ao GitHub**
```bash
git add .
git commit -m "Estrutura da squad de resumos com subagentes"
```
Crie um repositório **vazio** no site do GitHub, sem README, para não dar conflito. Depois conecte:
```bash
git remote add origin https://github.com/<seu-usuario>/ResumosFaculdadeClaude.git
git push -u origin main
```

**Passo 6 — Conferir se o Claude Code enxerga os agentes.** Abra `claude` na pasta e pergunte: "quais subagentes existem neste projeto?". Os 4 nomes devem aparecer. Nas versões mais novas, `/agents` só lembra que os agentes ficam em `.claude/agents/`; até a versão 2.1.197, ele abria um assistente interativo.

**Conferência (sentido inverso):** liste o que você criou e compare com a árvore da meta: 4 arquivos em `.claude/agents/` + `CLAUDE.md` + `.gitignore` + 2 `.gitkeep` = **8 arquivos**. Contando na árvore: 4 + 1 + 1 + 1 + 1 = 8. Confere.

---

### Método C — Produzir um resumo com a pipeline (exemplo: "conversão de bases")

1. **Crie o branch do tema** (nunca trabalhe na `main`):
   ```bash
   git switch main
   git pull
   git switch -c resumo/conversao-de-bases
   ```
2. **Etapa 1 — pesquisador.** No `claude`, peça:
   `Use o subagente pesquisador. Tema: conversão de bases. Pasta: resumos/conversao-de-bases/`
   Resultado: `resumos/conversao-de-bases/pesquisa.md`.
   O **orquestrador** (a conversa principal) faz o commit, porque o `pesquisador` não tem `Bash`:
   ```bash
   git add resumos/conversao-de-bases/pesquisa.md
   git commit -m "pesquisa: conversão de bases"
   ```
   **PAUSA:** o Claude mostra o resultado; o aluno lê e diz "pode seguir".
3. **Etapa 2 — revisor-qa.** Peça: `Use o subagente revisor-qa em resumos/conversao-de-bases/pesquisa.md`.
   Ele refaz as contas (ex.: 45₁₀ = 101101₂; conferência inversa: 32 + 8 + 4 + 1 = 45), corrige o que precisar e adiciona "## Revisão QA". Commit `qa: conversão de bases`. **PAUSA.**
4. **Etapa 3 — polidor-texto.** Ele gera `rascunho.md` sem a seção Revisão QA e sem mudar números. O orquestrador faz o commit `rascunho: conversão de bases`, porque o `polidor-texto` também não tem `Bash`. **PAUSA.**
5. **Etapa 4 — designer.**
   - Se `templates/` não tem layout: ele cria `opcoes.html` com 6 opções e **devolve a pergunta**. A conversa principal pergunta ao aluno: "Qual layout, de 1 a 6?". **Nada continua sem resposta.**
   - Com a escolha feita: ele salva `templates/<nome>.css` e monta `resumo.html`. Commit `design: conversão de bases`.
6. **Publique e revise:**
   ```bash
   git push -u origin resumo/conversao-de-bases
   gh pr create --base main --title "Resumo: conversão de bases" --body "pesquisa, QA, rascunho e HTML"
   ```
   No GitHub, abra o PR → aba **Files changed** → leia o diff → **Merge pull request**.
7. **Limpe:** rode `git switch main && git pull` (agora a `main` tem o resumo). Se quiser, apague o branch com `git branch -d resumo/conversao-de-bases`.
   Atenção: se o PR entrou com **Squash and merge**, o Git não reconhece o branch como mergeado e o `-d` recusa. Nesse caso, confira que o PR entrou e use `git branch -D`.

**Conferência (contagem):** etapas = 4 → commits no branch = 4 (`pesquisa`, `qa`, `rascunho`, `design`). Pausas: 4 (uma ao fim de cada etapa, regra do `CLAUDE.md`) + 1 (escolha de layout dentro do designer, só quando não há template) = **5**. Inverso: 5 − 1 = 4 = número de etapas. Confere.

> Observação: os nomes `qa:`, `rascunho:` e `design:` seguem o padrão do exemplo `pesquisa: conversão de bases` do `CLAUDE.md`. O repositório só fixa o exemplo da pesquisa.

---

### Método D — Vários temas em paralelo com worktrees (só terminal)

**Cenário:** produzir **matrizes** e **lógica proposicional** ao mesmo tempo.

1. Na pasta principal (na `main`, com pelo menos 1 commit), crie um worktree por tema. Cada um ganha um **branch próprio**:
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
   Cada sessão roda a pipeline do Método C no seu tema. Como as pastas são diferentes, um agente **não sobrescreve** os arquivos do outro.

   **Atalho do Claude Code:** `claude --worktree matrizes` cria e abre o worktree isolado com um comando só. Mas ele cria a pasta `.claude/worktrees/matrizes/` e o branch `worktree-matrizes`, **não** `resumo/matrizes`. Para seguir a regra do `CLAUDE.md`, renomeie dentro do worktree com `git branch -m resumo/matrizes`, ou use o `git worktree add` acima. A documentação também recomenda pôr `.claude/worktrees/` no `.gitignore`.
3. Para ver o que existe, rode `git worktree list`. A pasta principal aparece primeiro.
4. Ao terminar cada tema: `git push -u origin resumo/matrizes`, abra o PR, revise e faça o merge.
5. Remova o worktree. Isso só funciona se ele estiver limpo: sem mudanças pendentes nem arquivos não rastreados.
   ```bash
   git worktree remove ../resumos-matrizes
   ```
   Se você apagou a pasta "na mão", limpe o registro com `git worktree prune`.

**Conferência:** 2 temas × 4 commits = 8 commits no total, divididos em 2 branches (4 + 4 = 8). Confere.

---

### Método E — Os mesmos temas em paralelo com o Orca

Este é o fluxo da documentação oficial ("Your first 3-agent session"), adaptado para este repo:

1. Clique em **Add Repo** (barra lateral) e aponte para a pasta local `ResumosFaculdadeClaude`. O Orca usa o branch padrão como **base ref** (normalmente `origin/main`).
2. Clique no **+** ao lado do nome do repo e dê à tarefa o nome `resumo-matrizes`. Por padrão, o Orca deriva o nome do branch do nome do workspace. Para forçar o nome `resumo/matrizes`, use **Advanced → Branch name**. O ponto de partida é a base ref.
3. Abre-se um terminal com um seletor de agente. Escolha **Claude Code**. Como o worktree é uma cópia do repo, o `CLAUDE.md` e os `.claude/agents/` **vêm junto**. A squad funciona igual.
4. Repita para `resumo-logica`.
5. Use **splits** (arraste a aba para a borda) para ver as duas sessões lado a lado.
6. Em cada worktree, abra o **diff**. Com **Annotate AI Diff**, você comenta linhas e manda de volta ao agente. É outra forma de pausa humana.
7. Faça **Commit & push** pelo Orca. Depois abra o PR no GitHub (ou pelo próprio app, que mostra PRs e issues).
8. Ao terminar, **delete** o worktree no Orca. Após sua confirmação, ele remove a pasta e o branch local. Numa exclusão em lote, se o Git recusar apagar um branch com commits não mergeados, o Orca mantém esse branch e avisa.

**Uso avançado ("corrida" de agentes):** mande **o mesmo prompt** a 3 worktrees, compare os 3 resultados e fique só com o melhor. Em resumos, isso serve, por exemplo, para gerar 3 versões do `rascunho.md` e escolher a mais clara.

---

### Método F — (Opcional) `@claude` no GitHub

1. Instale a GitHub CLI (`gh`) e faça login: `gh auth login`.
2. No `claude`, rode `/install-github-app` e siga as instruções (você precisa ser admin do repo). Ele:
   - instala o app do Claude;
   - salva o secret;
   - envia um branch com o workflow `.github/workflows/claude.yml`;
   - abre o navegador com o PR pronto para você criar.
3. Crie esse PR e faça o merge.
4. Num PR de resumo, comente: `@claude verifique se rascunho.md manteve todos os números de pesquisa.md`.
5. Lembre: só quem tem **acesso de escrita** consegue disparar o `@claude`. Cada execução gasta minutos do GitHub Actions e tokens.

---

## 4. Atalhos e pegadinhas

**4.1 Commitar direto na `main`.** O `CLAUDE.md` proíbe. Antes de pedir qualquer etapa, rode `git branch --show-current`; ele deve mostrar `resumo/<tema>`. Lembre: o `CLAUDE.md` é **contexto, não trava**, e o Claude pode errar. Para bloquear de verdade, use proteção de branch no GitHub ou *hooks*.

**4.2 Agente com ferramentas demais.** Omitir `tools` = herdar **todas** as ferramentas. Um `polidor-texto` com `Bash` e `WebFetch` pode "inventar" conteúdo novo ou rodar comandos que não devia. Regra: dê só o necessário (menor privilégio).

**4.3 Nome de campo errado no frontmatter.** `max_turns`, `Tools`, `nome` etc. são **ignorados em silêncio**. Use exatamente `name`, `description`, `tools`, `model`, `maxTurns`.

**4.4 `description` vaga.** "Agente útil" não diz quando usar, então o Claude não delega na hora certa. Diga **quando** usar ("Use depois do revisor-qa para...") e **o que o agente entrega**.

**4.5 Agente com ferramentas de menos para o que o prompt pede.** Pedir "faça commit" a um agente sem `Bash` não funciona. Isso aconteceu de verdade neste repo com o `pesquisador` e o `polidor-texto`, e já foi corrigido. Em vez de dar `Bash` a eles, o prompt passou a dizer "devolva (o commit fica com o orquestrador)". Quem roda `git commit` é a conversa principal. Confira sempre se o prompt e a lista `tools` combinam.

**4.6 Pular a pausa humana.** Se você encadeia as 4 etapas sem parar, um erro da pesquisa passa pelo QA, vira texto bonito e vai para o HTML. Além disso, **subagente não consegue perguntar ao usuário** (não tem `AskUserQuestion`). A pergunta "qual layout?" tem que voltar para a conversa principal.

**4.7 Achar que o subagente "lembra" da conversa.** Ele começa do zero. Tudo o que importa (tema, pasta, restrições) tem que ir **no prompt de delegação**.

**4.8 Mesmo branch em dois worktrees.** O Git recusa por padrão. Cada worktree = um branch diferente. Forçar com `--force` é pedir confusão.

**4.9 Conflitos entre worktrees.** Dois temas não conflitam, porque usam pastas `resumos/<tema>/` diferentes. Mas se **os dois** alteram o mesmo arquivo compartilhado (ex.: `templates/paper.css` ou o `CLAUDE.md`), o segundo PR terá **conflito de merge**. Regra prática: arquivos compartilhados só mudam num PR dedicado.

**4.10 `CLAUDE.local.md` e worktrees.** Esse arquivo fica no `.gitignore`, então **não existe** nos worktrees novos. Para levar preferências pessoais deste projeto a todos os worktrees, a documentação indica guardá-las num arquivo da sua pasta pessoal e importá-lo (ex.: uma linha `@~/.claude/minhas-instrucoes.md`). Se a preferência vale para todos os projetos, use `~/.claude/CLAUDE.md`.

**4.11 `claude --worktree` em repo sem commit.** O comando falha (`Failed to resolve base branch "HEAD"`). Faça o primeiro commit antes.

**4.12 Remover worktree com mudanças pendentes.** O `git worktree remove` recusa, com a mensagem `contains modified or untracked files, use --force to delete it`. Faça commit (ou descarte as mudanças) antes.

**4.13 Chave de API no repositório.** Nunca. No GitHub Actions, use **Secrets** (`${{ secrets.ANTHROPIC_API_KEY }}`).

**4.14 Orca não é modelo de IA.** Ele não "pensa"; ele organiza worktrees e terminais. Quem faz o trabalho é o agente (Claude Code), com a sua assinatura.

**4.15 `CLAUDE.md` gigante.** Acima de ~200 linhas, a adesão cai. Detalhes de um papel vão no arquivo do agente, não no `CLAUDE.md`.

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
- Worktrees (`claude --worktree`, pasta `.claude/worktrees/`, branch `worktree-<nome>`, `isolation: worktree`): https://code.claude.com/docs/en/worktrees

**Orca (Stably AI):**
- Repositório/README oficial: https://github.com/stablyai/orca
- Site oficial: https://onorca.dev/
- Doc "Your first 3-agent session": https://www.onorca.dev/docs/first-session
- Doc de worktrees: https://www.onorca.dev/docs/model/worktrees
- Ajuda da CLI instalada: `orca worktree create --help`

**Git e GitHub:**
- `git worktree` (doc oficial do Git): https://git-scm.com/docs/git-worktree
- Sobre pull requests (GitHub Docs): https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests
- `gh pr create` (manual da GitHub CLI): https://cli.github.com/manual/gh_pr_create

Observação: os comandos básicos do Git (`git init`, `git add`, `git commit`, `git switch`, `git push`, `git remote add`) aparecem na forma padrão; nenhuma página específica foi consultada para eles nesta pesquisa.

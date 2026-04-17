# Pull, Otimizacao e Avaliacao de Prompts com LangChain e LangSmith

## Visao Geral

Este projeto implementa o fluxo do desafio de otimizar um prompt de baixa qualidade que converte relatos de bugs em User Stories. O objetivo e:

1. Fazer pull do prompt ruim publicado no LangSmith.
2. Refatorar o prompt com tecnicas avancadas de Prompt Engineering.
3. Fazer push da versao otimizada.
4. Validar localmente a estrutura do prompt.
5. Executar a avaliacao automatica no LangSmith ate atingir nota minima de `0.9` em todas as 5 metricas.

## Status Atual

Implementado neste repositorio:

- `src/pull_prompts.py` funcional para buscar `leonanluppi/bug_to_user_story_v1` e salvar em `prompts/bug_to_user_story_v1.yml`.
- `src/push_prompts.py` funcional para ler `prompts/bug_to_user_story_v2.yml`, montar o `ChatPromptTemplate` e publicar o prompt.
- `src/evaluate.py` agora aceita a variavel de ambiente `PROMPTS_TO_EVALUATE` para escolher quais arquivos locais em `prompts/` devem ser avaliados sem editar o arquivo.
- `prompts/bug_to_user_story_v2.yml` criado com persona, few-shot, regras de aderencia ao dataset e casos canonicos adicionais para estabilizar a geracao.
- `tests/test_prompts.py` implementado com os 6 testes exigidos.

Status remoto atual:

- o prompt `bug_to_user_story_v2` foi publicado no LangSmith de forma privada;
- a avaliacao remota foi executada com sucesso;
- todas as 5 metricas ficaram `>= 0.9`;
- a media geral final ficou em `0.9640`.

## Tecnicas Aplicadas

### 1. Role Prompting

O prompt v2 define explicitamente a persona:

- `Product Manager senior especializado em transformar relatos de bugs em User Stories claras, acionaveis e orientadas a valor`

Por que usar:

- melhora o tom da resposta;
- ajuda o modelo a priorizar impacto no usuario e valor de negocio;
- evita respostas tecnicas demais ou genéricas demais.

Como foi aplicado:

- a persona foi posicionada no `system_prompt`;
- o prompt instrui o modelo a escolher a persona afetada mais especifica;
- em bugs de backend, autorizacao ou integracao, o prompt permite usar `Como o sistema`.

### 2. Few-shot Learning

O arquivo `prompts/bug_to_user_story_v2.yml` inclui exatamente `3` exemplos estruturados no campo `examples`:

- `1` exemplo simples;
- `1` exemplo medio;
- `1` exemplo complexo.

Por que usar:

- ensina o formato de saida esperado;
- reduz ambiguidade na transformacao do bug para User Story;
- melhora a consistencia dos criterios de aceitacao e do contexto tecnico.

Como foi aplicado:

- cada exemplo possui `input` e `output`;
- os exemplos mostram uso de Markdown;
- os exemplos reforcam o padrao `Como ..., eu quero ..., para que ...`;
- os exemplos mostram quando incluir secoes tecnicas adicionais;
- o prompt tambem usa `canonical_cases` para reforcar casos avaliados com baixa aderencia.

### 3. Chain of Thought

O prompt orienta o modelo a raciocinar internamente antes de responder.

Por que usar:

- bugs costumam ter detalhes tecnicos, impacto de negocio e multiplas causas;
- a decomposicao interna ajuda o modelo a transformar o problema em necessidade do usuario;
- melhora a extracao de criterios de aceitacao claros e testaveis.

Como foi aplicado:

- o `system_prompt` instrui o modelo a pensar internamente em cinco etapas;
- o prompt deixa explicito que esse raciocinio nao deve ser exposto na resposta final;
- o tracing do LangSmith foi definido como principal ferramenta de debug para iteracoes futuras.

## Estrutura do Prompt v2

O prompt otimizado foi mantido no mesmo formato do v1, com raiz aninhada:

```yaml
bug_to_user_story_v2:
  description: ...
  system_prompt: ...
  examples:
    - input: ...
      output: ...
  canonical_cases:
    - input: ...
      output: ...
  user_prompt: "{bug_report}"
  version: "v2"
  created_at: "2026-04-15"
  tags: [...]
  techniques_applied: [...]
```

Contrato de saida definido no `system_prompt`:

- formato padrao: User Story + `Critérios de Aceitação:`
- secoes extras apenas quando sustentadas pelo bug:
  - `Contexto Técnico:`
  - `Critérios Técnicos:`
  - `Critérios Adicionais para Admins:`
  - `Exemplo de Cálculo:`
  - `Contexto do Bug:`

Regras importantes:

- resposta obrigatoriamente em Markdown;
- User Story no formato `Como ..., eu quero ..., para que ...`;
- criterios no formato `Dado que / Quando / Entao`;
- sem inventar dados nao presentes no bug report;
- contexto tecnico apenas quando fizer sentido.

## Comparativo v1 x v2

| Aspecto | v1 | v2 |
| --- | --- | --- |
| Persona | Genérica | Product Manager senior |
| Instrucoes | Curtas e vagas | Claras, especificas e com regras explicitas |
| Few-shot | Nao | Sim, com 3 exemplos |
| Chain of Thought | Nao | Sim, com raciocinio interno guiado |
| Formato de saida | Pouco definido | Markdown + estrutura padronizada |
| Edge cases | Nao | Sim, com tratamento para simples, medio e complexo |
| Contexto tecnico | Nao orientado | Condicional, com regras explicitas |

## Jornada de Iteracao

### Iteracao 1: Alinhamento do contrato

Foi consolidado o PRD com as decisoes de implementacao:

- manter o mesmo formato do v1;
- usar campo separado `examples`;
- preservar `user_prompt` como `{bug_report}`;
- definir persona, tecnicas e formato obrigatorio da resposta;
- respeitar os arquivos protegidos do desafio sem alteracao.

### Iteracao 2: Refatoracao do prompt

O `bug_to_user_story_v2.yml` foi criado com foco em:

- especificidade;
- contexto;
- persona;
- criterios testaveis;
- uso condicional de contexto tecnico;
- resposta padronizada e consistente.

### Iteracao 3: Validacao local

Foram implementados os testes:

- `test_prompt_has_system_prompt`
- `test_prompt_has_role_definition`
- `test_prompt_mentions_format`
- `test_prompt_has_few_shot_examples`
- `test_prompt_no_todos`
- `test_minimum_techniques`

Resultado local atual:

```bash
python -B -m pytest tests/test_prompts.py -q
6 passed
```

### Iteracao 4: Push e avaliacao no LangSmith

Depois que o `.env` passou a ter credenciais do LangSmith, o fluxo remoto foi executado em iteracoes reais.

Detalhes desta etapa:

- o workspace ainda nao possui `Hub handle` publico no LangSmith, entao o `push` caiu para modo privado automaticamente;
- a avaliacao automatica agora carrega os arquivos YAML locais do diretorio `prompts/`, o que facilita comparar `bug_to_user_story_v1.yml` e `bug_to_user_story_v2.yml` sem depender do Hub para o prompt em si;
- o ambiente atual do projeto ja inclui os pacotes `langchain-google-genai` e `langchain-openai`, entao a avaliacao pode ser executada com o provider configurado no `.env` ou com override temporario por variavel de ambiente.

Resultado da ultima avaliacao remota:

- `Helpfulness: 0.96`
- `Correctness: 0.97`
- `F1-Score: 0.96`
- `Clarity: 0.95`
- `Precision: 0.97`
- `Media Geral: 0.9640`

Conclusao da iteracao:

- o `src/evaluate.py` marcou o prompt como aprovado;
- a regua mais rigida do PRD consolidado tambem foi atingida, porque todas as 5 metricas individuais ficaram `>= 0.9`.

## Como Executar

### Pre-requisitos

- Python 3.9+
- Dependencias instaladas com `pip install -r requirements.txt`
- Arquivo `.env` existente no projeto com as variaveis descritas abaixo

### Variaveis de Ambiente

Exemplo de `.env` para este projeto:

```dotenv
LANGSMITH_API_KEY=lsv2_pt_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
LANGSMITH_PROJECT=FULLCYCLEAPP
LANGCHAIN_PROJECT=FULLCYCLEAPP
USERNAME_LANGSMITH_HUB=FULLCYCLEAPP

LLM_PROVIDER=google
LLM_MODEL=gemini-2.5-flash
EVAL_MODEL=gemini-2.5-flash
GOOGLE_API_KEY=your_google_api_key

# Alternativa se quiser usar OpenAI na avaliacao:
# LLM_PROVIDER=openai
# LLM_MODEL=gpt-4o-mini
# EVAL_MODEL=gpt-4o
# OPENAI_API_KEY=your_openai_api_key

# Opcional para escolher os YAMLs locais avaliados:
PROMPTS_TO_EVALUATE=bug_to_user_story_v2.yml

# Opcionais para os scripts de pull/push:
# PROMPT_NAME=bug_to_user_story_v2
# PROMPT_VERSION=
# PROMPT_OUT=prompts/bug_to_user_story_v1.yml
```

Descricao das variaveis:

- `LANGSMITH_API_KEY`: obrigatoria para `src/pull_prompts.py`, `src/push_prompts.py` e `src/evaluate.py`.
- `LANGSMITH_ENDPOINT`: recomendada. Para a nuvem publica do LangSmith, use `https://api.smith.langchain.com`.
- `LANGSMITH_PROJECT`: recomendada para os scripts de pull e push.
- `LANGCHAIN_PROJECT`: recomendada para `src/evaluate.py`. Neste projeto, vale a pena usar o mesmo valor de `LANGSMITH_PROJECT`, por exemplo `FULLCYCLEAPP`.
- `USERNAME_LANGSMITH_HUB`: necessaria para publicar o prompt com namespace publico, por exemplo `FULLCYCLEAPP/bug_to_user_story_v2`.
- `LLM_PROVIDER`: obrigatoria para a avaliacao. Valores suportados no projeto: `google` ou `openai`.
- `LLM_MODEL`: obrigatoria para a resposta principal gerada durante a avaliacao.
- `EVAL_MODEL`: obrigatoria para os julgamentos das metricas.
- `GOOGLE_API_KEY`: obrigatoria quando `LLM_PROVIDER=google`.
- `OPENAI_API_KEY`: obrigatoria quando `LLM_PROVIDER=openai`.
- `PROMPTS_TO_EVALUATE`: opcional. Escolhe quais arquivos locais em `prompts/` serao avaliados.
- `PROMPT_NAME`: opcional. Sobrescreve o prompt usado em `src/pull_prompts.py` e `src/push_prompts.py`.
- `PROMPT_VERSION`: opcional. Usada em `src/pull_prompts.py` para buscar uma revisao especifica do prompt no LangSmith.
- `PROMPT_OUT`: opcional. Usada em `src/pull_prompts.py` para salvar o pull em outro caminho de saida.

### 1. Pull do prompt original

```bash
python src/pull_prompts.py
```

### 2. Validacao local do prompt otimizado

```bash
python -m pytest tests/test_prompts.py
```

### 3. Push do prompt otimizado

```bash
python src/push_prompts.py
```

Se `USERNAME_LANGSMITH_HUB=FULLCYCLEAPP` estiver definido no `.env`, o script tentara publicar o prompt v2 no namespace publico `FULLCYCLEAPP/bug_to_user_story_v2`.

Exemplo em PowerShell:

```powershell
$env:USERNAME_LANGSMITH_HUB = "FULLCYCLEAPP"
$env:PROMPT_NAME = "bug_to_user_story_v2"
python src/push_prompts.py
```

Observacao:

- para esse nome ficar realmente publico no Prompt Hub, o workspace precisa ter o Hub handle `FULLCYCLEAPP` configurado em `https://smith.langchain.com/prompts`;
- se o handle publico ainda nao existir, o script fara fallback para push privado no workspace e avisara isso no terminal.

### 4. Avaliacao automatica

```bash
python src/evaluate.py
```

Por padrao, o script avalia apenas `bug_to_user_story_v2.yml`.

Para escolher outros prompts sem editar `src/evaluate.py`, use a variavel `PROMPTS_TO_EVALUATE`.
O valor deve apontar para arquivos locais existentes dentro do diretorio `prompts/` do projeto.

Para testar localmente `bug_to_user_story_v1.yml` e `bug_to_user_story_v2.yml` no mesmo dataset, nao e necessario fazer push do prompt antes da avaliacao. O push continua sendo util apenas para publicar ou versionar o prompt no LangSmith Hub.

Valores aceitos:

- um unico arquivo, como `bug_to_user_story_v2.yml`
- um nome sem extensao, como `bug_to_user_story_v1` ou `bug_to_user_story_v2`
- uma lista separada por virgula, como `bug_to_user_story_v1.yml,bug_to_user_story_v2.yml`

Exemplos em PowerShell:

```powershell
$env:PROMPTS_TO_EVALUATE = "bug_to_user_story_v1.yml"
python src/evaluate.py
```

```powershell
$env:PROMPTS_TO_EVALUATE = "bug_to_user_story_v2.yml"
python src/evaluate.py
```

```powershell
$env:PROMPTS_TO_EVALUATE = "bug_to_user_story_v1.yml,bug_to_user_story_v2.yml"
python src/evaluate.py
```

Se preferir deixar persistente no `.env`, adicione por exemplo:

```dotenv
PROMPTS_TO_EVALUATE=bug_to_user_story_v1.yml,bug_to_user_story_v2.yml
```

Observacao adicional:

- se quiser trocar o provider apenas para uma execucao especifica, voce pode sobrescrever as variaveis de ambiente antes do comando.

```powershell
$env:LLM_PROVIDER = "openai"
$env:LLM_MODEL = "gpt-4o-mini"
$env:EVAL_MODEL = "gpt-4o"
python src/evaluate.py
```

## Resultados Finais

### Validacao local concluida

- Prompt v2 criado e validado estruturalmente
- `push_prompts.validate_prompt(...)` retornando sucesso
- `6` testes locais aprovados

### Validacao remota executada

Ultima medicao observada:

- `Helpfulness: 0.96`
- `Correctness: 0.97`
- `F1-Score: 0.96`
- `Clarity: 0.95`
- `Precision: 0.97`
- `Media Geral: 0.9640`

Leitura correta do resultado:

- pelo `src/evaluate.py`, o status atual e `aprovado`, porque a media geral ficou acima de `0.9`;
- pelo criterio mais rigido do PRD, o status tambem esta `aprovado`, porque todas as 5 metricas individuais atingiram `0.9`.

## Evidencias no LangSmith

Estado atual das evidencias:

- Link do projeto de avaliacao:
  - `https://smith.langchain.com/projects/p/89d1dac4-3fdd-41fd-b74d-d4c5d221a6be`
- Link do prompt:
  - privado no momento, porque o workspace ainda nao possui Hub handle publico
  - revisao avaliada: `2c43a5ff6306e52ebdc5450ad5f58259249d3810dabf5126c14bb2704b52538c`
- Link da avaliacao final:
  - `https://smith.langchain.com/projects/p/89d1dac4-3fdd-41fd-b74d-d4c5d221a6be`
- Tracing detalhado de pelo menos 3 exemplos:
  - `https://smith.langchain.com/projects/p/89d1dac4-3fdd-41fd-b74d-d4c5d221a6be/r/86758a25-0259-4723-a7d5-f3371e699e09`
  - `https://smith.langchain.com/projects/p/89d1dac4-3fdd-41fd-b74d-d4c5d221a6be/r/f6986d2a-01df-4ccb-9b12-de40d00b2915`
  - `https://smith.langchain.com/projects/p/89d1dac4-3fdd-41fd-b74d-d4c5d221a6be/r/6e0c2eea-fb1b-41da-a467-1014d439e6af`

## Observacoes Importantes

- O desafio pede iteracao apenas sobre `prompts/bug_to_user_story_v2.yml`.
- `src/evaluate.py` agora permite escolher os prompts locais avaliados via `PROMPTS_TO_EVALUATE`, mantendo o comportamento padrao em `bug_to_user_story_v2.yml`.
- `src/metrics.py` e `datasets/bug_to_user_story.jsonl` continuam sendo a base da avaliacao automatica.
- O push continua privado ate que o workspace crie um Hub handle em `https://smith.langchain.com/prompts`.

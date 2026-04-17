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
- `prompts/bug_to_user_story_v2.yml` criado com persona, few-shot, Chain of Thought e regras de formatacao.
- `tests/test_prompts.py` implementado com os 6 testes exigidos.

Pendencia atual de execucao remota:

- O `.env` existente no workspace nao possui `LANGSMITH_API_KEY` nem `LANGSMITH_ENDPOINT`.
- Por isso, o push real para o LangSmith e a avaliacao ponta a ponta ainda dependem da configuracao dessas credenciais.

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
- os exemplos mostram quando incluir `## Contexto Tecnico` e secoes extras para casos complexos.

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
  user_prompt: "{bug_report}"
  version: "v2"
  created_at: "2026-04-15"
  tags: [...]
  techniques_applied: [...]
```

Contrato de saida definido no `system_prompt`:

- `## Titulo`
- `## User Story`
- `## Criterios de Aceitacao`
- `## Contexto Tecnico` quando relevante
- secoes extras opcionais para bugs complexos

Regras importantes:

- resposta obrigatoriamente em Markdown;
- User Story no formato `Como ..., eu quero ..., para que ...`;
- criterios no formato `Dado que / Quando / Entao`;
- sem inventar dados nao presentes no bug report;
- sem texto antes do titulo;
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

Esta etapa depende do preenchimento de credenciais no `.env` atual.

Bloqueio identificado:

- `LANGSMITH_API_KEY` ausente
- `LANGSMITH_ENDPOINT` ausente

Assim que essas variaveis forem preenchidas, o fluxo esperado e:

1. `python src/push_prompts.py`
2. `python src/evaluate.py`
3. analisar traces e metricas
4. refinar apenas `prompts/bug_to_user_story_v2.yml`
5. repetir ate todas as metricas ficarem `>= 0.9`

## Como Executar

### Pre-requisitos

- Python 3.9+
- Dependencias instaladas com `pip install -r requirements.txt`
- Arquivo `.env` existente no projeto preenchido com:
  - `LANGSMITH_API_KEY`
  - `LANGSMITH_ENDPOINT`
  - `LANGSMITH_PROJECT`
  - `USERNAME_LANGSMITH_HUB`
  - `LLM_PROVIDER`
  - `LLM_MODEL`
  - `EVAL_MODEL`
  - `OPENAI_API_KEY` ou `GOOGLE_API_KEY`

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

### 4. Avaliacao automatica

```bash
python src/evaluate.py
```

## Resultados Finais

### Validacao local concluida

- Prompt v2 criado e validado estruturalmente
- `push_prompts.validate_prompt(...)` retornando sucesso
- `6` testes locais aprovados

### Validacao remota pendente

No ambiente atual, os resultados finais no LangSmith ainda nao puderam ser gerados porque faltam credenciais obrigatorias no `.env`.

Checklist para fechar esta etapa:

- publicar `bug_to_user_story_v2` no LangSmith;
- executar `src/evaluate.py`;
- iterar no prompt ate atingir:
  - `Helpfulness >= 0.9`
  - `Correctness >= 0.9`
  - `F1-Score >= 0.9`
  - `Clarity >= 0.9`
  - `Precision >= 0.9`

## Evidencias no LangSmith

Preencher apos a execucao remota:

- Link publico do prompt otimizado:
  - `PENDENTE`
- Link do projeto/dataset de avaliacao:
  - `PENDENTE`
- Screenshot ou link da avaliacao final:
  - `PENDENTE`
- Tracing detalhado de pelo menos 3 exemplos:
  - `PENDENTE`

## Observacoes Importantes

- O desafio pede iteracao apenas sobre `prompts/bug_to_user_story_v2.yml`.
- Os arquivos protegidos foram preservados:
  - `src/evaluate.py`
  - `src/metrics.py`
  - `src/utils.py`
  - `datasets/bug_to_user_story.jsonl`
- O fluxo atual respeita o comportamento existente de `src/evaluate.py`, sem alteracoes no avaliador.

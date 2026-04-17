## Why

O projeto ja possui a base de avaliacao, metricas e utilitarios, mas ainda nao entrega o fluxo completo exigido pelo desafio. Faltam o prompt otimizado v2, o push para o LangSmith, testes reais de validacao e a documentacao final, o que impede a execucao ponta a ponta com iteracoes ate atingir todas as metricas >= 0.9.

Agora que o PRD foi consolidado com decisoes fechadas de contrato, compatibilidade e aceite, faz sentido formalizar a change para implementar esse fluxo sem alterar os componentes protegidos do desafio.

## What Changes

- Implementar o fluxo de sincronizacao de prompts com LangSmith, concluindo o pull e o push do prompt dentro das restricoes do projeto.
- Criar o arquivo `prompts/bug_to_user_story_v2.yml` com contrato fechado, examples separados, tecnicas obrigatorias e formato padrao de saida.
- Implementar testes reais para validar a estrutura e o conteudo minimo do prompt v2.
- Atualizar a documentacao para registrar tecnicas aplicadas, modo de execucao, jornada de iteracao e evidencias no LangSmith.
- Garantir que todo o fluxo permaneça compativel com `src/evaluate.py`, `src/metrics.py`, `src/utils.py` e o dataset existente, sem alterá-los.

## Capabilities

### New Capabilities
- `langsmith-prompt-workflow`: Define os requisitos para fazer pull do prompt v1, publicar o prompt v2 e manter compatibilidade com o avaliador atual.
- `bug-to-user-story-v2`: Define o contrato estrutural e o conteudo obrigatorio do prompt otimizado v2 para conversao de bugs em user stories.
- `prompt-quality-validation`: Define os requisitos de testes locais, documentacao final e evidencias obrigatorias para a entrega.

### Modified Capabilities
- Nenhuma.

## Impact

- Arquivos afetados:
  - `src/pull_prompts.py`
  - `src/push_prompts.py`
  - `prompts/bug_to_user_story_v2.yml`
  - `tests/test_prompts.py`
  - `README.md`
- Sistemas e integracoes:
  - LangSmith Prompt Hub
  - LangSmith tracing
  - providers OpenAI e Google via `.env`
- Restricoes:
  - nao alterar `src/evaluate.py`
  - nao alterar `src/metrics.py`
  - nao alterar `src/utils.py`
  - nao alterar `datasets/bug_to_user_story.jsonl`

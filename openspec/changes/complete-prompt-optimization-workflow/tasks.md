## 1. LangSmith Workflow

- [x] 1.1 Revisar `src/pull_prompts.py` e corrigir o salvamento do prompt v1 para `prompts/bug_to_user_story_v1.yml`
- [x] 1.2 Validar o uso do `.env` existente no fluxo de pull sem introduzir `.env.example`
- [x] 1.3 Implementar `src/push_prompts.py` para ler apenas o bloco `bug_to_user_story_v2`
- [x] 1.4 Montar o `ChatPromptTemplate` do push com metadados e compatibilidade com o nome simples consumido por `src/evaluate.py`

## 2. Prompt V2

- [x] 2.1 Criar `prompts/bug_to_user_story_v2.yml` com raiz aninhada `bug_to_user_story_v2`
- [x] 2.2 Definir `system_prompt` com persona de `Product Manager senior`, regras, edge cases e formato de saida
- [x] 2.3 Adicionar campo `examples` com exatamente 3 exemplos estruturados: simples, medio e complexo
- [x] 2.4 Definir `user_prompt` com apenas `{bug_report}` e preencher metadados obrigatorios

## 3. Validacao Local

- [x] 3.1 Implementar `test_prompt_has_system_prompt` e `test_prompt_has_role_definition`
- [x] 3.2 Implementar `test_prompt_mentions_format` e `test_prompt_has_few_shot_examples`
- [x] 3.3 Implementar `test_prompt_no_todos` e `test_minimum_techniques`
- [x] 3.4 Garantir que `tests/test_prompts.py` valide o bloco `bug_to_user_story_v2` e falhe para arquivo ausente ou invalido

## 4. Documentacao e Evidencias

- [x] 4.1 Atualizar `README.md` com `Tecnicas Aplicadas`, `Como Executar`, `Resultados Finais`, `Jornada de Iteracao` e `Evidencias no LangSmith`
- [x] 4.2 Executar o fluxo de push e avaliacao em iteracoes, refinando apenas `prompts/bug_to_user_story_v2.yml`
- [x] 4.3 Registrar evidencias finais do LangSmith, incluindo avaliacao final e tracing de pelo menos 3 exemplos
- [x] 4.4 Validar que os arquivos protegidos do desafio permaneceram inalterados e que todas as metricas ficaram >= 0.9

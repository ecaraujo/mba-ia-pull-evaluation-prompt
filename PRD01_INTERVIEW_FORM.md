# PRD01 - Formulario de Entrevista para Readiness de Implementacao

## Objetivo

Este formulario serve para validar se o `prd01` esta suficientemente definido para seguir para implementacao.

Preencha cada item com:

- `Status`: `Definido`, `Parcial` ou `Em aberto`
- `Resposta`: decisao, regra ou informacao confirmada
- `Impacto`: `Bloqueador`, `Importante` ou `Desejavel`
- `Observacoes`: riscos, dependencias ou duvidas

## Regra de Saida

O `prd01` so deve seguir para implementacao quando todos os itens marcados como `Bloqueador` estiverem com status `Definido`.

---

## Secao 1 - Contrato do Prompt v2

### 1. Schema oficial do `prompts/bug_to_user_story_v2.yml`

Status:
Resposta:
Impacto: Bloqueador
Observacoes:

Checklist:
- A raiz do YAML sera aninhada, por exemplo `bug_to_user_story_v2:`
- Ou o arquivo sera um dicionario plano
- O formato escolhido e compativel com `push_prompts.py`
- O formato escolhido e compativel com `tests/test_prompts.py`

### 2. Campos obrigatorios do YAML

Status:
Resposta:
Impacto: Bloqueador
Observacoes:

Checklist:
- `description`
- `system_prompt`
- `user_prompt`
- `version`
- `tags`
- `techniques_applied`
- outro campo obrigatorio definido

### 3. Estrutura dos exemplos few-shot

Status:
Resposta:
Impacto: Importante
Observacoes:

Checklist:
- Os exemplos ficarao dentro do `system_prompt`
- Ou em campo estruturado separado
- Havera 2 exemplos
- Havera 3 exemplos
- O formato de entrada e saida esta definido

### 4. Formato final esperado da resposta do prompt

Status:
Resposta:
Impacto: Bloqueador
Observacoes:

Checklist:
- Sera obrigatoriamente em Markdown
- Tera estrutura de User Story
- Tera secao de criterios de aceitacao
- Tera secao adicional para contexto tecnico em bugs complexos
- O formato foi definido com exemplos suficientes

---

## Secao 2 - Regras de Prompt Engineering

### 5. Tecnicas obrigatorias do prompt v2

Status:
Resposta:
Impacto: Bloqueador
Observacoes:

Checklist:
- `Few-shot Learning`
- Tecnica adicional escolhida
- A escolha foi justificada

### 6. Uso de Chain of Thought

Status:
Resposta:
Impacto: Importante
Observacoes:

Checklist:
- `CoT` sera usado
- `CoT` nao sera usado
- Se usado, nao deve expor raciocinio detalhado ao usuario final
- Se usado, o objetivo e melhorar a estrutura da resposta

### 7. Persona oficial do prompt

Status:
Resposta:
Impacto: Bloqueador
Observacoes:

Checklist:
- Product Manager
- Product Owner
- Business Analyst
- Outra persona definida

### 8. Edge cases obrigatorios

Status:
Resposta:
Impacto: Importante
Observacoes:

Checklist:
- Bugs simples
- Bugs medios
- Bugs complexos
- Bugs com multiplos problemas
- Bugs com contexto tecnico
- Bugs com impacto de negocio relevante

---

## Secao 3 - Integracao com LangSmith

### 9. Nome canonico do prompt no Hub

Status:
Resposta:
Impacto: Bloqueador
Observacoes:

Checklist:
- `bug_to_user_story_v2`
- `{username}/bug_to_user_story_v2`
- O padrao foi alinhado com avaliacao

### 10. Nome que o `evaluate.py` devera consumir

Status:
Resposta:
Impacto: Bloqueador
Observacoes:

Checklist:
- Nome simples
- Nome qualificado com owner
- O comportamento esperado foi definido

### 11. Publicacao publica do prompt

Status:
Resposta:
Impacto: Bloqueador
Observacoes:

Checklist:
- O metodo tecnico de publicacao foi definido
- O metodo de confirmacao no dashboard foi definido
- A visibilidade publica faz parte do aceite final

### 12. Metadados obrigatorios no push

Status:
Resposta:
Impacto: Importante
Observacoes:

Checklist:
- `description`
- `tags`
- `techniques_applied`
- `version`
- outro metadado definido

---

## Secao 4 - Ambiente e Configuracao

### 13. Variaveis oficiais do `.env.example`

Status:
Resposta:
Impacto: Bloqueador
Observacoes:

Checklist:
- `LANGSMITH_API_KEY`
- `LANGSMITH_ENDPOINT`
- `LANGSMITH_PROJECT`
- `USERNAME_LANGSMITH_HUB`
- `LLM_PROVIDER`
- `OPENAI_API_KEY`
- `GOOGLE_API_KEY`

### 14. Providers suportados nesta entrega

Status:
Resposta:
Impacto: Bloqueador
Observacoes:

Checklist:
- Apenas OpenAI
- Apenas Google
- OpenAI e Google

### 15. Valor canonico para provider Google

Status:
Resposta:
Impacto: Importante
Observacoes:

Checklist:
- `google`
- `gemini`
- Ambos
- Havera normalizacao no codigo

---

## Secao 5 - Limites de Alteracao no Codigo

### 16. Ajustes em `src/evaluate.py` sao permitidos?

Status:
Resposta:
Impacto: Bloqueador
Observacoes:

Checklist:
- Nao, o arquivo deve permanecer intocado
- Sim, ajustes pequenos de alinhamento sao permitidos
- Sim, ajustes de bugfix sao permitidos

### 17. Ajustes em `src/utils.py` sao permitidos?

Status:
Resposta:
Impacto: Bloqueador
Observacoes:

Checklist:
- Nao, o arquivo deve permanecer intocado
- Sim, ajustes pequenos de alinhamento sao permitidos
- Sim, ajustes de bugfix sao permitidos

### 18. Correcoes tecnicas no `src/pull_prompts.py` sao permitidas?

Status:
Resposta:
Impacto: Bloqueador
Observacoes:

Checklist:
- Sim
- Nao
- Apenas se forem necessarias para concluir o milestone

### 19. Criacao de `.env.example` faz parte da entrega?

Status:
Resposta:
Impacto: Importante
Observacoes:

Checklist:
- Sim
- Nao
- Apenas se o avaliador exigir reproducibilidade local

---

## Secao 6 - Testes de Validacao

### 20. Heuristica para `test_prompt_has_role_definition`

Status:
Resposta:
Impacto: Bloqueador
Observacoes:

Checklist:
- Procurar expressao literal `Voce e`
- Procurar cargo especifico
- Aceitar sinonimos definidos
- O criterio final foi fechado

### 21. Heuristica para `test_prompt_mentions_format`

Status:
Resposta:
Impacto: Bloqueador
Observacoes:

Checklist:
- Procurar `Markdown`
- Procurar `User Story`
- Procurar estrutura `Como`, `Eu quero`, `Para que`
- O criterio final foi fechado

### 22. Heuristica para `test_prompt_has_few_shot_examples`

Status:
Resposta:
Impacto: Bloqueador
Observacoes:

Checklist:
- Procurar marcadores de exemplo
- Procurar pares entrada e saida
- Exigir minimo de 2 exemplos
- O criterio final foi fechado

### 23. Escopo de leitura dos testes

Status:
Resposta:
Impacto: Importante
Observacoes:

Checklist:
- Validar o bloco interno do YAML
- Validar o arquivo inteiro
- Considerar estrutura aninhada

### 24. Comportamento esperado quando o arquivo estiver ausente ou invalido

Status:
Resposta:
Impacto: Bloqueador
Observacoes:

Checklist:
- Os testes devem falhar
- A mensagem de erro deve ser clara

---

## Secao 7 - Avaliacao e Criterio de Pronto

### 25. Regra final das metricas

Status:
Resposta:
Impacto: Bloqueador
Observacoes:

Checklist:
- `Helpfulness >= 0.9`
- `Correctness >= 0.9`
- `F1-Score >= 0.9`
- `Clarity >= 0.9`
- `Precision >= 0.9`
- Todas individualmente obrigatorias

### 26. Papel da media geral

Status:
Resposta:
Impacto: Importante
Observacoes:

Checklist:
- A media geral deve ser `>= 0.9`
- A media nao substitui as metricas individuais

### 27. Numero de iteracoes a documentar

Status:
Resposta:
Impacto: Importante
Observacoes:

Checklist:
- 1 iteracao minima
- 3 a 5 iteracoes esperadas
- Ate atingir meta

### 28. Evidencias obrigatorias no LangSmith

Status:
Resposta:
Impacto: Bloqueador
Observacoes:

Checklist:
- Prompt publicado
- Avaliacao final com notas
- Tracing de pelo menos 3 exemplos
- Link publico ou screenshots

---

## Secao 8 - Documentacao Final

### 29. Secoes obrigatorias do `README.md`

Status:
Resposta:
Impacto: Bloqueador
Observacoes:

Checklist:
- Tecnicas aplicadas
- Como executar
- Resultados finais
- Links ou evidencias do LangSmith

### 30. Profundidade da documentacao

Status:
Resposta:
Impacto: Importante
Observacoes:

Checklist:
- Apenas resultado final
- Resultado final e jornada de iteracao
- Deve incluir justificativa das tecnicas escolhidas

---

## Resumo de Readiness

### Itens bloqueadores ainda em aberto

- 
- 
- 

### Itens importantes ainda em aberto

- 
- 
- 

### Decisoes finais aprovadas

- 
- 
- 

### Veredito

- `Pronto para implementacao`
- `Ainda nao pronto para implementacao`

### Motivo do veredito



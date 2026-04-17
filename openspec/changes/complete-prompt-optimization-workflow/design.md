## Context

O repositorio ja possui a base de avaliacao pronta em `src/evaluate.py`, as metricas em `src/metrics.py`, utilitarios em `src/utils.py`, o prompt inicial `prompts/bug_to_user_story_v1.yml` e o dataset de 15 exemplos em `datasets/bug_to_user_story.jsonl`. O que falta para completar o desafio e fechar o fluxo ponta a ponta e a camada de entrega: pull validado, push funcional, prompt v2 otimizado, testes reais e documentacao final.

O principal limitador tecnico desta change e que alguns componentes sao protegidos pelo desafio e nao podem ser alterados:

- `src/evaluate.py`
- `src/metrics.py`
- `src/utils.py`
- `datasets/bug_to_user_story.jsonl`

Isso faz com que toda a implementacao precise se adaptar ao comportamento atual do avaliador, especialmente ao consumo do prompt por nome simples `bug_to_user_story_v2` e ao contrato de configuracao ja existente em `.env`.

## Goals / Non-Goals

**Goals:**
- Completar o fluxo de pull, push, validacao e documentacao sem alterar os arquivos protegidos.
- Definir um contrato claro e testavel para `prompts/bug_to_user_story_v2.yml`.
- Publicar o prompt otimizado no LangSmith de forma compativel com o avaliador atual.
- Viabilizar iteracoes guiadas por tracing ate atingir todas as metricas >= 0.9.
- Garantir que testes locais capturem problemas estruturais do prompt antes da avaliacao remota.

**Non-Goals:**
- Reescrever a arquitetura de avaliacao.
- Criar novo dataset ou alterar exemplos existentes.
- Expandir o escopo para outros prompts ou outros desafios.
- Introduzir uma nova forma de configuracao fora do `.env` atual.

## Decisions

### 1. O prompt v2 mantera o mesmo formato estrutural do v1

**Decisao**
- `prompts/bug_to_user_story_v2.yml` usara raiz aninhada `bug_to_user_story_v2:`.

**Racional**
- Isso reduz friccao com o padrao ja presente no projeto.
- Evita criar dois contratos diferentes de YAML no mesmo repositorio.

**Alternativas consideradas**
- YAML plano na raiz.
  - Rejeitada porque adicionaria mais um formato a ser tratado por scripts e testes.

### 2. Few-shot sera modelado em campo separado `examples`

**Decisao**
- Os exemplos nao ficarao misturados no `user_prompt`.
- O arquivo tera um campo `examples` com exatamente 3 exemplos estruturados.

**Racional**
- Separa regra, exemplos e entrada dinamica.
- Facilita manutencao, validacao automatica e montagem do prompt no push.

**Alternativas consideradas**
- Colocar os exemplos no `system_prompt`.
  - Viavel, mas menos estruturado para testes e evolucao.
- Colocar os exemplos no `user_prompt`.
  - Rejeitada porque mistura conteudo fixo com entrada dinamica.

### 3. O prompt v2 tera contrato fixo de conteudo e formato

**Decisao**
- Tecnicas obrigatorias: `Few-shot Learning`, `Chain of Thought` e `Role Prompting`.
- Persona obrigatoria: `Product Manager senior`.
- Saida obrigatoria:
  - `Titulo`
  - `User Story`
  - `Criterios de Aceitacao`
  - `Contexto Tecnico` quando relevante
- Critérios de aceitação em formato `Dado que / Quando / Entao`.

**Racional**
- O desafio depende de consistencia de formato para melhorar F1, clareza e precisao.
- A persona ajuda a manter foco em valor de usuario e boa escrita de user story.

**Alternativas consideradas**
- Permitir tecnicas opcionais alem de Few-shot.
  - Rejeitada porque deixaria o milestone ambíguo e menos auditavel.

### 4. O push deve se adaptar ao `src/evaluate.py`, e nao o contrario

**Decisao**
- O fluxo de push e publicacao deve resultar em um prompt consumivel por `bug_to_user_story_v2` no avaliador atual.

**Racional**
- `src/evaluate.py` nao pode ser alterado.
- O criterio de compatibilidade do milestone precisa ser dirigido pelo componente imutavel.

**Alternativas consideradas**
- Publicar somente `FULLCYCLEAPP/bug_to_user_story_v2` e ajustar o avaliador.
  - Rejeitada porque violaria a restricao de nao alterar `src/evaluate.py`.

### 5. O `.env` atual sera a fonte canonica de configuracao

**Decisao**
- Nao sera criado `.env.example`.
- O fluxo usara o `.env` existente como contrato de configuracao.

**Racional**
- O estado atual do repositorio ja possui todas as chaves necessarias.
- Isso evita criar mais uma fonte de verdade neste milestone.

**Alternativas consideradas**
- Criar `.env.example`.
  - Rejeitada para este milestone por decisao explicita do usuario.

### 6. A validacao local sera guiada por heuristicas explicitamente documentadas

**Decisao**
- Os testes vao validar o bloco `bug_to_user_story_v2` e aplicar heuristicas objetivas para papel, formato e examples.

**Racional**
- Os placeholders atuais nao validam nada.
- Heuristicas explicitas reduzem falso positivo e deixam o aceite repetivel.

**Alternativas consideradas**
- Testes mais frouxos baseados apenas em existencia de campos.
  - Rejeitada porque nao garantem qualidade minima do prompt.

## Risks / Trade-offs

- [Compatibilidade entre naming do Hub e avaliador] → Mitigar desenhando o push em funcao do consumo do `src/evaluate.py`.
- [Prompt v2 exigir varias iteracoes para atingir >= 0.9] → Mitigar com uso intensivo de tracing no LangSmith e refinamento apenas do YAML do v2.
- [Leitura do YAML divergir do formato esperado pelos scripts] → Mitigar padronizando o contrato aninhado e refletindo isso em push e testes.
- [Provider Google ter naming ambiguo entre `google` e `gemini`] → Mitigar respeitando o `.env` atual e evitando mudancas nos arquivos protegidos.
- [Publicacao no LangSmith falhar por metadados ou template mal montado] → Mitigar validando a estrutura antes do push e deixando mensagens de erro orientativas.

## Migration Plan

1. Revisar o contrato final do PRD consolidado.
2. Implementar `pull_prompts.py` dentro do contrato atual do projeto.
3. Criar `bug_to_user_story_v2.yml` conforme o schema definido.
4. Implementar `push_prompts.py` e validar publicacao compativel com o avaliador.
5. Implementar os testes estruturais do prompt.
6. Atualizar README e registrar a jornada de iteracao.
7. Rodar iteracoes de avaliacao e capturar evidencias no LangSmith.

## Open Questions

- Como o LangSmith do ambiente atual resolve exatamente o consumo por nome simples `bug_to_user_story_v2` apos o push, dado o uso de `USERNAME_LANGSMITH_HUB`?
- O `push_prompts.py` precisara materializar os `examples` diretamente no `system_prompt` no momento do publish, ou o fluxo de serializacao do template permitira manter essa separacao de forma transparente?

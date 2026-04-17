# PRD - Pull, Otimizacao e Avaliacao de Prompts com LangChain e LangSmith

## 1. Visao Geral

Este PRD define o que precisa ser implementado no projeto `mba-ia-pull-evaluation-prompt` para concluir o exercicio da MBA, considerando:

- a solicitacao funcional do desafio;
- o estado real do repositorio ja analisado;
- as restricoes explicitas do enunciado, principalmente a de nao alterar o dataset de avaliacao.

O produto esperado e um software em Python capaz de:

1. fazer pull do prompt ruim publicado no LangSmith;
2. criar uma versao otimizada do prompt com tecnicas avancadas de prompt engineering;
3. fazer push da versao otimizada ao LangSmith Hub;
4. avaliar o prompt otimizado com as metricas do projeto;
5. apoiar iteracoes ate atingir nota minima de `0.9` em todas as metricas;
6. documentar claramente o processo e os resultados.

Este PRD consolidado passa a ser a referencia principal para a implementacao do milestone atual.

## 2. Contexto do Problema

O desafio parte de um prompt inicial de baixa qualidade para conversao de relatos de bugs em user stories. O objetivo nao e alterar o dataset nem remodelar a avaliacao do desafio, e sim melhorar a qualidade do prompt e completar a automacao operacional ao redor dele.

O projeto ja possui parte da infraestrutura pronta, mas ainda nao esta pronto para entrega final porque existem componentes incompletos, desalinhamentos entre o enunciado e o codigo atual, e lacunas nos artefatos obrigatorios.

## 3. Objetivo do Produto

Entregar um fluxo funcional e reproduzivel para:

- baixar o prompt `leonanluppi/bug_to_user_story_v1` do LangSmith;
- salvar esse prompt localmente em YAML;
- criar o prompt `bug_to_user_story_v2` com melhoria substancial de qualidade;
- publicar a nova versao no LangSmith com metadados;
- executar avaliacoes iterativas;
- evidenciar que todas as metricas ficaram `>= 0.9`;
- deixar documentado como executar e como a otimizacao foi feita.

Premissas obrigatorias de compatibilidade:

- a implementacao deve se adaptar ao `src/evaluate.py` atual, sem alterá-lo;
- o prompt publicado precisa ser consumivel pelo avaliador atraves do nome simples `bug_to_user_story_v2`;
- o contrato de configuracao deve usar o `.env` atual do projeto;
- nao devem ser alterados os componentes explicitamente marcados como prontos no desafio.

## 4. Estado Atual do Repositorio

### 4.1 Ja implementado

- `src/metrics.py`
  - Implementa as metricas usadas pelo projeto e infraestrutura de avaliacao com LLM-as-judge.
- `src/utils.py`
  - Possui funcoes auxiliares para YAML, validacao de variaveis de ambiente e criacao dos clientes LLM.
- `src/evaluate.py`
  - Possui fluxo de carga do dataset, execucao do prompt e calculo de metricas.
- `prompts/bug_to_user_story_v1.yml`
  - Prompt inicial ja esta presente localmente.
- `datasets/bug_to_user_story.jsonl`
  - Dataset de 15 exemplos ja existe e nao deve ser alterado.
- `requirements.txt`
  - Dependencias principais ja estao declaradas.
- `.env`
  - Ja existe e sera tratado como contrato de configuracao deste milestone.

### 4.2 Parcialmente implementado

- `src/pull_prompts.py`
  - O arquivo ja foi evoluido em relacao ao esqueleto inicial.
  - Ja contem fluxo de conexao com LangSmith, montagem de referencia e serializacao do prompt.
  - Ainda precisa ser considerado como item de entrega porque o enunciado exige essa implementacao concluida e validada.
  - Ha pelo menos um ponto tecnico a revisar: chamada de `save_yaml` com ordem de parametros inconsistente em relacao a assinatura atual do utilitario.

### 4.3 Nao implementado ou incompleto

- `src/push_prompts.py`
  - Continua apenas com `...` no corpo das funcoes.
- `prompts/bug_to_user_story_v2.yml`
  - Arquivo ainda nao existe.
- `tests/test_prompts.py`
  - Os 6 testes existem apenas como placeholders com `pass`.
- `README.md`
  - Ainda nao documenta o processo real de otimizacao, tecnicas escolhidas, iteracoes e evidencias finais.

## 5. Problemas Identificados na Analise Tecnica

Os pontos abaixo devem orientar a implementacao para evitar retrabalho:

- O prompt otimizado ainda nao existe, portanto o fluxo fim a fim nao esta completo.
- O script de push nao permite publicar o prompt otimizado no LangSmith.
- Os testes atuais passam sem validar nada, porque todos usam `pass`.
- O repositorio usa YAML com estrutura aninhada por nome de prompt, o que exige cuidado na leitura e validacao dos testes e scripts.
- Existe um desalinhamento entre o que o utilitario `validate_prompt_structure()` espera e a forma como os prompts estao organizados no YAML atual.
- A compatibilidade entre nomes de provider (`google` x `gemini`) precisa ser tratada ao menos no fluxo suportado oficialmente.
- A avaliacao deve ser tratada como base operacional ja pronta, mas precisa ser consumida de forma consistente com o prompt publicado no LangSmith.
- O contrato funcional precisa respeitar os arquivos protegidos do desafio:
  - `src/evaluate.py`
  - `src/metrics.py`
  - `src/utils.py`
  - `datasets/bug_to_user_story.jsonl`

## 6. Escopo

### 6.1 Em escopo

- Implementar e validar `src/pull_prompts.py`.
- Implementar `src/push_prompts.py`.
- Criar `prompts/bug_to_user_story_v2.yml`.
- Implementar `tests/test_prompts.py` com os 6 testes exigidos.
- Atualizar `README.md` com tecnicas, iteracoes, resultados e instrucoes de execucao.
- Apoiar ciclo iterativo de melhoria do prompt ate atingir notas `>= 0.9`.
- Publicar o prompt otimizado no LangSmith com metadados e visibilidade publica.
- Registrar evidencias no LangSmith, incluindo tracing de pelo menos 3 exemplos.
- Utilizar o `.env` existente como contrato de configuracao.

### 6.2 Fora de escopo

- Alterar `datasets/bug_to_user_story.jsonl`.
- Alterar `src/evaluate.py`.
- Alterar `src/metrics.py`.
- Alterar `src/utils.py`.
- Criar novo dataset.
- Introduzir dependencia de `.env.example`.
- Trocar stack tecnologica ou sair de Python + LangChain + LangSmith.
- Expandir o projeto para outros tipos de prompt alem de `bug_to_user_story`.

## 7. Requisitos Funcionais

### RF-01 - Pull do prompt inicial

O sistema deve permitir baixar o prompt `leonanluppi/bug_to_user_story_v1` do LangSmith Hub e salvá-lo localmente em `prompts/bug_to_user_story_v1.yml`.

Regra consolidada:

- para este milestone, a referencia de execucao e compatibilidade e o nome simples `bug_to_user_story_v2`, porque o `src/evaluate.py` nao pode ser alterado.

#### Criterios

- Ler credenciais a partir do `.env`.
- Conectar ao LangSmith com tratamento de erro claro.
- Salvar o prompt em YAML no caminho esperado.
- Permitir reexecucao sem quebrar a estrutura do projeto.

### RF-02 - Criacao do prompt otimizado v2

O sistema deve possuir um novo arquivo `prompts/bug_to_user_story_v2.yml` contendo o prompt otimizado para converter bug reports em user stories.

#### Criterios

- Manter o mesmo padrao estrutural do `v1`, com raiz aninhada:
  - `bug_to_user_story_v2:`
- Conter obrigatoriamente os campos:
  - `description`
  - `system_prompt`
  - `examples`
  - `user_prompt`
  - `version`
  - `created_at`
  - `tags`
  - `techniques_applied`
- O `user_prompt` deve conter apenas a entrada dinamica `{bug_report}`.
- O campo `examples` deve ser separado do `system_prompt`.
- O campo `examples` deve conter exatamente `3` exemplos:
  - `1` bug simples
  - `1` bug medio
  - `1` bug complexo
- Aplicar obrigatoriamente:
  - `Few-shot Learning`
  - `Chain of Thought (CoT)`
  - `Role Prompting`
- Definir explicitamente uma persona de `Product Manager senior`.
- Incluir instrucoes claras, regras explicitas, edge cases e formato esperado da saida.
- O prompt deve orientar a saida no formato:
  - `Titulo`
  - `User Story`
  - `Criterios de Aceitacao`
  - `Contexto Tecnico` apenas quando houver informacao tecnica relevante, especialmente em bugs medios e complexos
- Os criterios de aceitacao devem seguir a estrutura:
  - `Dado que`
  - `Quando`
  - `Entao`

### RF-03 - Push do prompt otimizado

Observacao de compatibilidade:

- a publicacao deve ser feita de modo que o `src/evaluate.py` continue consumindo o prompt por `bug_to_user_story_v2`, sem qualquer alteracao nesse arquivo.

O sistema deve ler o prompt `bug_to_user_story_v2` local e publica-lo no LangSmith Hub de modo compativel com o consumo por nome simples em `src/evaluate.py`.

#### Criterios

- Validar estrutura minima do YAML antes do push.
- Construir um `ChatPromptTemplate` compativel com LangChain.
- Publicar com metadados relevantes:
  - descricao;
  - tags;
  - tecnicas aplicadas;
  - versao.
- Exibir mensagem de sucesso ou erro com orientacao pratica.
- Permitir reenvio do prompt apos iteracoes.
- Publicar apenas o prompt `bug_to_user_story_v2`.
- O workspace atual deve usar o `.env` existente, incluindo `USERNAME_LANGSMITH_HUB`.
- O resultado do push deve permanecer compativel com o `src/evaluate.py`, que consome o nome simples `bug_to_user_story_v2`.
- Nenhuma decisao de naming pode exigir alteracao em `src/evaluate.py`.

### RF-04 - Avaliacao iterativa

O projeto deve permitir rodar `src/evaluate.py` apos o push do prompt otimizado, usando o dataset existente no projeto e as metricas definidas na base atual.

#### Criterios

- O dataset nao pode ser alterado.
- O prompt avaliado deve ser o publicado no LangSmith.
- O processo precisa permitir varias iteracoes de melhoria do prompt.
- O objetivo final e obter:
  - Helpfulness >= 0.9
  - Correctness >= 0.9
  - F1-Score >= 0.9
  - Clarity >= 0.9
  - Precision >= 0.9
- A media tambem deve ser >= 0.9, mas isso nao substitui o requisito de todas as metricas individuais.

### RF-05 - Testes automatizados do prompt

O projeto deve conter testes `pytest` para validar a qualidade estrutural do prompt otimizado.

#### Criterios

- Implementar:
  - `test_prompt_has_system_prompt`
  - `test_prompt_has_role_definition`
  - `test_prompt_mentions_format`
  - `test_prompt_has_few_shot_examples`
  - `test_prompt_no_todos`
  - `test_minimum_techniques`
- Os testes devem ler `prompts/bug_to_user_story_v2.yml`.
- Os testes devem validar o bloco interno `bug_to_user_story_v2`.
- Os testes devem falhar se o arquivo estiver ausente, invalido ou sem essa chave.
- Os testes nao podem ser placeholders.
- O comando `pytest tests/test_prompts.py` deve executar validacoes reais.

#### Heuristicas obrigatorias dos testes

- `test_prompt_has_role_definition`
  - deve considerar valido quando o `system_prompt` trouxer definicao explicita de papel, como:
    - `Voce e`
    - `Voce atua como`
    - `Seu papel e`
- `test_prompt_mentions_format`
  - deve validar a presenca explicita de:
    - `Markdown`
    - `User Story`
    - estrutura `Como ... eu quero ... para que ...`
- `test_prompt_has_few_shot_examples`
  - deve validar:
    - campo `examples`
    - minimo de `2` exemplos como regra de teste
    - cada exemplo com entrada e saida definidas

### RF-06 - Documentacao do processo

O `README.md` deve documentar como o projeto funciona e como a otimizacao foi conduzida.

#### Criterios

- Explicar tecnicas aplicadas e justificativas.
- Mostrar como executar pull, push e avaliacao.
- Documentar resultados finais.
- Incluir link publico ou evidencias do LangSmith.
- Explicar a estrategia de iteracao e debug com tracing.
- Documentar tambem a jornada de iteracao, e nao apenas o resultado final.
- Conter obrigatoriamente as secoes:
  - `Tecnicas Aplicadas`
  - `Como Executar`
  - `Resultados Finais`
  - `Jornada de Iteracao`
  - `Evidencias no LangSmith`

## 8. Requisitos Nao Funcionais

### RNF-01 - Compatibilidade tecnica

- Linguagem: Python 3.9+.
- Framework principal: LangChain.
- Integracao de prompts e avaliacao: LangSmith.
- Formato dos prompts: YAML.

### RNF-02 - Reprodutibilidade

- O projeto deve ser executavel localmente com `venv` e `pip install -r requirements.txt`.
- O comportamento dos scripts deve depender do `.env` ja existente no projeto.
- Nao faz parte deste milestone criar `.env.example`.

### RNF-03 - Observabilidade

- O tracing do LangSmith deve ser usado como principal mecanismo de debug.
- Devem existir evidencias de pelo menos 3 execucoes analisadas com tracing.

### RNF-04 - Qualidade do prompt

- O prompt deve ser especifico, orientado a contexto e persona.
- O prompt deve prever edge cases.
- O prompt deve guiar o modelo a produzir saidas consistentes e testaveis.

## 9. Requisitos de Conteudo do Prompt v2

O arquivo `prompts/bug_to_user_story_v2.yml` deve refletir explicitamente os principios abaixo:

- especificidade;
- contexto;
- persona clara;
- formato padrao de user story;
- criterios de aceitacao bem definidos;
- few-shot com `3` exemplos;
- `Chain of Thought` e `Role Prompting` alem de few-shot;
- tratamento de casos simples, medios e complexos;
- proibicao de respostas vagas ou apenas tecnicas sem foco no valor para o usuario.

### Recomendacao de abordagem de prompt engineering

- `Few-shot Learning` como tecnica obrigatoria.
- `Role Prompting` como tecnica obrigatoria para definir a persona do agente.
- `Chain of Thought` como tecnica obrigatoria para estruturar o raciocinio em casos complexos.

Observacao importante:

- O CoT deve melhorar a qualidade do processo sem expor raciocinio detalhado desnecessario ao usuario final.
- O objetivo principal e qualidade de saida e nao verbosidade.

## 10. Historias de Implementacao

### Historia 1 - Como aluno, quero baixar o prompt inicial do LangSmith

Para que eu possa usar a versao ruim como ponto de partida local.

#### Tarefas tecnicas

- Revisar e concluir `src/pull_prompts.py`.
- Garantir leitura correta de variaveis:
  - `LANGSMITH_API_KEY`
  - `LANGSMITH_ENDPOINT` se aplicavel
  - `USERNAME_LANGSMITH_HUB` se aplicavel
- Garantir salvamento correto em YAML.

### Historia 2 - Como aluno, quero criar um prompt v2 otimizado

Para que eu possa aumentar a nota em todas as metricas.

#### Tarefas tecnicas

- Criar `prompts/bug_to_user_story_v2.yml`.
- Definir persona, formato de saida e regras.
- Inserir `3` exemplos few-shot em campo separado `examples`.
- Cobrir edge cases.
- Incluir metadados de tecnicas aplicadas.

### Historia 3 - Como aluno, quero publicar o prompt otimizado no LangSmith

Para que ele possa ser avaliado pelo fluxo do projeto.

#### Tarefas tecnicas

- Implementar `src/push_prompts.py`.
- Ler YAML local.
- Validar estrutura.
- Converter para `ChatPromptTemplate`.
- Fazer push com metadados.
- Garantir que o prompt publicado continue consumivel pelo `src/evaluate.py` sem alterar esse arquivo.

### Historia 4 - Como aluno, quero validar o prompt otimizado com testes

Para que a qualidade estrutural do YAML nao dependa apenas de execucao manual.

#### Tarefas tecnicas

- Implementar os 6 testes obrigatorios.
- Adaptar a leitura do YAML para a estrutura real do arquivo.
- Garantir que os testes falhem quando o prompt estiver incompleto.
- Aplicar as heuristicas definidas neste PRD para papel, formato e examples.

### Historia 5 - Como aluno, quero iterar com apoio do LangSmith

Para que eu consiga diagnosticar porque as metricas ainda estao baixas.

#### Tarefas tecnicas

- Rodar push e avaliacao em ciclos.
- Inspecionar tracing do LangSmith.
- Ajustar apenas `prompts/bug_to_user_story_v2.yml`.
- Repetir ate atingir o alvo.

### Historia 6 - Como avaliador, quero documentacao clara da jornada

Para que eu possa entender o raciocinio, a execucao e as evidencias finais.

#### Tarefas tecnicas

- Atualizar `README.md`.
- Explicar tecnicas escolhidas.
- Descrever iteracoes e aprendizados.
- Incluir links e capturas do LangSmith.

## 11. Ajustes Tecnicos Necessarios Detectados na Base

Mesmo com a regra de preservar os componentes ja fornecidos, a implementacao precisa considerar os seguintes ajustes ou validacoes pontuais:

1. Revisar `src/pull_prompts.py` para garantir compatibilidade com a assinatura real de `save_yaml`.
2. Padronizar a leitura dos arquivos YAML considerando estrutura aninhada por nome do prompt.
3. Garantir que `tests/test_prompts.py` e `src/push_prompts.py` saibam localizar corretamente o bloco `bug_to_user_story_v2`.
4. Validar o fluxo de provider suportado no `.env`, principalmente se o usuario optar por OpenAI ou Google.
5. Confirmar que o nome do prompt publicado no Hub permanece alinhado com o nome simples consumido por `src/evaluate.py`.

## 12. Dependencias

### Dependencias externas

- Conta e API key do LangSmith.
- API key da OpenAI ou Google.
- Acesso ao LangSmith Prompt Hub.

### Dependencias internas

- `src/utils.py`
- `src/metrics.py`
- `src/evaluate.py`
- `prompts/bug_to_user_story_v1.yml`
- `datasets/bug_to_user_story.jsonl`
- `.env`

## 13. Fluxo Esperado de Uso

1. Configurar ambiente virtual.
2. Configurar `.env` com as credenciais.
3. Executar `python src/pull_prompts.py`.
4. Criar ou ajustar `prompts/bug_to_user_story_v2.yml`.
5. Executar `python src/push_prompts.py`.
6. Executar `python src/evaluate.py`.
7. Inspecionar traces no LangSmith.
8. Ajustar somente o prompt v2.
9. Repetir o ciclo ate todas as metricas atingirem `>= 0.9`.
10. Rodar `pytest tests/test_prompts.py`.
11. Atualizar README com a versao final e as evidencias.

## 14. Criterios de Aceite do Projeto

O projeto sera considerado pronto quando:

- `src/pull_prompts.py` estiver funcional e validado.
- `src/push_prompts.py` estiver funcional e validado.
- `prompts/bug_to_user_story_v2.yml` existir e estiver completo.
- `tests/test_prompts.py` executar os 6 testes reais com sucesso.
- `README.md` estiver atualizado com tecnicas, iteracoes, resultados e modo de execucao.
- O prompt `bug_to_user_story_v2` estiver publicado no LangSmith.
- Houver evidencias publicas ou capturas do LangSmith.
- O dataset permanecer inalterado.
- `src/evaluate.py`, `src/metrics.py`, `src/utils.py` e `datasets/bug_to_user_story.jsonl` permanecerem inalterados.
- Todas as metricas de avaliacao ficarem `>= 0.9` individualmente.

## 15. Riscos

- O prompt v2 pode exigir varias iteracoes para atingir os thresholds.
- O tracing pode mostrar problemas semanticos que nao sao visiveis apenas lendo o YAML.
- O push pode falhar por formato incorreto do prompt ou falta de metadados adequados.
- Os testes podem precisar considerar a estrutura exata do YAML para nao gerar falso positivo.
- A divergencia entre nomes de provider ou nomes de prompt pode causar falhas aparentes de avaliacao mesmo quando o prompt estiver bom.

## 16. Estrategia Recomendada de Entrega

### Fase 1 - Fechar infraestrutura minima

- Concluir `pull_prompts.py`.
- Implementar `push_prompts.py`.
- Adaptar tudo ao `.env` existente, sem introduzir dependencia de `.env.example`.

### Fase 2 - Criar o prompt otimizado

- Construir `bug_to_user_story_v2.yml`.
- Aplicar `Few-shot Learning` obrigatoriamente.
- Aplicar `Role Prompting` e `Chain of Thought`.
- Criar campo `examples` com `3` exemplos estruturados.

### Fase 3 - Validar localmente

- Implementar testes.
- Garantir leitura correta do YAML.

### Fase 4 - Iterar com LangSmith

- Publicar prompt.
- Rodar avaliacao.
- Inspecionar tracing.
- Refinar apenas o `bug_to_user_story_v2.yml`.

### Fase 5 - Consolidar entrega

- Atualizar `README.md`.
- Registrar evidencias finais.

## 17. Entregaveis Finais

- `src/pull_prompts.py` funcional
- `src/push_prompts.py` funcional
- `prompts/bug_to_user_story_v2.yml`
- `tests/test_prompts.py` implementado
- `README.md` atualizado
- evidencias de avaliacao e tracing no LangSmith

## 18. Resumo Executivo

Pelo estado atual do repositorio, o nucleo de avaliacao e utilitarios ja existe, mas o projeto ainda nao atende o desafio porque faltam os artefatos principais da entrega: prompt otimizado, push para o LangSmith, testes reais e documentacao final.

O foco da implementacao deve ser completar esse fluxo com o minimo de mudanca estrutural, preservando dataset e base de avaliacao, e concentrando o esforco de qualidade no arquivo `prompts/bug_to_user_story_v2.yml` e no ciclo iterativo de melhoria orientado por tracing e metricas.

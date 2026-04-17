## ADDED Requirements

### Requirement: Local tests must validate the prompt structure and content heuristics
The project SHALL provide real `pytest` validations for the optimized prompt instead of placeholder tests.

#### Scenario: Tests validate the nested prompt block
- **WHEN** `tests/test_prompts.py` loads `prompts/bug_to_user_story_v2.yml`
- **THEN** it MUST validate the `bug_to_user_story_v2` block
- **THEN** it MUST fail if the file is missing, invalid, or missing that key

#### Scenario: Role, format, and examples heuristics are enforced
- **WHEN** the prompt is tested
- **THEN** the tests MUST validate explicit role-definition signals
- **THEN** the tests MUST validate explicit format signals for Markdown and User Story structure
- **THEN** the tests MUST validate that examples contain input and output pairs

### Requirement: Documentation must capture execution and optimization journey
The project SHALL update `README.md` with both the final outcome and the iteration process used to improve the prompt.

#### Scenario: README contains required sections
- **WHEN** the final documentation is reviewed
- **THEN** it MUST contain `Tecnicas Aplicadas`, `Como Executar`, `Resultados Finais`, `Jornada de Iteracao`, and `Evidencias no LangSmith`

#### Scenario: README explains optimization choices
- **WHEN** the documentation is reviewed
- **THEN** it MUST explain the chosen prompt-engineering techniques and why they were selected

### Requirement: LangSmith evidence must be captured for final delivery
The final delivery SHALL include evidence that the optimized prompt was evaluated and debugged through LangSmith.

#### Scenario: Final evidence includes evaluation and tracing
- **WHEN** the delivery is finalized
- **THEN** it MUST include a public link or screenshots from LangSmith
- **THEN** it MUST include final evaluation results
- **THEN** it MUST include tracing evidence for at least three examples

#### Scenario: Dataset remains unchanged
- **WHEN** the implementation is completed
- **THEN** `datasets/bug_to_user_story.jsonl` MUST remain unchanged

## ADDED Requirements

### Requirement: Prompt v2 file must follow the approved YAML contract
The optimized prompt file SHALL use the same nested structure as the v1 prompt and define the approved fields under the `bug_to_user_story_v2` root key.

#### Scenario: Prompt file uses nested root
- **WHEN** `prompts/bug_to_user_story_v2.yml` is loaded
- **THEN** it MUST contain the root key `bug_to_user_story_v2`

#### Scenario: Prompt file contains required fields
- **WHEN** the prompt definition is parsed
- **THEN** it MUST contain `description`, `system_prompt`, `examples`, `user_prompt`, `version`, `created_at`, `tags`, and `techniques_applied`

### Requirement: Prompt v2 must include the approved prompt-engineering techniques
The optimized prompt SHALL use `Few-shot Learning`, `Chain of Thought`, and `Role Prompting` to improve bug-to-user-story generation quality.

#### Scenario: Techniques metadata is declared
- **WHEN** the prompt metadata is inspected
- **THEN** `techniques_applied` MUST list `Few-shot Learning`, `Chain of Thought`, and `Role Prompting`

#### Scenario: Persona is explicitly defined
- **WHEN** the `system_prompt` is inspected
- **THEN** it MUST define an explicit `Product Manager senior` role or equivalent senior PM persona

### Requirement: Prompt v2 must separate examples from user input
The optimized prompt SHALL keep the dynamic user input limited to `{bug_report}` and store few-shot examples in a dedicated `examples` field.

#### Scenario: User prompt contains only dynamic input
- **WHEN** the `user_prompt` field is inspected
- **THEN** it MUST represent only the bug report input contract
- **THEN** it MUST not embed the fixed few-shot examples

#### Scenario: Exactly three structured examples are present
- **WHEN** the `examples` field is inspected
- **THEN** it MUST contain exactly three examples
- **THEN** those examples MUST represent one simple, one medium, and one complex bug

### Requirement: Prompt v2 must enforce the approved output format
The optimized prompt SHALL instruct the model to respond in Markdown with a user story structure focused on user value and testable acceptance criteria.

#### Scenario: Output structure is defined
- **WHEN** the prompt instructions are inspected
- **THEN** they MUST require the sections `Titulo`, `User Story`, and `Criterios de Aceitacao`

#### Scenario: Technical context is conditional
- **WHEN** the bug contains relevant technical information, especially in medium or complex cases
- **THEN** the prompt MUST allow or require a `Contexto Tecnico` section

#### Scenario: Acceptance criteria are testable
- **WHEN** the prompt describes the acceptance criteria format
- **THEN** it MUST instruct the model to use `Dado que`, `Quando`, and `Entao`

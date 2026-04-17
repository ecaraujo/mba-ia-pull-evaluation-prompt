## ADDED Requirements

### Requirement: Pull prompt v1 from LangSmith
The system SHALL fetch the challenge prompt `leonanluppi/bug_to_user_story_v1` from LangSmith and persist it locally as `prompts/bug_to_user_story_v1.yml`, while remaining compatible with the existing `.env` contract.

#### Scenario: Default pull execution
- **WHEN** the user runs `python src/pull_prompts.py` without overriding the prompt name
- **THEN** the system fetches `leonanluppi/bug_to_user_story_v1`
- **THEN** the system saves the result to `prompts/bug_to_user_story_v1.yml`

#### Scenario: Pull uses environment-based credentials
- **WHEN** the script starts
- **THEN** it MUST read LangSmith configuration from the existing `.env`
- **THEN** it MUST fail with a clear message if required credentials are missing

### Requirement: Publish prompt v2 compatibly with the evaluator
The system SHALL publish the optimized prompt `bug_to_user_story_v2` to LangSmith in a way that remains consumable by the existing `src/evaluate.py` without modifying that file.

#### Scenario: Push publishes the optimized prompt
- **WHEN** the user runs `python src/push_prompts.py`
- **THEN** the system reads `prompts/bug_to_user_story_v2.yml`
- **THEN** the system publishes only the `bug_to_user_story_v2` prompt

#### Scenario: Push preserves evaluator compatibility
- **WHEN** the optimized prompt is published
- **THEN** the published prompt MUST remain resolvable by the name `bug_to_user_story_v2` in the current evaluation flow
- **THEN** no changes to `src/evaluate.py` are required

### Requirement: Push must attach prompt metadata
The system SHALL publish prompt metadata needed to identify the optimized artifact and support iteration tracking.

#### Scenario: Metadata is sent during push
- **WHEN** the optimized prompt is published
- **THEN** the payload MUST include description, tags, techniques applied, and version

#### Scenario: Invalid prompt structure blocks publish
- **WHEN** the local prompt file is missing required fields
- **THEN** the push flow MUST stop before publication
- **THEN** the user MUST receive a clear validation error

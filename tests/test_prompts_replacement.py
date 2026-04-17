"""Testes automatizados para validacao do prompt v2."""

from __future__ import annotations

import re
import sys
from pathlib import Path

import pytest
import yaml

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils import validate_prompt_structure


PROMPT_FILE = Path(__file__).resolve().parent.parent / "prompts" / "bug_to_user_story_v2.yml"
PROMPT_KEY = "bug_to_user_story_v2"


def _load_prompt_block() -> dict:
    """Carrega e valida o bloco raiz do prompt otimizado."""
    if not PROMPT_FILE.exists():
        pytest.fail(f"Arquivo de prompt nao encontrado: {PROMPT_FILE}")

    with PROMPT_FILE.open("r", encoding="utf-8") as file:
        data = yaml.safe_load(file)

    if not isinstance(data, dict):
        pytest.fail("O YAML do prompt deve ser um objeto na raiz.")

    prompt_block = data.get(PROMPT_KEY)
    if not isinstance(prompt_block, dict):
        pytest.fail(f"O YAML deve conter o bloco raiz '{PROMPT_KEY}'.")

    return prompt_block


def _flatten_prompt_text(prompt_block: dict) -> str:
    """Concatena os textos do prompt para buscas simples."""
    examples = prompt_block.get("examples", [])
    parts = [
        str(prompt_block.get("description", "")),
        str(prompt_block.get("system_prompt", "")),
        str(prompt_block.get("user_prompt", "")),
        str(prompt_block.get("techniques_applied", "")),
    ]

    for example in examples:
        if isinstance(example, dict):
            parts.append(str(example.get("input", example.get("bug_report", ""))))
            parts.append(
                str(
                    example.get(
                        "output",
                        example.get("user_story", example.get("reference", "")),
                    )
                )
            )

    return "\n".join(parts)


class TestPrompts:
    def test_prompt_has_system_prompt(self):
        """Verifica se o campo 'system_prompt' existe e nao esta vazio."""
        prompt_block = _load_prompt_block()

        system_prompt = str(prompt_block.get("system_prompt", "")).strip()
        is_valid, errors = validate_prompt_structure(prompt_block)

        assert system_prompt, "system_prompt nao pode estar vazio"
        assert is_valid or "system_prompt est" not in " ".join(errors)

    def test_prompt_has_role_definition(self):
        """Verifica se o prompt define uma persona explicita."""
        prompt_block = _load_prompt_block()
        system_prompt = str(prompt_block.get("system_prompt", ""))

        patterns = [
            r"\bVoc[eê]\s+[ée]\b",
            r"\bVoc[eê]\s+atua\s+como\b",
            r"\bSeu\s+papel\s+[ée]\b",
            r"Product Manager",
        ]

        assert any(
            re.search(pattern, system_prompt, flags=re.IGNORECASE)
            for pattern in patterns
        ), (
            "O system_prompt deve definir claramente uma persona, por exemplo: "
            "'Voce e um Product Manager...'."
        )

    def test_prompt_mentions_format(self):
        """Verifica se o prompt exige Markdown e User Story no formato padrao."""
        prompt_block = _load_prompt_block()
        prompt_text = _flatten_prompt_text(prompt_block).lower()

        assert "markdown" in prompt_text, "O prompt deve exigir saida em Markdown."
        assert "user story" in prompt_text, "O prompt deve mencionar explicitamente User Story."
        assert "como [" in prompt_text or "como um" in prompt_text, (
            "O prompt deve indicar a estrutura 'Como...'."
        )
        assert "eu quero" in prompt_text, "O prompt deve indicar a estrutura 'eu quero...'."
        assert "para que" in prompt_text, "O prompt deve indicar a estrutura 'para que...'."

    def test_prompt_has_few_shot_examples(self):
        """Verifica se o prompt contem exemplos estruturados de entrada e saida."""
        prompt_block = _load_prompt_block()
        examples = prompt_block.get("examples")

        assert isinstance(examples, list), "examples deve ser uma lista."
        assert len(examples) >= 2, "O prompt deve conter pelo menos 2 exemplos few-shot."

        for index, example in enumerate(examples, start=1):
            assert isinstance(example, dict), f"O exemplo {index} deve ser um objeto."

            example_input = str(example.get("input", example.get("bug_report", ""))).strip()
            example_output = str(
                example.get("output", example.get("user_story", example.get("reference", "")))
            ).strip()

            assert example_input, f"O exemplo {index} deve conter uma entrada."
            assert example_output, f"O exemplo {index} deve conter uma saida."

    def test_prompt_no_todos(self):
        """Garante que nenhum campo contenha TODOs pendentes."""
        prompt_block = _load_prompt_block()
        prompt_text = _flatten_prompt_text(prompt_block).upper()

        assert "[TODO]" not in prompt_text, "Nao deve haver marcadores [TODO] no prompt."
        assert "TODO" not in prompt_text, "Nao deve haver TODOs pendentes no prompt."

    def test_minimum_techniques(self):
        """Verifica se pelo menos 2 tecnicas foram listadas nos metadados."""
        prompt_block = _load_prompt_block()
        techniques = prompt_block.get("techniques_applied")

        assert isinstance(techniques, list), "techniques_applied deve ser uma lista."
        assert len(techniques) >= 2, "O prompt deve listar pelo menos 2 tecnicas."


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])

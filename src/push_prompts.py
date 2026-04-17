"""
Script para fazer push de prompts otimizados ao LangSmith Prompt Hub.

Este script:
1. Le o prompt otimizado de prompts/bug_to_user_story_v2.yml
2. Valida a estrutura esperada do YAML
3. Monta um ChatPromptTemplate com system prompt, few-shot examples e user prompt
4. Faz push publico para o LangSmith Hub com metadados
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path
from typing import Any

from langsmith import Client
from langchain_core.prompts import ChatPromptTemplate

from utils import load_yaml, check_env_vars, print_section_header

try:
    from dotenv import load_dotenv
except ModuleNotFoundError as e:
    raise SystemExit(
        "Pacote 'python-dotenv' nao instalado. Rode: python -m pip install python-dotenv"
    ) from e


def _project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _prompt_key(prompt_name: str) -> str:
    prompt_ref = prompt_name.split(":", 1)[0]
    return prompt_ref.rsplit("/", 1)[-1]


def _public_prompt_identifier(prompt_name: str) -> str:
    prompt_ref = prompt_name.split(":", 1)[0].strip()
    if "/" in prompt_ref:
        return prompt_ref

    hub_handle = (os.getenv("USERNAME_LANGSMITH_HUB") or "").strip().strip("/")
    if hub_handle:
        return f"{hub_handle}/{_prompt_key(prompt_name)}"

    return _prompt_key(prompt_name)


def _prompt_file_path(root: Path, prompt_name: str) -> Path:
    return root / "prompts" / f"{_prompt_key(prompt_name)}.yml"


def _slugify_tag(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.strip().lower()).strip("-")


def _get_example_input(example: dict[str, Any]) -> str:
    if "input" in example:
        input_value = example["input"]
        if isinstance(input_value, dict):
            return str(input_value.get("bug_report", "")).strip()
        return str(input_value).strip()
    return str(example.get("bug_report", "")).strip()


def _get_example_output(example: dict[str, Any]) -> str:
    if "output" in example:
        output_value = example["output"]
        if isinstance(output_value, dict):
            return str(
                output_value.get("user_story", output_value.get("reference", ""))
            ).strip()
        return str(output_value).strip()
    return str(example.get("user_story", example.get("reference", ""))).strip()


def _build_prompt_template(prompt_data: dict[str, Any]) -> ChatPromptTemplate:
    messages: list[tuple[str, str]] = [("system", prompt_data["system_prompt"].strip())]

    few_shot_blocks = list(prompt_data.get("examples", [])) + list(
        prompt_data.get("canonical_cases", [])
    )

    for example in few_shot_blocks:
        example_input = _get_example_input(example)
        example_output = _get_example_output(example)
        if example_input and example_output:
            messages.append(("human", example_input))
            messages.append(("ai", example_output))

    messages.append(("human", prompt_data["user_prompt"].strip()))
    return ChatPromptTemplate.from_messages(messages)


def _build_readme(prompt_name: str, prompt_data: dict[str, Any]) -> str:
    techniques = prompt_data.get("techniques_applied", [])
    tags = prompt_data.get("tags", [])
    version = prompt_data.get("version", "")

    return "\n".join(
        [
            f"# {prompt_name}",
            "",
            prompt_data.get("description", "").strip(),
            "",
            f"- Version: {version}",
            f"- Techniques: {', '.join(techniques)}",
            f"- Tags: {', '.join(tags)}",
        ]
    ).strip()


def _load_prompt_data(file_path: Path, prompt_name: str) -> dict[str, Any]:
    prompt_file = load_yaml(str(file_path))
    if prompt_file is None:
        raise ValueError(f"Nao foi possivel carregar o arquivo: {file_path}")

    prompt_data = prompt_file.get(_prompt_key(prompt_name))
    if not isinstance(prompt_data, dict):
        raise ValueError(
            f"O arquivo {file_path} deve conter o bloco raiz '{_prompt_key(prompt_name)}'."
        )
    return prompt_data


def push_prompt_to_langsmith(prompt_name: str, prompt_data: dict[str, Any]) -> bool:
    """
    Faz push do prompt otimizado para o LangSmith Hub.
    """
    api_key = (os.getenv("LANGSMITH_API_KEY") or "").strip()
    endpoint = (os.getenv("LANGSMITH_ENDPOINT") or "").strip()
    project = (os.getenv("LANGSMITH_PROJECT") or "").strip()

    if endpoint:
        os.environ.setdefault("LANGCHAIN_ENDPOINT", endpoint)
    if project:
        os.environ.setdefault("LANGCHAIN_PROJECT", project)
    os.environ.setdefault("LANGCHAIN_API_KEY", api_key)

    template = _build_prompt_template(prompt_data)
    tags = list(dict.fromkeys(prompt_data.get("tags", [])))
    techniques = prompt_data.get("techniques_applied", [])

    prompt_tags = tags + [f"technique:{_slugify_tag(item)}" for item in techniques]
    commit_tags = [prompt_data.get("version", "").strip()] + [
        _slugify_tag(item) for item in techniques
    ]
    commit_tags = [tag for tag in commit_tags if tag]
    public_prompt_identifier = _public_prompt_identifier(prompt_name)
    private_prompt_identifier = _prompt_key(prompt_name)

    client = Client(api_url=endpoint or None, api_key=api_key)
    push_kwargs = {
        "object": template,
        "description": prompt_data.get("description", "").strip(),
        "readme": _build_readme(prompt_name, prompt_data),
        "tags": prompt_tags,
        "commit_tags": commit_tags,
    }

    def _push(prompt_identifier: str, *, is_public: bool, with_commit_tags: bool):
        kwargs = dict(push_kwargs)
        if with_commit_tags:
            kwargs["commit_tags"] = commit_tags
        return client.push_prompt(
            prompt_identifier,
            is_public=is_public,
            **kwargs,
        )

    def _is_commit_tag_conflict(error_text: str) -> bool:
        return "already exists on commit" in error_text

    def _is_nothing_to_commit(error_text: str) -> bool:
        normalized = error_text.lower()
        return (
            "nothing to commit" in normalized
            or "prompt has not changed since latest commit" in normalized
        )

    try:
        print(f"Tentando publicar no Prompt Hub como: {public_prompt_identifier}")
        prompt_url = _push(
            public_prompt_identifier,
            is_public=True,
            with_commit_tags=True,
        )
        print(f"Prompt publicado com sucesso: {prompt_url}")
        return True
    except Exception as exc:
        error_text = str(exc)
        if "Cannot create a public prompt without first" not in error_text:
            if _is_nothing_to_commit(error_text):
                print(
                    "Prompt ja estava publicado e sem alteracoes desde o ultimo commit. "
                    "Nenhum novo commit foi criado."
                )
                return True

            if not _is_commit_tag_conflict(error_text):
                raise

            print(
                "Aviso: conflito de tags de commit detectado no LangSmith. "
                "Repetindo o push sem commit_tags para registrar a nova iteracao."
            )
            try:
                prompt_url = _push(
                    public_prompt_identifier,
                    is_public=True,
                    with_commit_tags=False,
                )
                print(f"Prompt publicado com sucesso: {prompt_url}")
            except Exception as retry_exc:
                retry_error_text = str(retry_exc)
                if not _is_nothing_to_commit(retry_error_text):
                    raise
                print(
                    "Prompt ja estava publicado e sem alteracoes desde o ultimo commit. "
                    "Nenhum novo commit foi criado."
                )
            return True

        print(
            "Aviso: LangSmith ainda nao possui um Hub handle publico configurado. "
            "Fazendo push privado para permitir a avaliacao local/remota."
        )
        try:
            prompt_url = _push(
                private_prompt_identifier,
                is_public=False,
                with_commit_tags=True,
            )
        except Exception as private_exc:
            private_error_text = str(private_exc)
            if _is_nothing_to_commit(private_error_text):
                print(
                    "Prompt ja estava publicado de forma privada e sem alteracoes "
                    "desde o ultimo commit."
                )
                print(
                    "Para deixa-lo publico depois, crie um Hub handle em "
                    "https://smith.langchain.com/prompts e execute o push novamente."
                )
                return True

            if not _is_commit_tag_conflict(private_error_text):
                raise

            print(
                "Aviso: conflito de tags de commit detectado no push privado. "
                "Repetindo sem commit_tags."
            )
            try:
                prompt_url = _push(
                    private_prompt_identifier,
                    is_public=False,
                    with_commit_tags=False,
                )
            except Exception as private_retry_exc:
                private_retry_error_text = str(private_retry_exc)
                if not _is_nothing_to_commit(private_retry_error_text):
                    raise
                print(
                    "Prompt ja estava publicado de forma privada e sem alteracoes "
                    "desde o ultimo commit."
                )
                print(
                    "Para deixa-lo publico depois, crie um Hub handle em "
                    "https://smith.langchain.com/prompts e execute o push novamente."
                )
                return True
        print(f"Prompt publicado de forma privada: {prompt_url}")
        print(
            "Para deixar o prompt publico depois, crie um Hub handle em "
            "https://smith.langchain.com/prompts e execute o push novamente."
        )
        return True


def validate_prompt(prompt_data: dict[str, Any]) -> tuple[bool, list[str]]:
    """
    Valida estrutura basica de um prompt.
    """
    errors: list[str] = []
    required_fields = [
        "description",
        "system_prompt",
        "examples",
        "user_prompt",
        "version",
        "created_at",
        "tags",
        "techniques_applied",
    ]

    for field in required_fields:
        if field not in prompt_data:
            errors.append(f"Campo obrigatorio faltando: {field}")

    if not str(prompt_data.get("system_prompt", "")).strip():
        errors.append("system_prompt esta vazio")

    if str(prompt_data.get("user_prompt", "")).strip() != "{bug_report}":
        errors.append("user_prompt deve ser exatamente '{bug_report}'")

    examples = prompt_data.get("examples")
    if not isinstance(examples, list):
        errors.append("examples deve ser uma lista")
    else:
        if len(examples) != 3:
            errors.append("examples deve conter exatamente 3 exemplos")
        for index, example in enumerate(examples, start=1):
            if not isinstance(example, dict):
                errors.append(f"Exemplo {index} deve ser um objeto")
                continue
            if not _get_example_input(example):
                errors.append(f"Exemplo {index} esta sem entrada")
            if not _get_example_output(example):
                errors.append(f"Exemplo {index} esta sem saida")

    tags = prompt_data.get("tags")
    if not isinstance(tags, list) or not tags:
        errors.append("tags deve ser uma lista nao vazia")

    techniques = prompt_data.get("techniques_applied")
    if not isinstance(techniques, list) or len(techniques) < 2:
        errors.append("techniques_applied deve listar pelo menos 2 tecnicas")

    if "TODO" in str(prompt_data.get("system_prompt", "")):
        errors.append("system_prompt ainda contem TODOs")

    return (len(errors) == 0, errors)


def main() -> int:
    root = _project_root()
    load_dotenv(dotenv_path=root / ".env")

    print_section_header("Push do prompt otimizado")

    if not check_env_vars(["LANGSMITH_API_KEY"]):
        return 1

    prompt_name = os.getenv("PROMPT_NAME", "bug_to_user_story_v2").strip()
    prompt_path = _prompt_file_path(root, prompt_name)

    try:
        prompt_data = _load_prompt_data(prompt_path, prompt_name)
    except ValueError as exc:
        print(f"Erro: {exc}")
        return 1

    is_valid, errors = validate_prompt(prompt_data)
    if not is_valid:
        print("Prompt invalido:")
        for error in errors:
            print(f"  - {error}")
        return 1

    try:
        push_prompt_to_langsmith(prompt_name, prompt_data)
        return 0
    except Exception as exc:
        print(f"Erro ao fazer push do prompt: {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())

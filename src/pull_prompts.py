"""
Script para fazer pull de prompts do LangSmith Prompt Hub.

- Carrega .env
- Conecta ao LangSmith
- Faz pull de um prompt (privado: "nome"; público: "owner/nome")
- Salva em YAML

Requisitos:
  pip install python-dotenv langsmith pyyaml
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any, Dict, Optional

from utils import save_yaml, check_env_vars, print_section_header

# Carrega .env (mantém o import do dotenv, mas falha com mensagem clara se não estiver instalado)
try:
    from dotenv import load_dotenv
except ModuleNotFoundError as e:
    raise SystemExit(
        "Pacote 'python-dotenv' não instalado. Rode: python -m pip install python-dotenv"
    ) from e


def _project_root() -> Path:
    # src/pull_prompts.py -> raiz do projeto é o pai de src
    return Path(__file__).resolve().parents[1]


def _build_prompt_ref(prompt_name: str) -> str:
    """
    Se USERNAME_LANGSMITH_HUB estiver definido, monta "username/prompt".
    Se não, usa só "prompt" (funciona bem para prompts privados do seu workspace).
    """
    if "/" in prompt_name:
        return prompt_name
    username = (os.getenv("USERNAME_LANGSMITH_HUB") or "").strip()
    if username:
        return f"{username}/{prompt_name}"
    return prompt_name


def _prompt_file_name(prompt_name: str) -> str:
    prompt_ref = prompt_name.split(":", 1)[0]
    return f"{prompt_ref.rsplit('/', 1)[-1]}.yml"


def _serialize_prompt(prompt: Any) -> Dict[str, Any]:
    # serialização robusta
    if hasattr(prompt, "model_dump") and callable(getattr(prompt, "model_dump")):
        return prompt.model_dump()  # pydantic v2
    if hasattr(prompt, "dict") and callable(getattr(prompt, "dict")):
        return prompt.dict()  # pydantic v1
    if hasattr(prompt, "to_json") and callable(getattr(prompt, "to_json")):
        return prompt.to_json()
    return {"_type": "unknown", "repr": repr(prompt)}


def pull_prompts_from_langsmith(
    prompt_name: str,
    output_path: Path,
    version: Optional[str] = None,
) -> Path:
    """
    Faz pull do prompt no LangSmith e salva em YAML.
    version: commit hash/tag, ex: "12344e88" -> prompt:12344e88
    """
    try:
        from langsmith import Client
    except ModuleNotFoundError as e:
        raise SystemExit(
            "Pacote 'langsmith' não instalado. Rode: python -m pip install langsmith"
        ) from e

    # Variáveis do seu .env
    api_key = (os.getenv("LANGSMITH_API_KEY") or "").strip()
    endpoint = (os.getenv("LANGSMITH_ENDPOINT") or "").strip()
    project = (os.getenv("LANGSMITH_PROJECT") or "").strip()

    # Validação mínima (usa seu utils.check_env_vars)
    if not check_env_vars(["LANGSMITH_API_KEY"]):
        raise SystemExit(1)

    # Compat: algumas libs antigas usam LANGCHAIN_*
    # (o Client também pode usar LANGCHAIN_ENDPOINT como default) :contentReference[oaicite:1]{index=1}
    if endpoint:
        os.environ.setdefault("LANGCHAIN_ENDPOINT", endpoint)
    if project:
        os.environ.setdefault("LANGCHAIN_PROJECT", project)
    os.environ.setdefault("LANGCHAIN_API_KEY", api_key)

    # Conecta explicitamente para não depender de nomes de env vars
    client = Client(api_url=endpoint or None, api_key=api_key)

    prompt_ref = _build_prompt_ref(prompt_name)
    if version:
        prompt_ref = f"{prompt_ref}:{version}"

    print_section_header("Pull do prompt")
    print(f"Prompt ref: {prompt_ref}")

    prompt = client.pull_prompt(prompt_ref)  # :contentReference[oaicite:2]{index=2}

    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Alguns objetos têm .save(); se não tiver, salva YAML serializado
    try:
        if hasattr(prompt, "save") and callable(getattr(prompt, "save")):
            prompt.save(str(output_path))
            print(f"Salvo via prompt.save() em: {output_path}")
            return output_path
    except Exception:
        pass

    data = _serialize_prompt(prompt)
    save_yaml(data, str(output_path))
    print(f"Salvo via YAML fallback em: {output_path}")
    return output_path


def main() -> int:
    root = _project_root()
    load_dotenv(dotenv_path=root / ".env")

    # defaults
    prompt_name = os.getenv("PROMPT_NAME", "leonanluppi/bug_to_user_story_v1").strip()
    version = (os.getenv("PROMPT_VERSION") or "").strip() or None
    output_path = Path(
        os.getenv("PROMPT_OUT", str(root / "prompts" / _prompt_file_name(prompt_name)))
    )

    pull_prompts_from_langsmith(prompt_name, output_path, version=version)
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""Compatibility shims loaded automatically by Python's site module.

This project's `src/evaluate.py` expects `from langchain import hub`, but the
runtime currently has `langchain 1.x`, which no longer exposes that symbol.
To avoid changing the protected evaluator script, we recreate a small
compatibility layer that forwards `hub.pull(...)` to `langsmith.Client`.
"""

from __future__ import annotations

import os
import sys
import types


def _install_langchain_hub_compat() -> None:
    try:
        import langchain
        from langsmith import Client
    except Exception:
        return

    if hasattr(langchain, "hub") and "langchain.hub" in sys.modules:
        return

    def _pull(prompt_name: str):
        api_key = (os.getenv("LANGSMITH_API_KEY") or "").strip()
        endpoint = (os.getenv("LANGSMITH_ENDPOINT") or "").strip()
        client = Client(api_url=endpoint or None, api_key=api_key or None)
        return client.pull_prompt(prompt_name)

    hub_module = types.ModuleType("langchain.hub")
    hub_module.pull = _pull

    sys.modules["langchain.hub"] = hub_module
    setattr(langchain, "hub", hub_module)


_install_langchain_hub_compat()

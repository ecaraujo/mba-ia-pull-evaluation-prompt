"""Compatibility helpers for projects still using `langchain.hub` imports."""

from __future__ import annotations

import os

from langsmith import Client


def pull(prompt_name: str):
    api_key = (os.getenv("LANGSMITH_API_KEY") or "").strip()
    endpoint = (os.getenv("LANGSMITH_ENDPOINT") or "").strip()
    client = Client(api_url=endpoint or None, api_key=api_key or None)
    return client.pull_prompt(prompt_name)

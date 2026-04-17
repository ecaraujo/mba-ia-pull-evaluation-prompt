from __future__ import annotations

import importlib
import sys
from pathlib import Path


def test_langchain_hub_compat_import(monkeypatch):
    src_path = str(Path(__file__).resolve().parent.parent / "src")
    monkeypatch.syspath_prepend(src_path)

    sys.modules.pop("langchain", None)
    sys.modules.pop("langchain.hub", None)

    langchain = importlib.import_module("langchain")

    assert hasattr(langchain, "hub")
    assert callable(langchain.hub.pull)

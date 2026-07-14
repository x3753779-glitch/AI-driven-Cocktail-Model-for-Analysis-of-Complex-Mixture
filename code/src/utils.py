from __future__ import annotations

import json
import random
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


def set_random_seed(seed: int) -> None:
    random.seed(seed)
    try:
        import numpy as np

        np.random.seed(seed)
    except Exception:
        pass


def read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def now_text() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class RunLogger:
    def __init__(self, log_path: Path):
        self.log_path = log_path
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        self._lines: list[str] = []

    def info(self, message: str) -> None:
        line = f"{now_text()} {message}"
        self._lines.append(line)
        print(message)

    def save(self) -> None:
        self.log_path.write_text("\n".join(self._lines) + "\n", encoding="utf-8")


def load_config(path: Path) -> dict[str, Any]:
    try:
        import yaml

        with path.open("r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except Exception:
        return _load_simple_yaml(path)


def _parse_scalar(value: str) -> Any:
    value = value.strip()
    if value in {"null", "None", ""}:
        return None
    if value == "true":
        return True
    if value == "false":
        return False
    if value.startswith('"') and value.endswith('"'):
        return value[1:-1]
    if value.startswith("'") and value.endswith("'"):
        return value[1:-1]
    try:
        if "." in value:
            return float(value)
        return int(value)
    except ValueError:
        return value


def _load_simple_yaml(path: Path) -> dict[str, Any]:
    root: dict[str, Any] = {}
    stack: list[tuple[int, Any]] = [(-1, root)]
    last_key_at_indent: dict[int, str] = {}

    for raw in path.read_text(encoding="utf-8").splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        text = raw.strip()

        while stack and indent <= stack[-1][0]:
            stack.pop()
        parent = stack[-1][1]

        if text.startswith("- "):
            item = _parse_scalar(text[2:])
            if not isinstance(parent, list):
                key = last_key_at_indent.get(indent - 2)
                container = stack[-1][1]
                if isinstance(container, dict) and key:
                    container[key] = []
                    parent = container[key]
                    stack.append((indent, parent))
                else:
                    raise ValueError(f"Unsupported YAML list at line: {raw}")
            parent.append(item)
            continue

        if ":" not in text:
            raise ValueError(f"Unsupported YAML line: {raw}")
        key, value = text.split(":", 1)
        key = key.strip()
        value = value.strip()
        if value:
            parent[key] = _parse_scalar(value)
        else:
            parent[key] = {}
            stack.append((indent, parent[key]))
        last_key_at_indent[indent] = key

    return root


def package_root() -> Path:
    return Path(__file__).resolve().parents[1]


def python_version() -> str:
    return sys.version.replace("\n", " ")

from __future__ import annotations

import csv
from pathlib import Path

from .checks import check_file_exists


class ModelRunner:
    def __init__(self, root: Path, config: dict):
        self.root = root
        self.config = config

    def run(self) -> dict:
        manifest_path = self.root / self.config["manifest"]
        check_file_exists(manifest_path, "model manifest")
        models = []
        missing = []
        with manifest_path.open("r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            required = {"model_id", "task", "model_file", "metadata_file", "source_file", "framework", "fallback_mode"}
            present = set(reader.fieldnames or [])
            absent = required - present
            if absent:
                raise ValueError(f"Model manifest is missing columns: {', '.join(sorted(absent))}")
            for row in reader:
                model_path = self.root / row["model_file"]
                metadata_path = self.root / row["metadata_file"] if row["metadata_file"] else None
                source_path = self.root / row["source_file"] if row["source_file"] else None
                available = model_path.exists() and model_path.stat().st_size > 0
                metadata_available = metadata_path is None or metadata_path.exists()
                source_available = source_path is None or source_path.exists()
                item = {
                    "model_id": row["model_id"],
                    "task": row["task"],
                    "model_file": row["model_file"],
                    "metadata_file": row["metadata_file"],
                    "source_file": row["source_file"],
                    "framework": row["framework"],
                    "available": available,
                    "metadata_available": metadata_available,
                    "source_available": source_available,
                    "fallback_mode": row["fallback_mode"],
                }
                models.append(item)
                if not available or not metadata_available or not source_available:
                    missing.append(item)

        if missing and not bool(self.config.get("source_required_when_model_missing", True)):
            missing_ids = ", ".join(m["model_id"] for m in missing)
            raise FileNotFoundError(f"Missing required files and fallback mode is disabled: {missing_ids}")

        return {
            "mode": self.config.get("mode", "load_existing_or_rebuild_if_missing"),
            "inference_backend": self.config.get("inference_backend", "tensorflow_keras"),
            "total_models": len(models),
            "available_models": sum(1 for m in models if m["available"] and m["metadata_available"] and m["source_available"]),
            "missing_models": [m["model_id"] for m in missing],
            "models": models,
        }

from __future__ import annotations

import shutil
from pathlib import Path

from .dataset import DatasetArtifact


class FigureGenerator:
    def __init__(self, results_dir: Path):
        self.results_dir = results_dir

    def generate(self, artifacts: list[DatasetArtifact]) -> list[Path]:
        out_dir = self.results_dir / "figures"
        out_dir.mkdir(parents=True, exist_ok=True)
        outputs = []
        for artifact in artifacts:
            if artifact.artifact_type != "figure":
                continue
            name = artifact.figure_id or artifact.file.stem
            target = out_dir / f"{name}.png"
            shutil.copy2(artifact.file, target)
            outputs.append(target)
        return outputs


class TableGenerator:
    def __init__(self, results_dir: Path):
        self.results_dir = results_dir

    def generate(self, artifacts: list[DatasetArtifact]) -> list[Path]:
        out_dir = self.results_dir / "tables"
        out_dir.mkdir(parents=True, exist_ok=True)
        outputs = []
        for artifact in artifacts:
            if artifact.artifact_type not in {"csv_table", "xlsx_table"}:
                continue
            table_id = artifact.table_id or artifact.file.stem
            suffix = artifact.file.suffix
            target = out_dir / f"{table_id}{suffix}"
            shutil.copy2(artifact.file, target)
            outputs.append(target)
        return outputs

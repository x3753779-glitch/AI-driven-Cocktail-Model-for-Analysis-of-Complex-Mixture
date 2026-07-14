from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .checks import load_and_check_manifest


@dataclass(frozen=True)
class DatasetArtifact:
    record_id: str
    file: Path
    label: str
    partition: str
    group: str
    artifact_type: str
    figure_id: str
    table_id: str


class DatasetBuilder:
    def __init__(self, root: Path, manifest_path: Path):
        self.root = root
        self.manifest_path = manifest_path

    def load(self) -> list[DatasetArtifact]:
        rows = load_and_check_manifest(self.manifest_path, self.root)
        artifacts = []
        for row in rows:
            artifacts.append(
                DatasetArtifact(
                    record_id=row["record_id"].strip(),
                    file=self.root / row["file"].strip(),
                    label=row["label"].strip(),
                    partition=row["partition"].strip(),
                    group=row["group"].strip(),
                    artifact_type=row["artifact_type"].strip(),
                    figure_id=row["figure_id"].strip(),
                    table_id=row["table_id"].strip(),
                )
            )
        return artifacts

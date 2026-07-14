from __future__ import annotations

import csv
from pathlib import Path


REQUIRED_MANIFEST_COLUMNS = {
    "record_id",
    "file",
    "label",
    "partition",
    "group",
    "artifact_type",
    "figure_id",
    "table_id",
}
ALLOWED_PARTITIONS = {"1", "2", "3", "4"}
ALLOWED_ARTIFACT_TYPES = {"csv_table", "xlsx_table", "figure", "metrics"}


class ReproductionCheckError(RuntimeError):
    pass


def fail(message: str) -> None:
    raise ReproductionCheckError(message)


def check_file_exists(path: Path, description: str) -> None:
    if not path.exists():
        fail(f"Missing {description}: {path}")
    if path.is_file() and path.stat().st_size == 0:
        fail(f"Empty {description}: {path}")


def check_output_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
    probe = path / ".write_check"
    try:
        probe.write_text("ok", encoding="utf-8")
        probe.unlink()
    except Exception as exc:
        fail(f"Output directory is not writable: {path}. Reason: {exc}")


def load_and_check_manifest(path: Path, root: Path) -> list[dict[str, str]]:
    check_file_exists(path, "manifest")
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        columns = set(reader.fieldnames or [])
        missing = REQUIRED_MANIFEST_COLUMNS - columns
        if missing:
            fail(f"Manifest is missing required columns: {', '.join(sorted(missing))}")
        rows = list(reader)

    if not rows:
        fail("Manifest contains no rows.")

    ids = set()
    for row in rows:
        record_id = row["record_id"].strip()
        if not record_id:
            fail("Manifest contains an empty record_id.")
        if record_id in ids:
            fail(f"Manifest contains duplicated record_id: {record_id}")
        ids.add(record_id)

        partition = row["partition"].strip()
        if partition not in ALLOWED_PARTITIONS:
            fail(f"Invalid partition for {record_id}: {partition}")

        artifact_type = row["artifact_type"].strip()
        if artifact_type not in ALLOWED_ARTIFACT_TYPES:
            fail(f"Invalid artifact_type for {record_id}: {artifact_type}")

        label = row["label"].strip()
        if not label:
            fail(f"Empty label for {record_id}")

        file_path = root / row["file"].strip()
        check_file_exists(file_path, f"manifest file for {record_id}")

    return rows


def check_expected_outputs(results_dir: Path) -> None:
    required = [
        results_dir / "metrics.json",
        results_dir / "run_log.txt",
        results_dir / "tables" / "metrics_summary.csv",
    ]
    for path in required:
        check_file_exists(path, f"output {path.name}")

    figures_dir = results_dir / "figures"
    if not figures_dir.exists() or not any(figures_dir.glob("*.png")):
        fail(f"No PNG figures were generated in {figures_dir}")

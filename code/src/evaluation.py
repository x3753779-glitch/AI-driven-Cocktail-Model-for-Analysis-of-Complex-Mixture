from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

from .dataset import DatasetArtifact
from .utils import read_json, write_json


class Evaluator:
    def __init__(self, results_dir: Path):
        self.results_dir = results_dir

    def collect_metrics(self, artifacts: list[DatasetArtifact]) -> dict[str, Any]:
        metrics: dict[str, Any] = {
            "cocktail": {
                "reported_table": "tables/Table_cocktail_gid_summary.csv",
                "reported_figure": "figures/Figure_cocktail_gid_prediction_barplot.png",
            }
        }

        for artifact in artifacts:
            if artifact.artifact_type != "metrics":
                continue
            raw = read_json(artifact.file)
            cleaned = self._clean_metric_payload(raw)
            if artifact.record_id.startswith("blood_physiology"):
                metrics["blood_physiology_three_components"] = cleaned
            elif artifact.record_id.startswith("blood_drug"):
                metrics["blood_drug_spiking"] = cleaned
            else:
                metrics[artifact.record_id] = cleaned

        write_json(self.results_dir / "metrics.json", metrics)
        self._write_metrics_summary(metrics)
        return metrics

    def _clean_metric_payload(self, payload: dict[str, Any]) -> dict[str, Any]:
        cleaned = dict(payload)
        cleaned.pop("outputs", None)
        return cleaned

    def _write_metrics_summary(self, metrics: dict[str, Any]) -> None:
        table_path = self.results_dir / "tables" / "metrics_summary.csv"
        table_path.parent.mkdir(parents=True, exist_ok=True)
        rows = []
        for task, payload in metrics.items():
            if not isinstance(payload, dict):
                continue
            for key in ["mae", "rmse", "mape"]:
                if key in payload:
                    rows.append({"task": task, "metric": key, "value": payload[key]})
            component_mae = payload.get("component_mae")
            if isinstance(component_mae, dict):
                for component, value in component_mae.items():
                    rows.append({"task": task, "metric": f"component_mae:{component}", "value": value})
            trend = payload.get("first3_trend_report")
            if isinstance(trend, dict):
                matched = all(bool(v.get("matched")) for v in trend.values() if isinstance(v, dict))
                rows.append({"task": task, "metric": "first3_trend_all_matched", "value": matched})

        with table_path.open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["task", "metric", "value"])
            writer.writeheader()
            writer.writerows(rows)

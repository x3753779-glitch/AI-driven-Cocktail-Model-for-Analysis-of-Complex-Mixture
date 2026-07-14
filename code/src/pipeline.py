from __future__ import annotations

import shutil
from pathlib import Path

from .checks import ReproductionCheckError, check_expected_outputs, check_file_exists, check_output_dir
from .dataset import DatasetBuilder
from .evaluation import Evaluator
from .model import ModelRunner
from .plotting import FigureGenerator, TableGenerator
from .preprocessing import Preprocessor
from .utils import RunLogger, load_config, package_root, python_version, set_random_seed


class ReproductionPipeline:
    def __init__(self, config_path: str | Path):
        self.root = package_root()
        self.config_path = (self.root / config_path).resolve() if not Path(config_path).is_absolute() else Path(config_path)
        self.config = load_config(self.config_path)
        self.results_dir = self.root / self.config["output"]["results_dir"]
        self.logger = RunLogger(self.results_dir / "run_log.txt")

    def run_all(self) -> None:
        try:
            self._run_all()
        except ReproductionCheckError:
            self.logger.save()
            raise
        except Exception as exc:
            self.logger.save()
            raise RuntimeError(f"Reproduction failed: {exc}") from exc

    def _run_all(self) -> None:
        self.logger.info("[1/7] Checking configuration and input files...")
        set_random_seed(int(self.config.get("random_seed", 42)))
        check_file_exists(self.config_path, "configuration file")
        check_output_dir(self.results_dir)
        self._prepare_results_dir()

        manifest_path = self.root / self.config["data"]["manifest"]
        artifacts = DatasetBuilder(self.root, manifest_path).load()

        self.logger.info("[2/7] Loading processed manifest...")
        self.logger.info(f"      Loaded {len(artifacts)} manifest entries.")

        self.logger.info("[3/7] Applying declared preprocessing policy...")
        preprocessing_report = Preprocessor(self.config.get("preprocessing", {})).run()

        self.logger.info("[4/7] Resolving model/reported-output mode...")
        model_report = ModelRunner(self.root, self.config.get("model", {})).run()

        self.logger.info("[5/7] Generating figures and tables...")
        figures = FigureGenerator(self.results_dir).generate(artifacts)
        tables = TableGenerator(self.results_dir).generate(artifacts)

        self.logger.info("[6/7] Collecting quantitative metrics...")
        metrics = Evaluator(self.results_dir).collect_metrics(artifacts)

        self.logger.info("[7/7] Writing run summary and validating outputs...")
        self._write_run_summary(figures, tables, preprocessing_report, model_report, metrics)
        self.logger.save()
        check_expected_outputs(self.results_dir)
        self.logger.info("Reproduction completed successfully.")
        self.logger.save()

    def _prepare_results_dir(self) -> None:
        if bool(self.config.get("output", {}).get("overwrite", True)) and self.results_dir.exists():
            for child in self.results_dir.iterdir():
                if child.name == "README.md":
                    continue
                if child.is_dir():
                    shutil.rmtree(child)
                else:
                    child.unlink()
        (self.results_dir / "figures").mkdir(parents=True, exist_ok=True)
        (self.results_dir / "tables").mkdir(parents=True, exist_ok=True)

    def _write_run_summary(
        self,
        figures: list[Path],
        tables: list[Path],
        preprocessing_report: dict,
        model_report: dict,
        metrics: dict,
    ) -> None:
        summary = self.results_dir / "run_summary.txt"
        lines = [
            "Clean reproduction package run summary",
            f"Config: {self.config_path.relative_to(self.root)}",
            f"Python: {python_version()}",
            "",
            "Preprocessing policy:",
            str(preprocessing_report),
            "",
            "Model mode:",
            str(model_report),
            "",
            "Generated figures:",
            *[str(p.relative_to(self.root)) for p in figures],
            "",
            "Generated tables:",
            *[str(p.relative_to(self.root)) for p in tables],
            str((self.results_dir / "tables" / "metrics_summary.csv").relative_to(self.root)),
            "",
            "Metrics groups:",
            *sorted(metrics.keys()),
        ]
        summary.write_text("\n".join(lines) + "\n", encoding="utf-8")

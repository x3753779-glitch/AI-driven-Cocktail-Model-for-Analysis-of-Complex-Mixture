from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.dont_write_bytecode = True

from src.pipeline import ReproductionPipeline


def main() -> int:
    parser = argparse.ArgumentParser(description="Reproduce manuscript figures, tables, and metrics.")
    parser.add_argument("--config", default="config/default.yaml", help="Path to the YAML config file.")
    args = parser.parse_args()

    config_path = Path(args.config)
    pipeline = ReproductionPipeline(config_path)
    pipeline.run_all()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

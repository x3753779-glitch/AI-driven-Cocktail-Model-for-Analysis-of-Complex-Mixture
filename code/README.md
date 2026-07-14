# Reproduction Package

This directory contains the files required to reproduce the manuscript figures, tables, and quantitative outputs.

## Installation

Create a Python environment and install the default dependencies:

```bash
pip install -r requirements.txt
```

Optional extended dependencies:

```bash
pip install -r requirements-optional.txt
```

## Reproduction

Run from this directory:

```bash
python reproduce.py
```

Optional:

```bash
python reproduce.py --config config/default.yaml
```

The command checks the packaged files, loads the standardized manifests, verifies required model artifacts, and writes outputs to `results/`.

## File Layout

```text
config/
data/
models/
results/
src/
```

Main configuration:

```text
config/default.yaml
```

Data registry:

```text
config/dataset_manifest.csv
```

Model registry:

```text
config/model_manifest.csv
```

Generated outputs:

```text
results/
  figures/
  tables/
  metrics.json
  run_log.txt
  run_summary.txt
```

# AI-driven Cocktail Model for Analysis of Complex Mixture

This repository contains the source code, trained model artifacts, example data, processed outputs, and supplementary videos for an AI-driven workflow for analysis of complex liquid mixtures.

The release package is intended to support manuscript review, public reuse, and archival through GitHub Releases and Zenodo. The online demonstration interface is available at:

https://huggingface.co/spaces/SXHIR/liquid-analyzer

## Repository Contents

```text
AI-driven-Cocktail-Model-for-Analysis-of-Complex-Mixture/
├── code/
│   ├── config/                    # Dataset/model manifests and runtime configuration
│   ├── data/                      # Packaged source and processed example data
│   ├── models/                    # Trained model artifacts and model metadata
│   ├── results/                   # Reproduced figures, tables, metrics, and logs
│   ├── src/                       # Reproduction pipeline source code
│   ├── reproduce.py               # Main reproduction entry point
│   ├── requirements.txt           # Required Python dependencies
│   └── requirements-optional.txt  # Optional extended dependencies
├── docs/
│   ├── citation.md                # Human-readable citation notes
│   └── data_availability.md       # Data and artifact availability notes
├── videos/
│   ├── cocktail-model_detection_experiment.mp4
│   ├── cocktail-model_application.mp4
│   └── online_liquid-analysis_interface_workflow.mp4
├── CITATION.cff                   # Citation metadata for GitHub and Zenodo
├── LICENSE                        # Open-source license
└── README.md
```

## Project Overview

The workflow provides a reproducible package for representative complex-mixture analysis tasks. It includes:

- Cocktail-mixture detection and component analysis.
- Cocktail-model application examples for liquid-analysis workflows.
- Blood-mixture related example outputs used in the manuscript-supporting package.
- Packaged trained models and manifests needed to verify the released artifacts.
- Reproducible figures, tables, metrics, and run logs.

The repository is organized as a release-ready research artifact. It is not only a code snapshot: it also includes the model files, example data, processed outputs, and demonstration videos needed to document the version used for manuscript submission.

## Installation

Use Python 3.10 or newer. From the repository root:

```bash
cd code
python -m pip install -r requirements.txt
```

Optional dependencies are listed separately:

```bash
python -m pip install -r requirements-optional.txt
```

On Windows, the package can be run from PowerShell. If using the project author's local Conda environment, the tested Python path is:

```powershell
D:\conda_envs\chatenv\python.exe
```

## Reproduction

Run the reproduction workflow from the `code/` directory:

```bash
python reproduce.py
```

Or provide the configuration file explicitly:

```bash
python reproduce.py --config config/default.yaml
```

The workflow checks packaged files, loads the dataset and model manifests, verifies trained model artifacts, regenerates figures and tables, and writes outputs to:

```text
code/results/
```

The main generated outputs include:

- `code/results/figures/`
- `code/results/tables/`
- `code/results/metrics.json`
- `code/results/run_log.txt`
- `code/results/run_summary.txt`

## Data and Models

The release includes example data and processed outputs under `code/data/`. The trained model artifacts are included under `code/models/`.

The main registries are:

- `code/config/dataset_manifest.csv`
- `code/config/model_manifest.csv`

These manifests define the packaged data artifacts, trained model files, metadata files, and generated outputs used by the reproduction workflow.

## Demonstration Videos

The three supplementary videos are stored in `videos/` and are named by their purpose:

| File | Purpose |
|---|---|
| `videos/cocktail-model_detection_experiment.mp4` | Cocktail-model detection experiment. |
| `videos/cocktail-model_application.mp4` | Cocktail-model application workflow. |
| `videos/online_liquid-analysis_interface_workflow.mp4` | Online liquid-analysis interface workflow using the Hugging Face Space. |

## Online Demonstration

An online demonstration of the liquid-analysis interface is hosted on Hugging Face Spaces:

https://huggingface.co/spaces/SXHIR/liquid-analyzer

The online interface demonstrates the liquid-analysis workflow corresponding to this public release.

## Manuscript Version Information

The planned first formal GitHub Release is:

```text
v1.0.0 – Initial public release
```

This version is intended to identify the source code, data-processing workflow, trained models, example data, supplementary videos, and online interface associated with the manuscript-related release package. The software release author is Xiaohe Shang. After creating the GitHub Release, archive it with Zenodo and use the Zenodo DOI for manuscript citation.

## Citation

If you use this repository, cite the archived release and the associated manuscript.

Before publication, cite the software release using the metadata in `CITATION.cff`. The software, GitHub repository, Hugging Face site, code, trained models, data-processing workflow, and demonstrations should be cited under `Shang, X.`. After Zenodo archival, update the citation with the Zenodo DOI. After manuscript publication, also cite the final paper separately.

Suggested pre-DOI citation:

```text
Shang, X. AI-driven Cocktail Model for Analysis of Complex Mixture. Version v1.0.0. GitHub repository. https://github.com/x3753779-glitch/AI-driven-Cocktail-Model-for-Analysis-of-Complex-Mixture
```

## License

This repository is released under the MIT License. See `LICENSE`.

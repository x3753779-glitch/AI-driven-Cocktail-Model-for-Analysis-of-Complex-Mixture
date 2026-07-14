# AI-driven Cocktail Model for Analysis of Complex Mixture

This repository provides the code, processed data, packaged model artifacts, reproduction outputs, and supplementary demonstration videos for an AI-driven analytical framework for complex liquid mixtures.

The package supports reproduction of the reported figures, tables, and quantitative metrics for cocktail-mixture and blood-mixture analysis. An online demonstration interface is also available at:

https://huggingface.co/spaces/SXHIR/liquid-analyzer

## Contents

1. [Introduction](#introduction)
2. [Repository structure](#repository-structure)
3. [Code package](#code-package)
4. [Data and model artifacts](#data-and-model-artifacts)
5. [Supplementary videos](#supplementary-videos)
6. [Online demonstration](#online-demonstration)
7. [Reproduction](#reproduction)
8. [Data availability](#data-availability)
9. [Citation](#citation)

## Introduction

Complex liquid-mixture analysis requires quantitative interpretation of overlapping spectral or sensor-derived signatures. This repository accompanies an AI-driven workflow designed to identify and quantify components in representative cocktail and blood-mixture settings. The included reproduction package contains standardized inputs, trained model artifacts, processed outputs, and scripts for generating the main reported figures and tables.

The organization of this repository follows a paper-supporting layout: the code package is separated from supplementary videos, processed artifacts are kept with the reproduction workflow, and the online demonstration is linked as an external interface.

## Repository structure

```text
AI-driven Cocktail Model for Analysis of Complex Mixture/
├── code/
│   ├── config/
│   ├── data/
│   ├── models/
│   ├── results/
│   ├── src/
│   ├── reproduce.py
│   ├── requirements.txt
│   └── requirements-optional.txt
├── videos/
│   ├── Supplementary_Movie_S1_cocktail_demo.mp4
│   ├── Supplementary_Movie_S2_blood_demo.mp4
│   └── Supplementary_Movie_S3_online_website_demo.mp4
├── docs/
│   ├── data_availability.md
│   └── citation.md
└── README.md
```

## Code package

The `code/` directory contains the complete reproduction package. It includes the configuration files, processed inputs, model registry, packaged model artifacts, generated figures and tables, and the one-command reproduction entry point.

Main entry point:

```text
code/reproduce.py
```

Main configuration:

```text
code/config/default.yaml
```

## Data and model artifacts

The packaged artifacts are organized inside `code/data/` and `code/models/`. They are included to support direct reproduction of the reported outputs without requiring access to external raw acquisition files.

Generated outputs are stored in:

```text
code/results/
```

The results directory includes reproduced figures, tables, metrics, and run logs.

## Supplementary videos

The supplementary videos are provided in `videos/`:

| File | Description |
|---|---|
| `Supplementary_Movie_S1_cocktail_demo.mp4` | Cocktail-mixture demonstration video |
| `Supplementary_Movie_S2_blood_demo.mp4` | Blood-mixture demonstration video |
| `Supplementary_Movie_S3_online_website_demo.mp4` | Online website demonstration video |

## Online demonstration

The web demonstration is hosted on Hugging Face Spaces:

https://huggingface.co/spaces/SXHIR/liquid-analyzer

This interface provides an online demonstration of the liquid-mixture analyzer corresponding to the workflow released in this repository.

## Reproduction

From the repository root, install the required dependencies and run:

```bash
cd code
pip install -r requirements.txt
python reproduce.py
```

Optional extended dependencies are listed in:

```bash
pip install -r requirements-optional.txt
```

The reproduction command checks packaged files, loads the standardized manifests, verifies model artifacts, regenerates figures and tables, and writes the results to `code/results/`.

## Data availability

The data supporting the findings of this study are available in the paper and in this repository. The reproduction package includes processed data, trained model artifacts, generated outputs, and supplementary demonstration videos required to reproduce the released results.

The online demonstration is available at:

https://huggingface.co/spaces/SXHIR/liquid-analyzer

## Citation

If you use this repository, please cite the associated paper. A placeholder citation note is provided in `docs/citation.md` and can be updated after the final bibliographic information is available.


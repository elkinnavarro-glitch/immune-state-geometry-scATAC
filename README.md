# Geometric Constraints and Vulnerability in Single-Cell ATAC-seq Immune States

Reproducible analysis pipeline for studying informational geometry, topological persistence, and vulnerability in immune state organization using single-cell ATAC-seq data.

## Overview

This repository contains the complete computational pipeline for analyzing immune system geometry and critical transitions using:

- **Information Bottleneck** implementation for state-space dimensionality reduction
- **Topological Data Analysis** (TDA) with persistence diagrams and barcodes
- **Vulnerability Simulations** for robustness assessment across perturbations

## Data Availability

The single-cell ATAC-seq data used in this study is available under GEO accession **GSE194122**.

Processed data tables supporting the findings of this study, including the reduced informational coordinates, topological persistence summaries, and vulnerability metrics, are available in the Supplementary Information and at the Zenodo repository:

- **GEO**: [GSE194122](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE194122)
- **Zenodo**: [10.5281/zenodo.XXXXXX](https://zenodo.org/record/XXXXXX) *(pending)*

### Processed Data Files

<!-- TABLES_AUTO -->

*Processed data files are located in the `data/processed/` directory and will be automatically catalogued when running the generation script.*

## Code Availability

All custom Python scripts used for the analysis are available in this repository:

### Repository Structure

```
immune-state-geometry-scATAC/
├── README.md                           # This file
├── LICENSE                             # MIT License
├── environment.yml                     # Conda environment specification
├── requirements.txt                    # Python dependencies
├── Makefile                            # Automation targets
│
├── src/                                # Python source code
│   ├── info_bottleneck/               # Information Bottleneck implementation
│   │   ├── __init__.py
│   │   ├── reduction.py               # IB-based dimensionality reduction
│   │   ├── metrics.py                 # Information-theoretic metrics
│   │   └── utils.py
│   │
│   ├── tda_pipeline/                  # Topological Data Analysis
│   │   ├── __init__.py
│   │   ├── persistence.py             # Persistent homology computation
│   │   ├── barcodes.py                # Barcode extraction and visualization
│   │   └── summaries.py               # TDA summary statistics
│   │
│   ├── vulnerability/                 # Vulnerability simulations
│   │   ├── __init__.py
│   │   ├── simulations.py             # Perturbation and robustness tests
│   │   ├── metrics.py                 # Vulnerability indices
│   │   └── recovery.py                # Recovery analysis
│   │
│   └── utils/                         # General utilities
│       ├── __init__.py
│       ├── io.py                      # Data loading and saving
│       ├── visualization.py           # Plotting functions
│       └── validation.py              # Data validation
│
├── notebooks/                          # Jupyter notebooks for each figure
│   ├── 01_data_loading.ipynb
│   ├── 02_info_architecture.ipynb     # Generates Fig. 1
│   ├── 03_state_separation.ipynb      # Generates Fig. 2
│   ├── 04_vulnerability_curves.ipynb  # Generates Fig. 3
│   ├── 05_vulnerability_summary.ipynb # Generates Fig. 4
│   └── ED_extended_data.ipynb         # Extended Data figures
│
├── data/                               # Data directory structure
│   ├── raw/                           # Raw input data (not included, see GEO)
│   │   └── .gitkeep
│   │
│   └── processed/                     # Processed data files
│       ├── Fig1_InfoArchitecture.tsv
│       ├── Fig2_Separation.tsv
│       ├── Fig3_VulnerabilityCurves.tsv
│       ├── Fig4_VulnerabilitySummary.tsv
│       └── ED2_TDA_summaries.tsv
│
├── results/                            # Analysis outputs
│   ├── figures/                       # Final figure PDFs
│   │   ├── Fig1_InfoArchitecture.pdf
│   │   ├── Fig2_Separation.pdf
│   │   ├── Fig3_VulnerabilityCurves.pdf
│   │   ├── Fig4_VulnerabilitySummary.pdf
│   │   └── ED_*.pdf
│   │
│   └── tables/                        # Supplementary tables
│       └── *.tsv
│
├── metadata/                           # Pipeline metadata
│   ├── audit_log.tsv                  # Complete audit trail
│   ├── data_hashes.tsv                # Input data integrity checksums
│   └── git_versions.txt               # Software versions at execution
│
├── scripts/                            # Standalone executable scripts
│   ├── generate_data_code_section.py # Auto-generate Data & Code Availability
│   ├── run_full_pipeline.py          # End-to-end analysis
│   └── validate_reproducibility.py   # Reproducibility checks
│
└── .gitignore
```

### Key Analysis Scripts

- `src/info_bottleneck/`: Information Bottleneck implementation for state-space reduction
- `src/tda_pipeline/`: Topological Data Analysis (persistence diagrams, barcodes, summaries)
- `src/vulnerability/`: Vulnerability and perturbation simulations over the reduced manifold
- `notebooks/`: End-to-end analysis notebooks corresponding to main and supplementary figures

## Reproducibility

### Quick Start

1. **Clone the repository**:
   ```bash
   git clone https://github.com/elkinnavarro-glitch/immune-state-geometry-scATAC.git
   cd immune-state-geometry-scATAC
   ```

2. **Create the conda environment**:
   ```bash
   conda env create -f environment.yml
   conda activate immune-geometry
   ```

3. **Download raw data** (from GEO):
   ```bash
   # Download GSE194122 data to data/raw/
   ```

4. **Download processed data** (from Zenodo, optional):
   ```bash
   # Or download supplementary tables from Zenodo to data/processed/
   ```

5. **Run the full pipeline**:
   ```bash
   python scripts/run_full_pipeline.py
   ```

   Or run individual notebooks:
   ```bash
   jupyter notebook notebooks/02_info_architecture.ipynb
   ```

6. **Generate Data & Code Availability section**:
   ```bash
   python scripts/generate_data_code_section.py
   ```

### Reproducibility Audit

A complete audit log of the computational pipeline (`metadata/audit_log.tsv`), mapping each figure to its generating script and input data hash, is provided in the repository metadata to ensure full reproducibility.

**Audit log columns**:
- `figure_id`: Figure identifier (e.g., Fig1, Fig2, ED2)
- `script_path`: Path to generating script
- `input_hash`: SHA256 of input data
- `output_hash`: SHA256 of output data
- `execution_date`: Timestamp of execution
- `python_version`: Python version used
- `dependencies`: Version pins of key packages

## Citation

If you use this code or data in your research, please cite:

```bibtex
@article{Navarro2024,
  title={Geometric constraints and vulnerability in immune state organization},
  author={Navarro, E. and others},
  journal={PNAS},
  year={2024}
}
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

**Elkin Navarro Quiroz**
- Email: elkin.navarro@unisimonbolivar.edu.co
- GitHub: [@elkinnavarro-glitch](https://github.com/elkinnavarro-glitch)
- Institution: Centro de Investigaciones en Ciencias de la Vida, Universidad Simón Bolívar, Barranquilla, Colombia

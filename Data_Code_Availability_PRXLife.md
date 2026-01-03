# Data & Code Availability

## Data Availability

The single-cell ATAC-seq data used in this study is available under GEO accession **GSE194122**.

Processed data tables supporting the findings of this study, including the reduced informational coordinates, topological persistence summaries, and vulnerability metrics, are available in the Supplementary Information and at the Zenodo repository linked below.

### Processed Data Tables

<!-- TABLES_AUTO -->

### Supplementary Files

**Data Repository**: https://zenodo.org/XXXXXX (DOI: 10.5281/zenodo.XXXXXX)

## Code Availability

All custom Python scripts used for the analysis, including the Information Bottleneck implementation, Topological Data Analysis pipeline, and Vulnerability simulations, are available at:

- **Repository**: https://github.com/elkinnavarro-glitch/immune-state-geometry-scATAC
- **DOI**: 10.5281/zenodo.XXXXXX

### Analysis Scripts

<!-- SCRIPTS_AUTO -->

### Figure Generation

Final figure PDFs used in the manuscript:

<!-- FIGS_AUTO -->

## Reproducibility and Audit Trail

A complete audit log of the computational pipeline (`metadata/audit_log.tsv`), mapping each figure to its generating script and input data hash, is provided in the repository metadata to ensure full reproducibility.

To reproduce all analyses:

1. Clone the repository: `git clone https://github.com/elkinnavarro-glitch/immune-state-geometry-scATAC.git`
2. Download raw data from GEO (GSE194122)
3. Download processed data from Zenodo (10.5281/zenodo.XXXXXX)
4. Install dependencies: `pip install -r requirements.txt`
5. Run analysis pipeline: `python scripts/run_analysis.py`

---

**Generated**: <!-- TIMESTAMP --> by automated Data & Code Availability generator

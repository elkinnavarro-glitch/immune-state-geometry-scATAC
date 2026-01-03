# Reproducibility Guide

## Overview

This repository contains a fully reproducible analysis pipeline with automated metadata generation. The **Data & Code Availability** section is generated automatically whenever data files or scripts are updated.

## Automated Generation

### How It Works

The repository includes:

1. **Python Script** (`scripts/generate_data_code_section.py`)
   - Scans repository for processed data files (`.tsv`)
   - Collects figure PDFs (matching `Fig*.pdf` pattern)
   - Discovers Python analysis scripts
   - Generates comprehensive markdown document

2. **GitHub Actions Workflow** (`.github/workflows/generate_data_availability.yml`)
   - Automatically triggers on push when data or script files change
   - Generates `Data_Code_Availability_PRXLife_auto.md` on main branch
   - Commits changes automatically with proper attribution

3. **Template File** (`Data_Code_Availability_PRXLife.md`)
   - Contains placeholders for auto-generated content
   - Includes sections for:
     - Processed data tables (with descriptions)
     - Analysis scripts
     - Generated figure PDFs
     - Metadata audit log reference

### Audit Trail

Every analysis is tracked in `metadata/audit_log.tsv`:

| Column | Purpose |
|--------|----------|
| `figure_id` | Figure or extended data identifier |
| `script_path` | Script that generated the output |
| `input_hash` | Hash of input data (reproducibility verification) |
| `output_hash` | Hash of output (integrity verification) |
| `execution_date` | When analysis was run |
| `python_version` | Python version used |
| `dependencies` | Analysis dependencies list |

## Running Manually

To generate the data availability section manually:

```bash
python scripts/generate_data_code_section.py
```

This generates `Data_Code_Availability_PRXLife_auto.md` with current repository state.

## File Structure

```
.
├── Data_Code_Availability_PRXLife.md          # Template (with placeholders)
├── Data_Code_Availability_PRXLife_auto.md     # Auto-generated (DO NOT EDIT)
├── REPRODUCIBILITY.md                         # This file
├── scripts/
│   └── generate_data_code_section.py         # Generator script
├── metadata/
│   └── audit_log.tsv                         # Audit trail
└── .github/workflows/
    └── generate_data_availability.yml        # GitHub Actions trigger
```

## Adding New Data or Figures

1. **Add processed data file** (e.g., `results/Fig5_NewAnalysis.tsv`)
   - Automatic detection: ✓
   - Push trigger: ✓
   - Auto-generation: ✓

2. **Add figure PDF** (e.g., `results/Fig5_newanalysis.pdf`)
   - Automatic detection: ✓
   - Push trigger: ✓
   - Auto-generation: ✓

3. **Update audit log** (`metadata/audit_log.tsv`)
   - New row: `Fig5 | scripts/analyze_fig5.py | [hash] | [hash] | [date] | [version] | [deps]`

The workflow will automatically detect changes and regenerate the documentation.

## Customization

### Modify File Descriptions

Edit the `describe_table()` function in `scripts/generate_data_code_section.py`:

```python
def describe_table(f: pathlib.Path) -> str:
    name = f.name
    descriptions = {
        "Fig5_NewAnalysis": "Custom description for Fig5.",
        # Add more...
    }
    # ...
```

### Adjust Workflow Triggers

Edit `.github/workflows/generate_data_availability.yml` to change when generation runs:

```yaml
on:
  push:
    branches:
      - main
    paths:
      - '**.tsv'      # Trigger on TSV files
      - '**.pdf'      # Trigger on PDF files
```

## Verification

### Check Workflow Runs

1. Go to **Actions** tab
2. Click **Generate Data & Code Availability Section**
3. View logs for each run

### Manual Testing

```bash
# Generate locally
python scripts/generate_data_code_section.py

# Check output
cat Data_Code_Availability_PRXLife_auto.md

# Compare with template
diff Data_Code_Availability_PRXLife.md Data_Code_Availability_PRXLife_auto.md
```

## Integration with Zenodo

When preparing for Zenodo deposition:

1. Update `.zenodo.json` with repository info
2. Ensure `Data_Code_Availability_PRXLife_auto.md` is current
3. Include in manuscript supplementary materials
4. Reference Zenodo DOI in automated comments

## FAQ

**Q: Can I edit `Data_Code_Availability_PRXLife_auto.md` manually?**
A: No. It's auto-generated. Edit `Data_Code_Availability_PRXLife.md` template instead.

**Q: Why didn't the workflow trigger?**
A: Check that your push included `.tsv`, `.pdf`, or script file changes.

**Q: How do I add custom metadata?**
A: Modify the template or extend the Python script with custom logic.

**Q: What if generation fails?**
A: Check the GitHub Actions logs for error messages. Common issues:
- Missing Python dependencies
- File path errors
- Invalid markdown syntax in descriptions

## Support

For issues or questions, open a GitHub issue with the `reproducibility` label.

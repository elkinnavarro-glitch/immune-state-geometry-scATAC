#!/usr/bin/env python3
"""
Automatic Data & Code Availability section generator.

This script scans the repository structure for processed data tables and figure PDFs,
and automatically generates a formatted Data & Code Availability section to be
included in the README or manuscript supplementary information.

Usage:
    python scripts/generate_data_code_section.py

Output:
    - Prints markdown-formatted Data & Code Availability section
    - Optionally updates README.md if template markers are present
"""

import pathlib
import sys
from datetime import datetime
from typing import List, Tuple


def get_tsv_files(root: pathlib.Path, search_pattern="*.tsv") -> List[pathlib.Path]:
    """Recursively find TSV files in the repository."""
    return sorted(root.rglob(search_pattern))


def get_pdf_figures(root: pathlib.Path) -> List[pathlib.Path]:
    """Find PDF figure files (matching Fig*.pdf pattern)."""
    figures = sorted(root.rglob("Fig*.pdf"))
    return figures


def describe_table(filepath: pathlib.Path) -> str:
    """Generate description for a data table based on filename."""
    name = filepath.name
    descriptions = {
        "Fig1_InfoArchitecture": "Reduced informational coordinates and cluster assignments (Fig. 1).",
        "Fig2_Separation": "State separation metrics and pairwise distances (Fig. 2).",
        "Fig3_VulnerabilityCurves": "Vulnerability curves across perturbation fractions (Fig. 3).",
        "Fig4_VulnerabilitySummary": "Summary vulnerability metrics by state and donor (Fig. 4).",
        "ED2_TDA": "Topological Data Analysis persistence summaries (Extended Data 2).",
        "ED_Supplementary": "Additional supplementary data tables.",
    }
    
    for key, desc in descriptions.items():
        if key in name:
            return desc
    
    return "Processed analysis table."


def generate_tables_section(root: pathlib.Path) -> str:
    """Generate markdown section for processed data tables."""
    tsv_files = get_tsv_files(root)
    
    if not tsv_files:
        return "*No processed data files found. Tables will be added as analysis progresses.*"
    
    lines = []
    for filepath in tsv_files:
        # Skip metadata files
        if filepath.parent.name == "metadata":
            continue
        
        rel_path = filepath.relative_to(root)
        desc = describe_table(filepath)
        lines.append(f"- `{rel_path}` – {desc}")
    
    return "\n".join(lines) if lines else "*No processed data files found.*"


def generate_figures_section(root: pathlib.Path) -> str:
    """Generate markdown section for final figures."""
    pdf_files = get_pdf_figures(root)
    
    if not pdf_files:
        return "*Figure PDFs will be added upon completion of analysis.*"
    
    lines = []
    for filepath in pdf_files:
        rel_path = filepath.relative_to(root)
        lines.append(f"- `{rel_path}`")
    
    return "\n".join(lines) if lines else "*No figure PDFs found.*"


def update_readme(root: pathlib.Path, tables_block: str, figs_block: str) -> None:
    """Update README.md if it contains template markers."""
    readme_path = root / "README.md"
    
    if not readme_path.exists():
        print(f"Warning: README.md not found at {readme_path}", file=sys.stderr)
        return
    
    text = readme_path.read_text(encoding="utf-8")
    
    # Check for template markers
    if "<!-- TABLES_AUTO -->" in text:
        text = text.replace("<!-- TABLES_AUTO -->", tables_block)
        print(f"✓ Updated processed data tables section")
    
    if "<!-- FIGS_AUTO -->" in text:
        text = text.replace("<!-- FIGS_AUTO -->", figs_block)
        print(f"✓ Updated figures section")
    
    # Write updated content
    readme_path.write_text(text, encoding="utf-8")
    print(f"✓ README.md updated successfully")


def main():
    """Main execution function."""
    # Determine repository root
    root = pathlib.Path(__file__).parent.parent.resolve()
    
    print(f"Repository root: {root}")
    print(f"Scanning for data files and figures...\n")
    
    # Generate sections
    tables_block = generate_tables_section(root)
    figs_block = generate_figures_section(root)
    
    # Display generated sections
    print("=" * 70)
    print("PROCESSED DATA FILES")
    print("=" * 70)
    print(tables_block)
    print()
    print("=" * 70)
    print("FIGURE PDFs")
    print("=" * 70)
    print(figs_block)
    print()
    
    # Attempt to update README
    print("=" * 70)
    print("UPDATING README.md")
    print("=" * 70)
    update_readme(root, tables_block, figs_block)
    
    print(f"\nGeneration completed at {datetime.now().isoformat()}")


if __name__ == "__main__":
    main()

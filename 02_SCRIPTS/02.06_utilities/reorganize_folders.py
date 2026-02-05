"""
Reorganize project folders to follow naming conventions
Moves files from old structure to new numbered structure

Author: WSD3 / Claude Code
Date: 2026-01-13
Version: 1.0.0
"""

import shutil
from pathlib import Path
from datetime import datetime

# Base project path
PROJECT_ROOT = Path(r"G:\My Drive\LLM\project_manifest")

def stamp(msg):
    """Print timestamped message"""
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

def create_new_structure():
    """Create new folder structure"""

    stamp("=== Creating New Folder Structure ===")

    folders = [
        # STAGE 00: Raw data
        "00_STAGE00_RAW_DATA/00.01_panjiva_imports_raw",
        "00_STAGE00_RAW_DATA/00.02_panjiva_exports_raw",
        "00_STAGE00_RAW_DATA/00.05_master_archive",

        # STAGE 01: Preprocessing output
        "00_DATA/00.02_PREPROCESSED/01.01_annual_files",
        "00_DATA/00.02_PREPROCESSED/01.02_validation_reports",

        # STAGE 02: Classification
        "00_DATA/00.03_MATCHED/02.01_phase01_filters",
        "00_DATA/00.03_MATCHED/02.02_phase02_carriers",
        "00_DATA/00.03_MATCHED/02.03_phase04_hs2",
        "00_DATA/00.03_MATCHED/02.04_phase05_hs4",
        "00_DATA/00.03_MATCHED/02.05_phase06_hs6",
        "00_DATA/00.03_MATCHED/02.06_phase07_keywords",
        "00_DATA/00.03_MATCHED/02.07_phase08_combinatorial",
        "00_DATA/00.03_MATCHED/02.08_phase09_refinements",
        "00_DATA/00.03_MATCHED/02.09_phase10_highvalue",
        "00_DATA/00.03_MATCHED/02.10_final_output",

        # Dictionaries
        "01_DICTIONARIES/03.01_cargo_classification",
        "01_DICTIONARIES/03.02_hs_codes",
        "01_DICTIONARIES/03.03_ports",
        "01_DICTIONARIES/03.04_ships",

        # Scripts (already created)
        "04_SCRIPTS/utilities",

        # Documentation
        "05_DOCUMENTATION/05.01_pipeline_docs",
        "05_DOCUMENTATION/05.02_dashboards",
        "05_DOCUMENTATION/05.03_phase_summaries",
        "05_DOCUMENTATION/05.04_logs",

        # Checkpoints
        "06_CHECKPOINTS",

        # Archive (keep old structure here)
        "_ARCHIVE"
    ]

    for folder in folders:
        path = PROJECT_ROOT / folder
        path.mkdir(parents=True, exist_ok=True)
        stamp(f"Created: {folder}")

def reorganize_files():
    """Move files from old structure to new structure"""

    stamp("\n=== Reorganizing Files ===")

    # File moves (old_path → new_path)
    moves = [
        # Raw data
        ("00_raw_data/00_01_panjiva_imports_raw", "00_STAGE00_RAW_DATA/00.01_panjiva_imports_raw"),
        ("00_raw_data/00_05_all_raw_archive", "00_STAGE00_RAW_DATA/00.05_master_archive"),

        # Preprocessing outputs
        ("00_DATA/00.02_PREPROCESSED", "00_DATA/00.02_PREPROCESSED/01.01_annual_files"),

        # Classification outputs
        ("_archive/2026-01-16_pre_reorganization/03_DOCUMENTATION/03.04_summaries/classification_full_2023", "00_DATA/00.03_MATCHED/02.10_final_output/2023"),
        ("_archive/2026-01-16_pre_reorganization/03_DOCUMENTATION/03.04_summaries/classification_full_2024", "00_DATA/00.03_MATCHED/02.10_final_output/2024"),
        ("_archive/2026-01-16_pre_reorganization/03_DOCUMENTATION/03.04_summaries/classification_full_2025", "00_DATA/00.03_MATCHED/02.10_final_output/2025"),

        # Dictionaries (already moved cargo dict, now move others)
        ("01.01_dictionary", "01_DICTIONARIES"),

        # Documentation
        ("03_DOCUMENTATION/03.04_summaries", "05_DOCUMENTATION/05.01_pipeline_docs"),

        # Archive old structure
        ("user_notes", "_ARCHIVE/user_notes"),
        ("_archive", "_ARCHIVE/old_archive")
    ]

    for old_rel, new_rel in moves:
        old_path = PROJECT_ROOT / old_rel
        new_path = PROJECT_ROOT / new_rel

        if old_path.exists():
            stamp(f"\nMoving: {old_rel} → {new_rel}")

            # If destination exists, merge folders
            if new_path.exists() and old_path.is_dir():
                stamp(f"  Merging with existing folder...")
                for item in old_path.rglob('*'):
                    if item.is_file():
                        rel_path = item.relative_to(old_path)
                        dest = new_path / rel_path
                        dest.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(item, dest)
                        stamp(f"  Copied: {rel_path}")
            else:
                # Simple move
                new_path.parent.mkdir(parents=True, exist_ok=True)
                if new_path.exists():
                    stamp(f"  Destination exists, skipping: {new_path}")
                else:
                    shutil.move(str(old_path), str(new_path))
                    stamp(f"  Moved successfully")
        else:
            stamp(f"Source not found (skipping): {old_rel}")

def create_readme_files():
    """Create README files in key folders"""

    stamp("\n=== Creating README Files ===")

    readmes = {
        "00_STAGE00_RAW_DATA/README.md": """# Stage 00: Raw Data

This folder contains all raw data files before any processing.

## Subfolders

- `00.01_panjiva_imports_raw/` - Original ZIP and CSV files from Panjiva (170 files)
- `00.02_panjiva_exports_raw/` - Export data (future)
- `00.05_master_archive/` - Consolidated master files after preprocessing
""",

        "00_DATA/00.02_PREPROCESSED/README.md": """# Stage 01: Preprocessing Outputs

This folder contains the output of Stage 00 preprocessing pipeline.

## Subfolders

- `01.01_annual_files/` - Year-split files (2023, 2024, 2025)
- `01.02_validation_reports/` - Data quality validation results
""",

        "00_DATA/00.03_MATCHED/README.md": """# Stage 02: Classification Pipeline

This folder contains classification outputs for all phases.

## Subfolders

- `02.01-02.09/` - Phase-specific intermediate outputs (checkpoints)
- `02.10_final_output/` - Final classified files by year

## Phases

1. Phase 01: Filters (SHIP_SPARES, FROB)
2. Phase 02-03: Carrier locks
3. Phase 04: HS2 matching
4. Phase 05: HS4 matching
5. Phase 06: HS6 matching
6. Phase 07: Keyword matching
7. Phase 08: Combinatorial rules
8. Phase 09: Refinements
9. Phase 10: High-value specific grades
""",

        "01_DICTIONARIES/README.md": """# Reference Dictionaries

All reference data used across the pipeline.

## Subfolders

- `03.01_cargo_classification/` - Main classification dictionary (v2.0.0)
- `03.02_hs_codes/` - HS code hierarchy and lookups
- `03.03_ports/` - US port dictionary, ACE codes
- `03.04_ships/` - Ship registry, carrier SCAC codes
""",

        "06_CHECKPOINTS/README.md": """# Pipeline Checkpoints

Parquet checkpoint files for resume capability.

Checkpoints are created after each major stage to allow resuming if processing is interrupted.

## Naming Pattern

`{stage_name}_checkpoint_{phase}_{YYYYMMDD_HHMM}.parquet`
"""
    }

    for rel_path, content in readmes.items():
        path = PROJECT_ROOT / rel_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        stamp(f"Created: {rel_path}")

def main():
    """Main reorganization function"""

    stamp("="*60)
    stamp("PROJECT FOLDER REORGANIZATION")
    stamp("="*60)

    # Step 1: Create new structure
    create_new_structure()

    # Step 2: Create README files
    create_readme_files()

    # Step 3: Reorganize files
    stamp("\nWARNING: File reorganization disabled for safety")
    stamp("Please review the new folder structure first")
    stamp("Then manually run: reorganize_files()")

    # Uncomment to actually move files:
    # reorganize_files()

    stamp("\n=== Reorganization Plan Complete ===")
    stamp("Review the new structure, then enable file moves if desired")

if __name__ == "__main__":
    main()

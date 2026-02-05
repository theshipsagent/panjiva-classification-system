"""
Update path references in all production scripts to use new folder structure.
"""

import os
import re
from pathlib import Path

# Define base path
BASE = Path(r"G:\My Drive\LLM\project_manifest")
SCRIPTS_DIR = BASE / "02_SCRIPTS"

# Define path mappings (old -> new)
PATH_MAPPINGS = [
    # Data paths
    (r'01_step_one/01_01_panjiva_imports_step_one', r'00_DATA/00.02_PREPROCESSED'),
    (r'01_step_one/01_02_panjiva_exports_step_one', r'00_DATA/00.02_PREPROCESSED'),
    (r'01_step_one', r'00_DATA/00.02_PREPROCESSED'),
    (r'01_STAGE01_PREPROCESSING/01\.01_annual_files', r'00_DATA/00.02_PREPROCESSED'),
    (r'01_STAGE01_PREPROCESSING', r'00_DATA/00.02_PREPROCESSED'),

    # Classification outputs
    (r'02_STAGE02_CLASSIFICATION/usace_2023_portcall_master', r'00_DATA/00.04_FINAL/usace_2023_portcall_master'),
    (r'02_STAGE02_CLASSIFICATION', r'00_DATA/00.03_MATCHED'),

    # Documentation
    (r'build_documentation/classification_full', r'_archive/2026-01-16_pre_reorganization/build_documentation/classification_full'),
    (r'build_documentation', r'03_DOCUMENTATION/03.04_summaries'),

    # Dictionaries
    (r'01\.01_dictionary', r'01_DICTIONARIES/01.03_vessels'),  # for ships_register
    (r'03_DICTIONARIES/03\.01_cargo_classification', r'01_DICTIONARIES/01.01_cargo_classification'),
    (r'03_DICTIONARIES/03\.05_us_flag_inventory', r'01_DICTIONARIES/01.03_vessels/us_flag_inventory'),
    (r'03_DICTIONARIES', r'01_DICTIONARIES'),

    # Special cases for ship registry
    (r'01_DICTIONARIES/01\.03_vessels/01_ships_register\.csv', r'01_DICTIONARIES/01.03_vessels/01_ships_register.csv'),
]

def update_file(file_path):
    """Update path references in a single file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content
        changes = []

        # Apply each path mapping
        for old_pattern, new_pattern in PATH_MAPPINGS:
            # Escape backslashes for regex
            old_regex = old_pattern.replace('\\', '\\\\')

            # Count matches before replacement
            matches = len(re.findall(old_regex, content))
            if matches > 0:
                # Replace
                content = re.sub(old_regex, new_pattern, content)
                changes.append(f"  {old_pattern} -> {new_pattern} ({matches} replacements)")

        # Write back if changes were made
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

            print(f"\nUpdated: {file_path.relative_to(SCRIPTS_DIR)}")
            for change in changes:
                print(change)

            return True

        return False

    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    print("Scanning scripts for old path references...\n")

    updated_count = 0
    total_count = 0

    # Walk through all Python files in 02_SCRIPTS
    for root, dirs, files in os.walk(SCRIPTS_DIR):
        for file in files:
            if file.endswith('.py'):
                total_count += 1
                file_path = Path(root) / file

                if update_file(file_path):
                    updated_count += 1

    print(f"\n=== Summary ===")
    print(f"Total scripts scanned: {total_count}")
    print(f"Scripts updated: {updated_count}")
    print(f"Scripts unchanged: {total_count - updated_count}")

if __name__ == "__main__":
    main()

"""
Create randomized 15K record samples from each preprocessed source for pipeline testing.
"""

import pandas as pd
from pathlib import Path
import numpy as np

# Define paths
BASE = Path(r"G:\My Drive\LLM\project_manifest")
PREPROCESSED = BASE / "00_DATA" / "00.02_PREPROCESSED"
TEST_DIR = BASE / "04_DEVELOPMENT" / "04.02_tests" / "test_samples_15k"

# Create test directory
TEST_DIR.mkdir(exist_ok=True)

print("Creating 15K randomized test samples...\n")

# Define source files
sources = {
    "panjiva_imports_2023": PREPROCESSED / "panjiva_imports_2023_AUTHORITATIVE_v1.0.0.csv",
    "panjiva_exports_2023": PREPROCESSED / "panjiva_exports_2023_AUTHORITATIVE_v1.0.0.csv",
    "usace_entrance_2023": PREPROCESSED / "usace_2023_entrance_AUTHORITATIVE_v1.0.0.csv",
    "usace_clearance_2023": PREPROCESSED / "usace_2023_clearance_AUTHORITATIVE_v1.0.0.csv"
}

# Sample each source
for name, source_path in sources.items():
    print(f"Processing {name}...")
    print(f"  Source: {source_path}")

    if not source_path.exists():
        print(f"  ERROR: File not found!")
        continue

    # Read file
    try:
        print(f"  Reading file...")
        df = pd.read_csv(source_path, low_memory=False)
        total_records = len(df)
        print(f"  Total records: {total_records:,}")

        # Sample 15K records (or all if less than 15K)
        sample_size = min(15000, total_records)
        print(f"  Sampling {sample_size:,} records...")

        # Set random seed for reproducibility
        np.random.seed(42)
        sample_df = df.sample(n=sample_size, random_state=42)

        # Save sample
        output_path = TEST_DIR / f"{name}_sample_15k.csv"
        sample_df.to_csv(output_path, index=False)

        print(f"  Saved: {output_path}")
        print(f"  Sample size: {len(sample_df):,} records")
        print(f"  File size: {output_path.stat().st_size / 1024 / 1024:.1f} MB")
        print()

    except Exception as e:
        print(f"  ERROR: {e}")
        print()

print(f"\n=== Summary ===")
print(f"Test samples saved to: {TEST_DIR}")
print(f"\nNext steps:")
print(f"1. Run preprocessing on samples")
print(f"2. Run matching algorithms")
print(f"3. Test port call master generation")

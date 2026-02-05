"""
Test the simplified pipeline end-to-end on 15K samples
"""

import pandas as pd
import subprocess
import sys
from pathlib import Path
from datetime import datetime

BASE = Path(r"G:\My Drive\LLM\project_manifest")
TEST_DIR = BASE / "04_DEVELOPMENT" / "04.02_tests"
SAMPLES_DIR = TEST_DIR / "test_samples_15k"
SCRIPTS_DIR = BASE / "02_SCRIPTS" / "02.02_matching"
OUTPUT_DIR = TEST_DIR / "test_output_simplified"
OUTPUT_DIR.mkdir(exist_ok=True)

# Override paths to use test samples
TEST_DATA = BASE / "00_DATA" / "00.02_PREPROCESSED"
TEST_MATCHED = BASE / "00_DATA" / "00.03_MATCHED"
TEST_FINAL = BASE / "00_DATA" / "00.04_FINAL"

# Ensure test directories exist
TEST_DATA.mkdir(parents=True, exist_ok=True)
TEST_MATCHED.mkdir(parents=True, exist_ok=True)
TEST_FINAL.mkdir(parents=True, exist_ok=True)

print("="*80)
print("TESTING SIMPLIFIED PIPELINE ON 15K SAMPLES")
print("="*80)
print(f"Test started: {datetime.now()}\n")

# Copy test samples to expected locations (temporary for testing)
print("Step 0: Setting up test data...")
import shutil

samples = {
    'panjiva_imports_2023_sample_15k.csv': 'panjiva_imports_2023_AUTHORITATIVE_v1.0.0.csv',
    'panjiva_exports_2023_sample_15k.csv': 'panjiva_exports_2023_AUTHORITATIVE_v1.0.0.csv',
    'usace_entrance_2023_sample_15k.csv': 'usace_2023_entrance_AUTHORITATIVE_v1.0.0.csv',
    'usace_clearance_2023_sample_15k.csv': 'usace_2023_clearance_AUTHORITATIVE_v1.0.0.csv'
}

for sample_name, target_name in samples.items():
    src = SAMPLES_DIR / sample_name
    dst = TEST_DATA / target_name
    if src.exists():
        shutil.copy2(src, dst)
        print(f"  Copied {sample_name} -> {target_name}")
    else:
        print(f"  [ERROR] Sample not found: {sample_name}")
        sys.exit(1)

print("\n[OK] Test data ready\n")

# Step 1: Match entrance to imports
print("="*80)
print("STEP 1: Match Entrance -> Imports")
print("="*80)

result = subprocess.run([
    sys.executable,
    str(SCRIPTS_DIR / "match_entrance_to_imports_SIMPLE.py")
], capture_output=True, text=True)

print(result.stdout)
if result.returncode != 0:
    print(f"\n[ERROR] Step 1 failed:")
    print(result.stderr)
    sys.exit(1)

print("\n[OK] Step 1 complete\n")

# Step 2: Match clearance to exports
print("="*80)
print("STEP 2: Match Clearance -> Exports")
print("="*80)

result = subprocess.run([
    sys.executable,
    str(SCRIPTS_DIR / "match_clearance_to_exports_SIMPLE.py")
], capture_output=True, text=True)

print(result.stdout)
if result.returncode != 0:
    print(f"\n[ERROR] Step 2 failed:")
    print(result.stderr)
    sys.exit(1)

print("\n[OK] Step 2 complete\n")

# Step 3: Marry entrance + clearance
print("="*80)
print("STEP 3: Marry Entrance + Clearance -> Port Calls")
print("="*80)

result = subprocess.run([
    sys.executable,
    str(SCRIPTS_DIR / "marry_entrance_clearance_SIMPLE.py")
], capture_output=True, text=True)

print(result.stdout)
if result.returncode != 0:
    print(f"\n[ERROR] Step 3 failed:")
    print(result.stderr)
    sys.exit(1)

print("\n[OK] Step 3 complete\n")

# Analyze results
print("="*80)
print("ANALYZING RESULTS")
print("="*80)

# Find generated files
entrance_files = list(TEST_MATCHED.glob("usace_2023_entrance_with_import_flags_v2.0.0_*.csv"))
clearance_files = list(TEST_MATCHED.glob("usace_2023_clearance_with_export_flags_v2.0.0_*.csv"))
portcall_files = list(TEST_FINAL.glob("usace_2023_portcall_master_SIMPLE_v2.0.0_*.csv"))

if entrance_files:
    ent_file = sorted(entrance_files)[-1]
    ent_df = pd.read_csv(ent_file)
    print(f"\nEntrance with flags:")
    print(f"  File: {ent_file.name}")
    print(f"  Records: {len(ent_df):,}")
    print(f"  Columns: {len(ent_df.columns)}")
    print(f"  With import manifest: {ent_df['Has_Import_Manifest'].sum():,} ({ent_df['Has_Import_Manifest'].sum()/len(ent_df)*100:.1f}%)")
    print(f"  File size: {ent_file.stat().st_size / 1024 / 1024:.1f} MB")

if clearance_files:
    clr_file = sorted(clearance_files)[-1]
    clr_df = pd.read_csv(clr_file)
    print(f"\nClearance with flags:")
    print(f"  File: {clr_file.name}")
    print(f"  Records: {len(clr_df):,}")
    print(f"  Columns: {len(clr_df.columns)}")
    print(f"  With export manifest: {clr_df['Has_Export_Manifest'].sum():,} ({clr_df['Has_Export_Manifest'].sum()/len(clr_df)*100:.1f}%)")
    print(f"  File size: {clr_file.stat().st_size / 1024 / 1024:.1f} MB")

if portcall_files:
    pc_file = sorted(portcall_files)[-1]
    pc_df = pd.read_csv(pc_file)
    print(f"\nPort Call Master (SIMPLIFIED):")
    print(f"  File: {pc_file.name}")
    print(f"  Records: {len(pc_df):,}")
    print(f"  Columns: {len(pc_df.columns)} (vs 85 in old AUTHORITATIVE)")
    print(f"  File size: {pc_file.stat().st_size / 1024 / 1024:.1f} MB")
    print(f"\n  Record types:")
    print(f"    BOTH: {(pc_df['Record_Type'] == 'BOTH').sum():,}")
    print(f"    ENTRANCE_ONLY: {(pc_df['Record_Type'] == 'ENTRANCE_ONLY').sum():,}")
    print(f"    CLEARANCE_ONLY: {(pc_df['Record_Type'] == 'CLEARANCE_ONLY').sum():,}")
    print(f"\n  Manifest flags:")
    print(f"    With import manifest: {pc_df['Has_Import_Manifest'].sum():,}")
    print(f"    With export manifest: {pc_df['Has_Export_Manifest'].sum():,}")
    print(f"    With both manifests: {((pc_df['Has_Import_Manifest']) & (pc_df['Has_Export_Manifest'])).sum():,}")

    # Show sample records
    print(f"\n  Sample port calls with manifests:")
    sample = pc_df[pc_df['Has_Import_Manifest'] | pc_df['Has_Export_Manifest']].head(5)
    print(sample[['PORTCALL_ID', 'Vessel_Name', 'Has_Import_Manifest', 'Import_VOY_RECID', 'Has_Export_Manifest', 'Export_VOY_RECID']].to_string(index=False))

print("\n" + "="*80)
print("SIMPLIFIED PIPELINE TEST COMPLETE")
print("="*80)
print(f"\nTest completed: {datetime.now()}")
print(f"\nAll output files in: {TEST_FINAL}")

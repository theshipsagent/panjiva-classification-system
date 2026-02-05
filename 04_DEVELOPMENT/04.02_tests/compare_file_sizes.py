"""
Compare old AUTHORITATIVE approach vs new SIMPLIFIED approach
"""
import os
import pandas as pd
from glob import glob

print("="*80)
print("FILE SIZE COMPARISON: Old vs New Approach")
print("="*80)

# Find old AUTHORITATIVE file
auth_patterns = [
    r"G:\My Drive\LLM\project_manifest\02_STAGE02_CLASSIFICATION\usace_2023_portcall_master*AUTHORITATIVE*.csv",
    r"G:\My Drive\LLM\project_manifest\00_DATA\00.04_FINAL\usace_2023_portcall_master*AUTHORITATIVE*.csv"
]

auth_files = []
for pattern in auth_patterns:
    auth_files.extend(glob(pattern))

if auth_files:
    old_file = max(auth_files, key=os.path.getmtime)
    old_size = os.path.getsize(old_file) / 1024 / 1024
    old_df = pd.read_csv(old_file, nrows=0)

    print(f"\nOLD APPROACH (with cargo data):")
    print(f"  File: {os.path.basename(old_file)}")
    print(f"  Size: {old_size:.1f} MB")
    print(f"  Columns: {len(old_df.columns)}")
else:
    print("\nOLD APPROACH file not found")
    old_size = None

# New SIMPLIFIED file
new_file = r"G:\My Drive\LLM\project_manifest\00_DATA\00.04_FINAL\usace_2023_portcall_master_SIMPLE_v2.0.0_20260116_1804.csv"
new_size = os.path.getsize(new_file) / 1024 / 1024
new_df = pd.read_csv(new_file, nrows=0)

print(f"\nNEW APPROACH (foreign keys only):")
print(f"  File: {os.path.basename(new_file)}")
print(f"  Size: {new_size:.1f} MB")
print(f"  Columns: {len(new_df.columns)}")

# Comparison
if old_size:
    reduction_size = (1 - new_size/old_size) * 100
    reduction_cols = (1 - len(new_df.columns)/len(old_df.columns)) * 100

    print(f"\n" + "="*80)
    print("IMPROVEMENTS")
    print("="*80)
    print(f"  Size reduction: {reduction_size:.1f}% ({old_size:.1f} MB -> {new_size:.1f} MB)")
    print(f"  Column reduction: {reduction_cols:.1f}% ({len(old_df.columns)} -> {len(new_df.columns)})")
    print(f"\nBENEFITS:")
    print(f"  - Cleaner data model (no cargo duplication)")
    print(f"  - Faster queries (smaller file, fewer columns)")
    print(f"  - Flexible joins (users get cargo details only when needed)")
    print(f"  - Better normalization (single source of truth for cargo data)")

print(f"\n" + "="*80)

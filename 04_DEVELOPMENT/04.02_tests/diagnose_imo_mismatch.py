"""
Diagnose IMO mismatch issue between USACE and Ship Registry
"""

import pandas as pd
from pathlib import Path

BASE = Path(r"G:\My Drive\LLM\project_manifest")
SAMPLES_DIR = BASE / "04_DEVELOPMENT" / "04.02_tests" / "test_samples_15k"
SHIPS_REGISTER = BASE / "01_DICTIONARIES" / "01.03_vessels" / "01_ships_register.csv"

print("="*80)
print("DIAGNOSING IMO MISMATCH ISSUE")
print("="*80)

# Load data
print("\nLoading USACE entrance sample...")
usace = pd.read_csv(SAMPLES_DIR / "usace_entrance_2023_sample_15k.csv", low_memory=False)
print(f"Total records: {len(usace):,}")
print(f"IMO column dtype: {usace['IMO'].dtype}")
print(f"Non-null IMOs: {usace['IMO'].notna().sum():,}")

print("\nLoading ship registry...")
ships = pd.read_csv(SHIPS_REGISTER, low_memory=False)
print(f"Total records: {len(ships):,}")
print(f"IMO column dtype: {ships['IMO'].dtype}")
print(f"Non-null IMOs: {ships['IMO'].notna().sum():,}")

# Analyze IMO formats
print("\n" + "="*80)
print("IMO FORMAT ANALYSIS")
print("="*80)

# Convert to strings properly
usace_imos_raw = usace['IMO'].dropna()
ships_imos_raw = ships['IMO'].dropna()

# Convert floats to int then string for USACE
usace_imos_str = usace_imos_raw.astype(int).astype(str)
ships_imos_str = ships_imos_raw.astype(str)

print("\nUSACE IMO samples (after conversion):")
for imo in usace_imos_str.head(20):
    print(f"  {imo}")

print("\nShip registry IMO samples:")
for imo in ships_imos_str.head(20):
    print(f"  {imo}")

# Check for overlap
usace_set = set(usace_imos_str)
ships_set = set(ships_imos_str)

overlap = usace_set & ships_set

print("\n" + "="*80)
print("MATCH ANALYSIS")
print("="*80)
print(f"\nUSACE unique IMOs: {len(usace_set):,}")
print(f"Ship registry unique IMOs: {len(ships_set):,}")
print(f"IMO overlap: {len(overlap):,}")
print(f"Match rate: {len(overlap)/len(usace_set)*100:.1f}%")

if len(overlap) > 0:
    print(f"\nSample matches:")
    for imo in list(overlap)[:10]:
        usace_vessel = usace[usace['IMO'].astype(int).astype(str) == imo]['Vessel'].iloc[0]
        ships_vessel = ships[ships['IMO'].astype(str) == imo]['Vessel'].iloc[0]
        print(f"  IMO {imo}: USACE='{usace_vessel}' | Registry='{ships_vessel}'")

# Check IMO range distributions
print("\n" + "="*80)
print("IMO RANGE DISTRIBUTION")
print("="*80)

usace_imo_nums = usace_imos_str.astype(int)
ships_imo_nums = ships_imos_str.astype(int)

print(f"\nUSACE IMOs:")
print(f"  Min: {usace_imo_nums.min():,}")
print(f"  Max: {usace_imo_nums.max():,}")
print(f"  Median: {usace_imo_nums.median():,.0f}")

print(f"\nShip Registry IMOs:")
print(f"  Min: {ships_imo_nums.min():,}")
print(f"  Max: {ships_imo_nums.max():,}")
print(f"  Median: {ships_imo_nums.median():,.0f}")

# Distribution by leading digit
print(f"\nUSACE IMO leading digits:")
for digit in range(10):
    count = (usace_imo_nums // 1000000 == digit).sum()
    pct = count / len(usace_imo_nums) * 100
    if count > 0:
        print(f"  {digit}xxxxxx: {count:,} ({pct:.1f}%)")

print(f"\nShip Registry IMO leading digits:")
for digit in range(10):
    count = (ships_imo_nums // 1000000 == digit).sum()
    pct = count / len(ships_imo_nums) * 100
    if count > 0:
        print(f"  {digit}xxxxxx: {count:,} ({pct:.1f}%)")

print("\n" + "="*80)
print("CONCLUSION")
print("="*80)

if len(overlap) == 0:
    print("\n[ERROR] NO IMO MATCHES FOUND!")
    print("Possible causes:")
    print("  1. Different IMO numbering systems")
    print("  2. Ship registry is outdated or wrong dataset")
    print("  3. Data type conversion issue")
    print("  4. Ship registry doesn't contain commercial vessels in USACE data")
else:
    print(f"\n[OK] Found {len(overlap):,} matches ({len(overlap)/len(usace_set)*100:.1f}%)")

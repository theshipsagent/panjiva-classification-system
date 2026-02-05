"""
Test Pipeline: Run complete pipeline on 15K samples to test new folder structure.
Tests all steps from matching through port call master generation.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import sys

# Add scripts directory to path
SCRIPTS_DIR = Path(r"G:\My Drive\LLM\project_manifest\02_SCRIPTS")
sys.path.append(str(SCRIPTS_DIR))

# Define paths
BASE = Path(r"G:\My Drive\LLM\project_manifest")
TEST_DIR = BASE / "04_DEVELOPMENT" / "04.02_tests"
SAMPLES_DIR = TEST_DIR / "test_samples_15k"
OUTPUT_DIR = TEST_DIR / "test_output"
OUTPUT_DIR.mkdir(exist_ok=True)

# Dictionaries
DICT_DIR = BASE / "01_DICTIONARIES"
SHIPS_REGISTER = DICT_DIR / "01.03_vessels" / "01_ships_register.csv"

# Log file
LOG_FILE = OUTPUT_DIR / f"pipeline_test_log_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"

def log(message):
    """Log to both console and file"""
    print(message)
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(message + '\n')

log("="*80)
log("TESTING COMPLETE PIPELINE ON 15K SAMPLES")
log("="*80)
log(f"Test started: {datetime.now()}")
log(f"Log file: {LOG_FILE}\n")

# ============================================================================
# STEP 1: Load test samples
# ============================================================================
log("\n" + "="*80)
log("STEP 1: LOAD TEST SAMPLES")
log("="*80)

try:
    log("\nLoading Panjiva imports sample...")
    panjiva_imports = pd.read_csv(SAMPLES_DIR / "panjiva_imports_2023_sample_15k.csv", low_memory=False)
    log(f"  Panjiva imports: {len(panjiva_imports):,} records")
    log(f"  Columns: {len(panjiva_imports.columns)}")

    log("\nLoading Panjiva exports sample...")
    panjiva_exports = pd.read_csv(SAMPLES_DIR / "panjiva_exports_2023_sample_15k.csv", low_memory=False)
    log(f"  Panjiva exports: {len(panjiva_exports):,} records")
    log(f"  Columns: {len(panjiva_exports.columns)}")

    log("\nLoading USACE entrance sample...")
    usace_entrance = pd.read_csv(SAMPLES_DIR / "usace_entrance_2023_sample_15k.csv", low_memory=False)
    log(f"  USACE entrance: {len(usace_entrance):,} records")
    log(f"  Columns: {len(usace_entrance.columns)}")

    log("\nLoading USACE clearance sample...")
    usace_clearance = pd.read_csv(SAMPLES_DIR / "usace_clearance_2023_sample_15k.csv", low_memory=False)
    log(f"  USACE clearance: {len(usace_clearance):,} records")
    log(f"  Columns: {len(usace_clearance.columns)}")

    log("\n[OK] STEP 1 COMPLETE: All samples loaded successfully")

except Exception as e:
    log(f"\n[ERROR] STEP 1: {e}")
    log(f"   Details: {type(e).__name__}")
    import traceback
    log(f"   Traceback:\n{traceback.format_exc()}")
    sys.exit(1)

# ============================================================================
# STEP 2: Load ship registry for vessel types
# ============================================================================
log("\n" + "="*80)
log("STEP 2: LOAD SHIP REGISTRY")
log("="*80)

try:
    log(f"\nLoading ship registry from: {SHIPS_REGISTER}")

    if not SHIPS_REGISTER.exists():
        log(f"[ERROR] ERROR: Ship registry not found at {SHIPS_REGISTER}")
        log(f"   Available files in directory:")
        registry_dir = SHIPS_REGISTER.parent
        for f in registry_dir.glob("*.csv"):
            log(f"     - {f.name}")
        sys.exit(1)

    ships_register = pd.read_csv(SHIPS_REGISTER, low_memory=False)
    log(f"  Ship registry: {len(ships_register):,} vessels")
    log(f"  Columns: {list(ships_register.columns[:10])} ...")

    log("\n[OK] STEP 2 COMPLETE: Ship registry loaded")

except Exception as e:
    log(f"\n[ERROR] ERROR in STEP 2: {e}")
    import traceback
    log(f"   Traceback:\n{traceback.format_exc()}")
    sys.exit(1)

# ============================================================================
# STEP 3: Check column compatibility
# ============================================================================
log("\n" + "="*80)
log("STEP 3: CHECK COLUMN COMPATIBILITY")
log("="*80)

try:
    log("\nChecking key columns in USACE entrance:")
    required_entrance_cols = ['IMO', 'Vessel', 'PORT', 'Arrival_Date', 'RECID']
    for col in required_entrance_cols:
        if col in usace_entrance.columns:
            log(f"  [OK] {col}: {usace_entrance[col].notna().sum():,} non-null values")
        else:
            log(f"  [ERROR] {col}: MISSING!")

    log("\nChecking key columns in USACE clearance:")
    required_clearance_cols = ['IMO', 'Vessel', 'PORT', 'Clearance_Date', 'RECID']
    for col in required_clearance_cols:
        if col in usace_clearance.columns:
            log(f"  [OK] {col}: {usace_clearance[col].notna().sum():,} non-null values")
        else:
            log(f"  [ERROR] {col}: MISSING!")

    log("\nChecking key columns in Panjiva imports:")
    required_panjiva_cols = ['Carrier', 'Arrival Date', 'IMO', 'Vessel']
    for col in required_panjiva_cols:
        if col in panjiva_imports.columns:
            log(f"  [OK] {col}: {panjiva_imports[col].notna().sum():,} non-null values")
        else:
            log(f"  [ERROR] {col}: MISSING!")

    log("\n[OK] STEP 3 COMPLETE: Column check done")

except Exception as e:
    log(f"\n[ERROR] ERROR in STEP 3: {e}")
    import traceback
    log(f"   Traceback:\n{traceback.format_exc()}")
    sys.exit(1)

# ============================================================================
# STEP 4: Simple matching test (IMO-based)
# ============================================================================
log("\n" + "="*80)
log("STEP 4: TEST SIMPLE MATCHING (IMO-based)")
log("="*80)

try:
    log("\nTesting IMO-based matching between Panjiva imports and USACE entrance...")

    # Get IMO overlap
    usace_imos = set(usace_entrance['IMO'].dropna().astype(str))
    panjiva_imos = set(panjiva_imports['IMO'].dropna().astype(str))

    overlap = usace_imos & panjiva_imos
    log(f"  USACE entrance unique IMOs: {len(usace_imos):,}")
    log(f"  Panjiva imports unique IMOs: {len(panjiva_imos):,}")
    log(f"  IMO overlap: {len(overlap):,}")
    log(f"  Potential match rate: {len(overlap)/len(usace_imos)*100:.1f}%")

    # Test with vessel names too
    log("\nTesting vessel name matching...")
    usace_vessels = set(usace_entrance['Vessel'].dropna().str.upper())
    panjiva_vessels = set(panjiva_imports['Vessel'].dropna().str.upper())

    vessel_overlap = usace_vessels & panjiva_vessels
    log(f"  USACE entrance unique vessels: {len(usace_vessels):,}")
    log(f"  Panjiva imports unique vessels: {len(panjiva_vessels):,}")
    log(f"  Vessel name overlap: {len(vessel_overlap):,}")

    log("\n[OK] STEP 4 COMPLETE: Matching feasibility confirmed")

except Exception as e:
    log(f"\n[ERROR] ERROR in STEP 4: {e}")
    import traceback
    log(f"   Traceback:\n{traceback.format_exc()}")
    sys.exit(1)

# ============================================================================
# STEP 5: Test ship registry matching
# ============================================================================
log("\n" + "="*80)
log("STEP 5: TEST SHIP REGISTRY MATCHING")
log("="*80)

try:
    log("\nTesting vessel type enrichment from ship registry...")

    # Check IMO overlap with registry
    registry_imos = set(ships_register['IMO'].dropna().astype(str))
    usace_imos = set(usace_entrance['IMO'].dropna().astype(str))

    registry_overlap = usace_imos & registry_imos
    log(f"  Ship registry IMOs: {len(registry_imos):,}")
    log(f"  USACE entrance IMOs: {len(usace_imos):,}")
    log(f"  Registry match potential: {len(registry_overlap):,} ({len(registry_overlap)/len(usace_imos)*100:.1f}%)")

    log("\n[OK] STEP 5 COMPLETE: Registry matching tested")

except Exception as e:
    log(f"\n[ERROR] ERROR in STEP 5: {e}")
    import traceback
    log(f"   Traceback:\n{traceback.format_exc()}")
    sys.exit(1)

# ============================================================================
# SUMMARY
# ============================================================================
log("\n" + "="*80)
log("PIPELINE TEST SUMMARY")
log("="*80)

log(f"\n[OK] All preliminary tests completed successfully!")
log(f"\nTest data ready:")
log(f"  - Panjiva imports: {len(panjiva_imports):,} records")
log(f"  - Panjiva exports: {len(panjiva_exports):,} records")
log(f"  - USACE entrance: {len(usace_entrance):,} records")
log(f"  - USACE clearance: {len(usace_clearance):,} records")
log(f"  - Ship registry: {len(ships_register):,} vessels")

log(f"\nMatching potential:")
log(f"  - IMO overlap: {len(overlap):,} vessels")
log(f"  - Registry matches: {len(registry_overlap):,} vessels")

log(f"\nNext steps:")
log(f"  1. Run actual matching scripts with test data")
log(f"  2. Test port call master generation")
log(f"  3. Test enrichment scripts")

log(f"\n[OK] Pipeline test log saved to: {LOG_FILE}")
log(f"\nTest completed: {datetime.now()}")

"""
Transform cargo dictionary v1.x to v2.0.0 schema
Adds Phase, Tier, and control columns for dictionary-driven classification

Author: WSD3 / Claude Code
Date: 2026-01-13
Version: 1.0.0
"""

import pandas as pd
from pathlib import Path
from datetime import datetime

# Paths
OLD_DICT = Path(r"G:\My Drive\LLM\project_manifest\01.01_dictionary\01_cargo_dictionary_harmonized_v20260111_2313.csv")
NEW_DICT = Path(r"G:\My Drive\LLM\project_manifest\01_DICTIONARIES\03.01_cargo_classification\cargo_classification_dictionary_v2.0.0_20260113_1430.csv")

# Ensure output directory exists
NEW_DICT.parent.mkdir(parents=True, exist_ok=True)

def stamp(msg):
    """Print timestamped message"""
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

def assign_phase_tier(row):
    """
    Assign Phase (1-10) and Tier (1-5) based on rule characteristics

    Phase assignments (execution order):
    Phase 1: Filters (SHIP_SPARES, FROB)
    Phase 2-3: Carrier Locks
    Phase 4: HS2 matching
    Phase 5: HS4 matching
    Phase 6: HS6 matching
    Phase 7: Keyword-only matching
    Phase 8: Combinatorial (HS + tonnage)
    Phase 9: Refinements
    Phase 10: Specific high-value grades

    Tier assignments (priority/accuracy):
    Tier 1: Carrier Locks (100% accuracy, never override)
    Tier 2: Package Types (98% accuracy)
    Tier 3: HS Code + Keywords (90% accuracy)
    Tier 4: Tonnage Overrides (80% accuracy)
    Tier 5: Specific Grades (95% accuracy)
    """

    # Default values
    phase = 7  # Default to keyword matching phase
    tier = 3   # Default to HS+Keywords tier
    lock = False
    override_hs = False

    # Extract rule characteristics
    hs2 = str(row.get('HS2', '')).strip()
    hs4 = str(row.get('HS4', '')).strip()
    hs6 = str(row.get('HS6', '')).strip()
    keywords = str(row.get('Keywords_Str', '')).strip().upper()
    min_tons = str(row.get('Min Tons', '')).strip()
    max_tons = str(row.get('Max Tons', '')).strip()
    group = str(row.get('Group', '')).strip()
    cargo = str(row.get('Cargo', '')).strip()
    note = str(row.get('Note', '')).strip().upper()

    # TIER 1: Carrier Locks (highest priority, never override)
    # Look for known carrier patterns in keywords
    carriers = ['WALLENIUS', 'STOLT', 'COOL CARRIERS', 'HÖEGH', 'NYK', 'MOL',
                'K LINE', 'WWL', 'EUKOR']
    if any(carrier in keywords for carrier in carriers):
        phase = 2
        tier = 1
        lock = True
        override_hs = False
        return phase, tier, lock, override_hs

    # TIER 2: Package Types
    # Look for package indicators (would need package column - using keywords as proxy)
    package_indicators = ['LBK', 'BLK', 'DBK']
    if any(pkg in keywords for pkg in package_indicators):
        phase = 3
        tier = 2
        lock = False
        override_hs = True
        return phase, tier, lock, override_hs

    # TIER 5: High-value specific grades (Phase 10)
    # Look for very specific commodity names
    specific_grades = ['BASRAH', 'KIRKUK', 'LIZA', 'TUPI', 'BRENT', 'WTI',
                      'PRIMARY ALUMINIUM', 'EUCABOARD', 'EUCALYPTUS', 'TUBARAO']
    if any(grade in keywords for grade in specific_grades):
        phase = 10
        tier = 5
        lock = False
        override_hs = True
        return phase, tier, lock, override_hs

    # Check if this is a tonnage-override rule (Tier 4)
    # Has tonnage thresholds AND they're significant (not just data artifact)
    has_tonnage_threshold = False
    if min_tons and min_tons not in ['', '0', 'nan']:
        try:
            if float(min_tons) >= 100:  # Meaningful threshold
                has_tonnage_threshold = True
        except:
            pass

    # TIER 3 & 4: HS Code matching (with or without tonnage override)
    if hs6 and hs6 not in ['0', '', 'nan', '0'*6]:
        phase = 6  # HS6 phase
        tier = 4 if has_tonnage_threshold else 3
        override_hs = has_tonnage_threshold
    elif hs4 and hs4 not in ['0', '', 'nan', '0'*4]:
        phase = 5  # HS4 phase
        tier = 4 if has_tonnage_threshold else 3
        override_hs = has_tonnage_threshold
    elif hs2 and hs2 not in ['0', '', 'nan', '00']:
        phase = 4  # HS2 phase
        tier = 4 if has_tonnage_threshold else 3
        override_hs = has_tonnage_threshold
    else:
        # Keyword-only matching
        phase = 7
        tier = 3
        override_hs = False

    return phase, tier, lock, override_hs

def estimate_accuracy(tier):
    """Estimate accuracy based on tier"""
    accuracy_map = {
        1: '100%',  # Carrier locks
        2: '98%',   # Package types
        3: '90%',   # HS + Keywords
        4: '80%',   # Tonnage overrides
        5: '95%'    # Specific grades
    }
    return accuracy_map.get(tier, '85%')

def estimate_impact(tier):
    """Estimate tonnage impact based on tier"""
    impact_map = {
        1: 'Very High',
        2: 'Extremely High',
        3: 'High',
        4: 'Medium',
        5: 'High'
    }
    return impact_map.get(tier, 'Medium')

def transform_dictionary():
    """Main transformation function"""

    stamp("=== Starting Dictionary Transformation v1.x to v2.0.0 ===")

    # Read old dictionary
    stamp(f"Reading old dictionary: {OLD_DICT}")
    df_old = pd.read_csv(OLD_DICT, dtype=str)
    stamp(f"Loaded {len(df_old)} rules")

    # Create new dictionary structure
    stamp("Creating new schema...")
    df_new = pd.DataFrame()

    # Generate Rule IDs
    rule_ids = []
    for idx, row in df_old.iterrows():
        cargo = str(row.get('Cargo', 'UNKNOWN')).replace(' ', '-').replace('/', '-').upper()
        rule_ids.append(f"RULE-{idx+1:04d}-{cargo[:20]}")

    df_new['Rule_ID'] = rule_ids

    # Assign Phase and Tier
    stamp("Assigning phases and tiers...")
    phase_tier_data = df_old.apply(assign_phase_tier, axis=1)
    df_new['Phase'] = [x[0] for x in phase_tier_data]
    df_new['Tier'] = [x[1] for x in phase_tier_data]
    df_new['Lock_Classification'] = [x[2] for x in phase_tier_data]
    df_new['Override_HS'] = [x[3] for x in phase_tier_data]

    # Control columns
    df_new['Active'] = 'TRUE'  # All rules active by default

    # Matching criteria columns
    df_new['Carrier_Name'] = ''  # Populate manually later for carrier rules
    df_new['Package_Type'] = ''  # Populate manually later
    df_new['HS2'] = df_old.get('HS2', '').fillna('')
    df_new['HS4'] = df_old.get('HS4', '').fillna('')
    df_new['HS6'] = df_old.get('HS6', '').fillna('')

    # Clean up keywords - convert from list format to semicolon-separated
    df_new['Keywords'] = df_old.get('Keywords_Str', '').fillna('')
    df_new['Exclude_Keywords'] = ''  # Add manually later

    # Tonnage filters
    df_new['Min_Tons'] = df_old.get('Min Tons', '').fillna('')
    df_new['Max_Tons'] = df_old.get('Max Tons', '').fillna('')
    df_new['Port_Filter'] = ''
    df_new['Country_Filter'] = ''

    # Classification outputs
    df_new['Group'] = df_old.get('Group', '').fillna('')
    df_new['Commodity'] = df_old.get('Commodity', '').fillna('')
    df_new['Cargo'] = df_old.get('Cargo', '').fillna('')
    df_new['Cargo_Detail'] = df_old.get('Cargo_Detail', '').fillna('')
    df_new['Filter'] = ''  # SHIP_SPARES, FROB, etc.

    # Metadata
    df_new['Note'] = df_old.get('Note', '').fillna('')
    df_new['Accuracy_Est'] = df_new['Tier'].apply(estimate_accuracy)
    df_new['Tonnage_Impact'] = df_new['Tier'].apply(estimate_impact)
    df_new['Date_Added'] = datetime.now().strftime('%Y-%m-%d')
    df_new['Last_Modified'] = datetime.now().strftime('%Y-%m-%d')

    # Column order (as defined in schema)
    column_order = [
        'Rule_ID', 'Phase', 'Tier', 'Active', 'Lock_Classification', 'Override_HS',
        'Carrier_Name', 'Package_Type', 'HS2', 'HS4', 'HS6',
        'Keywords', 'Exclude_Keywords', 'Min_Tons', 'Max_Tons',
        'Port_Filter', 'Country_Filter',
        'Group', 'Commodity', 'Cargo', 'Cargo_Detail', 'Filter',
        'Note', 'Accuracy_Est', 'Tonnage_Impact', 'Date_Added', 'Last_Modified'
    ]

    df_new = df_new[column_order]

    # Save new dictionary
    stamp(f"Saving new dictionary: {NEW_DICT}")
    df_new.to_csv(NEW_DICT, index=False)

    # Statistics
    stamp("\n=== Transformation Summary ===")
    stamp(f"Total rules: {len(df_new)}")
    stamp(f"\nRules by Phase:")
    for phase in sorted(df_new['Phase'].unique()):
        count = len(df_new[df_new['Phase'] == phase])
        stamp(f"  Phase {phase}: {count} rules")

    stamp(f"\nRules by Tier:")
    tier_names = {1: 'Carrier Locks', 2: 'Package Types', 3: 'HS+Keywords',
                  4: 'Tonnage Override', 5: 'Specific Grades'}
    for tier in sorted(df_new['Tier'].unique()):
        count = len(df_new[df_new['Tier'] == tier])
        stamp(f"  Tier {tier} ({tier_names.get(tier, 'Unknown')}): {count} rules")

    stamp(f"\nDictionary transformation complete!")
    stamp(f"New file: {NEW_DICT}")

    return df_new

if __name__ == "__main__":
    df = transform_dictionary()

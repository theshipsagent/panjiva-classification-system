"""
Panjiva Import Classification v1.0.0
======================================

Purpose: Classify preprocessed Panjiva data using dictionary rules

Process:
1. Load preprocessed data (59 columns with empty classification)
2. Load dictionary v3.6.0 (668 rules)
3. Execute phases in order (1 → 2 → 3 → 5 → 6)
4. For each phase, match rules and fill classification
5. Respect lock levels (prevent overriding locked classifications)
6. Track phase and rule that classified each record
7. Save classified data (same 59 columns, classification filled)

Input:  Preprocessed CSV (59 columns, classification empty)
Output: Classified CSV (59 columns, classification filled)

Author: WSD3 / Claude Code
Date: 2026-01-28
Version: 1.0.0
"""

import pandas as pd
import numpy as np
import logging
import sys
from pathlib import Path
from datetime import datetime
import traceback

# ============================================================================
# CONFIGURATION
# ============================================================================

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
DICTIONARY = PROJECT_ROOT / "00_REFERENCE" / "dictionary_v3.6.0.csv"
INPUT_DIR = PROJECT_ROOT / "03_DATA" / "01_preprocessed"
OUTPUT_DIR = PROJECT_ROOT / "03_DATA" / "02_classified"
LOG_DIR = PROJECT_ROOT / "05_LOGS"

# Create directories
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Logging setup
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
log_file = LOG_DIR / f"step02_classify_{timestamp}.log"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler(sys.stdout)
    ]
)

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def stamp(msg):
    """Print timestamped message"""
    logging.info(msg)

# ============================================================================
# DICTIONARY LOADING
# ============================================================================

def load_dictionary():
    """Load and filter classification dictionary"""
    stamp("\n" + "="*80)
    stamp("STEP 1: LOADING DICTIONARY")
    stamp("="*80)

    try:
        df_dict = pd.read_csv(DICTIONARY, dtype=str)
        stamp(f"Loaded {len(df_dict)} rules from dictionary")

        # Filter active rules only
        df_dict = df_dict[df_dict['Active'] == 'TRUE'].copy()
        stamp(f"Active rules: {len(df_dict)}")

        # Show phase distribution
        stamp("\nPhase distribution:")
        phase_counts = df_dict['Phase'].value_counts().sort_index()
        for phase, count in phase_counts.items():
            stamp(f"  Phase {phase}: {count} rules")

        return df_dict

    except Exception as e:
        stamp(f"ERROR loading dictionary: {e}")
        raise

# ============================================================================
# KEYWORD MATCHING LOGIC
# ============================================================================

def check_keyword_match(cargo_desc, rule):
    """
    Check if cargo description matches rule keywords

    Supports v3.6.0 keyword strategy:
    - Key_Phrases: Multi-word phrases (e.g., "CRUDE OIL", "PIG IRON")
    - Primary_Keywords: Standalone terms (e.g., "CEMENT", "STEEL")
    - Descriptor_Keywords: Modifiers (e.g., "HOT", "ROLLED", "PRIME")
    - Match_Strategy: PHRASE_REQUIRED or PRIMARY_SUFFICIENT
    - Keywords: Legacy semicolon-separated list
    """

    if pd.isna(cargo_desc) or cargo_desc == '':
        cargo_desc = ''

    cargo_desc_upper = str(cargo_desc).upper()

    # Get keyword fields
    key_phrases = str(rule.get('Key_Phrases', '')).strip()
    primary_kw = str(rule.get('Primary_Keywords', '')).strip()
    descriptor_kw = str(rule.get('Descriptor_Keywords', '')).strip()
    match_strategy = str(rule.get('Match_Strategy', 'PRIMARY_SUFFICIENT')).strip()
    legacy_keywords = str(rule.get('Keywords', '')).strip()

    # If no keywords at all, no keyword filter (always match)
    if not any([
        key_phrases and key_phrases != 'nan',
        primary_kw and primary_kw != 'nan',
        descriptor_kw and descriptor_kw != 'nan',
        legacy_keywords and legacy_keywords != 'nan'
    ]):
        return True

    # PHRASE_REQUIRED: Must match at least one key phrase
    if match_strategy == 'PHRASE_REQUIRED':
        if key_phrases and key_phrases != 'nan':
            phrase_list = [p.strip().upper() for p in key_phrases.split(',') if p.strip()]
            if any(phrase in cargo_desc_upper for phrase in phrase_list):
                return True
        return False

    # PRIMARY_SUFFICIENT: Match primary keywords OR key phrases
    matched = False

    # Check primary keywords
    if primary_kw and primary_kw != 'nan':
        primary_list = [k.strip().upper() for k in primary_kw.split(',') if k.strip()]
        if any(kw in cargo_desc_upper for kw in primary_list):
            matched = True

    # Check key phrases
    if not matched and key_phrases and key_phrases != 'nan':
        phrase_list = [p.strip().upper() for p in key_phrases.split(',') if p.strip()]
        if any(phrase in cargo_desc_upper for phrase in phrase_list):
            matched = True

    # Check legacy keywords (semicolon separated)
    if not matched and legacy_keywords and legacy_keywords != 'nan':
        legacy_list = [k.strip().upper() for k in legacy_keywords.split(';') if k.strip()]
        if any(kw in cargo_desc_upper for kw in legacy_list):
            matched = True

    return matched

# ============================================================================
# RULE MATCHING LOGIC
# ============================================================================

def check_match(record, rule):
    """
    Check if a rule matches a record

    Checks all matching criteria:
    - Carrier_SCAC
    - Vessel_Type
    - Package_Type
    - HS2/HS4/HS6
    - Keywords (via check_keyword_match)
    - Exclude_Keywords
    - Min_Tons/Max_Tons

    Returns True if ALL criteria match (AND logic)
    """

    # Carrier SCAC match
    carrier_scac = rule.get('Carrier_SCAC', '')
    if carrier_scac and pd.notna(carrier_scac) and str(carrier_scac).strip():
        record_carrier = str(record.get('Carrier', '')).upper()
        if str(carrier_scac).upper().strip() not in record_carrier:
            return False

    # Vessel Type match
    vessel_type = rule.get('Vessel_Type', '')
    if vessel_type and pd.notna(vessel_type) and str(vessel_type).strip():
        record_vtype = str(record.get('Vessel_Type_Simple', '')).upper()
        vessel_types = [v.strip().upper() for v in str(vessel_type).split(';') if v.strip()]
        if not any(vt in record_vtype for vt in vessel_types):
            return False

    # Package Type match
    package_type = rule.get('Package_Type', '')
    if package_type and pd.notna(package_type) and str(package_type).strip():
        record_pkg = str(record.get('Package_Type', '')).upper()
        package_types = [p.strip().upper() for p in str(package_type).split(';') if p.strip()]
        if not any(pt in record_pkg for pt in package_types):
            return False

    # HS Code matches
    for hs_level in ['HS2', 'HS4', 'HS6']:
        rule_hs = rule.get(hs_level, '')
        if rule_hs and pd.notna(rule_hs) and str(rule_hs).strip():
            record_hs = str(record.get(hs_level, '')).strip()
            if str(rule_hs).strip() != record_hs:
                return False

    # Keyword match
    cargo_desc = str(record.get('Goods Shipped', ''))
    if not check_keyword_match(cargo_desc, rule):
        return False

    # Exclude Keywords
    exclude_kw = rule.get('Exclude_Keywords', '')
    if exclude_kw and pd.notna(exclude_kw) and str(exclude_kw).strip():
        cargo_desc_upper = cargo_desc.upper()
        exclude_list = [k.strip().upper() for k in str(exclude_kw).split(';') if k.strip()]
        if any(ex in cargo_desc_upper for ex in exclude_list):
            return False

    # Tonnage filter
    min_tons = rule.get('Min_Tons', '')
    max_tons = rule.get('Max_Tons', '')

    if (min_tons and pd.notna(min_tons) and str(min_tons).strip()) or \
       (max_tons and pd.notna(max_tons) and str(max_tons).strip()):
        try:
            record_tons_str = str(record.get('Tons', '0')).replace(',', '')
            record_tons = float(record_tons_str) if record_tons_str else 0

            if min_tons and pd.notna(min_tons) and str(min_tons).strip():
                if record_tons < float(min_tons):
                    return False

            if max_tons and pd.notna(max_tons) and str(max_tons).strip():
                if record_tons > float(max_tons):
                    return False
        except:
            pass

    return True

def can_apply_rule(record, rule):
    """
    Check if rule can be applied based on lock levels and exclusions

    Lock level hierarchy:
    - Group unlocked: Can change Group/Commodity/Cargo/Cargo_Detail
    - Group locked, Commodity unlocked: Can change Commodity/Cargo/Cargo_Detail
    - Commodity locked, Cargo unlocked: Can change Cargo/Cargo_Detail
    - Cargo locked, Cargo_Detail unlocked: Can only change Cargo_Detail
    - All locked: Cannot apply rule
    """

    # Check Exclude_Groups
    exclude_groups = rule.get('Exclude_Groups', '')
    if exclude_groups and pd.notna(exclude_groups) and str(exclude_groups).strip():
        current_group = str(record.get('Group', '')).strip()
        if current_group:
            exclude_list = [g.strip() for g in str(exclude_groups).split(';') if g.strip()]
            if current_group in exclude_list:
                return False

    # Check lock levels
    # If Group is locked, rule must match current Group
    if str(record.get('Group_Locked', 'FALSE')).upper() == 'TRUE':
        rule_group = str(rule.get('Group', '')).strip()
        current_group = str(record.get('Group', '')).strip()
        if rule_group and current_group and rule_group != current_group:
            return False

    # If Commodity is locked, rule must match current Commodity
    if str(record.get('Commodity_Locked', 'FALSE')).upper() == 'TRUE':
        rule_commodity = str(rule.get('Commodity', '')).strip()
        current_commodity = str(record.get('Commodity', '')).strip()
        if rule_commodity and current_commodity and rule_commodity != current_commodity:
            return False

    # If Cargo is locked, rule must match current Cargo
    if str(record.get('Cargo_Locked', 'FALSE')).upper() == 'TRUE':
        rule_cargo = str(rule.get('Cargo', '')).strip()
        current_cargo = str(record.get('Cargo', '')).strip()
        if rule_cargo and current_cargo and rule_cargo != current_cargo:
            return False

    # If Cargo_Detail is locked, cannot apply any rule
    if str(record.get('Cargo_Detail_Locked', 'FALSE')).upper() == 'TRUE':
        return False

    return True

def apply_rule(record, rule):
    """
    Apply rule to record - update classification and locks

    Updates:
    - Group, Commodity, Cargo, Cargo_Detail (if provided by rule)
    - Lock flags (Group_Locked, Commodity_Locked, etc.)
    - Classified_Phase (which phase classified this record)
    - Last_Rule_ID (which rule was applied)
    """

    # Apply classification (only if rule provides value)
    if pd.notna(rule.get('Group')) and str(rule.get('Group', '')).strip():
        record['Group'] = rule['Group']

    if pd.notna(rule.get('Commodity')) and str(rule.get('Commodity', '')).strip():
        record['Commodity'] = rule['Commodity']

    if pd.notna(rule.get('Cargo')) and str(rule.get('Cargo', '')).strip():
        record['Cargo'] = rule['Cargo']

    if pd.notna(rule.get('Cargo_Detail')) and str(rule.get('Cargo_Detail', '')).strip():
        record['Cargo Detail'] = rule['Cargo_Detail']

    # Apply locks
    if str(rule.get('Lock_Group', 'FALSE')).upper() == 'TRUE':
        record['Group_Locked'] = 'TRUE'

    if str(rule.get('Lock_Commodity', 'FALSE')).upper() == 'TRUE':
        record['Commodity_Locked'] = 'TRUE'

    if str(rule.get('Lock_Cargo', 'FALSE')).upper() == 'TRUE':
        record['Cargo_Locked'] = 'TRUE'

    if str(rule.get('Lock_Cargo_Detail', 'FALSE')).upper() == 'TRUE':
        record['Cargo_Detail_Locked'] = 'TRUE'

    # Track classification
    record['Classified_Phase'] = rule['Phase']
    record['Last_Rule_ID'] = rule['Rule_ID']

    return record

# ============================================================================
# CLASSIFICATION ENGINE
# ============================================================================

def classify_in_phases(df, df_dict):
    """
    Main classification engine - process records through phases

    For each phase (1, 2, 3, 5, 6):
    1. Get rules for that phase
    2. For each record:
       - Check if any rule matches
       - Check if rule can be applied (lock check)
       - Apply first matching rule
    3. Track statistics
    """

    stamp("\n" + "="*80)
    stamp("STEP 3: CLASSIFYING RECORDS")
    stamp("="*80)

    # Get unique phases in order
    phases = sorted(df_dict['Phase'].unique(), key=lambda x: int(x))

    total_records = len(df)
    classified_by_phase = {}

    for phase in phases:
        stamp(f"\n--- Processing Phase {phase} ---")

        # Get rules for this phase
        phase_rules = df_dict[df_dict['Phase'] == phase].to_dict('records')
        stamp(f"Rules in phase: {len(phase_rules)}")

        matched_count = 0
        applied_count = 0

        # Process each record
        for idx, row in df.iterrows():
            record = row.to_dict()

            # Try each rule in order
            for rule in phase_rules:
                # Check if rule matches
                if check_match(record, rule):
                    matched_count += 1

                    # Check if rule can be applied (lock check)
                    if can_apply_rule(record, rule):
                        # Apply rule
                        record = apply_rule(record, rule)
                        applied_count += 1

                        # Update DataFrame
                        for col, val in record.items():
                            df.at[idx, col] = val

                        # Stop after first matching rule
                        break

        classified_by_phase[phase] = applied_count
        stamp(f"Phase {phase}: Matched {matched_count}, Applied {applied_count}")

    # Summary
    stamp("\n" + "="*80)
    stamp("CLASSIFICATION SUMMARY")
    stamp("="*80)

    total_classified = (df['Classified_Phase'] != '').sum()
    stamp(f"Total classified: {total_classified:,} / {total_records:,} ({total_classified/total_records*100:.1f}%)")

    stamp("\nBy phase:")
    for phase, count in classified_by_phase.items():
        stamp(f"  Phase {phase}: {count:,} ({count/total_records*100:.1f}%)")

    stamp("\nBy Group:")
    group_counts = df['Group'].value_counts()
    for group, count in group_counts.items():
        if group and group != '':
            stamp(f"  {group}: {count:,} ({count/total_records*100:.1f}%)")

    return df

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def load_preprocessed_data(input_file):
    """Load preprocessed data"""
    stamp("\n" + "="*80)
    stamp("STEP 2: LOADING PREPROCESSED DATA")
    stamp("="*80)

    df = pd.read_csv(input_file, dtype=str)
    stamp(f"Loaded {len(df):,} records")
    stamp(f"Columns: {len(df.columns)}")

    # Verify expected columns exist
    required_cols = ['Group', 'Commodity', 'Cargo', 'Cargo Detail',
                     'Group_Locked', 'Commodity_Locked', 'Cargo_Locked', 'Cargo_Detail_Locked',
                     'Classified_Phase', 'Last_Rule_ID']

    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        stamp(f"WARNING: Missing columns: {missing}")

    return df

def save_classified_data(df, input_filename, sample_size=None, year=None):
    """Save classified data"""
    stamp("\n" + "="*80)
    stamp("STEP 4: SAVING CLASSIFIED DATA")
    stamp("="*80)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    # Generate output filename
    if sample_size:
        filename = f"sample_{sample_size}_classified_v1.0.0_{timestamp}.csv"
    elif year:
        filename = f"panjiva_{year}_classified_v1.0.0_{timestamp}.csv"
    else:
        filename = f"panjiva_classified_v1.0.0_{timestamp}.csv"

    output_path = OUTPUT_DIR / filename
    df.to_csv(output_path, index=False)

    file_size_mb = output_path.stat().st_size / (1024 * 1024)
    stamp(f"Saved: {output_path.name}")
    stamp(f"  Records: {len(df):,}")
    stamp(f"  Columns: {len(df.columns)}")
    stamp(f"  Size: {file_size_mb:.1f} MB")

    return output_path

def main(input_file=None, sample_size=None, year=None):
    """Main classification pipeline"""

    try:
        stamp("\n" + "="*80)
        stamp("PANJIVA CLASSIFICATION v1.0.0")
        stamp("="*80)
        stamp(f"Start time: {datetime.now()}")

        # Step 1: Load dictionary
        df_dict = load_dictionary()

        # Step 2: Load preprocessed data
        if not input_file:
            # Auto-detect latest file
            pattern = f"*preprocessed*.csv"
            files = sorted(INPUT_DIR.glob(pattern), key=lambda x: x.stat().st_mtime, reverse=True)
            if not files:
                raise FileNotFoundError(f"No preprocessed files found in {INPUT_DIR}")
            input_file = files[0]
            stamp(f"Auto-detected input: {input_file.name}")

        df = load_preprocessed_data(input_file)

        # Step 3: Classify
        df = classify_in_phases(df, df_dict)

        # Step 4: Save
        output_path = save_classified_data(df, input_file.name, sample_size=sample_size, year=year)

        stamp("\n" + "="*80)
        stamp("CLASSIFICATION COMPLETE")
        stamp("="*80)
        stamp(f"End time: {datetime.now()}")
        stamp(f"Output: {output_path}")
        stamp(f"Log: {log_file}")

        return df

    except Exception as e:
        stamp("\n" + "="*80)
        stamp("CLASSIFICATION FAILED")
        stamp("="*80)
        stamp(f"Error: {str(e)}")
        stamp(f"Traceback:\n{traceback.format_exc()}")
        sys.exit(1)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Classify preprocessed Panjiva data')
    parser.add_argument('--input', type=str, help='Input preprocessed CSV file')
    parser.add_argument('--sample', type=int, help='Sample size (for output naming)')
    parser.add_argument('--year', type=int, help='Year (for output naming)')

    args = parser.parse_args()

    input_path = Path(args.input) if args.input else None
    main(input_file=input_path, sample_size=args.sample, year=args.year)

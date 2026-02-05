"""
DIAGNOSTIC: 5K Classification Test with Complete Column Validation

Tests:
1. Column name alignment (underscore vs space)
2. Data landing in correct columns
3. Dictionary matching logic
4. Classification coverage
5. Lock mechanism
6. Phase progression

Author: WSD3 / Claude Code
Date: 2026-01-19
Version: 1.0.0
"""

import pandas as pd
from pathlib import Path
from datetime import datetime
import traceback

# Paths
INPUT_FILE = Path(r"G:\My Drive\LLM\project_manifest\00_DATA\00.02_PREPROCESSED\panjiva_imports_2024_AUTHORITATIVE_v1.0.0.csv")
SHIP_REGISTRY = Path(r"G:\My Drive\LLM\project_manifest\01_DICTIONARIES\01.03_vessels\01_ships_register.csv")
DICTIONARY = Path(r"G:\My Drive\LLM\project_manifest\01_DICTIONARIES\01.01_cargo_classification\cargo_classification_dictionary_CURRENT_v3.6.0.csv")
OUTPUT_DIR = Path(r"G:\My Drive\LLM\project_manifest\03_DOCUMENTATION\03.04_summaries\diagnostic_5k_test")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def stamp(msg, level="INFO"):
    """Print timestamped message"""
    timestamp = datetime.now().strftime('%H:%M:%S')
    print(f"[{timestamp}] {level:8s} {msg}")

def diagnostic_section(title):
    """Print diagnostic section header"""
    print("\n" + "=" * 80)
    stamp(title, "SECTION")
    print("=" * 80)

# ============================================================================
# STEP 1: Load and validate input data
# ============================================================================

def load_sample():
    """Load 5K sample and validate columns"""
    diagnostic_section("STEP 1: Loading 5K Sample")

    stamp(f"Reading: {INPUT_FILE.name}")
    df = pd.read_csv(INPUT_FILE, dtype=str, nrows=5000)
    stamp(f"Loaded {len(df):,} records", "SUCCESS")

    # Check critical columns exist
    stamp("\nValidating critical columns:")
    required_cols = ['Vessel', 'Carrier', 'Goods Shipped', 'HS2', 'HS4', 'HS6', 'Tons']
    missing = []
    for col in required_cols:
        if col in df.columns:
            non_null = df[col].notna().sum()
            stamp(f"  OK {col:20s} - {non_null:,} non-null values", "OK")
        else:
            stamp(f"  !! {col:20s} - MISSING!", "ERROR")
            missing.append(col)

    if missing:
        stamp(f"CRITICAL: Missing columns: {missing}", "ERROR")
        return None

    # Show sample data
    stamp("\nSample record (first row):")
    first_row = df.iloc[0]
    for col in required_cols:
        value = str(first_row[col])[:60]
        stamp(f"  {col:20s}: {value}")

    return df

# ============================================================================
# STEP 2: Add vessel types
# ============================================================================

def map_vessel_type(detailed_type):
    """Map detailed vessel type to simplified category"""
    if pd.isna(detailed_type) or detailed_type == '':
        return ''

    detailed_type = str(detailed_type).upper()

    if any(x in detailed_type for x in ['BULK CARRIER', 'BULKER', 'CAPESIZE', 'PANAMAX',
                                          'HANDYMAX', 'HANDYSIZE', 'SUPRAMAX', 'ULTRAMAX']):
        return 'Bulk Carrier'
    if any(x in detailed_type for x in ['TANKER', 'VLCC', 'SUEZMAX', 'AFRAMAX', 'MR', 'LR']):
        return 'Tanker'
    if any(x in detailed_type for x in ['LPG', 'LNG', 'GAS CARRIER']):
        return 'LPG/LNG Carrier'
    if any(x in detailed_type for x in ['CONTAINER', 'TEU', 'FEEDER']):
        return 'Container'
    if any(x in detailed_type for x in ['RO-RO', 'RORO', 'CAR CARRIER', 'PCTC']):
        return 'RoRo'
    if any(x in detailed_type for x in ['REEFER', 'REFRIGERAT']):
        return 'Reefer'
    if any(x in detailed_type for x in ['GENERAL CARGO', 'MULTI-PURPOSE']):
        return 'General Cargo'

    return ''

def add_vessel_types(df):
    """Add vessel types from ship registry"""
    diagnostic_section("STEP 2: Adding Vessel Types")

    # Load ship registry
    stamp(f"Loading ship registry: {SHIP_REGISTRY.name}")
    df_ships = pd.read_csv(SHIP_REGISTRY, dtype=str)
    stamp(f"Loaded {len(df_ships):,} vessels from registry", "SUCCESS")

    # Create lookup
    vessel_lookup = {}
    for _, row in df_ships.iterrows():
        vessel_name = str(row['Vessel']).upper().strip()
        vessel_type = map_vessel_type(row.get('Type', ''))
        if vessel_name and vessel_type:
            vessel_lookup[vessel_name] = vessel_type

    stamp(f"Created lookup for {len(vessel_lookup):,} vessels with types")

    # Add Vessel_Type_Simple column
    df['Vessel_Type_Simple'] = df['Vessel'].apply(
        lambda x: vessel_lookup.get(str(x).upper().strip(), '') if pd.notna(x) else ''
    )

    matched = len(df[df['Vessel_Type_Simple'] != ''])
    stamp(f"Matched vessel types: {matched:,} / {len(df):,} ({matched/len(df)*100:.1f}%)", "SUCCESS")

    # Show examples
    stamp("\nVessel type examples:")
    examples = df[df['Vessel_Type_Simple'] != ''].head(5)
    for _, row in examples.iterrows():
        stamp(f"  {row['Vessel']:30s} => {row['Vessel_Type_Simple']}")

    return df

# ============================================================================
# STEP 3: Load and validate dictionary
# ============================================================================

def load_dictionary():
    """Load and validate classification dictionary"""
    diagnostic_section("STEP 3: Loading Classification Dictionary")

    stamp(f"Reading: {DICTIONARY.name}")
    df_dict = pd.read_csv(DICTIONARY, dtype=str)
    stamp(f"Loaded {len(df_dict):,} total rules", "SUCCESS")

    # Check critical columns
    stamp("\nValidating dictionary columns:")
    required_dict_cols = ['Rule_ID', 'Phase', 'Active', 'Group', 'Commodity', 'Cargo',
                          'Carrier_SCAC', 'Vessel_Type', 'HS2', 'HS4', 'HS6', 'Keywords',
                          'Lock_Group', 'Lock_Commodity', 'Lock_Cargo', 'Lock_Cargo_Detail']

    missing_dict = []
    for col in required_dict_cols:
        if col in df_dict.columns:
            stamp(f"  OK {col:25s}", "OK")
        else:
            stamp(f"  !! {col:25s} - MISSING!", "ERROR")
            missing_dict.append(col)

    if missing_dict:
        stamp(f"CRITICAL: Missing dictionary columns: {missing_dict}", "ERROR")
        return None

    # Filter active rules
    df_dict = df_dict[df_dict['Active'] == 'TRUE']
    stamp(f"\nActive rules: {len(df_dict):,}", "SUCCESS")

    # Show phase breakdown
    stamp("\nPhase breakdown:")
    for phase in sorted(df_dict['Phase'].unique()):
        count = len(df_dict[df_dict['Phase'] == phase])
        stamp(f"  Phase {phase}: {count:4d} rules")

    # Show sample rules
    stamp("\nSample rules from Phase 2 (Carrier locks):")
    phase2 = df_dict[df_dict['Phase'] == '2'].head(3)
    for _, rule in phase2.iterrows():
        rule_id = str(rule['Rule_ID'])[:30]
        carrier = str(rule['Carrier_SCAC'])[:10] if pd.notna(rule['Carrier_SCAC']) else 'N/A'
        group = str(rule['Group'])[:20]
        stamp(f"  {rule_id:30s} | {carrier:10s} => {group}")

    return df_dict

# ============================================================================
# STEP 4: Classification logic with diagnostics
# ============================================================================

def check_keyword_match(cargo_desc, rule):
    """Check keyword match - NEW v3.6.0 logic"""
    cargo_desc_upper = cargo_desc.upper()

    # Get keyword fields
    key_phrases = str(rule.get('Key_Phrases', '')).strip()
    primary_kw = str(rule.get('Primary_Keywords', '')).strip()
    legacy_keywords = str(rule.get('Keywords', '')).strip()

    # If no keywords at all, no keyword filter
    if not any([key_phrases != 'nan' and key_phrases,
                primary_kw != 'nan' and primary_kw,
                legacy_keywords != 'nan' and legacy_keywords]):
        return True

    # Check primary keywords
    if primary_kw and primary_kw != 'nan':
        primary_list = [k.strip().upper() for k in primary_kw.split(',')]
        if any(kw in cargo_desc_upper for kw in primary_list if kw):
            return True

    # Check key phrases
    if key_phrases and key_phrases != 'nan':
        phrase_list = [p.strip().upper() for p in key_phrases.split(',')]
        if any(phrase in cargo_desc_upper for phrase in phrase_list if phrase):
            return True

    # Fall back to legacy keywords (semicolon separated)
    if legacy_keywords and legacy_keywords != 'nan':
        legacy_list = [k.strip().upper() for k in legacy_keywords.split(';')]
        if any(kw in cargo_desc_upper for kw in legacy_list if kw):
            return True

    return False

def check_match(record, rule, verbose=False):
    """Check if a rule matches a record - with diagnostics"""

    checks = []

    # Carrier SCAC match
    carrier_scac = rule.get('Carrier_SCAC', '')
    if carrier_scac and pd.notna(carrier_scac) and carrier_scac.strip():
        record_carrier = str(record.get('Carrier', '')).upper()
        if carrier_scac.upper() not in record_carrier:
            if verbose:
                checks.append(f"FAIL: Carrier {carrier_scac} not in {record_carrier[:30]}")
            return False, checks
        checks.append(f"PASS: Carrier {carrier_scac}")

    # Vessel Type match
    vessel_type = rule.get('Vessel_Type', '')
    if vessel_type and pd.notna(vessel_type) and vessel_type.strip():
        record_vtype = str(record.get('Vessel_Type_Simple', '')).upper()
        vessel_types = [v.strip().upper() for v in str(vessel_type).split(';')]
        if not any(vt in record_vtype for vt in vessel_types):
            if verbose:
                checks.append(f"FAIL: Vessel type {vessel_type} not matched")
            return False, checks
        checks.append(f"PASS: Vessel type {vessel_type}")

    # HS Code matches
    for hs_level in ['HS2', 'HS4', 'HS6']:
        rule_hs = rule.get(hs_level, '')
        if rule_hs and pd.notna(rule_hs) and rule_hs.strip():
            record_hs = str(record.get(hs_level, '')).strip()
            if rule_hs.strip() != record_hs:
                if verbose:
                    checks.append(f"FAIL: {hs_level} {rule_hs} != {record_hs}")
                return False, checks
            checks.append(f"PASS: {hs_level} = {rule_hs}")

    # Keyword match
    cargo_desc = str(record.get('Goods Shipped', ''))
    if not check_keyword_match(cargo_desc, rule):
        if verbose:
            checks.append(f"FAIL: Keywords not matched in: {cargo_desc[:40]}")
        return False, checks
    checks.append("PASS: Keywords matched")

    # Tonnage filter
    min_tons = rule.get('Min_Tons', '')
    max_tons = rule.get('Max_Tons', '')
    if (min_tons and pd.notna(min_tons) and min_tons.strip()) or \
       (max_tons and pd.notna(max_tons) and max_tons.strip()):
        try:
            record_tons = float(str(record.get('Tons', '0')).replace(',', ''))
            if min_tons and pd.notna(min_tons) and min_tons.strip():
                if record_tons < float(min_tons):
                    if verbose:
                        checks.append(f"FAIL: Tons {record_tons} < {min_tons}")
                    return False, checks
            if max_tons and pd.notna(max_tons) and max_tons.strip():
                if record_tons > float(max_tons):
                    if verbose:
                        checks.append(f"FAIL: Tons {record_tons} > {max_tons}")
                    return False, checks
            checks.append(f"PASS: Tonnage in range")
        except:
            pass

    return True, checks

def can_apply_rule(record, rule):
    """Check if rule can be applied based on lock levels"""

    # Check Exclude_Groups
    exclude_groups = rule.get('Exclude_Groups', '')
    if exclude_groups and pd.notna(exclude_groups) and exclude_groups.strip():
        current_group = str(record.get('Group', '')).strip()
        if current_group:
            exclude_list = [g.strip() for g in str(exclude_groups).split(';')]
            if current_group in exclude_list:
                return False

    # Check lock levels
    if record.get('Group_Locked') == 'TRUE':
        rule_group = str(rule.get('Group', '')).strip()
        current_group = str(record.get('Group', '')).strip()
        if rule_group and current_group and rule_group != current_group:
            return False

    if record.get('Commodity_Locked') == 'TRUE':
        rule_commodity = str(rule.get('Commodity', '')).strip()
        current_commodity = str(record.get('Commodity', '')).strip()
        if rule_commodity and current_commodity and rule_commodity != current_commodity:
            return False

    if record.get('Cargo_Locked') == 'TRUE':
        rule_cargo = str(rule.get('Cargo', '')).strip()
        current_cargo = str(record.get('Cargo', '')).strip()
        if rule_cargo and current_cargo and rule_cargo != current_cargo:
            return False

    if record.get('Cargo_Detail_Locked') == 'TRUE':
        return False

    return True

def apply_rule(record, rule):
    """Apply rule to record - CRITICAL: Check column alignment"""

    def clean_value(val):
        """Convert nan/empty to TBN"""
        if not val or pd.isna(val):
            return 'TBN'
        val_str = str(val).strip()
        if not val_str or val_str.lower() == 'nan':
            return 'TBN'
        return val_str

    # Set taxonomy values from rule
    group = rule.get('Group', '')
    if group and pd.notna(group) and str(group).strip() and str(group).strip().lower() != 'nan':
        record['Group'] = group

    commodity = rule.get('Commodity', '')
    record['Commodity'] = clean_value(commodity)

    cargo = rule.get('Cargo', '')
    record['Cargo'] = clean_value(cargo)

    # CRITICAL: Dictionary uses 'Cargo_Detail' (underscore) but data column is 'Cargo Detail' (space)
    cargo_detail = rule.get('Cargo_Detail', '')
    record['Cargo Detail'] = clean_value(cargo_detail)

    # Set lock status
    if rule.get('Lock_Group') == 'TRUE':
        record['Group_Locked'] = 'TRUE'
    if rule.get('Lock_Commodity') == 'TRUE':
        record['Commodity_Locked'] = 'TRUE'
    if rule.get('Lock_Cargo') == 'TRUE':
        record['Cargo_Locked'] = 'TRUE'
    if rule.get('Lock_Cargo_Detail') == 'TRUE':
        record['Cargo_Detail_Locked'] = 'TRUE'

    # Track classification
    if not record.get('Classified_Phase'):
        record['Classified_Phase'] = rule.get('Phase', '')
    record['Last_Rule_ID'] = rule.get('Rule_ID', '')

    return record

def classify_with_diagnostics(df, df_dict):
    """Classify records with detailed diagnostics"""
    diagnostic_section("STEP 4: Classification with Diagnostics")

    # Initialize classification columns (use existing columns if present, otherwise create)
    stamp("Initializing classification columns...")
    if 'Group' not in df.columns:
        df['Group'] = ''
    if 'Commodity' not in df.columns:
        df['Commodity'] = ''
    if 'Cargo' not in df.columns:
        df['Cargo'] = ''
    if 'Cargo Detail' not in df.columns:
        df['Cargo Detail'] = ''

    df['Group_Locked'] = 'FALSE'
    df['Commodity_Locked'] = 'FALSE'
    df['Cargo_Locked'] = 'FALSE'
    df['Cargo_Detail_Locked'] = 'FALSE'
    df['Classified_Phase'] = ''
    df['Last_Rule_ID'] = ''

    # Process by phase
    phases = sorted(df_dict['Phase'].astype(int).unique())

    phase_stats = []

    for phase in phases:
        stamp(f"\n--- Processing Phase {phase} ---", "PHASE")
        phase_rules = df_dict[df_dict['Phase'] == str(phase)]
        stamp(f"Rules in phase: {len(phase_rules)}")

        phase_matches = 0
        match_examples = []

        for idx, record in df.iterrows():
            # Skip if fully locked
            if record['Cargo_Detail_Locked'] == 'TRUE':
                continue

            # Try each rule
            for _, rule in phase_rules.iterrows():
                matched, checks = check_match(record, rule, verbose=(idx < 10))

                if matched and can_apply_rule(record, rule):
                    df.loc[idx] = apply_rule(record, rule)
                    phase_matches += 1

                    # Store example
                    if len(match_examples) < 3:
                        match_examples.append({
                            'record_idx': idx,
                            'rule_id': rule['Rule_ID'],
                            'vessel': record['Vessel'],
                            'goods': str(record['Goods Shipped'])[:40],
                            'group': rule['Group']
                        })

                    break  # First match wins

        stamp(f"Matched: {phase_matches:,} records", "SUCCESS")

        # Show examples
        if match_examples:
            stamp("  Examples:")
            for ex in match_examples:
                stamp(f"    [{ex['record_idx']}] {ex['rule_id']:30s} => {ex['group']}")

        phase_stats.append({
            'Phase': phase,
            'Rules': len(phase_rules),
            'Matches': phase_matches
        })

    # Overall stats
    stamp("\n--- Phase Summary ---", "SUMMARY")
    for stat in phase_stats:
        stamp(f"  Phase {stat['Phase']}: {stat['Matches']:5,} records from {stat['Rules']:3d} rules")

    classified = len(df[df['Group'] != ''])
    stamp(f"\nTotal classified: {classified:,} / {len(df):,} ({classified/len(df)*100:.1f}%)", "SUCCESS")

    return df

# ============================================================================
# STEP 5: Column validation
# ============================================================================

def validate_columns(df):
    """Validate column alignment and data integrity"""
    diagnostic_section("STEP 5: Column Validation & Data Integrity")

    stamp("Checking classification columns exist:")
    class_cols = ['Group', 'Commodity', 'Cargo', 'Cargo Detail']
    for col in class_cols:
        if col in df.columns:
            non_empty = len(df[df[col].notna() & (df[col] != '')])
            stamp(f"  OK {col:20s} - {non_empty:,} non-empty", "OK")
        else:
            stamp(f"  !! {col:20s} - MISSING!", "ERROR")

    # Check for data in columns
    stamp("\nSample classified records:")
    classified = df[df['Group'] != ''].head(10)
    for idx, row in classified.iterrows():
        stamp(f"  [{idx}] {row['Group']:15s} | {row['Commodity']:20s} | {row['Cargo']:20s}")

    # Check for TBN values
    stamp("\nTBN (To Be Named) counts:")
    for col in ['Commodity', 'Cargo', 'Cargo Detail']:
        if col in df.columns:
            tbn_count = len(df[df[col] == 'TBN'])
            stamp(f"  {col:20s}: {tbn_count:,} TBN values")

    # Unclassified records
    unclassified = df[df['Group'] == '']
    stamp(f"\nUnclassified records: {len(unclassified):,}")
    if len(unclassified) > 0:
        stamp("Sample unclassified (first 5):")
        for idx, row in unclassified.head(5).iterrows():
            stamp(f"  [{idx}] HS{row['HS2']} | {str(row['Goods Shipped'])[:50]}")

    return df

# ============================================================================
# STEP 6: Save results
# ============================================================================

def save_results(df):
    """Save diagnostic results"""
    diagnostic_section("STEP 6: Saving Results")

    output_file = OUTPUT_DIR / "diagnostic_5k_classified.csv"
    stamp(f"Writing: {output_file}")
    df.to_csv(output_file, index=False)
    stamp("File saved successfully", "SUCCESS")

    # Save summary stats
    stats_file = OUTPUT_DIR / "diagnostic_5k_stats.csv"
    stats = []

    total = len(df)
    classified = len(df[df['Group'] != ''])

    stats.append({'Metric': 'Total Records', 'Count': total, 'Percentage': '100.0%'})
    stats.append({'Metric': 'Classified', 'Count': classified, 'Percentage': f'{classified/total*100:.1f}%'})
    stats.append({'Metric': 'Unclassified', 'Count': total - classified, 'Percentage': f'{(total-classified)/total*100:.1f}%'})

    # By phase
    for phase in sorted(df['Classified_Phase'].unique()):
        if phase:
            count = len(df[df['Classified_Phase'] == phase])
            stats.append({'Metric': f'Phase {phase}', 'Count': count, 'Percentage': f'{count/total*100:.1f}%'})

    # By group
    for group in df.groupby('Group').size().sort_values(ascending=False).index[:10]:
        if group:
            count = len(df[df['Group'] == group])
            stats.append({'Metric': f'Group: {group}', 'Count': count, 'Percentage': f'{count/total*100:.1f}%'})

    pd.DataFrame(stats).to_csv(stats_file, index=False)
    stamp(f"Stats saved: {stats_file.name}", "SUCCESS")

    stamp("\nOutput files:")
    stamp(f"  - {output_file.name}")
    stamp(f"  - {stats_file.name}")

# ============================================================================
# MAIN
# ============================================================================

def main():
    """Main diagnostic execution"""
    print("\n" + "=" * 80)
    print("  DIAGNOSTIC: 5K Classification Test with Column Validation")
    print("=" * 80)

    try:
        # Step 1: Load sample
        df = load_sample()
        if df is None:
            return

        # Step 2: Add vessel types
        df = add_vessel_types(df)

        # Step 3: Load dictionary
        df_dict = load_dictionary()
        if df_dict is None:
            return

        # Step 4: Classify with diagnostics
        df = classify_with_diagnostics(df, df_dict)

        # Step 5: Validate columns
        df = validate_columns(df)

        # Step 6: Save results
        save_results(df)

        print("\n" + "=" * 80)
        stamp("DIAGNOSTIC COMPLETE - Review output files for detailed analysis", "SUCCESS")
        print("=" * 80 + "\n")

    except Exception as e:
        stamp(f"ERROR: {str(e)}", "ERROR")
        stamp(traceback.format_exc(), "ERROR")

if __name__ == "__main__":
    main()

"""
Classification Test for v2.0.0 - 15K Validation
================================================

Tests classification on 15K sample from 2024 v2.0.0 AUTHORITATIVE data.
This validates that v2.0.0 pipeline works correctly before full production run.

Changes from 5K test:
- Uses 15K records (larger validation sample)
- Reads from AUTHORITATIVE v2.0.0 file
- Same classification logic

Input: panjiva_imports_2024_AUTHORITATIVE_v2.0.0.csv (first 15K records)
Output: Classified CSV + statistics

Author: WSD3 / Claude Code
Date: 2026-01-29
Version: 2.0.0
"""

import pandas as pd
from pathlib import Path
from datetime import datetime

# Paths
INPUT_FILE = Path(r"G:\My Drive\LLM\project_manifest\00_DATA\00.02_PREPROCESSED\panjiva_imports_2024_AUTHORITATIVE_v2.0.0.csv")
DICTIONARY = Path(r"G:\My Drive\LLM\project_manifest\01_DICTIONARIES\01.01_cargo_classification\cargo_classification_dictionary_CURRENT_v3.6.0.csv")
OUTPUT_DIR = Path(r"G:\My Drive\LLM\project_manifest\00_DATA\00.03_MATCHED")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE = OUTPUT_DIR / "sample_15k_classified_v2.0.0_validation.csv"
STATS_FILE = OUTPUT_DIR / "classification_stats_v2.0.0_15k_validation.csv"

SAMPLE_SIZE = 15000

def stamp(msg):
    """Print timestamped message"""
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

def load_data():
    """Load 15K sample from preprocessed v2.0.0 data"""
    stamp("=== Loading Preprocessed Data ===")
    stamp(f"Reading: {INPUT_FILE}")
    stamp(f"Sample size: {SAMPLE_SIZE:,} records")

    df = pd.read_csv(INPUT_FILE, dtype=str, nrows=SAMPLE_SIZE)
    stamp(f"Loaded {len(df):,} records with {len(df.columns)} columns")

    # Verify required columns exist
    required_cols = ['Group', 'Commodity', 'Cargo', 'Cargo Detail',
                     'Group_Locked', 'Commodity_Locked', 'Cargo_Locked', 'Cargo_Detail_Locked',
                     'Vessel_Type_Simple', 'Classified_Phase', 'Last_Rule_ID']

    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        stamp(f"ERROR: Missing required columns: {missing}")
        raise ValueError(f"Missing columns: {missing}")

    stamp(f"All required columns present")

    # Check vessel enrichment status
    vessel_populated = (df['Vessel_Type_Simple'].notna() & (df['Vessel_Type_Simple'] != '')).sum()
    stamp(f"Vessel types populated: {vessel_populated:,} / {len(df)} ({vessel_populated/len(df)*100:.1f}%)")

    return df

def load_dictionary():
    """Load classification dictionary"""
    stamp("\n=== Loading Dictionary ===")
    stamp(f"Reading: {DICTIONARY}")

    df_dict = pd.read_csv(DICTIONARY, dtype=str)
    stamp(f"Loaded {len(df_dict)} total rules")

    # Filter to active rules only
    df_dict = df_dict[df_dict['Active'].str.upper() == 'TRUE'].copy()
    stamp(f"Active rules: {len(df_dict)}")

    return df_dict

def check_match(record, rule):
    """Check if record matches rule criteria"""

    # Check Carrier SCAC
    if pd.notna(rule.get('Carrier_SCAC')) and rule['Carrier_SCAC'] != '':
        carrier_scac = str(rule['Carrier_SCAC']).upper()
        record_carrier = str(record.get('Carrier', '')).upper()
        if carrier_scac not in record_carrier:
            return False

    # Check Vessel Type
    if pd.notna(rule.get('Vessel_Type')) and rule['Vessel_Type'] != '':
        rule_vessel_type = str(rule['Vessel_Type']).upper()
        record_vessel_type = str(record.get('Vessel_Type_Simple', '')).upper()
        if rule_vessel_type not in record_vessel_type:
            return False

    # Check HS codes
    for hs_level in ['HS2', 'HS4', 'HS6']:
        if pd.notna(rule.get(hs_level)) and rule[hs_level] != '':
            rule_hs = str(rule[hs_level]).strip()
            record_hs = str(record.get(hs_level, '')).strip()
            if rule_hs != record_hs:
                return False

    # Check Keywords (simple substring match for now)
    if pd.notna(rule.get('Keywords')) and rule['Keywords'] != '':
        keywords = str(rule['Keywords']).upper().split(',')
        goods = str(record.get('Goods Shipped', '')).upper()
        if not any(kw.strip() in goods for kw in keywords):
            return False

    # Check Exclude_Keywords
    if pd.notna(rule.get('Exclude_Keywords')) and rule['Exclude_Keywords'] != '':
        exclude_kws = str(rule['Exclude_Keywords']).upper().split(',')
        goods = str(record.get('Goods Shipped', '')).upper()
        if any(kw.strip() in goods for kw in exclude_kws):
            return False

    # Check Package Type
    if pd.notna(rule.get('Package_Type')) and rule['Package_Type'] != '':
        rule_pkg = str(rule['Package_Type']).upper()
        record_pkg = str(record.get('Package_Type', '')).upper()
        if rule_pkg != record_pkg:
            return False

    return True

def can_apply_rule(record, rule):
    """Check if rule can be applied based on locks"""

    # Check if Group is locked
    if str(record.get('Group_Locked', 'FALSE')).upper() == 'TRUE':
        if str(record.get('Group', '')) != '':
            return False  # Group already locked, can't override

    # Check if trying to change a locked commodity
    if str(record.get('Commodity_Locked', 'FALSE')).upper() == 'TRUE':
        if str(record.get('Commodity', '')) != '':
            return False

    # Check if trying to change a locked cargo
    if str(record.get('Cargo_Locked', 'FALSE')).upper() == 'TRUE':
        if str(record.get('Cargo', '')) != '':
            return False

    # Check if trying to change a locked cargo detail
    if str(record.get('Cargo_Detail_Locked', 'FALSE')).upper() == 'TRUE':
        if str(record.get('Cargo Detail', '')) != '':
            return False

    return True

def apply_rule(record, rule):
    """Apply rule to record (set classification + locks)"""

    # Set classification fields
    if pd.notna(rule.get('Group')) and rule['Group'] != '':
        record['Group'] = rule['Group']

    if pd.notna(rule.get('Commodity')) and rule['Commodity'] != '':
        record['Commodity'] = rule['Commodity']

    if pd.notna(rule.get('Cargo')) and rule['Cargo'] != '':
        record['Cargo'] = rule['Cargo']

    if pd.notna(rule.get('Cargo_Detail')) and rule['Cargo_Detail'] != '':
        record['Cargo Detail'] = rule['Cargo_Detail']

    # Set lock flags
    if str(rule.get('Lock_Group', 'FALSE')).upper() == 'TRUE':
        record['Group_Locked'] = 'TRUE'

    if str(rule.get('Lock_Commodity', 'FALSE')).upper() == 'TRUE':
        record['Commodity_Locked'] = 'TRUE'

    if str(rule.get('Lock_Cargo', 'FALSE')).upper() == 'TRUE':
        record['Cargo_Locked'] = 'TRUE'

    if str(rule.get('Lock_Cargo_Detail', 'FALSE')).upper() == 'TRUE':
        record['Cargo_Detail_Locked'] = 'TRUE'

    # Set tracking fields
    record['Classified_Phase'] = rule.get('Phase', '')
    record['Last_Rule_ID'] = rule.get('Rule_ID', '')

    return record

def classify_in_phases(df, df_dict):
    """Classify records by phase"""
    stamp("\n=== Classifying Records ===")

    # Get unique phases, sorted
    phases = sorted([int(p) for p in df_dict['Phase'].unique() if pd.notna(p) and p != ''])
    stamp(f"Phases to process: {phases}")

    for phase in phases:
        stamp(f"\nProcessing Phase {phase}...")

        # Filter rules for this phase
        phase_rules = df_dict[df_dict['Phase'] == str(phase)].copy()
        stamp(f"  Rules in phase: {len(phase_rules)}")

        phase_matches = 0

        # Process each record
        for idx in df.index:
            record = df.loc[idx].copy()

            # Try each rule in phase
            for _, rule in phase_rules.iterrows():
                # Check if rule matches AND can be applied (lock check)
                if check_match(record, rule) and can_apply_rule(record, rule):
                    # Apply rule
                    df.loc[idx] = apply_rule(record, rule)
                    phase_matches += 1
                    break  # First match wins in phase

        stamp(f"  Matched: {phase_matches} records")

    # Count classified
    classified = (df['Group'].notna() & (df['Group'] != '')).sum()
    stamp(f"\nTotal classified: {classified} / {len(df)} ({classified/len(df)*100:.1f}%)")

    return df

def generate_stats(df):
    """Generate classification statistics"""
    stamp("\n=== Generating Statistics ===")

    stats = []

    # Overall stats
    total = len(df)
    classified = (df['Group'].notna() & (df['Group'] != '')).sum()
    stats.append({
        'Metric': 'Total Records',
        'Count': total,
        'Percentage': '100.0%'
    })
    stats.append({
        'Metric': 'Classified',
        'Count': classified,
        'Percentage': f'{classified/total*100:.1f}%'
    })
    stats.append({
        'Metric': 'Unclassified',
        'Count': total - classified,
        'Percentage': f'{(total-classified)/total*100:.1f}%'
    })

    # By Phase
    stats.append({'Metric': '', 'Count': '', 'Percentage': ''})
    stats.append({'Metric': 'By Phase:', 'Count': '', 'Percentage': ''})

    phase_counts = df[df['Classified_Phase'].notna() & (df['Classified_Phase'] != '')]['Classified_Phase'].value_counts()
    for phase in sorted([int(p) for p in phase_counts.index]):
        count = phase_counts[str(phase)]
        stats.append({
            'Metric': f'  Phase {phase}',
            'Count': count,
            'Percentage': f'{count/total*100:.1f}%'
        })

    # By Group
    stats.append({'Metric': '', 'Count': '', 'Percentage': ''})
    stats.append({'Metric': 'By Group:', 'Count': '', 'Percentage': ''})

    group_counts = df[df['Group'].notna() & (df['Group'] != '')]['Group'].value_counts()
    for group, count in group_counts.items():
        stats.append({
            'Metric': f'  {group}',
            'Count': count,
            'Percentage': f'{count/total*100:.1f}%'
        })

    df_stats = pd.DataFrame(stats)
    stamp(f"Generated {len(stats)} statistics")

    return df_stats

def main():
    """Main classification pipeline"""
    try:
        stamp("\n" + "="*80)
        stamp("CLASSIFICATION VALIDATION TEST - 15K Sample v2.0.0")
        stamp("="*80)
        stamp(f"Start time: {datetime.now()}")

        # Load data
        df = load_data()

        # Load dictionary
        df_dict = load_dictionary()

        # Classify
        df = classify_in_phases(df, df_dict)

        # Generate statistics
        df_stats = generate_stats(df)

        # Save outputs
        stamp("\n=== Saving Outputs ===")
        df.to_csv(OUTPUT_FILE, index=False)
        stamp(f"Saved classified data: {OUTPUT_FILE}")

        df_stats.to_csv(STATS_FILE, index=False)
        stamp(f"Saved statistics: {STATS_FILE}")

        stamp("\n" + "="*80)
        stamp("VALIDATION TEST COMPLETE")
        stamp("="*80)
        stamp(f"End time: {datetime.now()}")

    except Exception as e:
        stamp("\n" + "="*80)
        stamp("VALIDATION TEST FAILED")
        stamp("="*80)
        stamp(f"Error: {str(e)}")
        import traceback
        stamp(f"Traceback:\n{traceback.format_exc()}")
        raise

if __name__ == "__main__":
    main()

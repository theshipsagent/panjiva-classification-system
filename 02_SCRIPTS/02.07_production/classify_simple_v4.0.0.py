"""
Simple Classification Script v4.0.0
Replaces overcomplicated 668-rule system with 46-rule sequential classifier

Sequential Execution (Order Matters!):
  Phase 1: Carrier Filter #1 (RoRo, Reefer, Exclusions) - LOCK ALL
  Phase 2: Carrier Filter #2 (Dry/Liquid/Gas by vessel type) - LOCK GROUP ONLY
  Phase 3: White Noise Filter (Exclusions)
  Phase 4: First Pass Keywords (Commodity classification)
"""

import pandas as pd
import sys
from pathlib import Path
from datetime import datetime

# Configuration
DICTIONARY = Path(r"G:\My Drive\LLM\project_manifest\01_DICTIONARIES\01.01_cargo_classification\cargo_classification_dictionary_v4.0.0_SIMPLE.csv")
INPUT_FILE = Path(r"G:\My Drive\LLM\project_manifest\panjiva_2023_RAW_SAMPLE_15K_for_manual_classification.csv")
OUTPUT_FILE = Path(r"G:\My Drive\LLM\project_manifest\00_DATA\00.03_MATCHED\panjiva_2023_SIMPLE_15K_classified_v4.0.0.csv")
STATS_FILE = Path(r"G:\My Drive\LLM\project_manifest\00_DATA\00.03_MATCHED\classification_stats_2023_v4.0.0_SIMPLE.csv")

def load_dictionary():
    """Load classification dictionary"""
    print(f"\nLoading dictionary: {DICTIONARY.name}")
    df_dict = pd.read_csv(DICTIONARY, dtype=str)
    df_dict = df_dict[df_dict['Active'] == 'TRUE']
    print(f"  Loaded {len(df_dict)} active rules")
    print(f"  Phases: {sorted(df_dict['Phase'].unique())}")
    return df_dict

def check_match(record, rule):
    """Check if record matches rule criteria"""

    # Carrier SCAC match (substring, pipe-separated list)
    if pd.notna(rule['Carrier_SCAC']) and rule['Carrier_SCAC'].strip():
        carrier_scacs = [s.strip().upper() for s in rule['Carrier_SCAC'].split('|')]
        record_carrier = str(record.get('Carrier', '')).upper()
        if not any(scac in record_carrier for scac in carrier_scacs):
            return False

    # Vessel Type match
    if pd.notna(rule['Vessel_Type']) and rule['Vessel_Type'].strip():
        if str(record.get('Vessel_Type_Simple', '')).upper() != rule['Vessel_Type'].upper():
            return False

    # Package Type match (pipe-separated list)
    if pd.notna(rule['Package_Type']) and rule['Package_Type'].strip():
        package_types = [s.strip().upper() for s in rule['Package_Type'].split('|')]
        record_package = str(record.get('Package_Type', '')).upper()
        if record_package not in package_types:
            return False

    # HS2 match (normalize: "27.0" → "27", "27" → "27")
    if pd.notna(rule['HS2']) and rule['HS2'].strip():
        record_hs2 = str(record.get('HS2', '')).replace('.0', '')
        rule_hs2 = str(rule['HS2']).replace('.0', '')
        if record_hs2 != rule_hs2:
            return False

    # HS4 match (normalize: "2709.0" → "2709", "2709" → "2709")
    if pd.notna(rule['HS4']) and rule['HS4'].strip():
        record_hs4 = str(record.get('HS4', '')).replace('.0', '')
        rule_hs4 = str(rule['HS4']).replace('.0', '')
        if record_hs4 != rule_hs4:
            return False

    # Keywords match (pipe-separated, substring match in Goods Shipped)
    if pd.notna(rule['Keywords']) and rule['Keywords'].strip():
        keywords = [s.strip().upper() for s in rule['Keywords'].split('|')]
        # Try both column names (Goods Shipped Description or Goods Shipped)
        goods_desc = str(record.get('Goods Shipped Description', record.get('Goods Shipped', ''))).upper()

        # Normalize: remove extra spaces, punctuation for better matching
        import re
        goods_desc = re.sub(r'\s+', ' ', goods_desc)  # Multiple spaces → single space
        goods_desc = re.sub(r"['\"]", '', goods_desc)  # Remove quotes/apostrophes
        goods_desc = goods_desc.strip()

        if not any(kw in goods_desc for kw in keywords):
            return False

    # Tonnage filters
    record_tons = record.get('Tons', 0)
    try:
        record_tons = float(record_tons) if pd.notna(record_tons) else 0
    except:
        record_tons = 0

    # Min tons
    if pd.notna(rule['Min_Tons']) and rule['Min_Tons'] != '':
        try:
            min_tons = float(rule['Min_Tons'])
            if record_tons < min_tons:
                return False
        except:
            pass

    # Max tons
    if pd.notna(rule['Max_Tons']) and rule['Max_Tons'] != '':
        try:
            max_tons = float(rule['Max_Tons'])
            if record_tons > max_tons:
                return False
        except:
            pass

    return True

def can_apply_rule(record, rule):
    """Check if rule can be applied based on lock levels"""

    # If Group is locked, cannot change Group
    if record.get('Group_Locked') == 'TRUE':
        if pd.notna(record.get('Group')) and record.get('Group') != '':
            if record.get('Group') != rule['Group']:
                return False

    # If Commodity is locked, cannot change Commodity
    if record.get('Commodity_Locked') == 'TRUE':
        if pd.notna(record.get('Commodity')) and record.get('Commodity') != '':
            if record.get('Commodity') != rule['Commodity']:
                return False

    # If Cargo is locked, cannot change Cargo
    if record.get('Cargo_Locked') == 'TRUE':
        if pd.notna(record.get('Cargo')) and record.get('Cargo') != '':
            if record.get('Cargo') != rule['Cargo']:
                return False

    # If Cargo_Detail is locked, cannot change anything
    if record.get('Cargo_Detail_Locked') == 'TRUE':
        return False

    return True

def classify_in_phases(df, df_dict):
    """Classify records sequentially through phases 1-4"""

    # Initialize classification columns
    for col in ['Group', 'Commodity', 'Cargo', 'Cargo_Detail',
                'Group_Locked', 'Commodity_Locked', 'Cargo_Locked', 'Cargo_Detail_Locked',
                'Classified_Phase', 'Last_Rule_ID']:
        if col not in df.columns:
            df[col] = ''

    total_records = len(df)
    phase_stats = {}

    # Process each phase sequentially (1, 2, 3, 4)
    for phase_str in sorted(df_dict['Phase'].unique()):
        phase = int(phase_str)
        phase_rules = df_dict[df_dict['Phase'] == phase_str].to_dict('records')

        print(f"\n  Phase {phase}: {len(phase_rules)} rules")
        matched_count = 0

        for idx in df.index:
            record = df.loc[idx]

            # Try each rule in order (can_apply_rule handles lock level checks)
            for rule in phase_rules:
                if check_match(record, rule) and can_apply_rule(record, rule):
                    # Apply rule directly to DataFrame (avoid SettingWithCopyWarning)
                    df.loc[idx, 'Group'] = rule['Group']
                    df.loc[idx, 'Commodity'] = rule['Commodity']
                    df.loc[idx, 'Cargo'] = rule['Cargo']
                    df.loc[idx, 'Cargo_Detail'] = rule['Cargo_Detail']
                    df.loc[idx, 'Group_Locked'] = rule['Lock_Group']
                    df.loc[idx, 'Commodity_Locked'] = rule['Lock_Commodity']
                    df.loc[idx, 'Cargo_Locked'] = rule['Lock_Cargo']
                    df.loc[idx, 'Cargo_Detail_Locked'] = rule['Lock_Cargo_Detail']
                    df.loc[idx, 'Classified_Phase'] = rule['Phase']
                    df.loc[idx, 'Last_Rule_ID'] = rule['Rule_ID']
                    matched_count += 1
                    break  # Stop after first match (priority matters!)

        phase_stats[phase] = matched_count
        pct = (matched_count / total_records * 100) if total_records > 0 else 0
        print(f"    Matched: {matched_count:,} records ({pct:.1f}%)")

    return df, phase_stats

def generate_statistics(df, phase_stats):
    """Generate classification statistics"""

    total = len(df)
    classified = (df['Group'].notna() & (df['Group'] != '')).sum()

    stats = []
    stats.append(['Metric', 'Count', 'Percentage'])
    stats.append(['Total Records', total, '100.0%'])
    stats.append(['Classified', classified, f'{classified/total*100:.1f}%'])
    stats.append(['Unclassified', total - classified, f'{(total-classified)/total*100:.1f}%'])
    stats.append(['', '', ''])

    stats.append(['By Phase:', '', ''])
    for phase in sorted(phase_stats.keys()):
        count = phase_stats[phase]
        pct = (count / total * 100) if total > 0 else 0
        stats.append([f'  Phase {phase}', count, f'{pct:.1f}%'])
    stats.append(['', '', ''])

    stats.append(['By Group:', '', ''])
    for group in df['Group'].value_counts().index:
        count = (df['Group'] == group).sum()
        pct = (count / total * 100) if total > 0 else 0
        stats.append([f'  {group}', count, f'{pct:.1f}%'])

    return pd.DataFrame(stats)

def main():
    print("="*70)
    print("SIMPLE CLASSIFICATION v4.0.0")
    print("="*70)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Load data
    print(f"\nLoading input: {INPUT_FILE.name}")
    df = pd.read_csv(INPUT_FILE, dtype=str, low_memory=False)
    print(f"  Loaded {len(df):,} records with {len(df.columns)} columns")

    # Load dictionary
    df_dict = load_dictionary()

    # Classify
    print(f"\nClassifying records...")
    df, phase_stats = classify_in_phases(df, df_dict)

    # Generate statistics
    print(f"\nGenerating statistics...")
    stats_df = generate_statistics(df, phase_stats)

    # Save results
    print(f"\nSaving results...")
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"  Classified data: {OUTPUT_FILE}")

    stats_df.to_csv(STATS_FILE, index=False, header=False)
    print(f"  Statistics: {STATS_FILE}")

    # Summary
    print(f"\n" + "="*70)
    print("CLASSIFICATION COMPLETE")
    print("="*70)
    classified = (df['Group'].notna() & (df['Group'] != '')).sum()
    print(f"Total Records: {len(df):,}")
    print(f"Classified: {classified:,} ({classified/len(df)*100:.1f}%)")
    print(f"Unclassified: {len(df) - classified:,}")
    print(f"\nPhase Distribution:")
    for phase in sorted(phase_stats.keys()):
        count = phase_stats[phase]
        pct = (count / len(df) * 100) if len(df) > 0 else 0
        print(f"  Phase {phase}: {count:,} ({pct:.1f}%)")
    print(f"\nCompleted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)

if __name__ == '__main__':
    main()

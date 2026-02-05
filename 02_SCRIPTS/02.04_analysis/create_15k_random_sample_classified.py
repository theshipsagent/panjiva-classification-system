"""
Create Random 15K Sample and Classify
======================================

Creates a random sample of 15K records from 2024 v2.0.0 data,
classifies it, and saves for user review.

Author: WSD3 / Claude Code
Date: 2026-01-28
"""

import pandas as pd
from pathlib import Path
from datetime import datetime
import numpy as np

def stamp(msg):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

# Paths
INPUT_FILE = Path(r"G:\My Drive\LLM\project_manifest\00_DATA\00.02_PREPROCESSED\panjiva_imports_2024_AUTHORITATIVE_v2.0.0.csv")
DICTIONARY = Path(r"G:\My Drive\LLM\project_manifest\01_DICTIONARIES\01.01_cargo_classification\cargo_classification_dictionary_CURRENT_v3.6.0.csv")
OUTPUT_DIR = Path(r"G:\My Drive\LLM\project_manifest\05_USER_NOTES")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE = OUTPUT_DIR / "sample_15k_classified_REVIEW.csv"
STATS_FILE = OUTPUT_DIR / "sample_15k_stats_REVIEW.csv"

def load_dictionary():
    """Load classification dictionary"""
    stamp("Loading dictionary...")
    df_dict = pd.read_csv(DICTIONARY, dtype=str)
    df_dict = df_dict[df_dict['Active'].str.upper() == 'TRUE'].copy()
    stamp(f"  Active rules: {len(df_dict)}")
    return df_dict

def check_match(record, rule):
    """Check if record matches rule criteria"""
    if pd.notna(rule.get('Carrier_SCAC')) and rule['Carrier_SCAC'] != '':
        carrier_scac = str(rule['Carrier_SCAC']).upper()
        record_carrier = str(record.get('Carrier', '')).upper()
        if carrier_scac not in record_carrier:
            return False

    if pd.notna(rule.get('Vessel_Type')) and rule['Vessel_Type'] != '':
        rule_vessel_type = str(rule['Vessel_Type']).upper()
        record_vessel_type = str(record.get('Vessel_Type_Simple', '')).upper()
        if rule_vessel_type not in record_vessel_type:
            return False

    for hs_level in ['HS2', 'HS4', 'HS6']:
        if pd.notna(rule.get(hs_level)) and rule[hs_level] != '':
            rule_hs = str(rule[hs_level]).strip()
            record_hs = str(record.get(hs_level, '')).strip()
            if rule_hs != record_hs:
                return False

    if pd.notna(rule.get('Keywords')) and rule['Keywords'] != '':
        keywords = str(rule['Keywords']).upper().split(',')
        goods = str(record.get('Goods Shipped', '')).upper()
        if not any(kw.strip() in goods for kw in keywords):
            return False

    if pd.notna(rule.get('Exclude_Keywords')) and rule['Exclude_Keywords'] != '':
        exclude_kws = str(rule['Exclude_Keywords']).upper().split(',')
        goods = str(record.get('Goods Shipped', '')).upper()
        if any(kw.strip() in goods for kw in exclude_kws):
            return False

    if pd.notna(rule.get('Package_Type')) and rule['Package_Type'] != '':
        rule_pkg = str(rule['Package_Type']).upper()
        record_pkg = str(record.get('Package_Type', '')).upper()
        if rule_pkg != record_pkg:
            return False

    return True

def can_apply_rule(record, rule):
    """Check if rule can be applied based on locks"""
    if str(record.get('Group_Locked', 'FALSE')).upper() == 'TRUE':
        if str(record.get('Group', '')) != '':
            return False
    if str(record.get('Commodity_Locked', 'FALSE')).upper() == 'TRUE':
        if str(record.get('Commodity', '')) != '':
            return False
    if str(record.get('Cargo_Locked', 'FALSE')).upper() == 'TRUE':
        if str(record.get('Cargo', '')) != '':
            return False
    if str(record.get('Cargo_Detail_Locked', 'FALSE')).upper() == 'TRUE':
        if str(record.get('Cargo Detail', '')) != '':
            return False
    return True

def apply_rule(record, rule):
    """Apply rule to record"""
    if pd.notna(rule.get('Group')) and rule['Group'] != '':
        record['Group'] = rule['Group']
    if pd.notna(rule.get('Commodity')) and rule['Commodity'] != '':
        record['Commodity'] = rule['Commodity']
    if pd.notna(rule.get('Cargo')) and rule['Cargo'] != '':
        record['Cargo'] = rule['Cargo']
    if pd.notna(rule.get('Cargo_Detail')) and rule['Cargo_Detail'] != '':
        record['Cargo Detail'] = rule['Cargo_Detail']

    if str(rule.get('Lock_Group', 'FALSE')).upper() == 'TRUE':
        record['Group_Locked'] = 'TRUE'
    if str(rule.get('Lock_Commodity', 'FALSE')).upper() == 'TRUE':
        record['Commodity_Locked'] = 'TRUE'
    if str(rule.get('Lock_Cargo', 'FALSE')).upper() == 'TRUE':
        record['Cargo_Locked'] = 'TRUE'
    if str(rule.get('Lock_Cargo_Detail', 'FALSE')).upper() == 'TRUE':
        record['Cargo_Detail_Locked'] = 'TRUE'

    record['Classified_Phase'] = rule.get('Phase', '')
    record['Last_Rule_ID'] = rule.get('Rule_ID', '')

    return record

def classify_in_phases(df, df_dict):
    """Classify records by phase"""
    stamp("\nClassifying records...")
    phases = sorted([int(p) for p in df_dict['Phase'].unique() if pd.notna(p) and p != ''])
    stamp(f"  Phases: {phases}")

    for phase in phases:
        phase_rules = df_dict[df_dict['Phase'] == str(phase)].copy()
        phase_matches = 0

        for idx in df.index:
            record = df.loc[idx].copy()
            for _, rule in phase_rules.iterrows():
                if check_match(record, rule) and can_apply_rule(record, rule):
                    df.loc[idx] = apply_rule(record, rule)
                    phase_matches += 1
                    break

        stamp(f"  Phase {phase}: {phase_matches} records")

    classified = (df['Group'].notna() & (df['Group'] != '')).sum()
    stamp(f"\nTotal classified: {classified:,} / {len(df):,} ({classified/len(df)*100:.1f}%)")

    return df

def generate_stats(df):
    """Generate classification statistics"""
    stamp("\nGenerating statistics...")

    stats = []
    total = len(df)
    classified = (df['Group'].notna() & (df['Group'] != '')).sum()

    stats.append({'Metric': 'Total Records', 'Count': total, 'Percentage': '100.0%'})
    stats.append({'Metric': 'Classified', 'Count': classified, 'Percentage': f'{classified/total*100:.1f}%'})
    stats.append({'Metric': 'Unclassified', 'Count': total - classified, 'Percentage': f'{(total-classified)/total*100:.1f}%'})

    # By Phase
    stats.append({'Metric': '', 'Count': '', 'Percentage': ''})
    stats.append({'Metric': 'By Phase:', 'Count': '', 'Percentage': ''})
    phase_counts = df[df['Classified_Phase'].notna() & (df['Classified_Phase'] != '')]['Classified_Phase'].value_counts()
    for phase in sorted([int(p) for p in phase_counts.index]):
        count = phase_counts[str(phase)]
        stats.append({'Metric': f'  Phase {phase}', 'Count': count, 'Percentage': f'{count/total*100:.1f}%'})

    # By Group
    stats.append({'Metric': '', 'Count': '', 'Percentage': ''})
    stats.append({'Metric': 'By Group:', 'Count': '', 'Percentage': ''})
    group_counts = df[df['Group'].notna() & (df['Group'] != '')]['Group'].value_counts()
    for group, count in group_counts.items():
        stats.append({'Metric': f'  {group}', 'Count': count, 'Percentage': f'{count/total*100:.1f}%'})

    # By Commodity (top 10)
    stats.append({'Metric': '', 'Count': '', 'Percentage': ''})
    stats.append({'Metric': 'Top 10 Commodities:', 'Count': '', 'Percentage': ''})
    commodity_counts = df[df['Commodity'].notna() & (df['Commodity'] != '')]['Commodity'].value_counts().head(10)
    for commodity, count in commodity_counts.items():
        stats.append({'Metric': f'  {commodity}', 'Count': count, 'Percentage': f'{count/total*100:.1f}%'})

    return pd.DataFrame(stats)

def main():
    stamp("="*80)
    stamp("CREATING 15K RANDOM SAMPLE FOR REVIEW")
    stamp("="*80)

    # Load data and sample randomly
    stamp("\n[1/4] Loading and sampling data...")
    stamp(f"  Reading: {INPUT_FILE.name}")

    # Read file and get random sample
    df_full = pd.read_csv(INPUT_FILE, dtype=str, low_memory=False)
    stamp(f"  Total records: {len(df_full):,}")

    # Random sample of 15K
    np.random.seed(42)  # For reproducibility
    sample_indices = np.random.choice(df_full.index, size=15000, replace=False)
    df = df_full.loc[sample_indices].reset_index(drop=True)
    stamp(f"  Sampled: 15,000 random records")
    stamp(f"  Columns: {len(df.columns)}")

    # Load dictionary
    stamp("\n[2/4] Loading dictionary...")
    df_dict = load_dictionary()

    # Classify
    stamp("\n[3/4] Classifying...")
    df = classify_in_phases(df, df_dict)

    # Generate stats
    df_stats = generate_stats(df)

    # Save outputs
    stamp("\n[4/4] Saving outputs...")
    df.to_csv(OUTPUT_FILE, index=False)
    stamp(f"  Saved: {OUTPUT_FILE.name}")
    stamp(f"  Size: {OUTPUT_FILE.stat().st_size / (1024*1024):.1f} MB")

    df_stats.to_csv(STATS_FILE, index=False)
    stamp(f"  Saved: {STATS_FILE.name}")

    stamp("\n" + "="*80)
    stamp("SAMPLE READY FOR REVIEW")
    stamp("="*80)
    stamp(f"\nReview file: {OUTPUT_FILE}")
    stamp(f"Statistics: {STATS_FILE}")

if __name__ == "__main__":
    main()

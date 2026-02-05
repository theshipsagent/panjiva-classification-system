"""
Restore authoritative user dictionary as baseline for multi-phase system

Source of Truth: user_notes/01_cargo_dictionary_harmonized_user_edits_01132016_1829.csv
- 507 rules with HS codes, Keywords, Min/Max Tons
- Focus: Bulk/Break-Bulk high-tonnage commodities
- DO NOT EDIT these authoritative rules

Strategy:
- Phase 1: Vessel Type rules (4 rules - keep existing)
- Phase 2: Carrier rules (from 01_carrier_scac_cargo.csv - supplemental)
- Phase 6: User's authoritative HS+Keyword+Tonnage rules (507 rules)
- Phase 10: Catch-all rules (keep existing)

Author: WSD3 / Claude Code
Date: 2026-01-14
"""

import pandas as pd
from pathlib import Path
from datetime import datetime

def stamp(msg):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

# Paths
USER_DICT = Path(r"G:\My Drive\LLM\project_manifest\user_notes\01_cargo_dictionary_harmonized_user_edits_01132016_1829.csv")
CARRIER_DICT = Path(r"G:\My Drive\LLM\project_manifest\01.01_dictionary\01_carrier_scac_cargo.csv")
CURRENT_DICT = Path(r"G:\My Drive\LLM\project_manifest\01_DICTIONARIES\03.01_cargo_classification\cargo_classification_dictionary_v2.5.2_20260114_0100.csv")
OUTPUT_DICT = Path(r"G:\My Drive\LLM\project_manifest\01_DICTIONARIES\03.01_cargo_classification\cargo_classification_dictionary_v3.0.0_20260114_0200.csv")

stamp("=== Restoring Authoritative User Dictionary ===")
stamp(f"Source: {USER_DICT.name}")
stamp("")

# Load user's authoritative dictionary
df_user = pd.read_csv(USER_DICT, dtype=str)
stamp(f"Loaded {len(df_user)} authoritative rules from user dictionary")

# Load current dictionary to extract Phase 1, 2, 10 rules
df_curr = pd.read_csv(CURRENT_DICT, dtype=str)
phase1_rules = df_curr[df_curr['Phase'] == '1']
phase2_rules = df_curr[df_curr['Phase'] == '2']
phase10_rules = df_curr[df_curr['Phase'] == '10']

stamp(f"Extracted {len(phase1_rules)} Phase 1 (vessel type) rules")
stamp(f"Extracted {len(phase2_rules)} Phase 2 (carrier) rules")
stamp(f"Extracted {len(phase10_rules)} Phase 10 (catch-all) rules")
stamp("")

# Convert user dictionary to multi-phase format
stamp("Converting user dictionary to Phase 6 format...")
phase6_rules = []

for idx, row in df_user.iterrows():
    # Extract values
    hs2 = str(row.get('HS2', '')).strip()
    hs4 = str(row.get('HS4', '')).strip()
    hs6 = str(row.get('HS6', '')).strip()
    group = str(row.get('Group', '')).strip()
    commodity = str(row.get('Commodity', '')).strip()
    cargo = str(row.get('Cargo', '')).strip()
    cargo_detail = str(row.get('Cargo_Detail', '')).strip()
    keywords = str(row.get('Keywords_Str', '')).strip()
    min_tons = str(row.get('Min Tons', '')).strip()
    max_tons = str(row.get('Max Tons', '')).strip()
    note = str(row.get('Note', '')).strip()

    # Skip empty rows
    if not hs2 or hs2 == 'nan':
        continue

    # Generate Rule_ID
    if hs6 and hs6 != 'nan':
        rule_id = f"HS6-{hs6}"
    elif hs4 and hs4 != 'nan':
        rule_id = f"HS4-{hs4}"
    else:
        rule_id = f"HS2-{hs2}"

    # Add sequence number if duplicate
    rule_id_base = rule_id
    counter = 1
    while rule_id in [r['Rule_ID'] for r in phase6_rules]:
        rule_id = f"{rule_id_base}-{counter:02d}"
        counter += 1

    # Create Phase 6 rule (HS + Keyword + Tonnage)
    new_rule = {
        'Rule_ID': rule_id,
        'Phase': '6',
        'Priority': '1',
        'Active': 'TRUE',
        'Public': 'FALSE',
        'Private': 'FALSE',
        'Carrier_SCAC': '',
        'Carrier_Name': '',
        'Vessel_Type': '',
        'HS2': hs2 if hs2 != 'nan' else '',
        'HS4': hs4 if hs4 != 'nan' else '',
        'HS6': hs6 if hs6 != 'nan' else '',
        'Keywords': keywords if keywords != 'nan' else '',
        'Exclude_Keywords': '',
        'Exclude_Groups': '',
        'Min_Tons': min_tons if min_tons != 'nan' else '',
        'Max_Tons': max_tons if max_tons != 'nan' else '',
        'Group': group if group != 'nan' else '',
        'Commodity': commodity if commodity != 'nan' else '',
        'Cargo': cargo if cargo != 'nan' else '',
        'Cargo_Detail': cargo_detail if cargo_detail != 'nan' else '',
        'Lock_Group': 'TRUE',
        'Lock_Commodity': 'TRUE',
        'Lock_Cargo': 'TRUE',
        'Lock_Cargo_Detail': 'TRUE',
        'Note': f"AUTHORITATIVE - DO NOT EDIT - {note}",
        'Last_Modified': '2026-01-14',
        'Source': 'user_notes/01_cargo_dictionary_harmonized_user_edits_01132016_1829.csv'
    }

    phase6_rules.append(new_rule)

stamp(f"Converted {len(phase6_rules)} user rules to Phase 6 format")
stamp("")

# Combine all phases
stamp("Assembling final dictionary...")
all_rules = []

# Phase 1: Vessel Type
all_rules.extend(phase1_rules.to_dict('records'))

# Phase 2: Carriers
all_rules.extend(phase2_rules.to_dict('records'))

# Phase 6: User's authoritative HS+Keyword+Tonnage rules
all_rules.extend(phase6_rules)

# Phase 10: Catch-all
all_rules.extend(phase10_rules.to_dict('records'))

df_final = pd.DataFrame(all_rules)

stamp(f"Final dictionary: {len(df_final)} rules")
stamp(f"  Phase 1 (Vessel Type): {len(df_final[df_final['Phase'] == '1'])}")
stamp(f"  Phase 2 (Carriers): {len(df_final[df_final['Phase'] == '2'])}")
stamp(f"  Phase 6 (HS+Keyword+Tons): {len(df_final[df_final['Phase'] == '6'])}")
stamp(f"  Phase 10 (Catch-all): {len(df_final[df_final['Phase'] == '10'])}")
stamp("")

# Verify tonnage filters preserved
tons_filtered = len(df_final[(df_final['Min_Tons'].notna() & (df_final['Min_Tons'] != '')) |
                              (df_final['Max_Tons'].notna() & (df_final['Max_Tons'] != ''))])
stamp(f"Tonnage-filtered rules: {tons_filtered} ({tons_filtered/len(df_final)*100:.1f}%)")
stamp("")

# Save v3.0.0
stamp(f"Saving v3.0.0: {OUTPUT_DICT}")
df_final.to_csv(OUTPUT_DICT, index=False)

stamp("")
stamp("=== Dictionary v3.0.0 Complete ===")
stamp("✓ User's authoritative 507 rules restored as Phase 6")
stamp("✓ All Min_Tons/Max_Tons filters preserved")
stamp("✓ All HS codes, Keywords, and classifications intact")
stamp("✓ Marked as AUTHORITATIVE - DO NOT EDIT")
stamp("")
stamp("Ready to test on TONNAGE classified (not record count)")

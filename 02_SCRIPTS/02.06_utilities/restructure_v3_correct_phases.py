"""
Restructure v3.0.0 with CORRECT phase order

CORRECT ORDER:
  Phase 1: Carriers (SCAC match, lock all 4, remove from processing)
  Phase 2: HS4 Broad Strokes (high-tonnage bulk commodities)
  Phase 3: Keywords (break-bulk, misclassification-prone)
  Phase 4: Problem Commodities (pig iron, ore, DRI, scrap, fertilizers, phos rock)
  Phase 5: Default (everything else -> General Cargo)
  Phase 6: Harmonization (empty for now, future use)

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
CURRENT_DICT = Path(r"G:\My Drive\LLM\project_manifest\01_DICTIONARIES\03.01_cargo_classification\cargo_classification_dictionary_v3.0.0_20260114_0200.csv")
OUTPUT_DICT = Path(r"G:\My Drive\LLM\project_manifest\01_DICTIONARIES\03.01_cargo_classification\cargo_classification_dictionary_v3.1.0_20260114_0230.csv")

stamp("=== Restructuring Dictionary with CORRECT Phase Order ===")
stamp("")

# Load current dictionary
df_curr = pd.read_csv(CURRENT_DICT, dtype=str)
df_user = pd.read_csv(USER_DICT, dtype=str)

stamp(f"Current dictionary: {len(df_curr)} rules")
stamp(f"User dictionary: {len(df_user)} rules")
stamp("")

# =========================================
# PHASE 1: CARRIERS (lock & remove)
# =========================================
carrier_rules = df_curr[df_curr['Carrier_SCAC'].notna() & (df_curr['Carrier_SCAC'] != '')]
stamp(f"Phase 1 (Carriers): {len(carrier_rules)} rules")

# Ensure carriers lock ALL 4 columns
for idx in carrier_rules.index:
    df_curr.at[idx, 'Phase'] = '1'
    df_curr.at[idx, 'Priority'] = '1'
    df_curr.at[idx, 'Lock_Group'] = 'TRUE'
    df_curr.at[idx, 'Lock_Commodity'] = 'TRUE'
    df_curr.at[idx, 'Lock_Cargo'] = 'TRUE'
    df_curr.at[idx, 'Lock_Cargo_Detail'] = 'TRUE'

phase1_rules = df_curr[df_curr['Phase'] == '1'].to_dict('records')

# =========================================
# PHASE 2: HS4 BROAD STROKES (high tonnage bulk)
# =========================================
stamp("")
stamp("Phase 2: Extracting HS4 broad stroke rules from user dictionary...")

# HS4 rules = rules with HS4 but minimal keywords (broad classification)
phase2_rules = []

# Top high-tonnage HS4 codes (petroleum, steel, cement, etc.)
high_tonnage_hs4 = ['2709', '2710', '7214', '2523', '4411', '8703', '7213', '6809',
                     '2501', '7601', '7201', '2606', '2619', '7210', '1701', '3105', '6810', '3102']

for _, row in df_user.iterrows():
    hs2 = str(row.get('HS2', '')).strip()
    hs4 = str(row.get('HS4', '')).strip()
    hs6 = str(row.get('HS6', '')).strip()
    keywords = str(row.get('Keywords_Str', '')).strip()

    # Skip empty
    if not hs2 or hs2 == 'nan':
        continue

    # HS4 rules: Has HS4, is in high-tonnage list OR has minimal keywords
    if hs4 and hs4 != 'nan':
        # High tonnage HS4 or simple/no keywords
        keyword_count = len([k for k in keywords.split(',') if k.strip()]) if keywords and keywords != 'nan' else 0
        if hs4 in high_tonnage_hs4 or keyword_count <= 2:
            # This is a broad stroke rule
            rule_id = f"HS4-{hs4}"

            # Check for duplicates
            counter = 1
            rule_id_base = rule_id
            while any(r['Rule_ID'] == rule_id for r in phase2_rules):
                rule_id = f"{rule_id_base}-{counter:02d}"
                counter += 1

            phase2_rules.append({
                'Rule_ID': rule_id,
                'Phase': '2',
                'Priority': '1',
                'Active': 'TRUE',
                'Public': 'FALSE',
                'Private': 'FALSE',
                'Carrier_SCAC': '',
                'Carrier_Name': '',
                'Vessel_Type': '',
                'HS2': hs2 if hs2 != 'nan' else '',
                'HS4': hs4 if hs4 != 'nan' else '',
                'HS6': '',  # Phase 2 = HS4 only, no HS6
                'Keywords': '',  # Phase 2 = no keywords, broad match
                'Exclude_Keywords': '',
                'Exclude_Groups': '',
                'Min_Tons': str(row.get('Min Tons', '')).strip() if str(row.get('Min Tons', '')).strip() != 'nan' else '',
                'Max_Tons': str(row.get('Max Tons', '')).strip() if str(row.get('Max Tons', '')).strip() != 'nan' else '',
                'Group': str(row.get('Group', '')).strip() if str(row.get('Group', '')).strip() != 'nan' else '',
                'Commodity': str(row.get('Commodity', '')).strip() if str(row.get('Commodity', '')).strip() != 'nan' else '',
                'Cargo': str(row.get('Cargo', '')).strip() if str(row.get('Cargo', '')).strip() != 'nan' else '',
                'Cargo_Detail': str(row.get('Cargo_Detail', '')).strip() if str(row.get('Cargo_Detail', '')).strip() != 'nan' else '',
                'Lock_Group': 'TRUE',
                'Lock_Commodity': 'TRUE',
                'Lock_Cargo': 'TRUE',
                'Lock_Cargo_Detail': 'TRUE',
                'Note': f"AUTHORITATIVE - Phase 2 HS4 Broad - {row.get('Note', '')}",
                'Last_Modified': '2026-01-14',
                'Source': 'user_notes - Phase 2 HS4 broad strokes'
            })

stamp(f"Phase 2 (HS4 Broad): {len(phase2_rules)} rules")

# =========================================
# PHASE 3: KEYWORD-BASED (break-bulk refinement)
# =========================================
stamp("")
stamp("Phase 3: Extracting keyword-based rules (break-bulk refinement)...")

phase3_rules = []

# Break-bulk misclassification-prone commodities
breakbulk_keywords = ['STEEL', 'ALUMINUM', 'ALUMINIUM', 'COPPER', 'PULP', 'PAPER',
                       'LUMBER', 'WOOD', 'TIMBER', 'PLYWOOD', 'COIL', 'PLATE', 'BEAM']

for _, row in df_user.iterrows():
    hs2 = str(row.get('HS2', '')).strip()
    hs4 = str(row.get('HS4', '')).strip()
    hs6 = str(row.get('HS6', '')).strip()
    keywords = str(row.get('Keywords_Str', '')).strip()

    if not hs2 or hs2 == 'nan':
        continue

    # Skip if already added to Phase 2
    if hs4 and any(r['HS4'] == hs4 for r in phase2_rules):
        continue

    # Keyword rules: Has keywords AND (is break-bulk related OR has multiple keywords)
    if keywords and keywords != 'nan':
        kw_upper = keywords.upper()
        is_breakbulk = any(bb in kw_upper for bb in breakbulk_keywords)
        keyword_count = len([k for k in keywords.split(',') if k.strip()])

        if is_breakbulk or keyword_count >= 3:
            # This is a keyword refinement rule
            if hs6 and hs6 != 'nan':
                rule_id = f"HS6-{hs6}"
            elif hs4 and hs4 != 'nan':
                rule_id = f"HS4-{hs4}-KW"
            else:
                rule_id = f"HS2-{hs2}-KW"

            # Check for duplicates
            counter = 1
            rule_id_base = rule_id
            while any(r['Rule_ID'] == rule_id for r in phase3_rules):
                rule_id = f"{rule_id_base}-{counter:02d}"
                counter += 1

            phase3_rules.append({
                'Rule_ID': rule_id,
                'Phase': '3',
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
                'Min_Tons': str(row.get('Min Tons', '')).strip() if str(row.get('Min Tons', '')).strip() != 'nan' else '',
                'Max_Tons': str(row.get('Max Tons', '')).strip() if str(row.get('Max Tons', '')).strip() != 'nan' else '',
                'Group': str(row.get('Group', '')).strip() if str(row.get('Group', '')).strip() != 'nan' else '',
                'Commodity': str(row.get('Commodity', '')).strip() if str(row.get('Commodity', '')).strip() != 'nan' else '',
                'Cargo': str(row.get('Cargo', '')).strip() if str(row.get('Cargo', '')).strip() != 'nan' else '',
                'Cargo_Detail': str(row.get('Cargo_Detail', '')).strip() if str(row.get('Cargo_Detail', '')).strip() != 'nan' else '',
                'Lock_Group': 'TRUE',
                'Lock_Commodity': 'TRUE',
                'Lock_Cargo': 'TRUE',
                'Lock_Cargo_Detail': 'TRUE',
                'Note': f"AUTHORITATIVE - Phase 3 Keyword - {row.get('Note', '')}",
                'Last_Modified': '2026-01-14',
                'Source': 'user_notes - Phase 3 keyword-based'
            })

stamp(f"Phase 3 (Keywords): {len(phase3_rules)} rules")

# =========================================
# PHASE 4: PROBLEM COMMODITIES
# =========================================
stamp("")
stamp("Phase 4: Extracting problem commodity rules...")

phase4_rules = []

problem_keywords = ['PIG IRON', 'IRON ORE', 'DRI', 'SCRAP', 'FERTILIZER', 'PHOS', 'PHOSPHATE',
                     'UREA', 'POTASH', 'CLINKER']

for _, row in df_user.iterrows():
    hs2 = str(row.get('HS2', '')).strip()
    keywords = str(row.get('Keywords_Str', '')).strip()

    if not hs2 or hs2 == 'nan':
        continue

    # Skip if already in Phase 2 or 3
    hs4 = str(row.get('HS4', '')).strip()
    hs6 = str(row.get('HS6', '')).strip()
    if any(r.get('HS4') == hs4 or r.get('HS6') == hs6 for r in phase2_rules + phase3_rules):
        continue

    # Problem commodities: Match specific high-tonnage misclassification-prone keywords
    if keywords and keywords != 'nan':
        kw_upper = keywords.upper()
        if any(prob in kw_upper for prob in problem_keywords):
            if hs6 and hs6 != 'nan':
                rule_id = f"HS6-{hs6}-PROB"
            elif hs4 and hs4 != 'nan':
                rule_id = f"HS4-{hs4}-PROB"
            else:
                rule_id = f"HS2-{hs2}-PROB"

            counter = 1
            rule_id_base = rule_id
            while any(r['Rule_ID'] == rule_id for r in phase4_rules):
                rule_id = f"{rule_id_base}-{counter:02d}"
                counter += 1

            phase4_rules.append({
                'Rule_ID': rule_id,
                'Phase': '4',
                'Priority': '1',
                'Active': 'TRUE',
                'Public': 'FALSE',
                'Private': 'FALSE',
                'Carrier_SCAC': '',
                'Carrier_Name': '',
                'Vessel_Type': '',
                'HS2': hs2 if hs2 != 'nan' else '',
                'HS4': str(row.get('HS4', '')).strip() if str(row.get('HS4', '')).strip() != 'nan' else '',
                'HS6': str(row.get('HS6', '')).strip() if str(row.get('HS6', '')).strip() != 'nan' else '',
                'Keywords': keywords if keywords != 'nan' else '',
                'Exclude_Keywords': '',
                'Exclude_Groups': '',
                'Min_Tons': str(row.get('Min Tons', '')).strip() if str(row.get('Min Tons', '')).strip() != 'nan' else '',
                'Max_Tons': str(row.get('Max Tons', '')).strip() if str(row.get('Max Tons', '')).strip() != 'nan' else '',
                'Group': str(row.get('Group', '')).strip() if str(row.get('Group', '')).strip() != 'nan' else '',
                'Commodity': str(row.get('Commodity', '')).strip() if str(row.get('Commodity', '')).strip() != 'nan' else '',
                'Cargo': str(row.get('Cargo', '')).strip() if str(row.get('Cargo', '')).strip() != 'nan' else '',
                'Cargo_Detail': str(row.get('Cargo_Detail', '')).strip() if str(row.get('Cargo_Detail', '')).strip() != 'nan' else '',
                'Lock_Group': 'TRUE',
                'Lock_Commodity': 'TRUE',
                'Lock_Cargo': 'TRUE',
                'Lock_Cargo_Detail': 'TRUE',
                'Note': f"AUTHORITATIVE - Phase 4 Problem Commodity - {row.get('Note', '')}",
                'Last_Modified': '2026-01-14',
                'Source': 'user_notes - Phase 4 problem commodities'
            })

stamp(f"Phase 4 (Problem Commodities): {len(phase4_rules)} rules")

# =========================================
# PHASE 5: DEFAULT (General Cargo catch-all)
# =========================================
stamp("")
stamp("Phase 5: Creating default catch-all rule...")

phase5_rules = [{
    'Rule_ID': 'DEFAULT-GENERAL-CARGO',
    'Phase': '5',
    'Priority': '999',
    'Active': 'TRUE',
    'Public': 'FALSE',
    'Private': 'FALSE',
    'Carrier_SCAC': '',
    'Carrier_Name': '',
    'Vessel_Type': '',
    'HS2': '',
    'HS4': '',
    'HS6': '',
    'Keywords': '',
    'Exclude_Keywords': '',
    'Exclude_Groups': '',
    'Min_Tons': '',
    'Max_Tons': '',
    'Group': 'Break-Bulk',
    'Commodity': 'General Cargo',
    'Cargo': 'General Cargo',
    'Cargo_Detail': 'General Cargo',
    'Lock_Group': 'FALSE',
    'Lock_Commodity': 'FALSE',
    'Lock_Cargo': 'FALSE',
    'Lock_Cargo_Detail': 'FALSE',
    'Note': 'Default catch-all - everything else',
    'Last_Modified': '2026-01-14',
    'Source': 'System default'
}]

stamp(f"Phase 5 (Default): {len(phase5_rules)} rule")

# =========================================
# ASSEMBLE FINAL DICTIONARY
# =========================================
stamp("")
stamp("Assembling final dictionary...")

all_rules = phase1_rules + phase2_rules + phase3_rules + phase4_rules + phase5_rules
df_final = pd.DataFrame(all_rules)

stamp(f"")
stamp(f"=== FINAL DICTIONARY v3.1.0 ===")
stamp(f"Total Rules: {len(df_final)}")
stamp(f"  Phase 1 (Carriers):           {len(phase1_rules):3d} rules")
stamp(f"  Phase 2 (HS4 Broad):          {len(phase2_rules):3d} rules")
stamp(f"  Phase 3 (Keywords):           {len(phase3_rules):3d} rules")
stamp(f"  Phase 4 (Problem Commodities): {len(phase4_rules):3d} rules")
stamp(f"  Phase 5 (Default):            {len(phase5_rules):3d} rules")
stamp(f"")

# Save
stamp(f"Saving: {OUTPUT_DICT}")
df_final.to_csv(OUTPUT_DICT, index=False)

stamp("")
stamp("=== Dictionary v3.1.0 Complete ===")
stamp("CORRECT phase order implemented:")
stamp("  1. Carriers (lock & remove)")
stamp("  2. HS4 broad strokes (high tonnage)")
stamp("  3. Keywords (break-bulk refinement)")
stamp("  4. Problem commodities (misclassification-prone)")
stamp("  5. Default (General Cargo catch-all)")
stamp("  6. (Empty - reserved for harmonization)")

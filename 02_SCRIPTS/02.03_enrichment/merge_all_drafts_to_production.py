"""
Merge all draft rule files into updated production dictionary

Author: WSD3 / Claude Code
Date: 2026-01-14
"""

import pandas as pd
from pathlib import Path
from datetime import datetime

def stamp(msg):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

# Paths
BASE_DICT = Path(r"G:\My Drive\LLM\project_manifest\user_notes\cargo_classification_dictionary_v3.5.0_DRAFT_refined_keywords.csv")
HS27_DRAFT = Path(r"G:\My Drive\LLM\project_manifest\user_notes\dictionary_rules_DRAFT_hs27_mineral_fuels.csv")
HS28_29_DRAFT = Path(r"G:\My Drive\LLM\project_manifest\user_notes\dictionary_rules_DRAFT_hs28-29_pure_chemicals.csv")
HS72_79_DRAFT = Path(r"G:\My Drive\LLM\project_manifest\user_notes\dictionary_rules_DRAFT_hs72-73_76-79_user_edits.csv")
TONS_2MIL_DRAFT = Path(r"G:\My Drive\LLM\project_manifest\user_notes\dictionary_rules_DRAFT_2mil_tons_plus.csv")
OUTPUT_FILE = Path(r"G:\My Drive\LLM\project_manifest\user_notes\cargo_classification_dictionary_v3.6.0_DRAFT_20260114.csv")

stamp("=== Merge All Draft Rules to Production Dictionary ===")
stamp("")

# Load base dictionary
stamp("Loading base dictionary v3.5.0...")
df_base = pd.read_csv(BASE_DICT, dtype=str)
stamp(f"  Base rules: {len(df_base)}")

# Load all draft files
stamp("")
stamp("Loading draft rule files...")

df_hs27 = pd.read_csv(HS27_DRAFT, dtype=str)
stamp(f"  HS27 Mineral Fuels: {len(df_hs27)} rules")

df_hs28_29 = pd.read_csv(HS28_29_DRAFT, dtype=str)
stamp(f"  HS28-29 Pure Chemicals: {len(df_hs28_29)} rules")

df_hs72_79 = pd.read_csv(HS72_79_DRAFT, dtype=str)
stamp(f"  HS72-73, 76-79 Metals: {len(df_hs72_79)} rules")

df_2mil = pd.read_csv(TONS_2MIL_DRAFT, dtype=str)
stamp(f"  2M+ Tons (Multi-commodity): {len(df_2mil)} rules")

stamp(f"  Total new rules to merge: {len(df_hs27) + len(df_hs28_29) + len(df_hs72_79) + len(df_2mil)}")

# Check for overlaps - we need to replace, not append
stamp("")
stamp("Checking for overlapping HS4 codes...")

new_rules = pd.concat([df_hs27, df_hs28_29, df_hs72_79, df_2mil], ignore_index=True)
new_hs4_codes = set(new_rules['HS4'].unique())
base_hs4_codes = set(df_base['HS4'].unique())

overlapping = new_hs4_codes.intersection(base_hs4_codes)
stamp(f"  Overlapping HS4 codes: {len(overlapping)}")
if len(overlapping) > 0:
    stamp(f"  Will REPLACE these HS4 codes with new user-edited rules")

# Remove overlapping HS4 codes from base
df_base_cleaned = df_base[~df_base['HS4'].isin(new_hs4_codes)].copy()
stamp(f"  Base rules after removing overlaps: {len(df_base_cleaned)}")

# Combine all
stamp("")
stamp("Merging all rules...")
df_merged = pd.concat([df_base_cleaned, new_rules], ignore_index=True)

# Sort by HS4
df_merged = df_merged.sort_values(['HS2', 'HS4', 'Rule_ID']).reset_index(drop=True)

stamp(f"  Total rules in v3.6.0: {len(df_merged)}")

# Show breakdown by Phase
stamp("")
stamp("Breakdown by Phase:")
for phase in sorted(df_merged['Phase'].unique()):
    count = len(df_merged[df_merged['Phase'] == phase])
    stamp(f"  Phase {phase}: {count} rules")

# Show breakdown by Group
stamp("")
stamp("Breakdown by Classification Group:")
group_counts = df_merged.groupby('Group').size().sort_values(ascending=False)
for group, count in group_counts.head(10).items():
    stamp(f"  {group}: {count} rules")

# Show new HS2 chapters with rules
stamp("")
stamp("HS2 chapters with user-edited rules:")
new_hs2 = sorted(new_rules['HS2'].unique())
for hs2 in new_hs2:
    count = len(new_rules[new_rules['HS2'] == hs2])
    stamp(f"  HS{hs2}: {count} rules")

# Save
stamp("")
stamp(f"Saving merged dictionary: {OUTPUT_FILE.name}")
df_merged.to_csv(OUTPUT_FILE, index=False)

stamp("")
stamp("Complete!")
stamp("")
stamp("Dictionary v3.6.0 DRAFT created with:")
stamp(f"  - {len(df_base_cleaned)} original rules")
stamp(f"  - {len(new_rules)} new user-edited rules")
stamp(f"  - {len(df_merged)} total rules")
stamp("")
stamp("New user-edited commodities:")
stamp("  - HS27: Mineral Fuels (Crude Oil, Petroleum, Coal, LNG)")
stamp("  - HS28-29: Pure Chemicals (Inorganic, Organic)")
stamp("  - HS72-73, 76-79: Metals (Steel, Iron, Nonferrous)")
stamp("  - Multi-commodity: Agricultural, Construction, Forestry, Fertilizers")

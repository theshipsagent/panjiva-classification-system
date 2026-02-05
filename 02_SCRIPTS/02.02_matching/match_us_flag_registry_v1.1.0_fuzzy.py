"""
Match US Flag Registry to Port Call Master - v1.1.0 (Fuzzy Matching)
Date: 2026-01-16

Purpose:
- Load v1.4.0 Port Call Master (with exact matches already done)
- Apply fuzzy name matching to remaining unmatched US flag vessels
- Use Levenshtein distance (0.85 threshold) for name similarity
- Disambiguate using ICST code and NRT when multiple candidates

Improvements over v1.0.0:
- Fuzzy string matching using difflib.SequenceMatcher
- Name normalization (remove common variations)
- ICST code weighting for disambiguation
- Expected improvement: +500-800 matches (30-40% of remaining unmatched)

Result: v1.5.0 Port Call Master with improved US Flag match rate (target: 70-80%)
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
from difflib import SequenceMatcher

print("="*80)
print("US FLAG REGISTRY FUZZY MATCHING v1.1.0")
print("="*80)

timestamp = datetime.now().strftime("%Y%m%d_%H%M")

# Paths
US_FLAG_DIR = Path(r"G:\My Drive\LLM\project_manifest\01_DICTIONARIES\03.05_us_flag_inventory")
PORT_CALL_FILE = Path(r"G:\My Drive\LLM\project_manifest\00_DATA/00.03_MATCHED\usace_2023_portcall_master_v1.4.0_usflag.csv")
OUTPUT_FILE = Path(r"G:\My Drive\LLM\project_manifest\00_DATA/00.03_MATCHED\usace_2023_portcall_master_v1.5.0_fuzzy.csv")

# ICST code mapping (expanded)
ICST_CODES = {
    # Tugs
    431: "Tug",
    432: "Push Boat",
    422: "Tug/Supply Offshore Support",
    # Barges - Deck
    341: "Deck Barge",
    342: "Deck Barge",
    343: "Deck Barge",
    # Barges - Dry Cargo
    344: "Open Dry Cargo Barge",
    345: "Covered Dry Cargo Barge",
    346: "Dry Cargo Barge",
    # Barges - Tank
    140: "Tank Barge",
    141: "Tank Barge",
    142: "Tank Barge",
    143: "Tank Barge",
    144: "Tank Barge",
    145: "Tank Barge",
    146: "Tank Barge",
    147: "Tank Barge",
    148: "Tank Barge",
    149: "Tank Barge",
    # Lakers
    600: "Laker",
    601: "Laker",
    602: "Laker",
    # Other vessels
    110: "General Cargo",
    111: "Container Vessel",
    112: "Ro-Ro Cargo",
    120: "Bulk Carrier",
    130: "Tanker",
    210: "Passenger Vessel",
    220: "Ferry",
    310: "Fishing Vessel",
    320: "Research/Survey",
    410: "Service Vessel",
    420: "Offshore Supply",
    500: "Special Purpose"
}

def clean_vessel_name(name):
    """
    Advanced vessel name cleaning for fuzzy matching
    """
    if pd.isna(name):
        return ""

    name = str(name).upper().strip()

    # Remove common prefixes
    prefixes = ['M/V ', 'MV ', 'M.V. ', 'S/S ', 'SS ', 'TUG ', 'T/B ', 'B/T ',
                'BARGE ', 'PUSH BOAT ', 'P/B ', 'TANK BARGE ', 'DECK BARGE ']
    for prefix in prefixes:
        if name.startswith(prefix):
            name = name[len(prefix):]

    # Remove common suffixes
    suffixes = [' TUG', ' BARGE', ' TANK', ' DECK', ' PUSH BOAT']
    for suffix in suffixes:
        if name.endswith(suffix):
            name = name[:-len(suffix)]

    # Normalize spacing and punctuation
    name = name.replace('.', '').replace(',', '').replace('-', ' ')
    name = ' '.join(name.split())  # Normalize spaces

    return name.strip()

def name_similarity(name1, name2):
    """
    Calculate similarity between two vessel names using SequenceMatcher
    Returns: float 0-1 (1 = identical)
    """
    if pd.isna(name1) or pd.isna(name2):
        return 0.0

    name1_clean = clean_vessel_name(name1)
    name2_clean = clean_vessel_name(name2)

    if not name1_clean or not name2_clean:
        return 0.0

    return SequenceMatcher(None, name1_clean, name2_clean).ratio()

def map_icst_to_category(icst_desc):
    """
    Map ICST description to simplified category for matching
    """
    if pd.isna(icst_desc):
        return ""

    icst = str(icst_desc).upper()

    if 'TUG' in icst and 'SUPPLY' in icst:
        return 'TUG_SUPPLY'
    elif 'TUG' in icst:
        return 'TUG'
    elif 'PUSH' in icst:
        return 'PUSH_BOAT'
    elif 'DECK BARGE' in icst:
        return 'DECK_BARGE'
    elif 'TANK BARGE' in icst:
        return 'TANK_BARGE'
    elif 'DRY' in icst and 'BARGE' in icst:
        return 'DRY_BARGE'
    elif 'LAKER' in icst:
        return 'LAKER'
    else:
        return 'OTHER'

# ============================================================================
# 1. Load US Flag Inventory
# ============================================================================
print("\n1. Loading US Flag Inventory files...")

us_flag_files = list(US_FLAG_DIR.glob("2023*.xlsx"))
print(f"   Found {len(us_flag_files)} Excel files")

all_us_vessels = []
for file in us_flag_files:
    vessel_category = file.stem.replace('2023 ', '').replace(' ', '_')
    print(f"   Loading {vessel_category}...")

    df = pd.read_excel(file)
    # Strip whitespace from column names
    df.columns = df.columns.str.strip()
    df['Source_File'] = vessel_category
    all_us_vessels.append(df)

us_register = pd.concat(all_us_vessels, ignore_index=True)
print(f"\n   Total US Flag vessels loaded: {len(us_register):,}")

# Clean and prepare US Flag data
print("\n2. Cleaning US Flag data...")
us_register['Vessel_Name_Clean'] = us_register['VS_NAME'].apply(clean_vessel_name)

# Map ICST codes to descriptions
us_register['ICST_DESC'] = us_register['ICST'].map(ICST_CODES)
us_register['ICST_Category'] = us_register['ICST_DESC'].apply(map_icst_to_category)

# Remove exact duplicates (same name + CG number)
us_register = us_register.drop_duplicates(subset=['VS_NAME', 'CG_NUMBER'], keep='first')
print(f"   Unique vessels after deduplication: {len(us_register):,}")

# ============================================================================
# 2. Load Port Call Master v1.4.0
# ============================================================================
print("\n3. Loading Port Call Master v1.4.0...")
portcall = pd.read_csv(PORT_CALL_FILE, low_memory=False)
print(f"   Total port calls: {len(portcall):,}")

# ============================================================================
# 3. Identify Unmatched US Flag Vessels
# ============================================================================
print("\n4. Identifying unmatched US flag vessels...")

# US flag vessels WITHOUT US Flag registry match
us_flag_unmatched = portcall[
    (portcall['Flag_Country'] == 'United States of America') &
    (portcall['USFlag_CG_Number'].isna())
].copy()

print(f"   Unmatched US flag port calls: {len(us_flag_unmatched):,}")

# Get unique vessels
unique_unmatched = us_flag_unmatched.drop_duplicates(subset=['Vessel_Name', 'IMO', 'ICST_Vessel_Type'])
print(f"   Unique unmatched vessels: {len(unique_unmatched):,}")

# ============================================================================
# 4. Fuzzy Matching
# ============================================================================
print("\n5. Fuzzy matching vessels...")
print("   Strategy: Name similarity >= 0.85 + ICST category match\n")

matches_found = []
unmatched_vessels = []

for idx, record in unique_unmatched.iterrows():
    vessel_name = record['Vessel_Name']
    vessel_nrt = record.get('NRT', np.nan)
    vessel_icst = record.get('ICST_Vessel_Type', '')

    # Clean name
    vessel_name_clean = clean_vessel_name(vessel_name)
    vessel_icst_category = map_icst_to_category(vessel_icst)

    # Calculate similarity scores for all US Flag vessels
    us_register['Name_Similarity'] = us_register['Vessel_Name_Clean'].apply(
        lambda x: name_similarity(vessel_name_clean, x)
    )

    # Filter by similarity threshold (0.85)
    candidates = us_register[us_register['Name_Similarity'] >= 0.85].copy()

    if len(candidates) == 0:
        unmatched_vessels.append({
            'Vessel_Name': vessel_name,
            'ICST_Vessel_Type': vessel_icst,
            'Best_Similarity': us_register['Name_Similarity'].max(),
            'Reason': 'No candidates above 0.85 threshold'
        })
        continue

    # Disambiguate using ICST category
    if len(candidates) > 1:
        # Prefer same ICST category
        icst_matches = candidates[candidates['ICST_Category'] == vessel_icst_category]

        if len(icst_matches) > 0:
            candidates = icst_matches
            match_method = 'FUZZY_ICST_MATCH'
        else:
            match_method = 'FUZZY_BEST_SIMILARITY'
    else:
        match_method = 'FUZZY_SINGLE_MATCH'

    # Disambiguate using NRT if still multiple candidates
    if len(candidates) > 1 and pd.notna(vessel_nrt):
        candidates['NRT_Diff'] = abs(candidates['NRT'] - vessel_nrt)
        best_nrt_match = candidates.loc[candidates['NRT_Diff'].idxmin()]
        match_method = 'FUZZY_NRT_DISAMBIGUATED'
        selected_match = best_nrt_match
    else:
        # Select highest similarity
        selected_match = candidates.loc[candidates['Name_Similarity'].idxmax()]

    # Store match
    matches_found.append({
        'PORTCALL_ID': record.get('PORTCALL_ID'),
        'Vessel_Name': vessel_name,
        'Matched_Name': selected_match['VS_NAME'],
        'Name_Similarity': selected_match['Name_Similarity'],
        'USFlag_CG_Number': selected_match['CG_NUMBER'],
        'USFlag_ICST_Code': selected_match.get('ICST', np.nan),
        'USFlag_ICST_Description': selected_match.get('ICST_DESC', np.nan),
        'USFlag_HP': selected_match.get('HP', np.nan),
        'USFlag_Length_ft': selected_match.get('REG_LNGTH', np.nan),
        'USFlag_Beam_ft': selected_match.get('REG_BRDTH', np.nan),
        'USFlag_Capacity_Tons': selected_match.get('CAP_TONS', np.nan),
        'USFlag_Year_Built': selected_match.get('YEAR', np.nan),
        'USFlag_Base_Port': selected_match.get('BASE1', np.nan),
        'USFlag_State': selected_match.get('STATE', np.nan),
        'USFlag_Match_Quality': match_method
    })

print(f"   Fuzzy matches found: {len(matches_found):,}")
print(f"   Still unmatched: {len(unmatched_vessels):,}")

# ============================================================================
# 5. Update Port Call Master
# ============================================================================
print("\n6. Updating Port Call Master with fuzzy matches...")

matches_df = pd.DataFrame(matches_found)

# Merge fuzzy matches back to portcall master
# For each matched vessel name, update ALL port calls for that vessel
for idx, match in matches_df.iterrows():
    vessel_name = match['Vessel_Name']

    # Find all port calls for this vessel (unmatched only)
    mask = (
        (portcall['Vessel_Name'] == vessel_name) &
        (portcall['Flag_Country'] == 'United States of America') &
        (portcall['USFlag_CG_Number'].isna())
    )

    # Update with US Flag data
    portcall.loc[mask, 'USFlag_CG_Number'] = match['USFlag_CG_Number']
    portcall.loc[mask, 'USFlag_ICST_Code'] = match['USFlag_ICST_Code']
    portcall.loc[mask, 'USFlag_ICST_Description'] = match['USFlag_ICST_Description']
    portcall.loc[mask, 'USFlag_HP'] = match['USFlag_HP']
    portcall.loc[mask, 'USFlag_Length_ft'] = match['USFlag_Length_ft']
    portcall.loc[mask, 'USFlag_Beam_ft'] = match['USFlag_Beam_ft']
    portcall.loc[mask, 'USFlag_Capacity_Tons'] = match['USFlag_Capacity_Tons']
    portcall.loc[mask, 'USFlag_Year_Built'] = match['USFlag_Year_Built']
    portcall.loc[mask, 'USFlag_Base_Port'] = match['USFlag_Base_Port']
    portcall.loc[mask, 'USFlag_State'] = match['USFlag_State']
    portcall.loc[mask, 'USFlag_Match_Quality'] = match['USFlag_Match_Quality']

# ============================================================================
# 6. Save Updated Port Call Master
# ============================================================================
print("\n7. Saving updated Port Call Master...")
portcall.to_csv(OUTPUT_FILE, index=False)
print(f"   Saved: {OUTPUT_FILE.name}")
file_size = OUTPUT_FILE.stat().st_size / (1024 * 1024)
print(f"   Size: {file_size:.1f} MB")

# ============================================================================
# 7. Generate Statistics
# ============================================================================
print("\n" + "="*80)
print("FUZZY MATCHING SUMMARY")
print("="*80)

# Overall US flag statistics
us_flag_total = len(portcall[portcall['Flag_Country'] == 'United States of America'])
us_flag_matched = portcall[
    (portcall['Flag_Country'] == 'United States of America') &
    (portcall['USFlag_CG_Number'].notna())
]
us_flag_matched_count = len(us_flag_matched)

print(f"\nUS Flag Vessels:")
print(f"  Total US flag port calls: {us_flag_total:,}")
print(f"  Matched to US Flag Register: {us_flag_matched_count:,} ({us_flag_matched_count/us_flag_total*100:.1f}%)")
print(f"  Unmatched: {us_flag_total - us_flag_matched_count:,} ({(us_flag_total - us_flag_matched_count)/us_flag_total*100:.1f}%)")

print(f"\nFuzzy Matching Results:")
print(f"  Unique vessels matched: {len(matches_found):,}")
print(f"  Port calls updated: {len(us_flag_unmatched[us_flag_unmatched['Vessel_Name'].isin(matches_df['Vessel_Name'])]):,}")

# Match quality distribution
if len(matches_df) > 0:
    print(f"\nFuzzy Match Quality Distribution:")
    quality_dist = matches_df['USFlag_Match_Quality'].value_counts()
    for quality, count in quality_dist.items():
        pct = count / len(matches_df) * 100
        print(f"  {quality:<30} {count:>5} ({pct:>5.1f}%)")

    print(f"\nName Similarity Statistics:")
    print(f"  Average similarity: {matches_df['Name_Similarity'].mean():.3f}")
    print(f"  Minimum similarity: {matches_df['Name_Similarity'].min():.3f}")
    print(f"  Maximum similarity: {matches_df['Name_Similarity'].max():.3f}")

# Top 10 fuzzy matches (show name variations)
if len(matches_df) > 0:
    print(f"\nTop 10 Fuzzy Matches (Examples of Name Variations):")
    print("-" * 80)
    for idx, row in matches_df.head(10).iterrows():
        print(f"  USACE: '{row['Vessel_Name']}'")
        print(f"  Match: '{row['Matched_Name']}' (Similarity: {row['Name_Similarity']:.3f})")
        print(f"  Method: {row['USFlag_Match_Quality']}")
        print()

# Save fuzzy match report
if len(matches_df) > 0:
    fuzzy_report = Path(r"G:\My Drive\LLM\project_manifest\00_DATA/00.03_MATCHED\us_flag_fuzzy_matches_v1.1.0.csv")
    matches_df.to_csv(fuzzy_report, index=False)
    print(f"\nFuzzy match report saved: {fuzzy_report.name}")

# Save remaining unmatched report
if len(unmatched_vessels) > 0:
    unmatched_df = pd.DataFrame(unmatched_vessels)
    unmatched_report = Path(r"G:\My Drive\LLM\project_manifest\00_DATA/00.03_MATCHED\us_flag_unmatched_v1.1.0.csv")
    unmatched_df.to_csv(unmatched_report, index=False)
    print(f"Remaining unmatched report saved: {unmatched_report.name}")

print("\n" + "="*80)
print("COMPLETE!")
print("="*80)
print(f"\nOutput: {OUTPUT_FILE}")
print(f"\nMatch Rate: {us_flag_matched_count/us_flag_total*100:.1f}% (v1.4.0: 62.3%)")
print(f"Improvement: +{(us_flag_matched_count/us_flag_total*100) - 62.3:.1f} percentage points")

"""
Match US Flag Vessels to Port Call Master
Version: 1.0.0
Date: 2026-01-16

Purpose:
- Load all US Flag inventory files (94,783 vessels: tugs, barges, self-propelled)
- Consolidate into single US flag register
- Match to unmatched US flag vessels in Port Call Master
- Enrich with: vessel type, NRT, length, beam, horsepower, capacity

Expected improvement: 16.8% match rate → 80%+ for US flag vessels
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import glob
from difflib import SequenceMatcher

print("="*80)
print("US FLAG REGISTRY MATCHING v1.0.0")
print("="*80)

timestamp = datetime.now().strftime("%Y%m%d_%H%M")

# File paths
US_FLAG_DIR = Path(r"G:\My Drive\LLM\project_manifest\01_DICTIONARIES\03.05_us_flag_inventory")
PORTCALL_FILE = Path(r"G:\My Drive\LLM\project_manifest\00_DATA/00.03_MATCHED\usace_2023_portcall_master_v1.3.0_restructured.csv")
OUTPUT_FILE = Path(r"G:\My Drive\LLM\project_manifest\00_DATA/00.03_MATCHED\usace_2023_portcall_master_v1.4.0_usflag.csv")

# ICST code mapping
ICST_CODES = {
    110: "Other Oil Tanker", 111: "Crude Oil Tanker", 112: "Crude/Products Tanker",
    113: "Oil Products Tanker", 114: "Oil/Chemical Tanker", 120: "Chemical Tanker",
    130: "Other Liquefied Gas Carrier", 131: "LPG Carrier", 132: "LNG Carrier",
    140: "Other Tank Barge", 141: "Single Hull Tanker Barge", 142: "Double Hull Tanker Barge",
    210: "Other Bulk/Oil Carrier", 220: "Other Bulk Carrier", 221: "Ore Carrier",
    310: "Container Vessel", 320: "Other Specialized Carrier", 325: "Vehicle Carrier",
    330: "Other General Cargo", 331: "Reefer", 333: "Other Ro/Ro Cargo",
    340: "Dry Cargo Barge", 341: "Deck Barge", 342: "Hopper Barge",
    344: "Open Dry Cargo Barge", 345: "Covered Dry Cargo Barge",
    349: "Other Dry Cargo Barge NEI",
    422: "Tug/Supply Offshore Support", 431: "Tug", 432: "Push Boat",
    600: "Other Lakers", 601: "Lakers—Bulk Carriers", 602: "Lakers—General Cargo"
}

def clean_vessel_name(name):
    """Standardize vessel name for matching"""
    if pd.isna(name):
        return ""
    name = str(name).upper().strip()
    # Remove common prefixes
    for prefix in ['M/V ', 'MV ', 'M.V. ', 'S/S ', 'SS ', 'T/B ', 'TB ']:
        if name.startswith(prefix):
            name = name[len(prefix):]
    return name.strip()

def vessel_similarity(name1, name2):
    """Calculate similarity between vessel names (0-1)"""
    name1 = clean_vessel_name(name1)
    name2 = clean_vessel_name(name2)
    if not name1 or not name2:
        return 0.0
    return SequenceMatcher(None, name1, name2).ratio()

# ============================================================================
# STEP 1: Load and Consolidate US Flag Inventory
# ============================================================================

print("\n1. Loading US Flag Inventory files...")
us_flag_files = list(US_FLAG_DIR.glob("2023*.xlsx"))
us_flag_files = [f for f in us_flag_files if 'tankb23 (1)' not in f.name]  # Remove duplicate

all_us_vessels = []

for file in us_flag_files:
    vessel_category = file.stem.replace('2023 ', '')
    print(f"   Loading {vessel_category}...")

    try:
        df = pd.read_excel(file)
        df['Source_File'] = vessel_category
        all_us_vessels.append(df)
    except Exception as e:
        print(f"   ERROR loading {file.name}: {e}")

us_register = pd.concat(all_us_vessels, ignore_index=True)
print(f"\n   Total US Flag vessels loaded: {len(us_register):,}")

# Clean and standardize
print("\n2. Cleaning US Flag data...")
us_register['Vessel_Name_Clean'] = us_register[' VS_NAME'].apply(clean_vessel_name)
us_register['ICST_Description'] = us_register[' ICST'].map(ICST_CODES)

# Remove duplicates (same vessel name + CG number)
print("   Removing duplicates...")
original_count = len(us_register)
us_register = us_register.drop_duplicates(subset=['Vessel_Name_Clean', ' CG_NUMBER'], keep='first')
print(f"   Removed {original_count - len(us_register):,} duplicates")
print(f"   Unique vessels: {len(us_register):,}")

# ============================================================================
# STEP 2: Load Port Call Master - Unmatched US Flag Vessels
# ============================================================================

print("\n3. Loading Port Call Master...")
portcall = pd.read_csv(PORTCALL_FILE, low_memory=False)
print(f"   Total port calls: {len(portcall):,}")

# Filter for US flag vessels without ship registry match
print("\n4. Identifying unmatched US flag vessels...")
us_unmatched = portcall[
    (portcall['Flag_Country'] == 'United States of America') &
    (portcall['Vessel_Type_Registry'].isna())
].copy()

print(f"   Unmatched US flag port calls: {len(us_unmatched):,}")

# Clean vessel names
us_unmatched['Vessel_Name_Clean'] = us_unmatched['Vessel_Name'].apply(clean_vessel_name)

# Get unique vessels
unique_vessels = us_unmatched[['Vessel_Name', 'Vessel_Name_Clean', 'ICST_Vessel_Type', 'NRT']].drop_duplicates(subset=['Vessel_Name_Clean'])
print(f"   Unique unmatched vessels: {len(unique_vessels):,}")

# ============================================================================
# STEP 3: Match US Flag Vessels
# ============================================================================

print("\n5. Matching vessels...")
print("   Strategy: Exact name match + ICST code verification")

matches = []
unmatched = []

for idx, vessel in unique_vessels.iterrows():
    vessel_name = vessel['Vessel_Name_Clean']
    usace_icst = vessel['ICST_Vessel_Type']
    usace_nrt = vessel['NRT']

    # Try exact name match
    candidates = us_register[us_register['Vessel_Name_Clean'] == vessel_name]

    if len(candidates) == 1:
        # Perfect match
        match = candidates.iloc[0]
        matches.append({
            'USACE_Vessel_Name': vessel['Vessel_Name'],
            'USFlag_Vessel_Name': match[' VS_NAME'],
            'CG_Number': match[' CG_NUMBER'],
            'ICST_Code': match[' ICST'],
            'ICST_Description': match['ICST_Description'],
            'NRT': match[' NRT'],
            'HP': match[' HP'],
            'Length_ft': match[' REG_LNGTH'],
            'Beam_ft': match.get(' REG_BRDTH', None),
            'Capacity_Tons': match.get(' CAP_TONS', None),
            'Year_Built': match.get(' YEAR', None),
            'Base_Port': match.get(' BASE1', None),
            'State': match.get(' STATE', None),
            'Source_File': match['Source_File'],
            'Match_Quality': 'EXACT_MATCH'
        })
    elif len(candidates) > 1:
        # Multiple matches - use ICST and NRT to disambiguate
        # Try ICST match first
        icst_match = candidates[candidates['ICST_Description'].str.contains(usace_icst.split()[0] if pd.notna(usace_icst) else '', case=False, na=False)]

        if len(icst_match) == 1:
            match = icst_match.iloc[0]
            matches.append({
                'USACE_Vessel_Name': vessel['Vessel_Name'],
                'USFlag_Vessel_Name': match[' VS_NAME'],
                'CG_Number': match[' CG_NUMBER'],
                'ICST_Code': match[' ICST'],
                'ICST_Description': match['ICST_Description'],
                'NRT': match[' NRT'],
                'HP': match[' HP'],
                'Length_ft': match[' REG_LNGTH'],
                'Beam_ft': match.get(' REG_BRDTH', None),
                'Capacity_Tons': match.get(' CAP_TONS', None),
                'Year_Built': match.get(' YEAR', None),
                'Base_Port': match.get(' BASE1', None),
                'State': match.get(' STATE', None),
                'Source_File': match['Source_File'],
                'Match_Quality': 'ICST_DISAMBIGUATED'
            })
        elif len(icst_match) > 1:
            # Try NRT match
            if pd.notna(usace_nrt):
                nrt_match = icst_match[abs(icst_match[' NRT'] - usace_nrt) < 100]
                if len(nrt_match) > 0:
                    match = nrt_match.iloc[0]
                    matches.append({
                        'USACE_Vessel_Name': vessel['Vessel_Name'],
                        'USFlag_Vessel_Name': match[' VS_NAME'],
                        'CG_Number': match[' CG_NUMBER'],
                        'ICST_Code': match[' ICST'],
                        'ICST_Description': match['ICST_Description'],
                        'NRT': match[' NRT'],
                        'HP': match[' HP'],
                        'Length_ft': match[' REG_LNGTH'],
                        'Beam_ft': match.get(' REG_BRDTH', None),
                        'Capacity_Tons': match.get(' CAP_TONS', None),
                        'Year_Built': match.get(' YEAR', None),
                        'Base_Port': match.get(' BASE1', None),
                        'State': match.get(' STATE', None),
                        'Source_File': match['Source_File'],
                        'Match_Quality': 'NRT_DISAMBIGUATED'
                    })
                else:
                    # Take first ICST match
                    match = icst_match.iloc[0]
                    matches.append({
                        'USACE_Vessel_Name': vessel['Vessel_Name'],
                        'USFlag_Vessel_Name': match[' VS_NAME'],
                        'CG_Number': match[' CG_NUMBER'],
                        'ICST_Code': match[' ICST'],
                        'ICST_Description': match['ICST_Description'],
                        'NRT': match[' NRT'],
                        'HP': match[' HP'],
                        'Length_ft': match[' REG_LNGTH'],
                        'Beam_ft': match.get(' REG_BRDTH', None),
                        'Capacity_Tons': match.get(' CAP_TONS', None),
                        'Year_Built': match.get(' YEAR', None),
                        'Base_Port': match.get(' BASE1', None),
                        'State': match.get(' STATE', None),
                        'Source_File': match['Source_File'],
                        'Match_Quality': 'FIRST_ICST_MATCH'
                    })
            else:
                # Take first match
                match = candidates.iloc[0]
                matches.append({
                    'USACE_Vessel_Name': vessel['Vessel_Name'],
                    'USFlag_Vessel_Name': match[' VS_NAME'],
                    'CG_Number': match[' CG_NUMBER'],
                    'ICST_Code': match[' ICST'],
                    'ICST_Description': match['ICST_Description'],
                    'NRT': match[' NRT'],
                    'HP': match[' HP'],
                    'Length_ft': match[' REG_LNGTH'],
                    'Beam_ft': match.get(' REG_BRDTH', None),
                    'Capacity_Tons': match.get(' CAP_TONS', None),
                    'Year_Built': match.get(' YEAR', None),
                    'Base_Port': match.get(' BASE1', None),
                    'State': match.get(' STATE', None),
                    'Source_File': match['Source_File'],
                    'Match_Quality': 'FIRST_MATCH'
                })
        else:
            # Take first candidate
            match = candidates.iloc[0]
            matches.append({
                'USACE_Vessel_Name': vessel['Vessel_Name'],
                'USFlag_Vessel_Name': match[' VS_NAME'],
                'CG_Number': match[' CG_NUMBER'],
                'ICST_Code': match[' ICST'],
                'ICST_Description': match['ICST_Description'],
                'NRT': match[' NRT'],
                'HP': match[' HP'],
                'Length_ft': match[' REG_LNGTH'],
                'Beam_ft': match.get(' REG_BRDTH', None),
                'Capacity_Tons': match.get(' CAP_TONS', None),
                'Year_Built': match.get(' YEAR', None),
                'Base_Port': match.get(' BASE1', None),
                'State': match.get(' STATE', None),
                'Source_File': match['Source_File'],
                'Match_Quality': 'FIRST_CANDIDATE'
            })
    else:
        # No match
        unmatched.append({
            'USACE_Vessel_Name': vessel['Vessel_Name'],
            'ICST_Vessel_Type': usace_icst,
            'NRT': usace_nrt
        })

print(f"\n   Matched: {len(matches):,}")
print(f"   Unmatched: {len(unmatched):,}")

# ============================================================================
# STEP 4: Update Port Call Master
# ============================================================================

print("\n6. Updating Port Call Master with US Flag data...")

# Create lookup dictionary
match_dict = {m['USACE_Vessel_Name']: m for m in matches}

# Add US Flag columns
portcall['USFlag_CG_Number'] = None
portcall['USFlag_ICST_Code'] = None
portcall['USFlag_ICST_Description'] = None
portcall['USFlag_HP'] = None
portcall['USFlag_Length_ft'] = None
portcall['USFlag_Beam_ft'] = None
portcall['USFlag_Capacity_Tons'] = None
portcall['USFlag_Year_Built'] = None
portcall['USFlag_Base_Port'] = None
portcall['USFlag_State'] = None
portcall['USFlag_Match_Quality'] = None

# Update matched vessels
for idx, row in portcall.iterrows():
    vessel_name = row['Vessel_Name']
    if vessel_name in match_dict:
        match = match_dict[vessel_name]
        portcall.loc[idx, 'USFlag_CG_Number'] = match['CG_Number']
        portcall.loc[idx, 'USFlag_ICST_Code'] = match['ICST_Code']
        portcall.loc[idx, 'USFlag_ICST_Description'] = match['ICST_Description']
        portcall.loc[idx, 'USFlag_HP'] = match['HP']
        portcall.loc[idx, 'USFlag_Length_ft'] = match['Length_ft']
        portcall.loc[idx, 'USFlag_Beam_ft'] = match['Beam_ft']
        portcall.loc[idx, 'USFlag_Capacity_Tons'] = match['Capacity_Tons']
        portcall.loc[idx, 'USFlag_Year_Built'] = match['Year_Built']
        portcall.loc[idx, 'USFlag_Base_Port'] = match['Base_Port']
        portcall.loc[idx, 'USFlag_State'] = match['State']
        portcall.loc[idx, 'USFlag_Match_Quality'] = match['Match_Quality']

        # Update Vessel_Type_Registry if still null
        if pd.isna(row['Vessel_Type_Registry']):
            portcall.loc[idx, 'Vessel_Type_Registry'] = match['ICST_Description']

# Save
print("\n7. Saving updated Port Call Master...")
portcall.to_csv(OUTPUT_FILE, index=False)
print(f"   Saved: {OUTPUT_FILE.name}")
file_size = OUTPUT_FILE.stat().st_size / (1024 * 1024)
print(f"   Size: {file_size:.1f} MB")

# ============================================================================
# SUMMARY
# ============================================================================

print("\n" + "="*80)
print("MATCH SUMMARY")
print("="*80)

print(f"\nUS Flag Inventory:")
print(f"  Total vessels in database: {len(us_register):,}")

print(f"\nPort Call Master - US Flag Vessels:")
us_flag_total = len(portcall[portcall['Flag_Country'] == 'United States of America'])
us_flag_matched_now = len(portcall[
    (portcall['Flag_Country'] == 'United States of America') &
    (portcall['USFlag_CG_Number'].notna())
])
print(f"  Total US flag port calls: {us_flag_total:,}")
print(f"  Matched to US Flag Register: {us_flag_matched_now:,}")
print(f"  Match rate: {us_flag_matched_now/us_flag_total*100:.1f}%")

print(f"\nMatch Quality Distribution:")
match_df = pd.DataFrame(matches)
if len(match_df) > 0:
    quality_counts = match_df['Match_Quality'].value_counts()
    for quality, count in quality_counts.items():
        print(f"  {quality:<25} {count:>6,}")

print(f"\nTop 10 Matched Vessel Types:")
if len(match_df) > 0:
    icst_counts = match_df['ICST_Description'].value_counts().head(10)
    for icst, count in icst_counts.items():
        print(f"  {icst:<40} {count:>5,}")

print(f"\nUnmatched US Flag Vessels: {len(unmatched):,}")
if len(unmatched) > 0:
    unmatched_df = pd.DataFrame(unmatched)
    print("\nTop 10 Unmatched Vessel Types:")
    unmatched_types = unmatched_df['ICST_Vessel_Type'].value_counts().head(10)
    for vtype, count in unmatched_types.items():
        print(f"  {vtype:<45} {count:>5,}")

# Save match report
match_report_file = Path(r"G:\My Drive\LLM\project_manifest\03_DOCUMENTATION/03.04_summaries\us_flag_match_report_v1.0.0.csv")
if len(match_df) > 0:
    match_df.to_csv(match_report_file, index=False)
    print(f"\nMatch report saved: {match_report_file.name}")

# Save unmatched report
unmatched_report_file = Path(r"G:\My Drive\LLM\project_manifest\03_DOCUMENTATION/03.04_summaries\us_flag_unmatched_v1.0.0.csv")
if len(unmatched) > 0:
    unmatched_df.to_csv(unmatched_report_file, index=False)
    print(f"Unmatched report saved: {unmatched_report_file.name}")

print("\n" + "="*80)
print("COMPLETE!")
print("="*80)
print(f"\nOutput: {OUTPUT_FILE}")

"""
Count Actual Matches - Fast Test
Version: 1.0.0
Purpose: Run matching logic and count matches without building full output
"""

import pandas as pd
from pathlib import Path

def parse_usace_date(date_val):
    if pd.isna(date_val):
        return None
    try:
        date_str = str(int(date_val)).zfill(5)
        month = int(date_str[:2])
        year_digit = int(date_str[2])
        day = int(date_str[3:])
        year = 2020 + year_digit
        return pd.Timestamp(year=year, month=month, day=day)
    except:
        return None

print("Loading data...")
ENTRANCE_FILE = Path(r"G:\My Drive\LLM\project_manifest\00_DATA/00.03_MATCHED\usace_2023_entrance_with_panjiva_match_v1.3.1.csv")
CLEARANCE_FILE = Path(r"G:\My Drive\LLM\project_manifest\00_DATA/00.03_MATCHED\usace_2023_clearance_with_panjiva_match_v1.0.1.csv")

entrance = pd.read_csv(ENTRANCE_FILE, low_memory=False)
clearance = pd.read_csv(CLEARANCE_FILE, low_memory=False)

print(f"Entrance: {len(entrance):,}")
print(f"Clearance: {len(clearance):,}")

# Parse dates
print("Parsing dates...")
entrance['Arrival_Date_Parsed'] = pd.to_datetime(entrance['Arrival_Date'], errors='coerce')
clearance['Clearance_Date_Parsed'] = clearance['Clearance_Date'].apply(parse_usace_date)

# Sort
print("Sorting...")
entrance_sorted = entrance.sort_values(['IMO', 'PORT', 'Arrival_Date_Parsed']).reset_index(drop=True)
clearance_sorted = clearance.sort_values(['IMO', 'PORT', 'Clearance_Date_Parsed']).reset_index(drop=True)

# Count matches
print("Counting matches...")
clearance_matched = set()
imo_matches = 0
name_matches = 0
no_matches = 0

for idx, ent_row in entrance_sorted.iterrows():
    if idx % 10000 == 0:
        print(f"  Processed {idx:,}/{len(entrance_sorted):,} - Matches so far: {imo_matches + name_matches:,}")

    vessel_imo = ent_row.get('IMO', '')
    vessel_name = ent_row.get('Vessel', '')
    port = ent_row.get('PORT', '')
    arrival_date = ent_row['Arrival_Date_Parsed']

    if pd.isna(arrival_date):
        no_matches += 1
        continue

    clear_match = None

    # Try IMO match
    if pd.notna(vessel_imo) and str(vessel_imo).strip() != '':
        candidates = clearance_sorted[
            (clearance_sorted['IMO'] == vessel_imo) &
            (clearance_sorted['PORT'] == port) &
            (clearance_sorted['Clearance_Date_Parsed'] > arrival_date) &
            (~clearance_sorted.index.isin(clearance_matched))
        ]

        if len(candidates) > 0:
            clear_match = candidates.iloc[0]
            clearance_matched.add(clear_match.name)
            imo_matches += 1

    # Try vessel name
    if clear_match is None and pd.notna(vessel_name) and str(vessel_name).strip() != '':
        candidates = clearance_sorted[
            (clearance_sorted['Vessel'] == vessel_name) &
            (clearance_sorted['PORT'] == port) &
            (clearance_sorted['Clearance_Date_Parsed'] > arrival_date) &
            (~clearance_sorted.index.isin(clearance_matched))
        ]

        if len(candidates) > 0:
            clear_match = candidates.iloc[0]
            clearance_matched.add(clear_match.name)
            name_matches += 1

    if clear_match is None:
        no_matches += 1

print("\n" + "="*60)
print("MATCHING RESULTS")
print("="*60)
print(f"Total entrances: {len(entrance_sorted):,}")
print(f"IMO matches: {imo_matches:,} ({imo_matches/len(entrance_sorted)*100:.1f}%)")
print(f"Name matches: {name_matches:,} ({name_matches/len(entrance_sorted)*100:.1f}%)")
print(f"No matches: {no_matches:,} ({no_matches/len(entrance_sorted)*100:.1f}%)")
print(f"Total BOTH: {imo_matches + name_matches:,} ({(imo_matches + name_matches)/len(entrance_sorted)*100:.1f}%)")
print(f"\nClearances matched: {len(clearance_matched):,} / {len(clearance_sorted):,} ({len(clearance_matched)/len(clearance_sorted)*100:.1f}%)")

"""
Match Tug-Barge Pairs Using Historical Pairing Patterns
Version: 1.0.0
Date: 2026-01-15

Purpose:
- Match unmatched tugs with unmatched barges at same port/date
- Use historical pairing patterns to disambiguate when multiple candidates
- Tugs typically stay with same barge for weeks/months/years

Logic:
1. Build historical pairing frequency (tug + barge at same port/date)
2. Match unmatched tugs/barges using:
   - Primary: Same PORT + same DATE (or ±1 day)
   - Disambiguation: Historical pairing frequency
3. Create TUG_BARGE_PAIR records

Input:
- Port call master: usace_2023_portcall_master_v1.0.0.csv

Output:
- Updated port call master with tug-barge pairs
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict

print("="*80)
print("TUG-BARGE PAIR MATCHING v1.0.0")
print("="*80)
print("\nUsing historical pairing patterns for disambiguation")

timestamp = datetime.now().strftime("%Y%m%d_%H%M")

# File paths
INPUT_FILE = Path(r"G:\My Drive\LLM\project_manifest\00_DATA/00.03_MATCHED\usace_2023_portcall_master_v1.0.0.csv")
OUTPUT_FILE = Path(r"G:\My Drive\LLM\project_manifest\00_DATA/00.03_MATCHED\usace_2023_portcall_master_v1.1.0.csv")

# Define vessel types
TUG_TYPES = ['TUG', 'PUSH BOAT', 'TUG/SUPPLY OFFSHORE SUPPORT']
BARGE_TYPES = ['DECK BARGE', 'OTHER TANK BARGE', 'DRY CARGO BARGE',
               'OTHER DRY CARGO BARGE NEI', 'COVERED DRY CARGO BARGE']

# Load data
print("\n1. Loading port call master...")
df = pd.read_csv(INPUT_FILE, low_memory=False)
print(f"   Total records: {len(df):,}")
print(f"   Match types: {df['Match_Type'].value_counts().to_dict()}")

# Parse dates
print("\n2. Parsing dates...")
df['Entrance_Date_Parsed'] = pd.to_datetime(df['Entrance_Arrival_Date'], errors='coerce')
df['Clearance_Date_Parsed'] = pd.to_datetime(df['Clearance_Clearance_Date'], errors='coerce')

# Identify tugs and barges in unmatched records
print("\n3. Identifying unmatched tugs and barges...")

# Unmatched entrances
entrance_only = df[df['Match_Type'] == 'ENTRANCE_ONLY'].copy()
entrance_tugs = entrance_only[entrance_only['Entrance_ICST_DESC'].isin(TUG_TYPES)]
entrance_barges = entrance_only[entrance_only['Entrance_ICST_DESC'].isin(BARGE_TYPES)]

print(f"   Unmatched entrance tugs: {len(entrance_tugs):,}")
print(f"   Unmatched entrance barges: {len(entrance_barges):,}")

# Unmatched clearances
clearance_only = df[df['Match_Type'] == 'CLEARANCE_ONLY'].copy()
clearance_tugs = clearance_only[clearance_only['Clearance_ICST_DESC'].isin(TUG_TYPES)]
clearance_barges = clearance_only[clearance_only['Clearance_ICST_DESC'].isin(BARGE_TYPES)]

print(f"   Unmatched clearance tugs: {len(clearance_tugs):,}")
print(f"   Unmatched clearance barges: {len(clearance_barges):,}")

# STEP 1: Build historical pairing frequency
print("\n4. Building historical pairing frequency...")
pairing_history = defaultdict(int)  # (tug_vessel, barge_vessel) -> count

# Look at ALL records (BOTH matched + unmatched) to find co-occurrences
all_records = df.copy()

# For entrance records
for port in all_records['Entrance_PORT'].dropna().unique():
    for date in all_records['Entrance_Date_Parsed'].dropna().unique():
        # Find all vessels at this port/date
        vessels_here = all_records[
            (all_records['Entrance_PORT'] == port) &
            (all_records['Entrance_Date_Parsed'] >= date - pd.Timedelta(days=1)) &
            (all_records['Entrance_Date_Parsed'] <= date + pd.Timedelta(days=1))
        ]

        tugs_here = vessels_here[vessels_here['Entrance_ICST_DESC'].isin(TUG_TYPES)]['Entrance_Vessel'].unique()
        barges_here = vessels_here[vessels_here['Entrance_ICST_DESC'].isin(BARGE_TYPES)]['Entrance_Vessel'].unique()

        # Record all tug-barge co-occurrences
        for tug in tugs_here:
            for barge in barges_here:
                pairing_history[(tug, barge)] += 1

# For clearance records
for port in all_records['Clearance_PORT'].dropna().unique():
    for date in all_records['Clearance_Date_Parsed'].dropna().unique():
        vessels_here = all_records[
            (all_records['Clearance_PORT'] == port) &
            (all_records['Clearance_Date_Parsed'] >= date - pd.Timedelta(days=1)) &
            (all_records['Clearance_Date_Parsed'] <= date + pd.Timedelta(days=1))
        ]

        tugs_here = vessels_here[vessels_here['Clearance_ICST_DESC'].isin(TUG_TYPES)]['Clearance_Vessel'].unique()
        barges_here = vessels_here[vessels_here['Clearance_ICST_DESC'].isin(BARGE_TYPES)]['Clearance_Vessel'].unique()

        for tug in tugs_here:
            for barge in barges_here:
                pairing_history[(tug, barge)] += 1

print(f"   Found {len(pairing_history):,} historical tug-barge co-occurrence patterns")

# Show top frequent pairs
print("\n   Top 10 most frequent tug-barge pairs:")
top_pairs = sorted(pairing_history.items(), key=lambda x: x[1], reverse=True)[:10]
for (tug, barge), count in top_pairs:
    print(f"      {tug[:30]} + {barge[:30]}: {count} times")

# STEP 2: Match unmatched tugs with barges (ENTRANCE)
print("\n5. Matching unmatched entrance tugs with barges...")
entrance_pairs = []
entrance_matched_indices = set()

for idx, tug_row in entrance_tugs.iterrows():
    if idx in entrance_matched_indices:
        continue

    tug_vessel = tug_row['Entrance_Vessel']
    tug_port = tug_row['Entrance_PORT']
    tug_date = tug_row['Entrance_Date_Parsed']

    if pd.isna(tug_date):
        continue

    # Find barges at same port within ±1 day
    barge_candidates = entrance_barges[
        (entrance_barges['Entrance_PORT'] == tug_port) &
        (entrance_barges['Entrance_Date_Parsed'] >= tug_date - pd.Timedelta(days=1)) &
        (entrance_barges['Entrance_Date_Parsed'] <= tug_date + pd.Timedelta(days=1)) &
        (~entrance_barges.index.isin(entrance_matched_indices))
    ]

    if len(barge_candidates) == 0:
        continue
    elif len(barge_candidates) == 1:
        # Easy case: only one barge
        barge_row = barge_candidates.iloc[0]
        entrance_pairs.append({
            'PORTCALL_ID': f"TUG_BARGE_ENT_{len(entrance_pairs)+1}",
            'Match_Type': 'TUG_BARGE_PAIR_ENTRANCE',
            'Tug_Vessel': tug_vessel,
            'Barge_Vessel': barge_row['Entrance_Vessel'],
            'PORT': tug_port,
            'Date': tug_date,
            'Pairing_Confidence': 'SINGLE_CANDIDATE',
            'Tug_Index': idx,
            'Barge_Index': barge_row.name
        })
        entrance_matched_indices.add(idx)
        entrance_matched_indices.add(barge_row.name)
    else:
        # Multiple barges - use historical pairing
        best_barge = None
        best_score = 0

        for barge_idx, barge_row in barge_candidates.iterrows():
            barge_vessel = barge_row['Entrance_Vessel']
            pairing_score = pairing_history.get((tug_vessel, barge_vessel), 0)

            if pairing_score > best_score:
                best_score = pairing_score
                best_barge = (barge_idx, barge_row, barge_vessel)

        if best_barge and best_score > 0:
            barge_idx, barge_row, barge_vessel = best_barge
            entrance_pairs.append({
                'PORTCALL_ID': f"TUG_BARGE_ENT_{len(entrance_pairs)+1}",
                'Match_Type': 'TUG_BARGE_PAIR_ENTRANCE',
                'Tug_Vessel': tug_vessel,
                'Barge_Vessel': barge_vessel,
                'PORT': tug_port,
                'Date': tug_date,
                'Pairing_Confidence': f'HISTORICAL_{best_score}X',
                'Tug_Index': idx,
                'Barge_Index': barge_idx
            })
            entrance_matched_indices.add(idx)
            entrance_matched_indices.add(barge_idx)

print(f"   Created {len(entrance_pairs):,} entrance tug-barge pairs")

# STEP 3: Match unmatched clearances
print("\n6. Matching unmatched clearance tugs with barges...")
clearance_pairs = []
clearance_matched_indices = set()

for idx, tug_row in clearance_tugs.iterrows():
    if idx in clearance_matched_indices:
        continue

    tug_vessel = tug_row['Clearance_Vessel']
    tug_port = tug_row['Clearance_PORT']
    tug_date = tug_row['Clearance_Date_Parsed']

    if pd.isna(tug_date):
        continue

    barge_candidates = clearance_barges[
        (clearance_barges['Clearance_PORT'] == tug_port) &
        (clearance_barges['Clearance_Date_Parsed'] >= tug_date - pd.Timedelta(days=1)) &
        (clearance_barges['Clearance_Date_Parsed'] <= tug_date + pd.Timedelta(days=1)) &
        (~clearance_barges.index.isin(clearance_matched_indices))
    ]

    if len(barge_candidates) == 0:
        continue
    elif len(barge_candidates) == 1:
        barge_row = barge_candidates.iloc[0]
        clearance_pairs.append({
            'PORTCALL_ID': f"TUG_BARGE_CLR_{len(clearance_pairs)+1}",
            'Match_Type': 'TUG_BARGE_PAIR_CLEARANCE',
            'Tug_Vessel': tug_vessel,
            'Barge_Vessel': barge_row['Clearance_Vessel'],
            'PORT': tug_port,
            'Date': tug_date,
            'Pairing_Confidence': 'SINGLE_CANDIDATE',
            'Tug_Index': idx,
            'Barge_Index': barge_row.name
        })
        clearance_matched_indices.add(idx)
        clearance_matched_indices.add(barge_row.name)
    else:
        best_barge = None
        best_score = 0

        for barge_idx, barge_row in barge_candidates.iterrows():
            barge_vessel = barge_row['Clearance_Vessel']
            pairing_score = pairing_history.get((tug_vessel, barge_vessel), 0)

            if pairing_score > best_score:
                best_score = pairing_score
                best_barge = (barge_idx, barge_row, barge_vessel)

        if best_barge and best_score > 0:
            barge_idx, barge_row, barge_vessel = best_barge
            clearance_pairs.append({
                'PORTCALL_ID': f"TUG_BARGE_CLR_{len(clearance_pairs)+1}",
                'Match_Type': 'TUG_BARGE_PAIR_CLEARANCE',
                'Tug_Vessel': tug_vessel,
                'Barge_Vessel': barge_vessel,
                'PORT': tug_port,
                'Date': tug_date,
                'Pairing_Confidence': f'HISTORICAL_{best_score}X',
                'Tug_Index': idx,
                'Barge_Index': barge_idx
            })
            clearance_matched_indices.add(idx)
            clearance_matched_indices.add(barge_idx)

print(f"   Created {len(clearance_pairs):,} clearance tug-barge pairs")

# STEP 4: Update Match_Type for paired records
print("\n7. Updating match types in master file...")

# Mark entrance pairs
for pair in entrance_pairs:
    df.loc[pair['Tug_Index'], 'Match_Type'] = 'TUG_BARGE_PAIR_ENTRANCE'
    df.loc[pair['Barge_Index'], 'Match_Type'] = 'TUG_BARGE_PAIR_ENTRANCE'
    df.loc[pair['Tug_Index'], 'Tug_Barge_Pair_ID'] = pair['PORTCALL_ID']
    df.loc[pair['Barge_Index'], 'Tug_Barge_Pair_ID'] = pair['PORTCALL_ID']
    df.loc[pair['Tug_Index'], 'Pairing_Confidence'] = pair['Pairing_Confidence']
    df.loc[pair['Barge_Index'], 'Pairing_Confidence'] = pair['Pairing_Confidence']

# Mark clearance pairs
for pair in clearance_pairs:
    df.loc[pair['Tug_Index'], 'Match_Type'] = 'TUG_BARGE_PAIR_CLEARANCE'
    df.loc[pair['Barge_Index'], 'Match_Type'] = 'TUG_BARGE_PAIR_CLEARANCE'
    df.loc[pair['Tug_Index'], 'Tug_Barge_Pair_ID'] = pair['PORTCALL_ID']
    df.loc[pair['Barge_Index'], 'Tug_Barge_Pair_ID'] = pair['PORTCALL_ID']
    df.loc[pair['Tug_Index'], 'Pairing_Confidence'] = pair['Pairing_Confidence']
    df.loc[pair['Barge_Index'], 'Pairing_Confidence'] = pair['Pairing_Confidence']

# Save updated file
print("\n8. Saving updated port call master...")
df.to_csv(OUTPUT_FILE, index=False)
print(f"   Saved: {OUTPUT_FILE.name}")

# Summary
print("\n" + "="*80)
print("TUG-BARGE PAIRING SUMMARY")
print("="*80)

print(f"\nOriginal unmatched:")
print(f"  Entrance tugs: {len(entrance_tugs):,}")
print(f"  Entrance barges: {len(entrance_barges):,}")
print(f"  Clearance tugs: {len(clearance_tugs):,}")
print(f"  Clearance barges: {len(clearance_barges):,}")

print(f"\nTug-Barge pairs created:")
print(f"  Entrance pairs: {len(entrance_pairs):,}")
print(f"  Clearance pairs: {len(clearance_pairs):,}")
print(f"  Total pairs: {len(entrance_pairs) + len(clearance_pairs):,}")

print(f"\nConfidence distribution:")
single_count = sum(1 for p in entrance_pairs + clearance_pairs if p['Pairing_Confidence'] == 'SINGLE_CANDIDATE')
historical_count = sum(1 for p in entrance_pairs + clearance_pairs if 'HISTORICAL' in p['Pairing_Confidence'])
print(f"  Single candidate (100% confidence): {single_count:,}")
print(f"  Historical pairing match: {historical_count:,}")

print(f"\nUpdated match type distribution:")
print(df['Match_Type'].value_counts())

print(f"\nReduction in unmatched:")
original_unmatched = len(entrance_tugs) + len(entrance_barges) + len(clearance_tugs) + len(clearance_barges)
pairs_matched = (len(entrance_pairs) + len(clearance_pairs)) * 2  # Each pair is 2 records
reduction = pairs_matched / original_unmatched * 100
print(f"  Original unmatched tug/barge records: {original_unmatched:,}")
print(f"  Now paired: {pairs_matched:,} ({reduction:.1f}%)")

print("\n" + "="*80)
print("COMPLETE!")
print("="*80)
print(f"\nOutput: {OUTPUT_FILE.name}")

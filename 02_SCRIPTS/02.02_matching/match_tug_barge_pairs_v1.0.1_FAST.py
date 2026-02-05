"""
Match Tug-Barge Pairs Using Historical Pairing Patterns - FAST VERSION
Version: 1.0.1
Date: 2026-01-15

Purpose:
- Match unmatched tugs with unmatched barges at same port/date
- Use historical pairing patterns (tugs stay with same barge for months/years)
- Optimized for speed using vectorized operations

Logic:
1. Build historical pairing frequency using efficient groupby
2. Match tugs + barges at same port/date (±1 day)
3. Disambiguate using historical pairing patterns
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
from collections import defaultdict

print("="*80)
print("TUG-BARGE PAIR MATCHING v1.0.1 FAST")
print("="*80)

timestamp = datetime.now().strftime("%Y%m%d_%H%M")

# File paths
INPUT_FILE = Path(r"G:\My Drive\LLM\project_manifest\00_DATA/00.03_MATCHED\usace_2023_portcall_master_v1.0.0.csv")
OUTPUT_FILE = Path(r"G:\My Drive\LLM\project_manifest\00_DATA/00.03_MATCHED\usace_2023_portcall_master_v1.1.0.csv")

# Vessel types
TUG_TYPES = ['TUG', 'PUSH BOAT', 'TUG/SUPPLY OFFSHORE SUPPORT']
BARGE_TYPES = ['DECK BARGE', 'OTHER TANK BARGE', 'DRY CARGO BARGE',
               'OTHER DRY CARGO BARGE NEI', 'COVERED DRY CARGO BARGE']

# Load
print("\n1. Loading data...")
df = pd.read_csv(INPUT_FILE, low_memory=False)
print(f"   Records: {len(df):,}")

# Parse dates
print("\n2. Parsing dates...")
df['Entrance_Date_Parsed'] = pd.to_datetime(df['Entrance_Arrival_Date'], errors='coerce')

# Create simplified date (YYYY-MM-DD) for grouping
df['Entrance_Date_Simple'] = df['Entrance_Date_Parsed'].dt.date

# Identify unmatched tugs/barges
print("\n3. Identifying unmatched tugs and barges...")
entrance_only = df[df['Match_Type'] == 'ENTRANCE_ONLY'].copy()

entrance_tugs = entrance_only[entrance_only['Entrance_ICST_DESC'].isin(TUG_TYPES)].copy()
entrance_barges = entrance_only[entrance_only['Entrance_ICST_DESC'].isin(BARGE_TYPES)].copy()

print(f"   Entrance tugs: {len(entrance_tugs):,}")
print(f"   Entrance barges: {len(entrance_barges):,}")

# FAST: Build historical pairing patterns
print("\n4. Building historical pairing patterns (FAST)...")

# For each date, find all tugs and barges that appeared together
entrance_tugs['Date_Simple'] = entrance_tugs['Entrance_Date_Parsed'].dt.date
entrance_barges['Date_Simple'] = entrance_barges['Entrance_Date_Parsed'].dt.date

# Group by port + date to find co-occurrences
pairing_count = defaultdict(int)

# Get unique port-date combinations where both tugs and barges exist
tug_port_dates = set(zip(entrance_tugs['Entrance_PORT'], entrance_tugs['Date_Simple']))
barge_port_dates = set(zip(entrance_barges['Entrance_PORT'], entrance_barges['Date_Simple']))
common_port_dates = tug_port_dates & barge_port_dates

print(f"   Found {len(common_port_dates):,} port-dates with both tugs and barges")

# For each common port-date, record all tug-barge pairs
for port, date in common_port_dates:
    tugs_here = entrance_tugs[
        (entrance_tugs['Entrance_PORT'] == port) &
        (entrance_tugs['Date_Simple'] == date)
    ]['Entrance_Vessel'].tolist()

    barges_here = entrance_barges[
        (entrance_barges['Entrance_PORT'] == port) &
        (entrance_barges['Date_Simple'] == date)
    ]['Entrance_Vessel'].tolist()

    # Record all combinations
    for tug in tugs_here:
        for barge in barges_here:
            pairing_count[(tug, barge)] += 1

print(f"   Historical pairing patterns: {len(pairing_count):,} unique tug-barge combinations")

# Show top pairs
if len(pairing_count) > 0:
    print("\n   Top 10 most frequent tug-barge pairs:")
    top_pairs = sorted(pairing_count.items(), key=lambda x: x[1], reverse=True)[:10]
    for (tug, barge), count in top_pairs:
        print(f"      {tug[:25]:<25} + {barge[:25]:<25}: {count}x")

# MATCH: Find tugs and barges at same port/date
print("\n5. Matching tugs with barges at same port/date...")

matched_pairs = []
matched_tug_indices = set()
matched_barge_indices = set()

for tug_idx, tug_row in entrance_tugs.iterrows():
    if tug_idx in matched_tug_indices:
        continue

    tug_vessel = tug_row['Entrance_Vessel']
    tug_port = tug_row['Entrance_PORT']
    tug_date = tug_row['Date_Simple']

    if pd.isna(tug_date):
        continue

    # Find barges at same port/date (±1 day)
    barge_candidates = entrance_barges[
        (entrance_barges['Entrance_PORT'] == tug_port) &
        (entrance_barges['Date_Simple'] >= tug_date - pd.Timedelta(days=1)) &
        (entrance_barges['Date_Simple'] <= tug_date + pd.Timedelta(days=1)) &
        (~entrance_barges.index.isin(matched_barge_indices))
    ]

    if len(barge_candidates) == 0:
        continue

    if len(barge_candidates) == 1:
        # Only one barge - perfect match
        barge_row = barge_candidates.iloc[0]
        matched_pairs.append({
            'Pair_ID': f"TB_ENT_{len(matched_pairs)+1}",
            'Tug_Index': tug_idx,
            'Barge_Index': barge_row.name,
            'Tug_Vessel': tug_vessel,
            'Barge_Vessel': barge_row['Entrance_Vessel'],
            'PORT': tug_port,
            'Date': tug_date,
            'Confidence': 'SINGLE'
        })
        matched_tug_indices.add(tug_idx)
        matched_barge_indices.add(barge_row.name)
    else:
        # Multiple barges - use historical pairing
        best_barge = None
        best_score = 0

        for barge_idx, barge_row in barge_candidates.iterrows():
            barge_vessel = barge_row['Entrance_Vessel']
            score = pairing_count.get((tug_vessel, barge_vessel), 0)

            if score > best_score:
                best_score = score
                best_barge = (barge_idx, barge_row, barge_vessel)

        if best_barge and best_score > 0:
            barge_idx, barge_row, barge_vessel = best_barge
            matched_pairs.append({
                'Pair_ID': f"TB_ENT_{len(matched_pairs)+1}",
                'Tug_Index': tug_idx,
                'Barge_Index': barge_idx,
                'Tug_Vessel': tug_vessel,
                'Barge_Vessel': barge_vessel,
                'PORT': tug_port,
                'Date': tug_date,
                'Confidence': f'HIST_{best_score}X'
            })
            matched_tug_indices.add(tug_idx)
            matched_barge_indices.add(barge_idx)
        elif len(barge_candidates) > 0:
            # No historical data - take first barge (random)
            barge_row = barge_candidates.iloc[0]
            matched_pairs.append({
                'Pair_ID': f"TB_ENT_{len(matched_pairs)+1}",
                'Tug_Index': tug_idx,
                'Barge_Index': barge_row.name,
                'Tug_Vessel': tug_vessel,
                'Barge_Vessel': barge_row['Entrance_Vessel'],
                'PORT': tug_port,
                'Date': tug_date,
                'Confidence': 'NO_HISTORY'
            })
            matched_tug_indices.add(tug_idx)
            matched_barge_indices.add(barge_row.name)

print(f"   Created {len(matched_pairs):,} tug-barge pairs")

# Update Match_Type
print("\n6. Updating match types...")
df['Tug_Barge_Pair_ID'] = None
df['Pairing_Confidence'] = None

for pair in matched_pairs:
    df.loc[pair['Tug_Index'], 'Match_Type'] = 'TUG_BARGE_PAIR'
    df.loc[pair['Barge_Index'], 'Match_Type'] = 'TUG_BARGE_PAIR'
    df.loc[pair['Tug_Index'], 'Tug_Barge_Pair_ID'] = pair['Pair_ID']
    df.loc[pair['Barge_Index'], 'Tug_Barge_Pair_ID'] = pair['Pair_ID']
    df.loc[pair['Tug_Index'], 'Pairing_Confidence'] = pair['Confidence']
    df.loc[pair['Barge_Index'], 'Pairing_Confidence'] = pair['Confidence']

# Save
print("\n7. Saving...")
df.to_csv(OUTPUT_FILE, index=False)
print(f"   Saved: {OUTPUT_FILE.name}")

# Summary
print("\n" + "="*80)
print("SUMMARY")
print("="*80)
print(f"\nOriginal unmatched tugs/barges: {len(entrance_tugs) + len(entrance_barges):,}")
print(f"Tug-barge pairs created: {len(matched_pairs):,}")
print(f"Records now paired: {len(matched_pairs) * 2:,} ({len(matched_pairs)*2/(len(entrance_tugs)+len(entrance_barges))*100:.1f}%)")

print(f"\nConfidence distribution:")
single = sum(1 for p in matched_pairs if p['Confidence'] == 'SINGLE')
hist = sum(1 for p in matched_pairs if 'HIST' in p['Confidence'])
no_hist = sum(1 for p in matched_pairs if p['Confidence'] == 'NO_HISTORY')
print(f"  SINGLE (only 1 candidate): {single:,}")
print(f"  HIST (historical pairing): {hist:,}")
print(f"  NO_HISTORY (random pick): {no_hist:,}")

print(f"\nUpdated match type distribution:")
print(df['Match_Type'].value_counts())

print("\n" + "="*80)
print("COMPLETE!")
print("="*80)

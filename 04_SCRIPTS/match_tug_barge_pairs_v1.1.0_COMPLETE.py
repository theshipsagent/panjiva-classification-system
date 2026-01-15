"""
Match Tug-Barge Pairs - ENTRANCE AND CLEARANCE
Version: 1.1.0
Date: 2026-01-15

Purpose:
- Match unmatched tugs with barges for BOTH entrance and clearance
- Use historical pairing patterns for disambiguation
- Fast vectorized operations
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
from collections import defaultdict

print("="*80)
print("TUG-BARGE PAIR MATCHING v1.1.0 COMPLETE")
print("="*80)
print("Processing BOTH entrance and clearance records")

timestamp = datetime.now().strftime("%Y%m%d_%H%M")

# File paths
INPUT_FILE = Path(r"G:\My Drive\LLM\project_manifest\02_STAGE02_CLASSIFICATION\usace_2023_portcall_master_v1.0.0.csv")
OUTPUT_FILE = Path(r"G:\My Drive\LLM\project_manifest\02_STAGE02_CLASSIFICATION\usace_2023_portcall_master_v1.1.0.csv")

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
df['Clearance_Date_Parsed'] = pd.to_datetime(df['Clearance_Clearance_Date'], errors='coerce')

# ============================================================================
# ENTRANCE TUG-BARGE MATCHING
# ============================================================================

print("\n" + "="*80)
print("ENTRANCE TUG-BARGE MATCHING")
print("="*80)

entrance_only = df[df['Match_Type'] == 'ENTRANCE_ONLY'].copy()
entrance_tugs = entrance_only[entrance_only['Entrance_ICST_DESC'].isin(TUG_TYPES)].copy()
entrance_barges = entrance_only[entrance_only['Entrance_ICST_DESC'].isin(BARGE_TYPES)].copy()

print(f"\n3. Unmatched entrance tugs: {len(entrance_tugs):,}")
print(f"   Unmatched entrance barges: {len(entrance_barges):,}")

# Build historical pairing for entrance
print("\n4. Building entrance historical pairing patterns...")
entrance_tugs['Date_Simple'] = entrance_tugs['Entrance_Date_Parsed'].dt.date
entrance_barges['Date_Simple'] = entrance_barges['Entrance_Date_Parsed'].dt.date

pairing_ent = defaultdict(int)

tug_port_dates = set(zip(entrance_tugs['Entrance_PORT'], entrance_tugs['Date_Simple']))
barge_port_dates = set(zip(entrance_barges['Entrance_PORT'], entrance_barges['Date_Simple']))
common_port_dates = tug_port_dates & barge_port_dates

for port, date in common_port_dates:
    tugs_here = entrance_tugs[
        (entrance_tugs['Entrance_PORT'] == port) &
        (entrance_tugs['Date_Simple'] == date)
    ]['Entrance_Vessel'].tolist()

    barges_here = entrance_barges[
        (entrance_barges['Entrance_PORT'] == port) &
        (entrance_barges['Date_Simple'] == date)
    ]['Entrance_Vessel'].tolist()

    for tug in tugs_here:
        for barge in barges_here:
            pairing_ent[(tug, barge)] += 1

print(f"   Entrance historical patterns: {len(pairing_ent):,} unique combinations")

# Match entrance tugs with barges
print("\n5. Matching entrance tugs with barges...")
entrance_pairs = []
matched_tug_ent = set()
matched_barge_ent = set()

for tug_idx, tug_row in entrance_tugs.iterrows():
    if tug_idx in matched_tug_ent:
        continue

    tug_vessel = tug_row['Entrance_Vessel']
    tug_port = tug_row['Entrance_PORT']
    tug_date = tug_row['Date_Simple']

    if pd.isna(tug_date):
        continue

    barge_candidates = entrance_barges[
        (entrance_barges['Entrance_PORT'] == tug_port) &
        (entrance_barges['Date_Simple'] >= tug_date - pd.Timedelta(days=1)) &
        (entrance_barges['Date_Simple'] <= tug_date + pd.Timedelta(days=1)) &
        (~entrance_barges.index.isin(matched_barge_ent))
    ]

    if len(barge_candidates) == 0:
        continue

    if len(barge_candidates) == 1:
        barge_row = barge_candidates.iloc[0]
        entrance_pairs.append({
            'Pair_ID': f"TB_ENT_{len(entrance_pairs)+1}",
            'Tug_Index': tug_idx,
            'Barge_Index': barge_row.name,
            'Confidence': 'SINGLE'
        })
        matched_tug_ent.add(tug_idx)
        matched_barge_ent.add(barge_row.name)
    else:
        best_barge = None
        best_score = 0

        for barge_idx, barge_row in barge_candidates.iterrows():
            barge_vessel = barge_row['Entrance_Vessel']
            score = pairing_ent.get((tug_vessel, barge_vessel), 0)

            if score > best_score:
                best_score = score
                best_barge = (barge_idx, barge_row, barge_vessel)

        if best_barge and best_score > 0:
            barge_idx, barge_row, barge_vessel = best_barge
            entrance_pairs.append({
                'Pair_ID': f"TB_ENT_{len(entrance_pairs)+1}",
                'Tug_Index': tug_idx,
                'Barge_Index': barge_idx,
                'Confidence': f'HIST_{best_score}X'
            })
            matched_tug_ent.add(tug_idx)
            matched_barge_ent.add(barge_idx)

print(f"   Entrance pairs created: {len(entrance_pairs):,}")

# ============================================================================
# CLEARANCE TUG-BARGE MATCHING
# ============================================================================

print("\n" + "="*80)
print("CLEARANCE TUG-BARGE MATCHING")
print("="*80)

clearance_only = df[df['Match_Type'] == 'CLEARANCE_ONLY'].copy()
clearance_tugs = clearance_only[clearance_only['Clearance_ICST_DESC'].isin(TUG_TYPES)].copy()
clearance_barges = clearance_only[clearance_only['Clearance_ICST_DESC'].isin(BARGE_TYPES)].copy()

print(f"\n6. Unmatched clearance tugs: {len(clearance_tugs):,}")
print(f"   Unmatched clearance barges: {len(clearance_barges):,}")

# Build historical pairing for clearance
print("\n7. Building clearance historical pairing patterns...")
clearance_tugs['Date_Simple'] = clearance_tugs['Clearance_Date_Parsed'].dt.date
clearance_barges['Date_Simple'] = clearance_barges['Clearance_Date_Parsed'].dt.date

pairing_clr = defaultdict(int)

tug_port_dates_clr = set(zip(clearance_tugs['Clearance_PORT'], clearance_tugs['Date_Simple']))
barge_port_dates_clr = set(zip(clearance_barges['Clearance_PORT'], clearance_barges['Date_Simple']))
common_port_dates_clr = tug_port_dates_clr & barge_port_dates_clr

for port, date in common_port_dates_clr:
    tugs_here = clearance_tugs[
        (clearance_tugs['Clearance_PORT'] == port) &
        (clearance_tugs['Date_Simple'] == date)
    ]['Clearance_Vessel'].tolist()

    barges_here = clearance_barges[
        (clearance_barges['Clearance_PORT'] == port) &
        (clearance_barges['Date_Simple'] == date)
    ]['Clearance_Vessel'].tolist()

    for tug in tugs_here:
        for barge in barges_here:
            pairing_clr[(tug, barge)] += 1

print(f"   Clearance historical patterns: {len(pairing_clr):,} unique combinations")

# Match clearance tugs with barges
print("\n8. Matching clearance tugs with barges...")
clearance_pairs = []
matched_tug_clr = set()
matched_barge_clr = set()

for tug_idx, tug_row in clearance_tugs.iterrows():
    if tug_idx in matched_tug_clr:
        continue

    tug_vessel = tug_row['Clearance_Vessel']
    tug_port = tug_row['Clearance_PORT']
    tug_date = tug_row['Date_Simple']

    if pd.isna(tug_date):
        continue

    barge_candidates = clearance_barges[
        (clearance_barges['Clearance_PORT'] == tug_port) &
        (clearance_barges['Date_Simple'] >= tug_date - pd.Timedelta(days=1)) &
        (clearance_barges['Date_Simple'] <= tug_date + pd.Timedelta(days=1)) &
        (~clearance_barges.index.isin(matched_barge_clr))
    ]

    if len(barge_candidates) == 0:
        continue

    if len(barge_candidates) == 1:
        barge_row = barge_candidates.iloc[0]
        clearance_pairs.append({
            'Pair_ID': f"TB_CLR_{len(clearance_pairs)+1}",
            'Tug_Index': tug_idx,
            'Barge_Index': barge_row.name,
            'Confidence': 'SINGLE'
        })
        matched_tug_clr.add(tug_idx)
        matched_barge_clr.add(barge_row.name)
    else:
        best_barge = None
        best_score = 0

        for barge_idx, barge_row in barge_candidates.iterrows():
            barge_vessel = barge_row['Clearance_Vessel']
            score = pairing_clr.get((tug_vessel, barge_vessel), 0)

            if score > best_score:
                best_score = score
                best_barge = (barge_idx, barge_row, barge_vessel)

        if best_barge and best_score > 0:
            barge_idx, barge_row, barge_vessel = best_barge
            clearance_pairs.append({
                'Pair_ID': f"TB_CLR_{len(clearance_pairs)+1}",
                'Tug_Index': tug_idx,
                'Barge_Index': barge_idx,
                'Confidence': f'HIST_{best_score}X'
            })
            matched_tug_clr.add(tug_idx)
            matched_barge_clr.add(barge_idx)

print(f"   Clearance pairs created: {len(clearance_pairs):,}")

# ============================================================================
# UPDATE DATAFRAME
# ============================================================================

print("\n" + "="*80)
print("UPDATING PORT CALL MASTER")
print("="*80)

# Initialize columns
df['Tug_Barge_Pair_ID'] = None
df['Pairing_Confidence'] = None

# Update entrance pairs
for pair in entrance_pairs:
    df.loc[pair['Tug_Index'], 'Match_Type'] = 'TUG_BARGE_PAIR'
    df.loc[pair['Barge_Index'], 'Match_Type'] = 'TUG_BARGE_PAIR'
    df.loc[pair['Tug_Index'], 'Tug_Barge_Pair_ID'] = pair['Pair_ID']
    df.loc[pair['Barge_Index'], 'Tug_Barge_Pair_ID'] = pair['Pair_ID']
    df.loc[pair['Tug_Index'], 'Pairing_Confidence'] = pair['Confidence']
    df.loc[pair['Barge_Index'], 'Pairing_Confidence'] = pair['Confidence']

# Update clearance pairs
for pair in clearance_pairs:
    df.loc[pair['Tug_Index'], 'Match_Type'] = 'TUG_BARGE_PAIR'
    df.loc[pair['Barge_Index'], 'Match_Type'] = 'TUG_BARGE_PAIR'
    df.loc[pair['Tug_Index'], 'Tug_Barge_Pair_ID'] = pair['Pair_ID']
    df.loc[pair['Barge_Index'], 'Tug_Barge_Pair_ID'] = pair['Pair_ID']
    df.loc[pair['Tug_Index'], 'Pairing_Confidence'] = pair['Confidence']
    df.loc[pair['Barge_Index'], 'Pairing_Confidence'] = pair['Confidence']

# Save
print("\n9. Saving updated file...")
df.to_csv(OUTPUT_FILE, index=False)
print(f"   Saved: {OUTPUT_FILE.name}")
file_size = OUTPUT_FILE.stat().st_size / (1024 * 1024)
print(f"   Size: {file_size:.1f} MB")

# ============================================================================
# SUMMARY
# ============================================================================

print("\n" + "="*80)
print("FINAL SUMMARY")
print("="*80)

print(f"\nENTRANCE Results:")
print(f"  Original unmatched tugs: {len(entrance_tugs):,}")
print(f"  Original unmatched barges: {len(entrance_barges):,}")
print(f"  Pairs created: {len(entrance_pairs):,}")
print(f"  Records paired: {len(entrance_pairs)*2:,} ({len(entrance_pairs)*2/(len(entrance_tugs)+len(entrance_barges))*100:.1f}%)")

print(f"\nCLEARANCE Results:")
print(f"  Original unmatched tugs: {len(clearance_tugs):,}")
print(f"  Original unmatched barges: {len(clearance_barges):,}")
print(f"  Pairs created: {len(clearance_pairs):,}")
print(f"  Records paired: {len(clearance_pairs)*2:,} ({len(clearance_pairs)*2/(len(clearance_tugs)+len(clearance_barges))*100:.1f}%)")

print(f"\nTOTAL Tug-Barge Operations:")
print(f"  Total pairs: {len(entrance_pairs) + len(clearance_pairs):,}")
print(f"  Total records: {(len(entrance_pairs) + len(clearance_pairs))*2:,}")

print(f"\nUpdated Match Type Distribution:")
match_counts = df['Match_Type'].value_counts()
for match_type, count in match_counts.items():
    pct = count / len(df) * 100
    print(f"  {match_type:<25} {count:>7,} ({pct:>5.1f}%)")

print(f"\nCargo Vessel Port Calls (BOTH): {match_counts.get('BOTH', 0):,}")
print(f"Tug-Barge Operations: {match_counts.get('TUG_BARGE_PAIR', 0)//2:,} operations ({match_counts.get('TUG_BARGE_PAIR', 0):,} records)")

remaining_ent = match_counts.get('ENTRANCE_ONLY', 0)
remaining_clr = match_counts.get('CLEARANCE_ONLY', 0)
print(f"Remaining unmatched: {remaining_ent + remaining_clr:,}")

print("\n" + "="*80)
print("COMPLETE!")
print("="*80)
print(f"\nOutput: {OUTPUT_FILE}")

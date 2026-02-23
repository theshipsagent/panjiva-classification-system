"""
Terminal Visit Matching with Business Rules
============================================
1. Extract terminal visits from raw MRTIS zone reports (first arrival + last departure)
2. Apply VesselType cleanup and default cargo assignments
3. Merge zone dictionary attributes (ZoneType, Activity, Cargoes)
4. Apply ZoneType-based defaults
5. Match to Panjiva manifests (imports - DISCHARGE operations)
6. Match to FGIS grain exports (exports - LOADING operations)
7. Validate and override incompatible combinations
8. Save results with full audit trail
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

import pandas as pd
from datetime import datetime, timedelta
sys.path.insert(0, 'G:/My Drive/LLM/project_mrtis')
from src.data.vessel_name_normalizer import build_name_key

print("="*80)
print("TERMINAL VISIT MATCHING WITH BUSINESS RULES")
print("="*80)

# ═══════════════════════════════════════════════════════════════════════════
# 1. LOAD ZONE DICTIONARY
# ═══════════════════════════════════════════════════════════════════════════
print("\n1. Loading zone dictionary...")
zone_dict = pd.read_csv('G:/My Drive/LLM/project_mrtis/terminal_zone_dictionary.csv', dtype=str)
print(f"   Zones: {len(zone_dict):,}")
print(f"   Columns: {list(zone_dict.columns)}")

# Build zone lookup
zone_lookup = {}
for _, row in zone_dict.iterrows():
    zone_lookup[row['Zone'].strip()] = {
        'Facility': row.get('Facility', ''),
        'VesselTypes': row.get('Vessel Types', ''),
        'Activity': row.get('Activity', ''),
        'Cargoes': row.get('Cargoes', ''),
        'ZoneType': row.get('ZoneType', ''),
        'Note': row.get('Note', ''),
    }

# Terminal zones only (exclude anchorages)
# Strip whitespace from Activity column for matching
zone_dict['Activity_clean'] = zone_dict['Activity'].str.strip()
terminal_zones = set(zone_dict[zone_dict['Activity_clean'].isin(['Discharge - Only', 'Load - Only', 'Load or Discharge'])]['Zone'].str.strip())
print(f"   Terminal zones (cargo facilities): {len(terminal_zones)}")

# ═══════════════════════════════════════════════════════════════════════════
# 2. EXTRACT TERMINAL VISITS FROM RAW ZONE REPORTS
# ═══════════════════════════════════════════════════════════════════════════
print("\n2. Extracting terminal visits from raw zone reports...")
src_dir = 'G:/My Drive/LLM/project_mrtis/00_source_files/'
files_2024 = [
    'Zone Report 01-01-24 - 12-31-24.csv',
    'Zone Report 01-01-24 - 12-31-24 (1).csv',
    'Zone Report 01-01-24 - 12-31-24 (2).csv',
    'Zone Report 01-01-24 - 12-31-24 (3).csv'
]

dfs = []
for f in files_2024:
    try:
        df = pd.read_csv(src_dir + f, dtype=str, low_memory=False)
        dfs.append(df)
    except:
        pass

raw = pd.concat(dfs, ignore_index=True)
print(f"   Raw zone events: {len(raw):,}")

# Filter to terminal zones only
raw['Zone_clean'] = raw['Zone'].str.strip()
terminal_events = raw[raw['Zone_clean'].isin(terminal_zones)].copy()
print(f"   Terminal zone events: {len(terminal_events):,}")

# Parse time and draft
terminal_events['Time_dt'] = pd.to_datetime(terminal_events['Time'], errors='coerce')
terminal_events['Draft_ft'] = terminal_events['Draft'].str.replace('ft','').str.strip()
terminal_events['Draft_ft'] = pd.to_numeric(terminal_events['Draft_ft'], errors='coerce')

# Sort by vessel and time
terminal_events = terminal_events.sort_values(['Name','IMO','Time_dt']).reset_index(drop=True)

# Extract terminal visits (Arrive → Depart pairs)
# Group by vessel + zone, then pair arrivals with departures
# Use FIRST arrival + LAST departure per visit to handle errant duplicates
visits = []
terminal_events['VesselKey'] = terminal_events['Name'].fillna('') + '|' + terminal_events['Zone_clean'].fillna('')

for vessel_zone_key, group in terminal_events.groupby('VesselKey'):
    if not vessel_zone_key or '|' not in vessel_zone_key:
        continue

    group = group.sort_values('Time_dt').reset_index(drop=True)

    # Sequentially pair Arrive → Depart events
    # Multiple arrivals/departures within one visit = use first/last
    i = 0
    while i < len(group):
        row = group.iloc[i]

        if row['Action'] == 'Arrive':
            # Collect all arrivals until we hit a departure
            arrivals = [row]
            j = i + 1
            while j < len(group) and group.iloc[j]['Action'] == 'Arrive':
                arrivals.append(group.iloc[j])
                j += 1

            # Collect all departures after the arrivals
            departures = []
            while j < len(group) and group.iloc[j]['Action'] == 'Depart':
                departures.append(group.iloc[j])
                j += 1

            if len(departures) > 0:
                # Use FIRST arrival and LAST departure
                arrive_row = arrivals[0]
                depart_row = departures[-1]

                visits.append({
                    'IMO': arrive_row['IMO'],
                    'VesselName': arrive_row['Name'],
                    'TerminalZone': arrive_row['Zone_clean'],
                    'ArrivalTime': arrive_row['Time'],
                    'DepartureTime': depart_row['Time'],
                    'ArrivalDraft_ft': arrive_row['Draft_ft'],
                    'DepartureDraft_ft': depart_row['Draft_ft'],
                    'DraftDelta_ft': depart_row['Draft_ft'] - arrive_row['Draft_ft'] if pd.notna(arrive_row['Draft_ft']) and pd.notna(depart_row['Draft_ft']) else None,
                    'Agent': arrive_row.get('Agent',''),
                    'VesselType': arrive_row.get('Type',''),
                })

            i = j if j > i else i + 1
        else:
            # Skip standalone departures (no matching arrival)
            i += 1

visits_df = pd.DataFrame(visits)

# Filter out service vessels (tugs, dredges, service boats)
exclude_vessels = ['Mack B', 'Allison', 'Allisonk', 'Bonita Aki']
visits_df = visits_df[~visits_df['VesselName'].isin(exclude_vessels)].copy()
print(f"   Terminal visits extracted: {len(visits_df):,} (service vessels excluded)")

# Parse datetime
visits_df['ArrivalTime_dt'] = pd.to_datetime(visits_df['ArrivalTime'], errors='coerce')
visits_df['DepartureTime_dt'] = pd.to_datetime(visits_df['DepartureTime'], errors='coerce')
visits_df['DraftDelta_ft'] = pd.to_numeric(visits_df['DraftDelta_ft'], errors='coerce')
visits_df['ArrivalDraft_ft'] = pd.to_numeric(visits_df['ArrivalDraft_ft'], errors='coerce')
visits_df['DepartureDraft_ft'] = pd.to_numeric(visits_df['DepartureDraft_ft'], errors='coerce')

# ═══════════════════════════════════════════════════════════════════════════
# 3. MERGE ZONE DICTIONARY ATTRIBUTES
# ═══════════════════════════════════════════════════════════════════════════
print("\n3. Merging zone dictionary attributes...")
visits_df['Facility'] = visits_df['TerminalZone'].map(lambda z: zone_lookup.get(z, {}).get('Facility', ''))
visits_df['ZoneVesselTypes'] = visits_df['TerminalZone'].map(lambda z: zone_lookup.get(z, {}).get('VesselTypes', ''))
visits_df['ZoneActivity'] = visits_df['TerminalZone'].map(lambda z: zone_lookup.get(z, {}).get('Activity', ''))
visits_df['ZoneCargoes'] = visits_df['TerminalZone'].map(lambda z: zone_lookup.get(z, {}).get('Cargoes', ''))
visits_df['ZoneType'] = visits_df['TerminalZone'].map(lambda z: zone_lookup.get(z, {}).get('ZoneType', ''))
visits_df['ZoneNote'] = visits_df['TerminalZone'].map(lambda z: zone_lookup.get(z, {}).get('Note', ''))

# ═══════════════════════════════════════════════════════════════════════════
# 4. VESSELTYPE CLEANUP AND DEFAULT CARGO ASSIGNMENTS
# ═══════════════════════════════════════════════════════════════════════════
print("\n4. Applying VesselType cleanup and defaults...")

# Standardize VesselType: find/replace variations of "Bulk"
visits_df['VesselType_Clean'] = visits_df['VesselType'].str.strip()
visits_df.loc[visits_df['VesselType_Clean'].str.contains('Bulk', case=False, na=False), 'VesselType_Clean'] = 'Bulk'

# Classify operation type based on draft delta
def classify_op(delta):
    if pd.isna(delta):
        return 'UNKNOWN'
    if delta < -2:
        return 'DISCHARGE'
    if delta > 2:
        return 'LOADING'
    return 'UNKNOWN'

visits_df['OperationType'] = visits_df['DraftDelta_ft'].apply(classify_op)

# Initialize default cargo columns
visits_df['DefaultCargoGroup'] = ''
visits_df['DefaultCargoCommodity'] = ''
visits_df['DefaultCargo'] = ''
visits_df['DefaultSource'] = ''

# VesselType-based defaults
vesseltype_rules = {
    'Cont': {'Group': 'Break Bulk', 'Commodity': 'Containers', 'Cargo': 'Containers'},
    'Reef': {'Group': 'Break Bulk', 'Commodity': 'Reefer', 'Cargo': 'Reefer'},
    'Pass': {'Group': 'Break Bulk', 'Commodity': 'Passengers', 'Cargo': 'Passengers'},
    'Bulk': {'Group': 'Dry Bulk', 'Commodity': 'Bulk', 'Cargo': 'Bulk'},
    'Tank': {'Group': 'Liquid Bulk', 'Commodity': 'Liquid Bulk', 'Cargo': 'Liquid Bulk'},
    'Gas': {'Group': 'Liquid Gas', 'Commodity': 'Liquid Gas', 'Cargo': 'Liquid Gas'},
}

for vtype, cargo in vesseltype_rules.items():
    mask = visits_df['VesselType_Clean'] == vtype
    visits_df.loc[mask, 'DefaultCargoGroup'] = cargo['Group']
    visits_df.loc[mask, 'DefaultCargoCommodity'] = cargo['Commodity']
    visits_df.loc[mask, 'DefaultCargo'] = cargo['Cargo']
    visits_df.loc[mask, 'DefaultSource'] = f'VesselType={vtype}'

print(f"   VesselType defaults applied: {(visits_df['DefaultSource'] != '').sum():,}")

# ═══════════════════════════════════════════════════════════════════════════
# 5. ZONETYPE-BASED DEFAULT CARGO ASSIGNMENTS
# ═══════════════════════════════════════════════════════════════════════════
print("\n5. Applying ZoneType-based defaults...")

# ZoneType rules
zonetype_rules = {
    'Elevator': {'Group': 'Dry Bulk', 'Commodity': 'Agricultural', 'Cargo': 'Grain', 'OpType': 'LOADING'},
}

for ztype, cargo in zonetype_rules.items():
    mask = (visits_df['ZoneType'] == ztype) & (visits_df['OperationType'] == cargo['OpType'])
    # Only override if no VesselType default was set
    mask_no_default = mask & (visits_df['DefaultSource'] == '')
    visits_df.loc[mask_no_default, 'DefaultCargoGroup'] = cargo['Group']
    visits_df.loc[mask_no_default, 'DefaultCargoCommodity'] = cargo['Commodity']
    visits_df.loc[mask_no_default, 'DefaultCargo'] = cargo['Cargo']
    visits_df.loc[mask_no_default, 'DefaultSource'] = f'ZoneType={ztype}'

print(f"   ZoneType defaults applied: {(visits_df['DefaultSource'].str.contains('ZoneType', na=False)).sum():,}")

# ═══════════════════════════════════════════════════════════════════════════
# 6. MATCH TO PANJIVA MANIFESTS (IMPORTS + EXPORTS)
# ═══════════════════════════════════════════════════════════════════════════
print("\n6. Matching to Panjiva manifests (imports + exports)...")

# Load import manifest (2024)
imp = pd.read_csv('G:/My Drive/LLM/project_manifest/PIPELINE/phase_07_enrichment/phase_07_output.csv',
                  usecols=['Arrival Date','Vessel','IMO','Port_Consolidated','Group','Commodity','Cargo','Tons','Bill of Lading Number','Shipper','Consignee'],
                  dtype=str, low_memory=False)
imp = imp[imp['Port_Consolidated'] == 'New Orleans'].copy()
imp['_date'] = pd.to_datetime(imp['Arrival Date'], errors='coerce').dt.date
imp = imp[imp['_date'].apply(lambda d: d.year if pd.notna(d) else 0) == 2024].copy()
imp = imp[imp['Group'] != 'EXCLUDED'].copy()
imp['_imo'] = imp['IMO'].fillna('').str.strip()
imp['_nk'] = imp['Vessel'].apply(lambda v: build_name_key(v) if pd.notna(v) else '')
print(f"   Import manifest: {len(imp):,} records")

# Load export manifest
try:
    exp = pd.read_csv('G:/My Drive/LLM/project_manifest/PIPELINE_EXPORTS/phase_07_enrichment/phase_07_output.csv',
                      usecols=['Arrival Date','Vessel','IMO','Port of Discharge (D)','Group','Commodity','Cargo','Tons','Bill of Lading Number','Shipper','Consignee'],
                      dtype=str, low_memory=False)
    exp = exp[exp['Port of Discharge (D)'].str.contains('New Orleans', case=False, na=False)].copy()
    exp['_date'] = pd.to_datetime(exp['Arrival Date'], errors='coerce').dt.date  # Export date (US departure)
    exp = exp[exp['_date'].apply(lambda d: d.year if pd.notna(d) else 0) == 2024].copy()
    exp = exp[exp['Group'] != 'EXCLUDED'].copy()
    exp['_imo'] = exp['IMO'].fillna('').str.strip()
    exp['_nk'] = exp['Vessel'].apply(lambda v: build_name_key(v) if pd.notna(v) else '')
    print(f"   Export manifest: {len(exp):,} records")
except Exception as e:
    exp = pd.DataFrame()
    print(f"   Export manifest: not available ({e})")

# Build import indices
imp_imo_idx = {}
imp_name_idx = {}
for _, row in imp.iterrows():
    imo = row['_imo']
    nk = row['_nk']
    if imo:
        if imo not in imp_imo_idx:
            imp_imo_idx[imo] = []
        imp_imo_idx[imo].append(row)
    if nk:
        if nk not in imp_name_idx:
            imp_name_idx[nk] = []
        imp_name_idx[nk].append(row)

# Build export indices
exp_imo_idx = {}
exp_name_idx = {}
for _, row in exp.iterrows():
    imo = row['_imo']
    nk = row['_nk']
    if imo:
        if imo not in exp_imo_idx:
            exp_imo_idx[imo] = []
        exp_imo_idx[imo].append(row)
    if nk:
        if nk not in exp_name_idx:
            exp_name_idx[nk] = []
        exp_name_idx[nk].append(row)

# Match
# PHASE 1 TEMPORAL WINDOW EXPANSION: Expanded from ±3 days to ±7 days
# Analysis shows 125 additional matches possible with wider window
window_days = 7
matched_count = 0
matched_imo = 0
matched_name = 0

visits_df['ManifestMatchStatus'] = 'UNMATCHED'
visits_df['ManifestMatchKey'] = ''
visits_df['ManifestBOLCount'] = 0
visits_df['ManifestTotalTons'] = ''
visits_df['ManifestCargoGroup'] = ''
visits_df['ManifestCargoCommodity'] = ''
visits_df['ManifestCargo'] = ''
visits_df['ManifestShippers'] = ''
visits_df['ManifestConsignees'] = ''
visits_df['ManifestDate'] = ''
visits_df['ManifestTimeDelta'] = ''

for idx, visit in visits_df.iterrows():
    op_type = visit['OperationType']
    imo = str(visit['IMO']).strip() if pd.notna(visit['IMO']) else ''
    name = visit['VesselName']
    nk = build_name_key(name) if pd.notna(name) else ''

    cargo_hits = []
    match_key = ''

    # Match DISCHARGE operations (imports) - use arrival date
    if op_type == 'DISCHARGE' and pd.notna(visit['ArrivalTime_dt']):
        ref_date = visit['ArrivalTime_dt'].date()
        lo = ref_date - timedelta(days=window_days)
        hi = ref_date + timedelta(days=window_days)

        if imo and imo in imp_imo_idx:
            for rec in imp_imo_idx[imo]:
                if rec['_date'] and lo <= rec['_date'] <= hi:
                    cargo_hits.append(rec)
            if cargo_hits:
                match_key = 'IMO'
                matched_imo += 1

        if not cargo_hits and nk and nk in imp_name_idx:
            for rec in imp_name_idx[nk]:
                if rec['_date'] and lo <= rec['_date'] <= hi:
                    cargo_hits.append(rec)
            if cargo_hits:
                match_key = 'NAME'
                matched_name += 1

    # Match LOADING operations (exports) - use departure date
    elif op_type == 'LOADING' and pd.notna(visit['DepartureTime_dt']):
        ref_date = visit['DepartureTime_dt'].date()
        lo = ref_date - timedelta(days=window_days)
        hi = ref_date + timedelta(days=window_days)

        if imo and imo in exp_imo_idx:
            for rec in exp_imo_idx[imo]:
                if rec['_date'] and lo <= rec['_date'] <= hi:
                    cargo_hits.append(rec)
            if cargo_hits:
                match_key = 'IMO'
                matched_imo += 1

        if not cargo_hits and nk and nk in exp_name_idx:
            for rec in exp_name_idx[nk]:
                if rec['_date'] and lo <= rec['_date'] <= hi:
                    cargo_hits.append(rec)
            if cargo_hits:
                match_key = 'NAME'
                matched_name += 1

    # Process matches (same for imports and exports)
    if cargo_hits:
        matched_count += 1
        tons_total = sum(float(r['Tons']) for r in cargo_hits if pd.notna(r.get('Tons')) and str(r.get('Tons')).replace('.','').replace('-','').isdigit())
        groups = list(set(r['Group'] for r in cargo_hits if pd.notna(r.get('Group'))))
        comms = list(set(r['Commodity'] for r in cargo_hits if pd.notna(r.get('Commodity'))))
        cargos = list(set(r['Cargo'] for r in cargo_hits if pd.notna(r.get('Cargo'))))
        shippers = list(set(r['Shipper'] for r in cargo_hits if pd.notna(r.get('Shipper'))))[:3]
        consignees = list(set(r['Consignee'] for r in cargo_hits if pd.notna(r.get('Consignee'))))[:3]

        nearest = min(cargo_hits, key=lambda r: abs((r['_date'] - ref_date).days))
        delta_days = (nearest['_date'] - ref_date).days

        visits_df.at[idx, 'ManifestMatchStatus'] = 'MATCHED'
        visits_df.at[idx, 'ManifestMatchKey'] = match_key
        visits_df.at[idx, 'ManifestBOLCount'] = len(cargo_hits)
        visits_df.at[idx, 'ManifestTotalTons'] = round(tons_total, 1) if tons_total > 0 else ''
        visits_df.at[idx, 'ManifestCargoGroup'] = ', '.join(groups)
        visits_df.at[idx, 'ManifestCargoCommodity'] = ', '.join(comms)
        visits_df.at[idx, 'ManifestCargo'] = ', '.join(cargos)
        visits_df.at[idx, 'ManifestShippers'] = ', '.join(shippers)
        visits_df.at[idx, 'ManifestConsignees'] = ', '.join(consignees)
        visits_df.at[idx, 'ManifestDate'] = nearest['_date'].isoformat()
        visits_df.at[idx, 'ManifestTimeDelta'] = delta_days

    if idx % 1000 == 0:
        print(f'   Processed {idx:,} / {len(visits_df):,}', end='\r')

print(f'   Matched: {matched_count:,} ({matched_count/len(visits_df)*100:.1f}%)')
print(f'     by IMO: {matched_imo:,}')
print(f'     by NAME: {matched_name:,}')

# ═══════════════════════════════════════════════════════════════════════════
# 7. MATCH TO FGIS GRAIN EXPORTS
# ═══════════════════════════════════════════════════════════════════════════
print("\n7. Matching to FGIS grain exports...")

# Load FGIS data (grain exports only for LMR)
try:
    fgis = pd.read_csv('G:/My Drive/LLM/project_manifest/RAW_DATA/00_04_fgis_raw/CY2023.csv', dtype=str, low_memory=False)
    fgis = fgis[fgis['Port'] == 'MISSISSIPPI R.'].copy()
    fgis['_date'] = pd.to_datetime(fgis['Cert Date'], format='%Y%m%d', errors='coerce').dt.date
    fgis['_vessel_nk'] = fgis['Carrier Name'].apply(lambda v: build_name_key(v) if pd.notna(v) else '')
    fgis['_tons'] = pd.to_numeric(fgis['Metric Ton'], errors='coerce')
    print(f"   FGIS LMR records: {len(fgis):,}")

    # Build vessel name index
    fgis_name_idx = {}
    for _, row in fgis.iterrows():
        nk = row['_vessel_nk']
        if nk:
            if nk not in fgis_name_idx:
                fgis_name_idx[nk] = []
            fgis_name_idx[nk].append(row)

    # Initialize FGIS columns
    visits_df['FGISMatchStatus'] = 'UNMATCHED'
    visits_df['FGISRecordCount'] = 0
    visits_df['FGISTotalTons'] = ''
    visits_df['FGISGrainTypes'] = ''
    visits_df['FGISCertDate'] = ''
    visits_df['FGISTimeDelta'] = ''

    # Match LOADING operations at Elevator zones (±96 hours)
    fgis_matched_count = 0
    window_hours = 96

    for idx, visit in visits_df.iterrows():
        # Only match LOADING operations (grain exports)
        if visit['OperationType'] == 'LOADING' and pd.notna(visit['DepartureTime_dt']):
            nk = build_name_key(visit['VesselName']) if pd.notna(visit['VesselName']) else ''

            if nk and nk in fgis_name_idx:
                ref_date = visit['DepartureTime_dt'].date()
                lo_date = ref_date - timedelta(hours=window_hours)
                hi_date = ref_date + timedelta(hours=window_hours)

                # Convert to dates for comparison
                lo = lo_date.date() if isinstance(lo_date, datetime) else lo_date
                hi = hi_date.date() if isinstance(hi_date, datetime) else hi_date

                grain_hits = []
                for rec in fgis_name_idx[nk]:
                    if rec['_date'] and lo <= rec['_date'] <= hi:
                        grain_hits.append(rec)

                if grain_hits:
                    fgis_matched_count += 1
                    tons_total = sum(r['_tons'] for r in grain_hits if pd.notna(r['_tons']))
                    grain_types = list(set(r['Grain'] for r in grain_hits if pd.notna(r.get('Grain'))))

                    nearest = min(grain_hits, key=lambda r: abs((r['_date'] - ref_date).days))
                    delta_days = (nearest['_date'] - ref_date).days

                    visits_df.at[idx, 'FGISMatchStatus'] = 'MATCHED'
                    visits_df.at[idx, 'FGISRecordCount'] = len(grain_hits)
                    visits_df.at[idx, 'FGISTotalTons'] = round(tons_total, 1) if tons_total > 0 else ''
                    visits_df.at[idx, 'FGISGrainTypes'] = ', '.join(grain_types)
                    visits_df.at[idx, 'FGISCertDate'] = nearest['_date'].isoformat()
                    visits_df.at[idx, 'FGISTimeDelta'] = delta_days

        if idx % 1000 == 0:
            print(f'   Processed {idx:,} / {len(visits_df):,}', end='\r')

    print(f'   FGIS matched: {fgis_matched_count:,}')

    # Update manifest columns to include FGIS for LOADING operations
    for idx, visit in visits_df.iterrows():
        if visit['FGISMatchStatus'] == 'MATCHED':
            # Override manifest with FGIS for grain exports
            visits_df.at[idx, 'ManifestMatchStatus'] = 'MATCHED'
            visits_df.at[idx, 'ManifestMatchKey'] = 'FGIS'
            visits_df.at[idx, 'ManifestCargoGroup'] = 'Dry Bulk'
            visits_df.at[idx, 'ManifestCargoCommodity'] = 'Agricultural'
            visits_df.at[idx, 'ManifestCargo'] = 'Grain'
            visits_df.at[idx, 'ManifestTotalTons'] = visit['FGISTotalTons']

except Exception as e:
    print(f"   FGIS matching skipped: {e}")

# ═══════════════════════════════════════════════════════════════════════════
# 7.5. FACILITY-BASED PREDICTIVE DEFAULTS (PHASE 3)
# ═══════════════════════════════════════════════════════════════════════════
print("\n7.5. Applying facility-based predictive cargo defaults...")

# Initialize predictive cargo columns
visits_df['PredictedCargoGroup'] = ''
visits_df['PredictedCargoCommodity'] = ''
visits_df['PredictedCargo'] = ''
visits_df['PredictedCargoSource'] = ''
visits_df['PredictionConfidence'] = ''

predicted_count = 0
confidence_counts = {'HIGH': 0, 'MEDIUM': 0, 'LOW': 0}

for idx, visit in visits_df.iterrows():
    # Only apply predictions to UNMATCHED visits (don't override manifest/FGIS matches)
    if visit['ManifestMatchStatus'] == 'MATCHED':
        continue

    facility = visit['Facility']
    zone_type = visit['ZoneType']
    zone_cargoes = str(visit['ZoneCargoes']).lower() if pd.notna(visit['ZoneCargoes']) else ''
    operation_type = visit['OperationType']
    vessel_type = visit['VesselType_Clean']

    predicted = False

    # ═══════════════════════════════════════════════════════════════════════
    # HIGH CONFIDENCE RULES (>80% match rate in analysis)
    # ═══════════════════════════════════════════════════════════════════════

    # RULE 1: Grain Elevators (9 facilities, 48-100% FGIS match rate)
    if zone_type == 'Elevator' and operation_type == 'LOADING':
        visits_df.at[idx, 'PredictedCargoGroup'] = 'Dry Bulk'
        visits_df.at[idx, 'PredictedCargoCommodity'] = 'Agricultural'
        visits_df.at[idx, 'PredictedCargo'] = 'Grain'
        visits_df.at[idx, 'PredictedCargoSource'] = 'ZoneType=Elevator+LOADING'
        visits_df.at[idx, 'PredictionConfidence'] = 'HIGH'
        predicted = True
        confidence_counts['HIGH'] += 1

    # RULE 2: Valero St Charles Refinery (100% match rate)
    elif facility == 'Valero St Charles' and operation_type == 'DISCHARGE' and vessel_type == 'Tank':
        visits_df.at[idx, 'PredictedCargoGroup'] = 'Liquid Bulk'
        visits_df.at[idx, 'PredictedCargoCommodity'] = 'Petroleum'
        visits_df.at[idx, 'PredictedCargo'] = 'Refined Products'
        visits_df.at[idx, 'PredictedCargoSource'] = 'Facility=Valero St Charles'
        visits_df.at[idx, 'PredictionConfidence'] = 'HIGH'
        predicted = True
        confidence_counts['HIGH'] += 1

    # ═══════════════════════════════════════════════════════════════════════
    # MEDIUM CONFIDENCE RULES (30-80% match rate or known patterns)
    # ═══════════════════════════════════════════════════════════════════════

    # RULE 3: Noranda Alumina - Bauxite from Jamaica (0% match but known pattern)
    elif facility == 'Noranda Alumina' and operation_type == 'DISCHARGE':
        visits_df.at[idx, 'PredictedCargoGroup'] = 'Dry Bulk'
        visits_df.at[idx, 'PredictedCargoCommodity'] = 'Non-Ferrous Raw Materials'
        visits_df.at[idx, 'PredictedCargo'] = 'Bauxite'
        visits_df.at[idx, 'PredictedCargoSource'] = 'Facility=Noranda Alumina (Jamaica origin)'
        visits_df.at[idx, 'PredictionConfidence'] = 'MEDIUM'
        predicted = True
        confidence_counts['MEDIUM'] += 1

    # RULE 4: Coal/Petcoke Export Terminals (Zone metadata based)
    elif ('coal' in zone_cargoes or 'petcoke' in zone_cargoes) and operation_type == 'LOADING':
        # Determine if Coal or Petcoke based on zone metadata
        if 'petcoke' in zone_cargoes and 'coal' not in zone_cargoes:
            cargo = 'Petcoke'
        elif 'coal' in zone_cargoes and 'petcoke' not in zone_cargoes:
            cargo = 'Coal'
        else:
            cargo = 'Petcoke'  # Default to petcoke if both mentioned

        visits_df.at[idx, 'PredictedCargoGroup'] = 'Dry Bulk'
        visits_df.at[idx, 'PredictedCargoCommodity'] = 'Carbon Products'
        visits_df.at[idx, 'PredictedCargo'] = cargo
        visits_df.at[idx, 'PredictedCargoSource'] = f'ZoneCargoes={cargo}+LOADING'
        visits_df.at[idx, 'PredictionConfidence'] = 'MEDIUM'
        predicted = True
        confidence_counts['MEDIUM'] += 1

    # RULE 5: Genesis Baton Rouge - Crude Oil (50% match rate)
    elif facility == 'Genesis Baton Rouge' and operation_type == 'DISCHARGE' and vessel_type == 'Tank':
        visits_df.at[idx, 'PredictedCargoGroup'] = 'Liquid Bulk'
        visits_df.at[idx, 'PredictedCargoCommodity'] = 'Petroleum'
        visits_df.at[idx, 'PredictedCargo'] = 'Crude Oil'
        visits_df.at[idx, 'PredictedCargoSource'] = 'Facility=Genesis Baton Rouge'
        visits_df.at[idx, 'PredictionConfidence'] = 'MEDIUM'
        predicted = True
        confidence_counts['MEDIUM'] += 1

    # RULE 6: Bauxite/Alumina terminals (Zone metadata based)
    elif 'bauxite' in zone_cargoes and operation_type == 'DISCHARGE':
        visits_df.at[idx, 'PredictedCargoGroup'] = 'Dry Bulk'
        visits_df.at[idx, 'PredictedCargoCommodity'] = 'Non-Ferrous Raw Materials'
        visits_df.at[idx, 'PredictedCargo'] = 'Bauxite'
        visits_df.at[idx, 'PredictedCargoSource'] = 'ZoneCargoes=Bauxite+DISCHARGE'
        visits_df.at[idx, 'PredictionConfidence'] = 'MEDIUM'
        predicted = True
        confidence_counts['MEDIUM'] += 1

    # RULE 7: Grain terminals (Non-Elevator types) - Zone metadata based
    elif 'grain' in zone_cargoes and operation_type == 'LOADING' and zone_type != 'Elevator':
        visits_df.at[idx, 'PredictedCargoGroup'] = 'Dry Bulk'
        visits_df.at[idx, 'PredictedCargoCommodity'] = 'Agricultural'
        visits_df.at[idx, 'PredictedCargo'] = 'Grain'
        visits_df.at[idx, 'PredictedCargoSource'] = 'ZoneCargoes=Grain+LOADING'
        visits_df.at[idx, 'PredictionConfidence'] = 'MEDIUM'
        predicted = True
        confidence_counts['MEDIUM'] += 1

    # RULE 8: Wood Pellets - Zone metadata based
    elif 'wood pellets' in zone_cargoes and operation_type == 'LOADING':
        visits_df.at[idx, 'PredictedCargoGroup'] = 'Dry Bulk'
        visits_df.at[idx, 'PredictedCargoCommodity'] = 'Forestry'
        visits_df.at[idx, 'PredictedCargo'] = 'Wood Pellets'
        visits_df.at[idx, 'PredictedCargoSource'] = 'ZoneCargoes=Wood Pellets+LOADING'
        visits_df.at[idx, 'PredictionConfidence'] = 'MEDIUM'
        predicted = True
        confidence_counts['MEDIUM'] += 1

    # RULE 9: Copper facilities (AST Chalmette, Copper named facilities)
    elif (facility == 'AST Chalmette Slip' or 'copper' in facility.lower()) and operation_type == 'DISCHARGE':
        visits_df.at[idx, 'PredictedCargoGroup'] = 'Break Bulk'
        visits_df.at[idx, 'PredictedCargoCommodity'] = 'Metals'
        visits_df.at[idx, 'PredictedCargo'] = 'Copper'
        visits_df.at[idx, 'PredictedCargoSource'] = f'Facility={facility}+DISCHARGE'
        visits_df.at[idx, 'PredictionConfidence'] = 'MEDIUM'
        predicted = True
        confidence_counts['MEDIUM'] += 1

    # ═══════════════════════════════════════════════════════════════════════
    # LOW CONFIDENCE RULES (Generic zone/vessel type fallbacks)
    # ═══════════════════════════════════════════════════════════════════════

    # RULE 7: Chemical Plants - LOADING operations
    elif zone_type == 'Chemical Plant' and operation_type == 'LOADING':
        visits_df.at[idx, 'PredictedCargoGroup'] = 'Liquid Bulk'
        visits_df.at[idx, 'PredictedCargoCommodity'] = 'Chemicals'
        visits_df.at[idx, 'PredictedCargo'] = 'Chemicals'
        visits_df.at[idx, 'PredictedCargoSource'] = 'ZoneType=Chemical Plant+LOADING'
        visits_df.at[idx, 'PredictionConfidence'] = 'LOW'
        predicted = True
        confidence_counts['LOW'] += 1

    # RULE 8: Petroleum Refineries - LOADING operations
    elif zone_type == 'Refinery' and operation_type == 'LOADING' and vessel_type == 'Tank':
        visits_df.at[idx, 'PredictedCargoGroup'] = 'Liquid Bulk'
        visits_df.at[idx, 'PredictedCargoCommodity'] = 'Petroleum'
        visits_df.at[idx, 'PredictedCargo'] = 'Refined Products'
        visits_df.at[idx, 'PredictedCargoSource'] = 'ZoneType=Refinery+LOADING'
        visits_df.at[idx, 'PredictionConfidence'] = 'LOW'
        predicted = True
        confidence_counts['LOW'] += 1

    # RULE 9: Crude Oil terminals - DISCHARGE operations
    elif zone_type == 'Crude Storage' and operation_type == 'DISCHARGE' and vessel_type == 'Tank':
        visits_df.at[idx, 'PredictedCargoGroup'] = 'Liquid Bulk'
        visits_df.at[idx, 'PredictedCargoCommodity'] = 'Petroleum'
        visits_df.at[idx, 'PredictedCargo'] = 'Crude Oil'
        visits_df.at[idx, 'PredictedCargoSource'] = 'ZoneType=Crude Storage+DISCHARGE'
        visits_df.at[idx, 'PredictionConfidence'] = 'LOW'
        predicted = True
        confidence_counts['LOW'] += 1

    # RULE 10: Steel at general cargo terminals - DISCHARGE operations
    elif (zone_type == 'General Cargo' and operation_type == 'DISCHARGE' and
          vessel_type == 'Gen' and 'steel' not in zone_cargoes.lower()):
        # Generic steel prediction for general cargo terminals with Gen vessels
        visits_df.at[idx, 'PredictedCargoGroup'] = 'Break Bulk'
        visits_df.at[idx, 'PredictedCargoCommodity'] = 'Steel'
        visits_df.at[idx, 'PredictedCargo'] = 'Steel'
        visits_df.at[idx, 'PredictedCargoSource'] = 'ZoneType=General Cargo+Gen vessel+DISCHARGE'
        visits_df.at[idx, 'PredictionConfidence'] = 'LOW'
        predicted = True
        confidence_counts['LOW'] += 1

    # RULE 11: Pig Iron - Zone metadata based or copper facilities LOADING
    elif 'pig iron' in zone_cargoes or (('copper' in facility.lower() or facility == 'AST Chalmette Slip') and operation_type == 'LOADING'):
        visits_df.at[idx, 'PredictedCargoGroup'] = 'Break Bulk'
        visits_df.at[idx, 'PredictedCargoCommodity'] = 'Ferrous Raw Materials'
        visits_df.at[idx, 'PredictedCargo'] = 'Pig Iron'
        visits_df.at[idx, 'PredictedCargoSource'] = f'ZoneCargoes=Pig Iron or Facility={facility}+LOADING'
        visits_df.at[idx, 'PredictionConfidence'] = 'LOW'
        predicted = True
        confidence_counts['LOW'] += 1

    # RULE 12: Manganese - Zone metadata or specific facilities
    elif 'manganese' in zone_cargoes or (facility in ['1st Street', '7th Street', 'AST Chalmette Slip'] and operation_type == 'DISCHARGE' and vessel_type == 'Gen'):
        visits_df.at[idx, 'PredictedCargoGroup'] = 'Dry Bulk'
        visits_df.at[idx, 'PredictedCargoCommodity'] = 'Ferro Alloys'
        visits_df.at[idx, 'PredictedCargo'] = 'Manganese'
        visits_df.at[idx, 'PredictedCargoSource'] = f'ZoneCargoes=Manganese or Facility={facility}'
        visits_df.at[idx, 'PredictionConfidence'] = 'LOW'
        predicted = True
        confidence_counts['LOW'] += 1

    # ═══════════════════════════════════════════════════════════════════════
    # OPERATION-AGNOSTIC FALLBACK RULES (Phase 3.1 - Added 2026-02-22)
    # For UNKNOWN operation type visits where specific rules don't apply
    # ═══════════════════════════════════════════════════════════════════════

    # FALLBACK 1: Grain Elevators (no operation type required)
    # Addresses UNKNOWN operation visits at grain facilities
    # Grain elevators are definitionally grain facilities
    elif zone_type == 'Elevator':
        visits_df.at[idx, 'PredictedCargoGroup'] = 'Dry Bulk'
        visits_df.at[idx, 'PredictedCargoCommodity'] = 'Agricultural'
        visits_df.at[idx, 'PredictedCargo'] = 'Grain'
        visits_df.at[idx, 'PredictedCargoSource'] = 'Fallback: ZoneType=Elevator'
        visits_df.at[idx, 'PredictionConfidence'] = 'MEDIUM'
        predicted = True
        confidence_counts['MEDIUM'] += 1

    # FALLBACK 2: General Cargo Terminals (generic default)
    # Addresses 149 UNKNOWN operation visits at general cargo facilities
    elif zone_type == 'General Cargo' and vessel_type == 'Gen':
        visits_df.at[idx, 'PredictedCargoGroup'] = 'Break Bulk'
        visits_df.at[idx, 'PredictedCargoCommodity'] = 'Steel'
        visits_df.at[idx, 'PredictedCargo'] = 'Steel'
        visits_df.at[idx, 'PredictedCargoSource'] = 'Fallback: ZoneType=General Cargo+Gen vessel'
        visits_df.at[idx, 'PredictionConfidence'] = 'LOW'
        predicted = True
        confidence_counts['LOW'] += 1

    # FALLBACK 3: Tank Storage (generic petroleum product default)
    # Addresses 130 UNKNOWN operation visits at tank terminals
    elif zone_type == 'Tank Storage' and vessel_type == 'Tank':
        visits_df.at[idx, 'PredictedCargoGroup'] = 'Liquid Bulk'
        visits_df.at[idx, 'PredictedCargoCommodity'] = 'Petroleum'
        visits_df.at[idx, 'PredictedCargo'] = 'Refined Products'
        visits_df.at[idx, 'PredictedCargoSource'] = 'Fallback: ZoneType=Tank Storage+Tank vessel'
        visits_df.at[idx, 'PredictionConfidence'] = 'LOW'
        predicted = True
        confidence_counts['LOW'] += 1

    if predicted:
        predicted_count += 1

print(f"   Predictions applied: {predicted_count:,}")
print(f"     HIGH confidence: {confidence_counts['HIGH']:,}")
print(f"     MEDIUM confidence: {confidence_counts['MEDIUM']:,}")
print(f"     LOW confidence: {confidence_counts['LOW']:,}")

# ═══════════════════════════════════════════════════════════════════════════
# 8. VALIDATE AND APPLY FINAL CARGO ASSIGNMENT
# ═══════════════════════════════════════════════════════════════════════════
print("\n8. Validating and finalizing cargo assignments...")

# Initialize final cargo columns
visits_df['FinalCargoGroup'] = ''
visits_df['FinalCargoCommodity'] = ''
visits_df['FinalCargo'] = ''
visits_df['FinalCargoSource'] = ''
visits_df['ValidationFlag'] = ''

# Validation rules
INCOMPATIBLE_VESSEL_CARGO = {
    'Cont': ['Dry Bulk', 'Liquid Bulk', 'Liquid Gas', 'Break Bulk'],  # Containers only
    'Gas': ['Dry Bulk', 'Liquid Bulk', 'Break Bulk'],  # Liquid Gas only
    'Pass': ['Dry Bulk', 'Liquid Bulk', 'Liquid Gas', 'Break Bulk'],  # Passengers only
    'Reef': ['Dry Bulk', 'Liquid Bulk', 'Liquid Gas'],  # Reefer containers only
    'Tank': ['Dry Bulk', 'Liquid Gas', 'Break Bulk'],  # Liquid Bulk only
    'Bulk': ['Liquid Bulk', 'Liquid Gas', 'Break Bulk'],  # Dry Bulk only (no containers/liquids)
    'Barge': ['Liquid Bulk', 'Liquid Gas'],  # Dry Bulk or Break Bulk only
    'Lift': ['Liquid Bulk', 'Liquid Gas'],  # Dry Bulk or Break Bulk only
    'Gen': ['Liquid Bulk', 'Liquid Gas'],  # Dry Bulk or Break Bulk only
}

for idx, visit in visits_df.iterrows():
    vtype = visit['VesselType_Clean']
    manifest_group = visit['ManifestCargoGroup']
    predicted_group = visit['PredictedCargoGroup']
    default_group = visit['DefaultCargoGroup']

    # Priority 1: Use manifest match if valid
    if visit['ManifestMatchStatus'] == 'MATCHED' and manifest_group:
        # Check if manifest cargo is compatible with vessel type
        if vtype in INCOMPATIBLE_VESSEL_CARGO:
            incompatible = INCOMPATIBLE_VESSEL_CARGO[vtype]
            if any(inc in manifest_group for inc in incompatible):
                # Manifest is incompatible - use prediction or default instead
                if predicted_group:
                    visits_df.at[idx, 'FinalCargoGroup'] = predicted_group
                    visits_df.at[idx, 'FinalCargoCommodity'] = visit['PredictedCargoCommodity']
                    visits_df.at[idx, 'FinalCargo'] = visit['PredictedCargo']
                    visits_df.at[idx, 'FinalCargoSource'] = f'Predicted ({visit["PredictedCargoSource"]}) - manifest incompatible'
                    visits_df.at[idx, 'ValidationFlag'] = f'PREDICTED_{visit["PredictionConfidence"]}'
                else:
                    visits_df.at[idx, 'FinalCargoGroup'] = default_group
                    visits_df.at[idx, 'FinalCargoCommodity'] = visit['DefaultCargoCommodity']
                    visits_df.at[idx, 'FinalCargo'] = visit['DefaultCargo']
                    visits_df.at[idx, 'FinalCargoSource'] = f'Default (manifest incompatible: {vtype} != {manifest_group})'
                    visits_df.at[idx, 'ValidationFlag'] = 'MANIFEST_OVERRIDE_INCOMPATIBLE'
            else:
                # Manifest is valid
                visits_df.at[idx, 'FinalCargoGroup'] = manifest_group
                visits_df.at[idx, 'FinalCargoCommodity'] = visit['ManifestCargoCommodity']
                visits_df.at[idx, 'FinalCargo'] = visit['ManifestCargo']
                visits_df.at[idx, 'FinalCargoSource'] = 'Manifest'
                visits_df.at[idx, 'ValidationFlag'] = 'OK'
        else:
            # No validation rules for this vessel type - use manifest
            visits_df.at[idx, 'FinalCargoGroup'] = manifest_group
            visits_df.at[idx, 'FinalCargoCommodity'] = visit['ManifestCargoCommodity']
            visits_df.at[idx, 'FinalCargo'] = visit['ManifestCargo']
            visits_df.at[idx, 'FinalCargoSource'] = 'Manifest'
            visits_df.at[idx, 'ValidationFlag'] = 'OK'

    # Priority 2: Use facility-based prediction (PHASE 3)
    elif predicted_group:
        visits_df.at[idx, 'FinalCargoGroup'] = predicted_group
        visits_df.at[idx, 'FinalCargoCommodity'] = visit['PredictedCargoCommodity']
        visits_df.at[idx, 'FinalCargo'] = visit['PredictedCargo']
        visits_df.at[idx, 'FinalCargoSource'] = f'Predicted ({visit["PredictedCargoSource"]})'
        visits_df.at[idx, 'ValidationFlag'] = f'PREDICTED_{visit["PredictionConfidence"]}'

    # Priority 3: Use generic default if no manifest or prediction
    elif default_group:
        visits_df.at[idx, 'FinalCargoGroup'] = default_group
        visits_df.at[idx, 'FinalCargoCommodity'] = visit['DefaultCargoCommodity']
        visits_df.at[idx, 'FinalCargo'] = visit['DefaultCargo']
        visits_df.at[idx, 'FinalCargoSource'] = visit['DefaultSource']
        visits_df.at[idx, 'ValidationFlag'] = 'DEFAULT_ONLY'

    # Priority 4: No assignment
    else:
        visits_df.at[idx, 'ValidationFlag'] = 'NO_CARGO_ASSIGNMENT'

print(f"   Validation flags:")
print(visits_df['ValidationFlag'].value_counts().to_string())

# ═══════════════════════════════════════════════════════════════════════════
# 9. SAVE RESULTS
# ═══════════════════════════════════════════════════════════════════════════
print("\n9. Saving results...")

out_path = 'G:/My Drive/LLM/project_manifest/user_notes/mrtis_terminal_visits_2024_WITH_RULES.csv'
visits_df.to_csv(out_path, index=False)

print(f"\n{out_path}")
print(f"   Rows: {len(visits_df):,}")
print(f"   Columns: {len(visits_df.columns)}")

print("\n" + "="*80)
print("SUMMARY")
print("="*80)
print(f"Total terminal visits: {len(visits_df):,}")
print(f"\nBy operation type:")
for op in ['DISCHARGE','LOADING','UNKNOWN']:
    count = (visits_df['OperationType'] == op).sum()
    print(f"  {op}: {count:,}")

print(f"\nCargo assignment sources:")
print(visits_df['FinalCargoSource'].value_counts().to_string())

print("\n" + "="*80)
print("DONE")
print("="*80)

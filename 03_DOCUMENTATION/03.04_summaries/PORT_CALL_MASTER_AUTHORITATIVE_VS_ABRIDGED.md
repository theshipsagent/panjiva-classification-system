# Port Call Master: Authoritative vs Abridged Versions
**Version:** v1.5.0
**Date:** 2026-01-16

---

## Quick Summary

| Aspect | Authoritative | Abridged |
|--------|--------------|----------|
| **Purpose** | Complete technical dataset with all matching metadata | Analytics-focused dataset for business intelligence |
| **Columns** | 82 | 43 |
| **File Size** | 47.4 MB | 33.6 MB |
| **Records** | 100,208 | 100,208 |
| **Removed** | None | 39 columns (technical metadata) |
| **Use Case** | Data engineering, matching verification, audits | Dashboards, reports, business analysis |

---

## File Locations

```
02_STAGE02_CLASSIFICATION/
├── usace_2023_portcall_master_v1.5.0_AUTHORITATIVE.csv  (47.4 MB)
└── usace_2023_portcall_master_v1.5.0_ABRIDGED.csv       (33.6 MB)
```

---

## What Was Removed from Abridged Version

### Category 1: Vessel Registry Technical Details (4 columns)
```
- NRT (Net Registered Tonnage - kept DWT instead)
- GRT (Gross Registered Tonnage - kept DWT instead)
- DWT_Draft_m (Draft in meters - kept DWT_Draft_ft)
- Registry_Match_Method (How vessel was matched to registry)
```
**Why removed:** DWT and draft in feet are sufficient for analysis. Match method is technical metadata.

---

### Category 2: USACE Record IDs and Port Codes (6 columns)
```
- Entrance_RECID (USACE entrance record ID)
- Entrance_Port_Name (Duplicate of Entrance_Port_USACE)
- Entrance_Port_Code (Numeric code - kept USACE name)
- Clearance_RECID (USACE clearance record ID)
- Clearance_Port_Name (Duplicate of Clearance_Port_USACE)
- Clearance_Port_Code (Numeric code - kept USACE name)
```
**Why removed:**
- RECIDs are internal USACE identifiers (not needed for analysis)
- Port names and codes are redundant (kept USACE standardized names)

---

### Category 3: Cargo Manifest Matching Metadata (8 columns)
```
Import Manifest:
- Import_VOY_RECID (Panjiva voyage ID)
- Import_Match_Days_Offset (Days between arrival and manifest)
- Import_Match_Pass (Which matching pass found manifest)
- Import_Match_Method (How manifest was matched)

Export Manifest:
- Export_VOY_RECID (Panjiva voyage ID)
- Export_Match_Days_Offset (Days between clearance and manifest)
- Export_Match_Pass (Which matching pass found manifest)
- Export_Match_Method (How manifest was matched)
```
**Why removed:** Technical matching metadata. Cargo data (carrier, tons, commodity) is retained.

**Kept in Abridged:**
- Import_Carrier, Import_Cargo_Group, Import_Cargo_Commodity, Import_Tons
- Export_Shipper, Export_Cargo_Group, Export_Cargo_Commodity, Export_Tons

---

### Category 4: Grain Export Technical Details (5 columns)
```
- FGIS_RECID (FGIS certificate serial number)
- Grain_Type (SOYBEANS / CORN / WHEAT / SORGHUM)
- Grain_Detail (Grain class/variety like HRW)
- Grain_MT (Metric tons of grain)
- Grain_Pounds (Pounds of grain)
```
**Why removed:** FGIS ID is technical. Grain type/detail are overly specific for most analysis.

**Kept in Abridged:**
- Grain_Export (TRUE/FALSE flag - simple indicator)

---

### Category 5: Entrance/Clearance Matching Metadata (4 columns)
```
- Match_Score (Entrance-clearance match confidence 0-1)
- Match_Method (How entrance/clearance were matched)
- Tug_Barge_Pair_ID (Tug-barge pairing ID)
- Tug_Barge_Confidence (Pairing confidence level)
```
**Why removed:** Technical matching metadata. Port call completeness is evident from Record_Type.

---

### Category 6: US Flag Registry Detailed Specs (11 columns)
```
- USFlag_CG_Number (Coast Guard number)
- USFlag_ICST_Code (ICST code 431, 432, etc.)
- USFlag_ICST_Description (Tug, Barge, etc.)
- USFlag_HP (Horsepower)
- USFlag_Length_ft (Length in feet)
- USFlag_Beam_ft (Beam in feet)
- USFlag_Capacity_Tons (Cargo capacity)
- USFlag_Year_Built (Year built)
- USFlag_Base_Port (Home port)
- USFlag_State (State of registration)
- USFlag_Match_Quality (Match confidence)
```
**Why removed:** Detailed US Flag specs are kept in authoritative version for specialized analysis.

**Kept in Abridged:**
- Flag_Country (Shows US flag)
- ICST_Vessel_Type (General vessel type)
- Vessel_Type_Registry (General vessel type from registry)

---

## What Remains in Abridged Version (43 columns)

### Core Identifiers (2)
```
✓ PORTCALL_ID - Unique port call identifier
✓ Record_Type - BOTH / ENTRANCE_ONLY / CLEARANCE_ONLY / TUG_BARGE_PAIR
```

### Vessel Data (10)
```
✓ Vessel_Name - Vessel name
✓ IMO - IMO number
✓ Flag_Country - Flag country (vessel registration)
✓ ICST_Vessel_Type - USACE vessel type classification
✓ Rig_Description - Rig description (Barge, Tug, etc.)
✓ Vessel_Type_Registry - Vessel type from ship registry
✓ DWT - Deadweight tonnage
✓ Grain_Capacity_m3 - Grain capacity in cubic meters
✓ TPC - Tonnes Per Centimeter (load calculation)
✓ DWT_Draft_ft - DWT draft in feet
```

### Timeline (3)
```
✓ Arrival_Date - Date vessel arrived at port
✓ Clearance_Date - Date vessel cleared port (departed)
✓ Port_Stay_Days - Days in port (decimal)
```

### Entrance Data (8)
```
✓ Entrance_Port_USACE - USACE standardized port name
✓ Entrance_Draft_ft - Draft in feet on arrival
✓ Entrance_Draft_in - Draft in inches (additional)
✓ Entrance_Draft_Pct_Max - Arrival draft as % of max
✓ Entrance_Activity - Expected activity (Discharge/Load)
✓ Entrance_Origin - Foreign or Coastwise
✓ Entrance_Previous_Port - Previous port name
✓ Entrance_Previous_Country - Previous port country
```

### Clearance Data (9)
```
✓ Clearance_Date - Date vessel cleared (duplicate but useful)
✓ Clearance_Port_USACE - USACE standardized port name
✓ Clearance_Draft_ft - Draft in feet on departure
✓ Clearance_Draft_in - Draft in inches (additional)
✓ Clearance_Draft_Pct_Max - Departure draft as % of max
✓ Clearance_Activity - Expected activity
✓ Clearance_Destination - Foreign or Coastwise
✓ Clearance_Next_Port - Next port name
✓ Clearance_Next_Country - Next port country
```

### Port Geography (4)
```
✓ Port_Stay_Days - Days in port (duplicate but useful)
✓ Port_Consolidated - Consolidated port region name
✓ Port_Coast - Gulf / Atlantic / Pacific / Great Lakes
✓ Port_Region - Port region classification
```

### Import Cargo (4)
```
✓ Import_Carrier - Carrier name from import manifest
✓ Import_Cargo_Group - Cargo group classification
✓ Import_Cargo_Commodity - Cargo commodity classification
✓ Import_Tons - Cargo tonnage from import manifest
```

### Export Cargo (4)
```
✓ Export_Shipper - Shipper name from export manifest
✓ Export_Cargo_Group - Cargo group classification
✓ Export_Cargo_Commodity - Cargo commodity classification
✓ Export_Tons - Cargo tonnage from export manifest
```

### Grain Export (1)
```
✓ Grain_Export - TRUE/FALSE flag if vessel loaded grain
```

---

## Use Case Comparison

### Use Authoritative Version For:
1. **Data Engineering**
   - Auditing matching algorithms
   - Verifying match quality
   - Debugging data issues
   - Tracing data lineage

2. **Technical Analysis**
   - US Flag fleet detailed specifications (HP, capacity, dimensions)
   - Grain export certificate verification
   - Matching algorithm performance
   - Tug-barge pairing analysis

3. **Regulatory Compliance**
   - Coast Guard number lookups
   - FGIS certificate tracking
   - USACE record reconciliation

4. **Advanced Analytics**
   - Tug horsepower vs cargo tonnage efficiency
   - Barge capacity utilization rates
   - Fleet age and replacement analysis
   - Home port regional specialization

---

### Use Abridged Version For:
1. **Business Intelligence Dashboards**
   - Port call volume by port/region
   - Import/export tonnage trends
   - Vessel traffic patterns
   - Cargo type distribution

2. **Market Analysis**
   - Trade flow analysis (import vs export)
   - Carrier market share
   - Port efficiency (port stay duration)
   - Vessel utilization (draft % of max)

3. **Executive Reporting**
   - Port call statistics
   - Tonnage summaries
   - Grain export highlights
   - Regional trade patterns

4. **General Analytics**
   - Faster loading times (29% smaller file)
   - Fewer columns to navigate
   - Focus on business metrics vs technical details
   - Easier for non-technical users

---

## Performance Comparison

### File Size
```
Authoritative: 47.4 MB (100%)
Abridged:      33.6 MB (71%)
Reduction:     13.9 MB (29%)
```

### Load Time Estimate
```
Authoritative: ~8-10 seconds (82 columns)
Abridged:      ~5-7 seconds (43 columns, 29% smaller)
Improvement:   ~30% faster
```

### Memory Usage
```
Authoritative: ~600 MB RAM (in pandas)
Abridged:      ~420 MB RAM (in pandas)
Reduction:     ~180 MB (30%)
```

---

## Analysis Examples

### Example 1: Port Stay Analysis (Both versions)
```python
import pandas as pd

# Abridged version is sufficient
df = pd.read_csv('usace_2023_portcall_master_v1.5.0_ABRIDGED.csv')

# Average port stay by port region
avg_stay = df.groupby('Port_Region')['Port_Stay_Days'].mean()

# Port calls by coast
coast_summary = df.groupby('Port_Coast').agg({
    'PORTCALL_ID': 'count',
    'Port_Stay_Days': 'mean',
    'Import_Tons': 'sum',
    'Export_Tons': 'sum'
})
```

### Example 2: Cargo Loaded at Port (Both versions)
```python
# Calculate cargo change (arrival vs departure draft)
df['Cargo_Change_Pct'] = df['Clearance_Draft_Pct_Max'] - df['Entrance_Draft_Pct_Max']

# Positive = loaded cargo, Negative = discharged cargo
loaded = df[df['Cargo_Change_Pct'] > 0]
discharged = df[df['Cargo_Change_Pct'] < 0]
```

### Example 3: US Flag Fleet Analysis (Authoritative ONLY)
```python
# REQUIRES AUTHORITATIVE VERSION (has USFlag_HP, USFlag_Capacity_Tons)
df_auth = pd.read_csv('usace_2023_portcall_master_v1.5.0_AUTHORITATIVE.csv')

# Tug efficiency: HP per ton moved
tugs = df_auth[
    (df_auth['USFlag_ICST_Description'] == 'Tug') &
    (df_auth['USFlag_HP'].notna())
]
tugs['HP_Per_Ton'] = tugs['USFlag_HP'] / tugs['Import_Tons']

# Barge capacity utilization
barges = df_auth[
    (df_auth['USFlag_ICST_Description'].str.contains('Barge', na=False)) &
    (df_auth['USFlag_Capacity_Tons'].notna())
]
barges['Utilization_Pct'] = (barges['Import_Tons'] / barges['USFlag_Capacity_Tons']) * 100
```

### Example 4: Grain Export Tracking (Authoritative has details, Abridged has flag)
```python
# Abridged: Simple grain export identification
df_abr = pd.read_csv('usace_2023_portcall_master_v1.5.0_ABRIDGED.csv')
grain_exports = df_abr[df_abr['Grain_Export'] == True]

# Authoritative: Detailed grain analysis
df_auth = pd.read_csv('usace_2023_portcall_master_v1.5.0_AUTHORITATIVE.csv')
grain_by_type = df_auth[df_auth['Grain_Export'] == True].groupby('Grain_Type').agg({
    'Grain_MT': 'sum',
    'Grain_Pounds': 'sum',
    'PORTCALL_ID': 'count'
})
```

---

## Recommendation

### Start with Abridged Version
- ✅ Covers 90% of analytics use cases
- ✅ 29% smaller, faster to load
- ✅ Easier to navigate (43 vs 82 columns)
- ✅ Focus on business metrics

### Use Authoritative Version When:
- ❗ Need US Flag vessel detailed specs (HP, capacity, dimensions, home port)
- ❗ Need grain export certificate details (FGIS ID, grain type/variety, MT/pounds)
- ❗ Need matching quality verification (match scores, methods, confidence)
- ❗ Need data lineage tracing (VOY_RECID, USACE RECID)
- ❗ Conducting technical audits or debugging

---

## Version History

```
v1.3.0 → v1.4.0 → v1.5.0 → AUTHORITATIVE + ABRIDGED
  71       82       82         82           43
columns  columns  columns   columns      columns

         +11      +0        (same)      (removed 39)
         US Flag  Fuzzy                technical
                  Matching             metadata
```

---

## Files Summary

| File | Columns | Size | Purpose | Column List CSV |
|------|---------|------|---------|----------------|
| **AUTHORITATIVE** | 82 | 47.4 MB | Complete technical dataset | PORT_CALL_MASTER_v1.5.0_COLUMN_LIST.csv |
| **ABRIDGED** | 43 | 33.6 MB | Analytics-focused dataset | PORT_CALL_MASTER_v1.5.0_ABRIDGED_COLUMN_LIST.csv |

---

**Created:** 2026-01-16
**Version:** v1.5.0
**Status:** ✅ PRODUCTION READY

**Recommendation:** Use ABRIDGED for dashboards and reports, AUTHORITATIVE for technical analysis.

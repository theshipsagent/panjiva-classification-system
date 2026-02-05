# Port Call Master v1.3.0 RESTRUCTURED - Data Dictionary
**File:** `usace_2023_portcall_master_v1.3.0_restructured.csv`
**Records:** 100,208 port calls
**Columns:** 71 (down from 115)
**Improvement:** Eliminated 44 duplicate columns

---

## Column Organization (71 Total)

| Category | Columns | Purpose |
|----------|---------|---------|
| **1. Core Identifiers** | 2 | Unique ID and record type |
| **2. Vessel Data (Common)** | 13 | Vessel specs that don't change during port call |
| **3. Timeline** | 3 | Arrival, departure, port stay |
| **4. Entrance (Arrival)** | 11 | Arrival-specific data (draft, origin, previous port) |
| **5. Clearance (Departure)** | 11 | Departure-specific data (draft, destination, next port) |
| **6. Port Geography** | 3 | Port region, coast, consolidated name |
| **7. Import Cargo** | 8 | Panjiva import manifest data |
| **8. Export Cargo** | 8 | Panjiva export manifest data |
| **9. Grain Export** | 7 | FGIS grain export certification |
| **10. Match Metadata** | 4 | How records were matched |

---

## Complete Column List

### 1. CORE IDENTIFIERS (2 columns)

| # | Column | Sample | Description |
|---|--------|--------|-------------|
| 1 | **PORTCALL_ID** | PC_000001 | Unique port call identifier |
| 2 | **Record_Type** | BOTH | BOTH / ENTRANCE_ONLY / CLEARANCE_ONLY / TUG_BARGE_PAIR |

---

### 2. VESSEL DATA - COMMON (13 columns)
**These values are the SAME for entrance and clearance (consolidated from both)**

| # | Column | Sample | Description |
|---|--------|--------|-------------|
| 3 | **Vessel_Name** | ST. MARYS CHALLENGER | Vessel name |
| 4 | **IMO** | 5009984 | IMO number (International Maritime Org ID) |
| 5 | **Flag_Country** | United States of America | Flag country (vessel registration) |
| 6 | **ICST_Vessel_Type** | OTHER DRY CARGO BARGE NEI | USACE ICST vessel type classification |
| 7 | **Rig_Description** | Barge, Scow | Rig description from USACE |
| 8 | **Vessel_Type_Registry** | Bulk Carrier | Vessel type from ship registry (if matched) |
| 9 | **DWT** | 11543 | Deadweight tonnage |
| 10 | **NRT** | 5136 | Net Registered Tonnage |
| 11 | **GRT** | 6969 | Gross Registered Tonnage |
| 12 | **Grain_Capacity_m3** | 0 | Grain capacity in cubic meters |
| 13 | **TPC** | 0 | Tonnes Per Centimeter (load calculation) |
| 14 | **DWT_Draft_m** | 6.471 | DWT draft in meters |
| 15 | **DWT_Draft_ft** | 21.23 | DWT draft in feet |
| 16 | **Registry_Match_Method** | IMO | How vessel was matched to ship registry |

---

### 3. TIMELINE (3 columns)

| # | Column | Sample | Description |
|---|--------|--------|-------------|
| 17 | **Arrival_Date** | 2023-05-03 | Date vessel arrived at port |
| 18 | **Clearance_Date** | 2023-06-11 | Date vessel cleared port (departed) |
| 19 | **Port_Stay_Days** | 39.0 | Days in port (decimal: 2.5 = 2 days 12 hours) |

---

### 4. ENTRANCE DATA - ARRIVAL SPECIFIC (11 columns)

| # | Column | Sample | Description |
|---|--------|--------|-------------|
| 20 | **Entrance_RECID** | 80588 | USACE entrance record ID |
| 21 | **Entrance_Port_Name** | Lake Michigan | Port name from entrance record |
| 22 | **Entrance_Port_USACE** | Lake Michigan | USACE standardized port name |
| 23 | **Entrance_Port_Code** | 3701 | USACE port numeric code |
| 24 | **Entrance_Draft_ft** | 18 | Draft in feet on arrival |
| 25 | **Entrance_Draft_in** | 0 | Draft in inches (additional) |
| 26 | **Entrance_Draft_Pct_Max** | 84.8 | Arrival draft as % of max (load indicator) |
| 27 | **Entrance_Activity** | Discharge | Expected activity (Discharge/Load) |
| 28 | **Entrance_Origin** | Foreign | Foreign or Coastwise |
| 29 | **Entrance_Previous_Port** | Owen Sound, ONT | Previous port name |
| 30 | **Entrance_Previous_Country** | Canada | Previous port country |

---

### 5. CLEARANCE DATA - DEPARTURE SPECIFIC (11 columns)

| # | Column | Sample | Description |
|---|--------|--------|-------------|
| 31 | **Clearance_RECID** | 81529 | USACE clearance record ID |
| 32 | **Clearance_Port_Name** | Lake Michigan | Port name from clearance record |
| 33 | **Clearance_Port_USACE** | Lake Michigan | USACE standardized port name |
| 34 | **Clearance_Port_Code** | 3701 | USACE port numeric code |
| 35 | **Clearance_Draft_ft** | 18 | Draft in feet on departure |
| 36 | **Clearance_Draft_in** | 0 | Draft in inches (additional) |
| 37 | **Clearance_Draft_Pct_Max** | 84.8 | Departure draft as % of max (load indicator) |
| 38 | **Clearance_Activity** | Discharge | Expected activity |
| 39 | **Clearance_Destination** | Foreign | Foreign or Coastwise |
| 40 | **Clearance_Next_Port** | Owen Sound, ONT | Next port name |
| 41 | **Clearance_Next_Country** | Canada | Next port country |

---

### 6. PORT GEOGRAPHY (3 columns)

| # | Column | Sample | Description |
|---|--------|--------|-------------|
| 42 | **Port_Consolidated** | Detroit-Milwaukee | Consolidated port region name |
| 43 | **Port_Coast** | Great Lakes | Gulf / Atlantic / Pacific / Great Lakes |
| 44 | **Port_Region** | Great Lakes | Port region classification |

---

### 7. IMPORT CARGO DATA (8 columns)
**From Panjiva import manifest match (entrance)**

| # | Column | Sample | Description |
|---|--------|--------|-------------|
| 45 | **Import_VOY_RECID** | VOY_0004994 | Panjiva voyage record ID |
| 46 | **Import_Carrier** | ALOM - Algoma Central | Carrier name from import manifest |
| 47 | **Import_Cargo_Group** | Steel Products | Cargo group classification |
| 48 | **Import_Cargo_Commodity** | Hot Rolled Steel | Cargo commodity classification |
| 49 | **Import_Tons** | 17000 | Cargo tonnage from import manifest |
| 50 | **Import_Match_Days_Offset** | 0 | Days between arrival and manifest date |
| 51 | **Import_Match_Pass** | 1 | Which matching pass found manifest (1-10) |
| 52 | **Import_Match_Method** | IMO | How manifest was matched (IMO/Vessel_Name/Port) |

---

### 8. EXPORT CARGO DATA (8 columns)
**From Panjiva export manifest match (clearance)**

| # | Column | Sample | Description |
|---|--------|--------|-------------|
| 53 | **Export_VOY_RECID** | VOY_EXP_0000351 | Panjiva voyage record ID |
| 54 | **Export_Shipper** | US Steel | Shipper name from export manifest |
| 55 | **Export_Cargo_Group** | Dry Bulk | Cargo group classification |
| 56 | **Export_Cargo_Commodity** | Barge | Cargo commodity classification |
| 57 | **Export_Tons** | 16025.01 | Cargo tonnage from export manifest |
| 58 | **Export_Match_Days_Offset** | 3 | Days between clearance and manifest date |
| 59 | **Export_Match_Pass** | 2 | Which matching pass found manifest |
| 60 | **Export_Match_Method** | Vessel_Name | How manifest was matched |

---

### 9. GRAIN EXPORT DATA (7 columns)
**From FGIS grain export certification match**

| # | Column | Sample | Description |
|---|--------|--------|-------------|
| 61 | **Grain_Export** | TRUE / FALSE | Flag: TRUE if vessel loaded grain for export |
| 62 | **FGIS_RECID** | 609731 | FGIS certificate serial number |
| 63 | **Grain_Type** | WHEAT | SOYBEANS / CORN / WHEAT / SORGHUM |
| 64 | **Grain_Detail** | HRW | Grain class/variety (e.g., HRW = Hard Red Winter) |
| 65 | **Grain_MT** | 10,780 | Metric tons of grain loaded |
| 66 | **Grain_Pounds** | 23,765,400 | Pounds of grain loaded |
| 67 | **Grain_Match_Quality** | Similarity_1.00_DateDiff_1d | Match confidence (vessel similarity + date offset) |

---

### 10. MATCH METADATA (4 columns)

| # | Column | Sample | Description |
|---|--------|--------|-------------|
| 68 | **Match_Score** | 0.8 | Entrance-clearance match confidence (0-1) |
| 69 | **Match_Method** | IMO | How entrance/clearance were matched (IMO/Vessel_Name) |
| 70 | **Tug_Barge_Pair_ID** | TB_ENT_27 | Tug-barge pairing ID (if applicable) |
| 71 | **Tug_Barge_Confidence** | HIST_1X | Pairing confidence (SINGLE/HIST_Xx) |

---

## Key Improvements Over v1.2.0

### Before (v1.2.0): 115 Columns
- Vessel data duplicated: Entrance_Vessel + Clearance_Vessel
- IMO duplicated: Entrance_IMO + Clearance_IMO
- DWT duplicated: Entrance_Vessel_DWT + Clearance_Vessel_DWT
- NRT/GRT duplicated
- Vessel type duplicated
- **44 columns were pure duplication**

### After (v1.3.0): 71 Columns
- **Common vessel data appears ONCE** (13 columns)
- Entrance/clearance **only contain unique data** (draft on arrival vs departure, origin vs destination)
- Import/export cargo clearly separated
- Grain export data standalone
- **Eliminated 44 redundant columns**

---

## Usage Examples

### Query by Record Type

```python
import pandas as pd

df = pd.read_csv('usace_2023_portcall_master_v1.3.0_restructured.csv', low_memory=False)

# Complete port calls only
complete_calls = df[df['Record_Type'] == 'BOTH']

# Entrance only (no clearance)
entrance_only = df[df['Record_Type'] == 'ENTRANCE_ONLY']

# Clearance only (no entrance)
clearance_only = df[df['Record_Type'] == 'CLEARANCE_ONLY']

# Tug-barge pairs
tug_barge = df[df['Record_Type'] == 'TUG_BARGE_PAIR']
```

### Calculate Cargo Loaded at Port

```python
# Draft change method (arrival vs departure)
df['Cargo_Change_Pct'] = df['Clearance_Draft_Pct_Max'] - df['Entrance_Draft_Pct_Max']

# Positive = loaded cargo
# Negative = discharged cargo
```

### Query Grain Exports

```python
# All grain export port calls
grain = df[df['Grain_Export'] == True]

# Specific grain type
soybeans = df[(df['Grain_Export'] == True) & (df['Grain_Type'] == 'SOYBEANS')]
```

### Query by Flag Country

```python
# US flag vessels
us_flag = df[df['Flag_Country'] == 'United States of America']

# US flag vessels WITHOUT ship registry match
us_unmatched = df[
    (df['Flag_Country'] == 'United States of America') &
    (df['Vessel_Type_Registry'].isna())
]
```

---

## Record Type Distribution

| Record_Type | Count | Percentage | Description |
|-------------|-------|------------|-------------|
| **BOTH** | 65,475 | 65.3% | Complete port call (entrance + clearance matched) |
| **CLEARANCE_ONLY** | 16,891 | 16.9% | Departure only (arrived before 2023 or import not captured) |
| **ENTRANCE_ONLY** | 16,100 | 16.1% | Arrival only (departed empty or after 2023) |
| **TUG_BARGE_PAIR** | 1,742 | 1.7% | Tug and barge operating together (871 operations × 2) |

---

## Data Quality Issues Identified

### Issue 1: Ship Registry Match Problems ⚠️

**Problem:** US flag vessels have only **16.8% match rate** to ship registry

**Affected Vessels:**
- US Flag: 8,422 unmatched (41% of all unmatched)
- TUG/SUPPLY OFFSHORE SUPPORT: 7,074 unmatched (34.4%)
- Barges: ~1,500 unmatched
- Containers: 3,014 unmatched (14.7%)

**Root Cause:**
- International ship registries don't include US domestic vessels
- Tugs, barges, lakers, offshore support vessels not in Lloyd's/IHS databases

**Solution Needed:**
- Add US Flag ship register
- Add container ship register
- Improve IMO matching for domestic vessels

### Issue 2: Null Vessel_Type_Registry

**Stats:**
- 20,561 entrance records (25%) have no vessel type from registry
- 20,598 clearance records (24.7%) have no vessel type from registry

**Recommendation:**
- Use **ICST_Vessel_Type** (from USACE) as fallback when **Vessel_Type_Registry** is null
- ICST data is 100% populated and accurate for US waters

---

## Next Steps

### 1. Fix Ship Registry Matching

**Priority 1: US Flag Vessels**
- Source US Flag ship register (mentioned as available)
- Match by IMO or vessel name
- Expected improvement: 16.8% → 80% match rate for US flag

**Priority 2: Containers**
- Download container ship register
- Match by IMO
- Expected improvement: Cover 3,014 unmatched containers

**Priority 3: Canadian Vessels**
- Canadian vessel register (6.9% match rate currently)
- Expected improvement: Cover 2,418 unmatched Canadian vessels

### 2. Further Column Reduction (Optional)

**If needed, reduce to ~40 essential columns:**
- Drop technical fields (RECID, port codes, match metadata)
- Keep only: ID, vessel, dates, ports, cargo, grain
- Create "analytics view" vs "technical view"

### 3. Add Calculated Fields

**Useful additions:**
- **Cargo_Loaded_Estimate**: Calculate from draft change
- **Round_Trip**: Flag if vessel returns to same port
- **Ballast_Indicator**: Flag if arrived/departed empty
- **Agency_Fee_Total**: Calculate port fees

---

**Generated:** 2026-01-16
**File:** usace_2023_portcall_master_v1.3.0_restructured.csv
**Columns:** 71 (down from 115)
**File Size:** 45.5 MB (down from 72.4 MB)

# Port Call Master v1.4.0 - Data Dictionary
**File:** `usace_2023_portcall_master_v1.4.0_usflag.csv`
**Records:** 100,208 port calls
**Columns:** 82 (added 11 US Flag columns)
**File Size:** 47.3 MB

---

## What's New in v1.4.0

### US Flag Registry Integration
- **Added 11 new columns** from US Coast Guard vessel inventory
- **Match rate improvement**: US flag vessels now 62.3% matched (up from 16.8%)
- **Vessels matched**: 7,612 of 12,224 US flag port calls
- **Match quality tracking**: EXACT_MATCH, ICST_DISAMBIGUATED, NRT_DISAMBIGUATED, etc.

### Key Benefits
1. **Coast Guard Numbers**: Unique US vessel identifiers (CG_Number)
2. **Accurate Vessel Types**: ICST codes from official US inventory
3. **Vessel Specifications**: Horsepower, length, beam, capacity
4. **Base Port & State**: US home port and registration state
5. **Year Built**: Vessel age tracking

---

## Column Organization (82 Total)

| Category | Columns | Purpose |
|----------|---------|---------|
| **1. Core Identifiers** | 2 | Unique ID and record type |
| **2. Vessel Data (Common)** | 13 | Vessel specs that don't change during port call |
| **3. US Flag Registry** | 11 | **NEW - US Coast Guard vessel data** |
| **4. Timeline** | 3 | Arrival, departure, port stay |
| **5. Entrance (Arrival)** | 11 | Arrival-specific data (draft, origin, previous port) |
| **6. Clearance (Departure)** | 11 | Departure-specific data (draft, destination, next port) |
| **7. Port Geography** | 3 | Port region, coast, consolidated name |
| **8. Import Cargo** | 8 | Panjiva import manifest data |
| **9. Export Cargo** | 8 | Panjiva export manifest data |
| **10. Grain Export** | 7 | FGIS grain export certification |
| **11. Match Metadata** | 5 | How records were matched |

---

## Complete Column List

### 1. CORE IDENTIFIERS (2 columns)

| # | Column | Sample | Description |
|---|--------|--------|-------------|
| 1 | **PORTCALL_ID** | PC_000001 | Unique port call identifier |
| 2 | **Record_Type** | BOTH | BOTH / ENTRANCE_ONLY / CLEARANCE_ONLY / TUG_BARGE_PAIR |

---

### 2. VESSEL DATA - COMMON (13 columns)

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

### 3. US FLAG REGISTRY (11 columns) ⭐ NEW

| # | Column | Sample | Description |
|---|--------|--------|-------------|
| 17 | **USFlag_CG_Number** | 1234567 | US Coast Guard official vessel number (unique ID) |
| 18 | **USFlag_ICST_Code** | 431 | ICST vessel type code (431=Tug, 432=Push Boat, 341=Deck Barge) |
| 19 | **USFlag_ICST_Description** | Tug | ICST vessel type description from US Flag inventory |
| 20 | **USFlag_HP** | 4500 | Horsepower (tugs, self-propelled vessels) |
| 21 | **USFlag_Length_ft** | 125.5 | Registered length in feet |
| 22 | **USFlag_Beam_ft** | 35.0 | Beam (width) in feet |
| 23 | **USFlag_Capacity_Tons** | 11543 | Cargo capacity in short tons (barges) |
| 24 | **USFlag_Year_Built** | 1998 | Year vessel was built |
| 25 | **USFlag_Base_Port** | New Orleans, LA | US home port / base of operations |
| 26 | **USFlag_State** | LA | State of US vessel registration |
| 27 | **USFlag_Match_Quality** | EXACT_MATCH | Match confidence (EXACT_MATCH / ICST_DISAMBIGUATED / NRT_DISAMBIGUATED / FIRST_CANDIDATE / FIRST_ICST_MATCH) |

**Match Quality Definitions:**
- **EXACT_MATCH**: Single vessel found with exact name match (454 vessels)
- **ICST_DISAMBIGUATED**: Multiple candidates, matched using ICST vessel type (37 vessels)
- **NRT_DISAMBIGUATED**: Multiple candidates, matched using Net Registered Tonnage proximity (19 vessels)
- **FIRST_CANDIDATE**: Multiple candidates with same ICST, selected first (25 vessels)
- **FIRST_ICST_MATCH**: Multiple ICST matches, selected first (4 vessels)

---

### 4. TIMELINE (3 columns)

| # | Column | Sample | Description |
|---|--------|--------|-------------|
| 28 | **Arrival_Date** | 2023-05-03 | Date vessel arrived at port |
| 29 | **Clearance_Date** | 2023-06-11 | Date vessel cleared port (departed) |
| 30 | **Port_Stay_Days** | 39.0 | Days in port (decimal: 2.5 = 2 days 12 hours) |

---

### 5. ENTRANCE DATA - ARRIVAL SPECIFIC (11 columns)

| # | Column | Sample | Description |
|---|--------|--------|-------------|
| 31 | **Entrance_RECID** | 80588 | USACE entrance record ID |
| 32 | **Entrance_Port_Name** | Lake Michigan | Port name from entrance record |
| 33 | **Entrance_Port_USACE** | Lake Michigan | USACE standardized port name |
| 34 | **Entrance_Port_Code** | 3701 | USACE port numeric code |
| 35 | **Entrance_Draft_ft** | 18 | Draft in feet on arrival |
| 36 | **Entrance_Draft_in** | 0 | Draft in inches (additional) |
| 37 | **Entrance_Draft_Pct_Max** | 84.8 | Arrival draft as % of max (load indicator) |
| 38 | **Entrance_Activity** | Discharge | Expected activity (Discharge/Load) |
| 39 | **Entrance_Origin** | Foreign | Foreign or Coastwise |
| 40 | **Entrance_Previous_Port** | Owen Sound, ONT | Previous port name |
| 41 | **Entrance_Previous_Country** | Canada | Previous port country |

---

### 6. CLEARANCE DATA - DEPARTURE SPECIFIC (11 columns)

| # | Column | Sample | Description |
|---|--------|--------|-------------|
| 42 | **Clearance_RECID** | 81529 | USACE clearance record ID |
| 43 | **Clearance_Port_Name** | Lake Michigan | Port name from clearance record |
| 44 | **Clearance_Port_USACE** | Lake Michigan | USACE standardized port name |
| 45 | **Clearance_Port_Code** | 3701 | USACE port numeric code |
| 46 | **Clearance_Draft_ft** | 18 | Draft in feet on departure |
| 47 | **Clearance_Draft_in** | 0 | Draft in inches (additional) |
| 48 | **Clearance_Draft_Pct_Max** | 84.8 | Departure draft as % of max (load indicator) |
| 49 | **Clearance_Activity** | Discharge | Expected activity |
| 50 | **Clearance_Destination** | Foreign | Foreign or Coastwise |
| 51 | **Clearance_Next_Port** | Owen Sound, ONT | Next port name |
| 52 | **Clearance_Next_Country** | Canada | Next port country |

---

### 7. PORT GEOGRAPHY (3 columns)

| # | Column | Sample | Description |
|---|--------|--------|-------------|
| 53 | **Port_Consolidated** | Detroit-Milwaukee | Consolidated port region name |
| 54 | **Port_Coast** | Great Lakes | Gulf / Atlantic / Pacific / Great Lakes |
| 55 | **Port_Region** | Great Lakes | Port region classification |

---

### 8. IMPORT CARGO DATA (8 columns)

| # | Column | Sample | Description |
|---|--------|--------|-------------|
| 56 | **Import_VOY_RECID** | VOY_0004994 | Panjiva voyage record ID |
| 57 | **Import_Carrier** | ALOM - Algoma Central | Carrier name from import manifest |
| 58 | **Import_Cargo_Group** | Steel Products | Cargo group classification |
| 59 | **Import_Cargo_Commodity** | Hot Rolled Steel | Cargo commodity classification |
| 60 | **Import_Tons** | 17000 | Cargo tonnage from import manifest |
| 61 | **Import_Match_Days_Offset** | 0 | Days between arrival and manifest date |
| 62 | **Import_Match_Pass** | 1 | Which matching pass found manifest (1-10) |
| 63 | **Import_Match_Method** | IMO | How manifest was matched (IMO/Vessel_Name/Port) |

---

### 9. EXPORT CARGO DATA (8 columns)

| # | Column | Sample | Description |
|---|--------|--------|-------------|
| 64 | **Export_VOY_RECID** | VOY_EXP_0000351 | Panjiva voyage record ID |
| 65 | **Export_Shipper** | US Steel | Shipper name from export manifest |
| 66 | **Export_Cargo_Group** | Dry Bulk | Cargo group classification |
| 67 | **Export_Cargo_Commodity** | Barge | Cargo commodity classification |
| 68 | **Export_Tons** | 16025.01 | Cargo tonnage from export manifest |
| 69 | **Export_Match_Days_Offset** | 3 | Days between clearance and manifest date |
| 70 | **Export_Match_Pass** | 2 | Which matching pass found manifest |
| 71 | **Export_Match_Method** | Vessel_Name | How manifest was matched |

---

### 10. GRAIN EXPORT DATA (7 columns)

| # | Column | Sample | Description |
|---|--------|--------|-------------|
| 72 | **Grain_Export** | TRUE / FALSE | Flag: TRUE if vessel loaded grain for export |
| 73 | **FGIS_RECID** | 609731 | FGIS certificate serial number |
| 74 | **Grain_Type** | WHEAT | SOYBEANS / CORN / WHEAT / SORGHUM |
| 75 | **Grain_Detail** | HRW | Grain class/variety (e.g., HRW = Hard Red Winter) |
| 76 | **Grain_MT** | 10,780 | Metric tons of grain loaded |
| 77 | **Grain_Pounds** | 23,765,400 | Pounds of grain loaded |
| 78 | **Grain_Match_Quality** | Similarity_1.00_DateDiff_1d | Match confidence (vessel similarity + date offset) |

---

### 11. MATCH METADATA (5 columns)

| # | Column | Sample | Description |
|---|--------|--------|-------------|
| 79 | **Match_Score** | 0.8 | Entrance-clearance match confidence (0-1) |
| 80 | **Match_Method** | IMO | How entrance/clearance were matched (IMO/Vessel_Name) |
| 81 | **Tug_Barge_Pair_ID** | TB_ENT_27 | Tug-barge pairing ID (if applicable) |
| 82 | **Tug_Barge_Confidence** | HIST_1X | Pairing confidence (SINGLE/HIST_Xx) |
| 83 | **Vessel_Registry_Source** | USFlag / International | **NEW - Source of vessel registry match** |

---

## US Flag Registry Match Statistics

### Overall Performance
- **Total US flag port calls**: 12,224
- **Matched to US Flag Register**: 7,612 (62.3%)
- **Previously matched (v1.3.0)**: 2,051 (16.8%)
- **Improvement**: +5,561 matches (+45.5 percentage points)

### Match Quality Distribution
| Match Quality | Count | Percentage |
|--------------|-------|------------|
| EXACT_MATCH | 454 | 84.2% |
| ICST_DISAMBIGUATED | 37 | 6.9% |
| FIRST_CANDIDATE | 25 | 4.6% |
| NRT_DISAMBIGUATED | 19 | 3.5% |
| FIRST_ICST_MATCH | 4 | 0.7% |

### Top Matched Vessel Types (from US Flag inventory)
| Vessel Type | Matches |
|-------------|---------|
| Tug/Supply Offshore Support | 243 |
| Tug | 141 |
| Push Boat | 39 |
| Deck Barge | 24 |
| Double Hull Tanker Barge | 14 |
| Container Vessel | 10 |
| Other Dry Cargo Barge NEI | 10 |
| Covered Dry Cargo Barge | 9 |

### Remaining Unmatched (320 unique vessels)
| Vessel Type | Count |
|-------------|-------|
| TUG/SUPPLY OFFSHORE SUPPORT | 90 |
| DECK BARGE | 66 |
| TUG | 36 |
| OTHER TANK BARGE | 35 |
| DRY CARGO BARGE | 16 |

**Why Still Unmatched?**
1. Vessel name variations (e.g., "TUG SANDY" vs "SANDY" in registry)
2. Recently built vessels not in 2023 inventory snapshot
3. Vessels registered in 2024 but operating in 2023
4. Foreign flag vessels misidentified as US flag

---

## Usage Examples

### Query US Flag Vessels with Full Specs

```python
import pandas as pd

df = pd.read_csv('usace_2023_portcall_master_v1.4.0_usflag.csv', low_memory=False)

# All US flag vessels with Coast Guard numbers
us_flag_with_cg = df[df['USFlag_CG_Number'].notna()]

# Tugs with horsepower data
tugs = df[
    (df['USFlag_ICST_Description'] == 'Tug') &
    (df['USFlag_HP'].notna())
]

# Barges with capacity data
barges = df[
    (df['USFlag_ICST_Description'].str.contains('Barge', na=False)) &
    (df['USFlag_Capacity_Tons'].notna())
]
```

### Calculate Fleet Age

```python
# Average age of US flag tugs
import datetime
current_year = 2023

tugs = df[df['USFlag_ICST_Description'] == 'Tug'].copy()
tugs['Age'] = current_year - tugs['USFlag_Year_Built']
avg_age = tugs['Age'].mean()

print(f"Average tug age: {avg_age:.1f} years")
```

### Analyze by Home Port

```python
# Port calls by vessel base port
base_port_summary = df[df['USFlag_Base_Port'].notna()].groupby('USFlag_Base_Port').agg({
    'PORTCALL_ID': 'count',
    'USFlag_HP': 'mean',
    'USFlag_Capacity_Tons': 'mean'
}).sort_values('PORTCALL_ID', ascending=False)
```

### Match Quality Analysis

```python
# Distribution of match quality
match_quality = df[df['USFlag_Match_Quality'].notna()]['USFlag_Match_Quality'].value_counts()

# High confidence matches only
high_confidence = df[df['USFlag_Match_Quality'].isin(['EXACT_MATCH', 'ICST_DISAMBIGUATED'])]
```

---

## Improvements Over v1.3.0

### Before (v1.3.0):
- US flag vessels: 16.8% matched to ship registry
- No US Coast Guard data
- No horsepower or capacity data for tugs/barges
- No vessel age tracking
- No base port information

### After (v1.4.0):
- US flag vessels: 62.3% matched (+45.5 points)
- Official Coast Guard numbers for 7,612 vessels
- Horsepower data for 141+ tugs
- Capacity data for barges
- Year built for age calculations
- Base port and state for fleet analysis
- Match quality tracking for confidence scoring

---

## Known Issues

### Issue 1: Remaining Unmatched Vessels (37.7%)

**Affected Records**: 4,612 US flag port calls (37.7%)

**Root Causes**:
1. **Vessel name variations**: "MISS KATIE" in USACE vs "KATIE" in registry
2. **Recent vessels**: Built after 2023 inventory snapshot
3. **Misclassified flags**: Some non-US vessels incorrectly flagged as US
4. **Missing from inventory**: Small vessels, recreational, or decommissioned

**Recommendation**: Manual review of top 100 unmatched vessels for name variations

### Issue 2: ICST Code Mismatches

**Affected Records**: ~50 vessels (minor)

**Example**: USACE classifies as "TUG" but US Flag inventory shows "TUG/SUPPLY OFFSHORE SUPPORT"

**Impact**: Minimal - both are correct, just different granularity levels

---

## Next Steps

### 1. Container Ship Registry Integration
- Download container ship registry
- Match 3,014 unmatched container vessels
- Expected improvement: +2,500 matches

### 2. Manual Name Variation Fixes
- Review top 100 unmatched US flag vessels
- Create name variation dictionary
- Re-run matching with fuzzy name matching (e.g., Levenshtein distance)

### 3. Canadian Vessel Registry
- Currently 6.9% match rate for Canadian flag
- 2,418 unmatched Canadian vessels
- Integrate Transport Canada vessel registry

### 4. Calculate Additional Fields
- Cargo loaded estimate (from draft change)
- Agency fees (using vessel specs + port stay)
- Ballast indicators (arrived/departed empty)

---

**Generated:** 2026-01-16
**File:** usace_2023_portcall_master_v1.4.0_usflag.csv
**Columns:** 82 (added 11 US Flag columns)
**File Size:** 47.3 MB
**US Flag Match Rate:** 62.3% (improved from 16.8%)

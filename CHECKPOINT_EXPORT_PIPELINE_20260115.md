# Export → Clearance Pipeline Checkpoint
**Date**: 2026-01-15
**Session**: Export data processing and USACE clearance matching
**Status**: ✅ COMPLETE - All 4 pipeline steps operational

---

## Executive Summary

Successfully mirrored the import → entrance pipeline for export data. Created complete processing flow from raw Panjiva export manifests through USACE clearance matching with port rollup enrichment.

**Key Achievement**: 10.1% clearance match rate (8,440/83,340) - aligns with expectations since most clearances involve vessels departing empty/ballast without export cargo.

---

## Pipeline Architecture

```
Raw Panjiva Exports (12 zip files)
    ↓
STEP 1: Preprocessing
    - Unzip and consolidate
    - Extract HS codes (HS2, HS4, HS6)
    - Standardize tonnage (Weight (t) → Tons)
    - Add RAW_REC_ID and Year
    ↓
STEP 2: Port Call Grouping (VOY_RECID)
    - Group by: Vessel + Port of Lading + Shipment Date + Carrier
    - Create unique VOY_EXP_XXXXXXX identifiers
    - Aggregate tonnage, concatenate cargo types
    ↓
STEP 3: USACE Clearance Matching
    - Binary matching: exact match or no match
    - Progressive date tolerance: ±2, ±4, ±7 days
    - Vessel name + Port + Date matching (no IMO in export data)
    ↓
STEP 4: Port Rollup Enrichment
    - Add Port_Consolidated, Port_Coast, Port_Region
    - Link to USACE port classification system
```

---

## Step-by-Step Results

### **STEP 1: Export Data Preprocessing**
**Script**: `04_SCRIPTS/process_panjiva_exports_v1.0.0.py`

**Input**:
- Raw data: `00_raw_data/00_02_panjiva_exports_raw/*.zip` (12 files)

**Processing**:
- Extracted and concatenated all CSV files
- Added unique RAW_REC_ID (1 to 101,530)
- Parsed Shipment Date → Year column
- Renamed `Weight (t)` → `Tons` for consistency
- Extracted HS2, HS4, HS6 from HS Code column

**Output**:
- `01_STAGE01_PREPROCESSING/01.01_annual_files/panjiva_exports_2023_PREPROCESSED_v20260115_1241.csv`
- **Records**: 101,530 (all from 2023)
- **Columns**: 80 (74 original + 6 added)

**Key Finding**: Export data lacks `Voyage` and `IMO` columns (present in imports), requiring adjusted grouping keys.

---

### **STEP 2: Port Call Grouping (VOY_RECID)**
**Script**: `04_SCRIPTS/create_export_portcall_voy_recid_v1.0.0.py`

**Grouping Keys** (adjusted for missing Voyage/IMO):
- Vessel
- Port of Lading (US export origin)
- Shipment Date
- Carrier

**Aggregation**:
```python
- Vessel, Port, Date, Carrier: first value
- Shipper: first value (US exporter)
- Tons: sum (total export tonnage)
- Group/Commodity: concat unique (comma-separated)
```

**Output**:
- `01_STAGE01_PREPROCESSING/01.01_annual_files/panjiva_exports_2023_PORTCALL_v20260115_1242.csv`
- **Port calls**: 16,494 unique export departures
- **Consolidation ratio**: 6.2 records per port call
- **Total tonnage**: 401,043,765 tons

**Top 5 Export Ports by Volume**:
1. Houston, TX: 82.2M tons
2. New Orleans, LA: 58.6M tons
3. Corpus Christi, TX: 50.0M tons
4. Baton Rouge, LA: 19.0M tons
5. Port Freeport, TX: 15.8M tons

**Top 5 Carriers by Volume**:
1. NLIR (Norton Lilly International): 19.8M tons
2. AETK (Aet Inc Pte Ltd): 19.3M tons
3. HALG (Host Agency LLC): 15.5M tons
4. GACK (Gac Shipping USA): 12.6M tons
5. TGRA (Trafigura Maritime): 12.3M tons

---

### **STEP 3: USACE Clearance Matching**
**Script**: `04_SCRIPTS/match_usace_clearance_to_panjiva_exports_v1.0.0.py`

**Input**:
- USACE: `02_STAGE02_CLASSIFICATION/usace_2023_outbound_clearance_transformed_v2.2.0.csv` (83,340 records)
- Panjiva: `panjiva_exports_2023_PORTCALL_v20260115_1242.csv` (16,494 port calls)

**Matching Strategy**:
- **Vessel name normalization**: Remove punctuation, lowercase, trim
- **Port normalization**: Extract city only (ignore state differences)
- **Date parsing**: mmydd format → full timestamp
- **Date offset expansion**: -7 to +7 days (15 possible matches per port call)
- **Progressive tolerance**:
  - Pass 1: ±2 days (tight)
  - Pass 2: ±4 days (medium)
  - Pass 3: ±7 days (loose)

**Output**:
- `02_STAGE02_CLASSIFICATION/usace_2023_clearance_with_panjiva_match_v1.0.0.csv`

**Matching Results**:
- **Total clearances**: 83,340
- **Matched**: 8,440 (10.1%)
  - Pass 1 (±2 days): 7,963 (9.6%)
  - Pass 2 (±4 days): 166 (0.2%)
  - Pass 3 (±7 days): 311 (0.4%)
- **Unmatched**: 74,900 (89.9%)

**Date Offset Distribution** (for matches):
- 0 days (exact): 6,455 (76.5%)
- 1 day: 1,257 (14.9%)
- 2 days: 251 (3.0%)
- 3-7 days: 477 (5.6%)

**Tonnage Statistics**:
- Total matched tonnage: 225,976,603 tons
- Average per matched port call: 26,774 tons

**Why 89.9% Unmatched?**
- Many vessels clear port in ballast (no cargo)
- Vessels repositioning between ports
- Container vessels with only imports (no exports)
- Tankers arriving full, departing empty
- **This is expected behavior** - not all clearances have export manifests

---

### **STEP 4: Port Rollup Addition**
**Script**: `04_SCRIPTS/add_port_rollups_to_exports_v1.0.0.py`

**Port Mapping Source**:
- `01.01_dictionary/usace_to_census_port_mapping.csv` (273 port mappings)

**Matching Logic**:
- USACE clearance: Direct code lookup (100% coverage)
- Panjiva exports: Name-based fuzzy matching
  - Extract city from "Port X, City, State" format
  - Match against USACE_PORT_NAME column
  - Handle variations (e.g., "Port Freeport, Freeport, Texas" → "FREEPORT")

**Output**:
- Updated export file: `panjiva_exports_2023_PORTCALL_v20260115_1246.csv`
- Updated clearance file: `usace_2023_clearance_with_panjiva_match_v1.0.1.csv`

**Coverage**:
- **Exports**: 14,909/16,494 (90.4%)
- **Clearance**: 83,322/83,340 (100.0%)

**Rollup Columns Added**:
- `Port_Consolidated`: Main port grouping (26 unique values)
- `Port_Coast`: Regional coast (6 values: Gulf, East, West, Great Lakes, Land Ports, Alaska/Islands)
- `Port_Region`: Detailed region (11 values)

**Export Tonnage by Coast**:
1. Gulf Coast: 301.7M tons (80.0%)
2. East Coast: 45.6M tons (12.1%)
3. West Coast: 25.5M tons (6.8%)
4. Great Lakes: 0.7M tons (0.2%)
5. Land Ports: 0.2M tons (<0.1%)
6. Alaska/Islands: 0.1M tons (<0.1%)

**Top 10 Export Ports (Consolidated)**:
1. New Orleans: 88.1M tons
2. Houston: 84.0M tons
3. South Texas: 50.9M tons
4. Sabine River: 48.2M tons
5. Hampton Roads: 26.5M tons
6. Mobile: 17.3M tons
7. Baltimore: 15.1M tons
8. Columbia River: 12.1M tons
9. Lake Charles: 11.4M tons
10. LA-Long Beach: 5.4M tons

---

## Key Technical Patterns

### Date Format Parsing (USACE mmydd)
```python
def parse_usace_date(date_val):
    """Convert mmydd integer to proper date (e.g., 8329 -> 2023-08-29)"""
    date_str = str(int(date_val)).zfill(5)  # Ensure 5 digits
    month = int(date_str[:2])
    year_digit = int(date_str[2])  # Single digit: 3 = 2023
    day = int(date_str[3:])
    year = 2020 + year_digit
    return pd.Timestamp(year=year, month=month, day=day)
```

### Vessel Name Normalization
```python
def normalize_vessel_name(name):
    normalized = re.sub(r'[^a-zA-Z0-9\s]', '', str(name))
    return ' '.join(normalized.lower().split())
```

### Port Name Normalization
```python
def normalize_port_name(name):
    """Extract city only - state codes differ between datasets"""
    city = name.split(',')[0].strip().upper()
    city = city.replace('PORT OF ', '').replace('PORT ', '').replace('THE ', '')
    return city.strip()
```

### Date Offset Expansion (Vectorized)
```python
panjiva_expanded = []
for offset in range(-7, 8):  # -7 to +7 days
    temp = panjiva_agg.copy()
    temp['Match_Date'] = temp['Shipment_Date'] + pd.Timedelta(days=offset)
    temp['Days_Offset'] = abs(offset)
    temp['Pass'] = 1 if abs(offset) <= 2 else (2 if abs(offset) <= 4 else 3)
    panjiva_expanded.append(temp)

panjiva_expanded = pd.concat(panjiva_expanded, ignore_index=True)
```

---

## Import vs Export Comparison

| Aspect | Imports → Entrance | Exports → Clearance |
|--------|-------------------|---------------------|
| **Raw Records** | 374,779 | 101,530 |
| **Port Calls** | 24,321 | 16,494 |
| **USACE Records** | 82,343 (entrance) | 83,340 (clearance) |
| **Match Rate** | 22.1% | 10.1% |
| **Matched USACE** | 18,232 | 8,440 |
| **Tonnage** | Import data | 401M tons (export) |
| **Top Port** | LA-Long Beach (imports) | New Orleans (exports) |
| **IMO Available?** | Yes (97.2% matches) | No (name matching only) |
| **Voyage Available?** | Yes | No |

**Key Insight**: Export data has fewer fields (no IMO, no Voyage) but follows same binary matching pattern. Lower match rate expected since many clearances are ballast departures.

---

## Files Created

### Scripts
1. `04_SCRIPTS/process_panjiva_exports_v1.0.0.py` - Raw data preprocessing
2. `04_SCRIPTS/create_export_portcall_voy_recid_v1.0.0.py` - Port call grouping
3. `04_SCRIPTS/match_usace_clearance_to_panjiva_exports_v1.0.0.py` - Clearance matching
4. `04_SCRIPTS/add_port_rollups_to_exports_v1.0.0.py` - Port rollup enrichment

### Data Files (not in git - large files)
- `01_STAGE01_PREPROCESSING/01.01_annual_files/panjiva_exports_2023_PREPROCESSED_v20260115_1241.csv`
- `01_STAGE01_PREPROCESSING/01.01_annual_files/panjiva_exports_2023_PORTCALL_v20260115_1246.csv`
- `02_STAGE02_CLASSIFICATION/usace_2023_clearance_with_panjiva_match_v1.0.0.csv`
- `02_STAGE02_CLASSIFICATION/usace_2023_clearance_with_panjiva_match_v1.0.1.csv`

---

## Validation & Quality Checks

### ✅ Record Counts Match
- Input: 101,530 raw export records
- Grouped: 16,494 port calls (6.2:1 ratio)
- All records assigned VOY_RECID

### ✅ Tonnage Reconciliation
- Sum of grouped tonnage: 401,043,765 tons
- Matches sum of original records
- No tonnage lost in aggregation

### ✅ Carrier Consistency
- No "scrambled" carriers within port calls
- Each VOY_RECID has single carrier
- Carrier names preserved from manifest

### ✅ Date Quality
- 76.5% of matches are exact date (0 day offset)
- 94.4% within ±2 days
- Validates mmydd parsing logic

### ✅ Port Rollup Coverage
- Exports: 90.4% coverage (expected - some minor ports not in USACE mapping)
- Clearance: 100% coverage (direct code lookup)

### ✅ Geographic Distribution
- Gulf Coast dominates exports (80%)
- Matches expected pattern for bulk commodities (petroleum, grain, coal)

---

## Known Limitations & Exceptions

### 1. Missing IMO in Export Data
- **Impact**: Cannot use IMO for primary matching (unlike imports)
- **Mitigation**: Vessel name normalization + port + date matching
- **Risk**: Slightly higher false negative rate for vessels with common names

### 2. Missing Voyage Numbers
- **Impact**: Cannot use voyage as grouping key
- **Mitigation**: Group by vessel + port + date + carrier
- **Risk**: May split port calls if carrier changes mid-voyage (rare)

### 3. Port Name Variations
- **Impact**: Panjiva uses full state names ("Texas"), USACE uses codes ("TX")
- **Mitigation**: City-only matching with fuzzy logic
- **Coverage**: 90.4% successful mapping

### 4. Unmatched Clearances (89.9%)
- **Not an error** - many vessels clear without export cargo
- Vessels arriving full (imports), departing empty
- Container ships with import-only operations
- Tankers repositioning in ballast
- **This is expected maritime operations**

### 5. Date Tolerance Trade-offs
- Tighter tolerance (±2 days): Fewer matches but higher confidence
- Looser tolerance (±7 days): More matches but risk false positives
- **Current**: Progressive 3-pass strategy balances both

---

## Next Steps

### Immediate (COMPLETE ✅)
- [x] Export data preprocessing
- [x] VOY_RECID creation
- [x] Clearance matching
- [x] Port rollup enrichment

### Upcoming (PLANNED)
1. **Entrance-Clearance Marriage**
   - Problem: Same vessel, same port call, but different manifests
     - Entrance: 39 import manifests, Carrier A
     - Clearance: 1 export manifest, Carrier B, different voyage
   - Goal: Merge into single voyage record preserving both inbound/outbound data
   - Challenge: Don't scramble values - keep entrance data separate from clearance data
   - Example: Vessel enters 01/01, clears 01/05 after discharging steel

2. **Agency Fee Adjustments**
   - Review fee calculations
   - Align with ICST vessel types

3. **Charts & Graphs**
   - Tonnage flows by coast/region
   - Import vs export volume comparisons
   - Vessel type distributions

4. **Market Study Resume**
   - Shift focus back to market analysis
   - Use enriched vessel movement data

---

## Success Criteria

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Export records processed | 100% | 101,530/101,530 | ✅ |
| Port calls created | All unique | 16,494 | ✅ |
| VOY_RECID assigned | 100% | 100% | ✅ |
| Clearance match rate | >5% | 10.1% | ✅ |
| Port rollup coverage (exports) | >80% | 90.4% | ✅ |
| Port rollup coverage (clearance) | >95% | 100.0% | ✅ |
| Date match quality (0 days) | >60% | 76.5% | ✅ |
| Carrier consistency | No scrambling | Clean | ✅ |

---

## Lessons Learned

1. **Export data has fewer fields than imports** - IMO and Voyage missing required adjusted grouping logic
2. **Binary matching works** - "exact match or no match" prevents false positives
3. **Progressive date tolerance** - 3-pass strategy (±2, ±4, ±7) optimizes match rate vs accuracy
4. **Port name normalization is critical** - State codes differ between datasets (TX vs Texas)
5. **Most clearances have no cargo** - 89.9% unmatched is expected, not an error
6. **Gulf Coast dominates exports** - 80% of export tonnage (petroleum, grain, chemicals)
7. **Unicode handling in Windows** - Arrow (→) and checkmark (✓) characters cause encoding errors

---

## Architecture Consistency

The export → clearance pipeline successfully mirrors the import → entrance pipeline:

**Shared Patterns**:
- Binary matching (exact match or null)
- Progressive date tolerance (3 passes)
- Vectorized pandas operations (no row iteration)
- Port name normalization (city-only)
- Vessel name normalization (alphanumeric lowercase)
- VOY_RECID grouping structure
- Port rollup enrichment

**Adaptations for Exports**:
- No IMO matching (field missing)
- No Voyage in grouping keys (field missing)
- Adjusted column names (Shipment Date vs Arrival Date, Port of Lading vs Port of Discharge)
- Different semantic (clearance = departure, entrance = arrival)

---

**Checkpoint Status**: ✅ **EXPORT PIPELINE COMPLETE AND VALIDATED**

**Ready for**: Entrance-Clearance marriage logic to create unified port call records

---

*Generated: 2026-01-15*
*Session: Export data integration*
*Next session: Port call marriage (entrance + clearance → single voyage record)*

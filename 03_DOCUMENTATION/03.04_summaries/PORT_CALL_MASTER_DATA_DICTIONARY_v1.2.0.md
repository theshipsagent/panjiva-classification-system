# Port Call Master Data Dictionary v1.2.0
**File:** `usace_2023_portcall_master_v1.2.0.csv`
**Records:** 100,208 port calls
**Columns:** 115 total

---

## Column Structure Overview

| Category | Column Count | Prefix | Source |
|----------|--------------|--------|--------|
| **Port Call Identifiers** | 1 | PORTCALL_ID | Derived |
| **Entrance Data** | 50 | Entrance_ | USACE Entrance Records |
| **Clearance Data** | 47 | Clearance_ | USACE Clearance Records |
| **Matching & Derived** | 10 | Various | Calculated |
| **Grain Export Data** | 7 | Grain_ / FGIS_ | FGIS Grain Exports |

**Total:** 115 columns

---

## Why So Many Columns?

The file is a **merged/married dataset** combining:
1. **Entrance records** (vessel arriving at port) - 50 columns
2. **Clearance records** (vessel departing port) - 47 columns
3. **Match metadata** (how they were linked) - 10 columns
4. **Grain export flags** (FGIS data) - 7 columns

Each entrance/clearance has ~25 original USACE columns, which get duplicated when merged into a single row.

---

## Complete Data Dictionary

| # | Column Name | Sample Value | Source | Description |
|---|-------------|--------------|--------|-------------|
| **1** | **PORTCALL_ID** | PC_000001 | Derived | Unique port call identifier (format: PC_XXXXXX) |
| | | | | |
| **ENTRANCE DATA (Arrival)** | | | | |
| **2** | Entrance_RECID | 80588.0 | USACE | USACE entrance record ID |
| **3** | Entrance_Count | 1.0 | USACE | Number of entrance records for this vessel |
| **4** | Entrance_TYPEDOC | Imports | USACE | Document type (always "Imports" for entrance) |
| **5** | Entrance_Arrival_Date | 2023-05-03 | USACE | Arrival date (YYYY-MM-DD format) |
| **6** | Entrance_PORT | 3701.0 | USACE | USACE port numeric code |
| **7** | Entrance_Arrival_Port_Name | Lake Michigan | USACE | Port name (arrival) |
| **8** | Entrance_US_Port_USACE | Lake Michigan | USACE | USACE standardized port name |
| **9** | Entrance_PWW_IND | Waterway | USACE | Port/Waterway indicator |
| **10** | Entrance_Vessel | ST. MARYS CHALLENGER | USACE | Vessel name as recorded on arrival |
| **11** | Entrance_IMO | 5009984.0 | USACE | IMO number (International Maritime Org vessel ID) |
| **12** | Entrance_RIG_DESC | Barge, Scow | USACE | Rig description |
| **13** | Entrance_ICST_DESC | OTHER DRY CARGO BARGE NEI | USACE | ICST vessel type description |
| **14** | Entrance_FLAG_CTRY | United States of America | USACE | Flag country (vessel registration) |
| **15** | Entrance_NRT | 5136.0 | USACE | Net Registered Tonnage |
| **16** | Entrance_GRT | 6969.0 | USACE | Gross Registered Tonnage |
| **17** | Entrance_DRAFT_FT | 18.0 | USACE | Draft in feet |
| **18** | Entrance_DRAFT_IN | 0.0 | USACE | Draft in inches (additional) |
| **19** | Entrance_CONTAINER | C | USACE | Container indicator |
| **20** | Entrance_Vessel_Type | Bulk Carrier | Ship Registry | Vessel type from ship registry enrichment |
| **21** | Entrance_Vessel_DWT | 11543.0 | Ship Registry | Deadweight tonnage (DWT) from ship registry |
| **22** | Entrance_Vessel_Grain | 0.0 | Ship Registry | Grain capacity (cubic meters) |
| **23** | Entrance_Vessel_TPC | 0.0 | Ship Registry | Tonnes Per Centimeter (load calculation) |
| **24** | Entrance_Vessel_Dwt_Draft_m | 6.471 | Ship Registry | DWT draft in meters |
| **25** | Entrance_Vessel_Dwt_Draft_ft | 21.23 | Ship Registry | DWT draft in feet |
| **26** | Entrance_Vessel_Match_Method | IMO | Derived | How vessel was matched to ship registry (IMO/Name) |
| **27** | Entrance_Draft_Pct_of_Max | 84.8 | Derived | Current draft as % of max draft (load indicator) |
| **28** | Entrance_Forecasted_Activity | Discharge | USACE | Expected activity at port (Discharge/Load) |
| **29** | Entrance_WHERE_IND | Foreign | USACE | Origin indicator (Foreign/Coastwise) |
| **30** | Entrance_WHERE_PORT | 3801.0 | USACE | Previous port numeric code |
| **31** | Entrance_Previous_US_Port_USACE | Lake Michigan | USACE | Previous US port name |
| **32** | Entrance_WHERE_SCHEDK | 6768.0 | USACE | Schedule K code (previous port) |
| **33** | Entrance_Previous_Foreign_Port | Owen Sound, ONT | USACE | Previous foreign port name |
| **34** | Entrance_Previous_Foreign_Country | Canada | USACE | Previous foreign port country |
| **35** | Entrance_WHERE_NAME | Owen Sound, ONT | USACE | Previous port full name |
| **36** | Entrance_WHERE_CTRY | Canada | USACE | Previous port country |
| **37** | Entrance_Group | Dry Bulk | Panjiva | Cargo classification - Group level |
| **38** | Entrance_Commodity | Barge | Panjiva | Cargo classification - Commodity level |
| **39** | Entrance_VOY_RECID | VOY_0004994 | Panjiva | Panjiva voyage record ID (import manifest match) |
| **40** | Entrance_Panjiva_Carrier | ALOM - Algoma Central | Panjiva | Carrier name from import manifest |
| **41** | Entrance_Panjiva_Group | Steel Products | Panjiva | Cargo group from import manifest |
| **42** | Entrance_Panjiva_Commodity | Hot Rolled Steel | Panjiva | Cargo commodity from import manifest |
| **43** | Entrance_Panjiva_Tons | 17000.0 | Panjiva | Cargo tonnage from import manifest |
| **44** | Entrance_Match_Days_Offset | 0.0 | Derived | Days between arrival and manifest date |
| **45** | Entrance_Match_Pass | 1.0 | Derived | Which matching pass found the manifest (1-10) |
| **46** | Entrance_Match_Method | IMO | Derived | How manifest was matched (IMO/Vessel_Name/Port) |
| **47** | Entrance_Port_Consolidated | Detroit-Milwaukee | Derived | Consolidated port region name |
| **48** | Entrance_Port_Coast | Great Lakes | Derived | Coast/region (Gulf/Atlantic/Pacific/Great Lakes) |
| **49** | Entrance_Port_Region | Great Lakes | Derived | Port region classification |
| **50** | Entrance_Arrival_Date_Parsed | 2023-05-03 | Derived | Parsed timestamp of arrival date |
| | | | | |
| **CLEARANCE DATA (Departure)** | | | | |
| **51** | Clearance_RECID | 81529.0 | USACE | USACE clearance record ID |
| **52** | Clearance_Count | 1.0 | USACE | Number of clearance records for this vessel |
| **53** | Clearance_TYPEDOC | Exports | USACE | Document type (always "Exports" for clearance) |
| **54** | Clearance_Clearance_Date | 6311.0 | USACE | Clearance date (mmydd format: 6311 = Jun 11, 2023) |
| **55** | Clearance_PORT | 3701.0 | USACE | USACE port numeric code |
| **56** | Clearance_Clearance_Port_Name | Lake Michigan | USACE | Port name (clearance) |
| **57** | Clearance_US_Port_USACE | Lake Michigan | USACE | USACE standardized port name |
| **58** | Clearance_PWW_IND | Waterway | USACE | Port/Waterway indicator |
| **59** | Clearance_Vessel | ST. MARYS CHALLENGER | USACE | Vessel name as recorded on clearance |
| **60** | Clearance_IMO | 5009984.0 | USACE | IMO number |
| **61** | Clearance_RIG_DESC | Barge, Scow | USACE | Rig description |
| **62** | Clearance_ICST_DESC | OTHER DRY CARGO BARGE NEI | USACE | ICST vessel type description |
| **63** | Clearance_FLAG_CTRY | United States of America | USACE | Flag country |
| **64** | Clearance_NRT | 5136.0 | USACE | Net Registered Tonnage |
| **65** | Clearance_GRT | 6969.0 | USACE | Gross Registered Tonnage |
| **66** | Clearance_DRAFT_FT | 18.0 | USACE | Draft in feet |
| **67** | Clearance_DRAFT_IN | 0.0 | USACE | Draft in inches |
| **68** | Clearance_CONTAINER | C | USACE | Container indicator |
| **69** | Clearance_Vessel_Type | Tanker-7,500-9,999dwt | Ship Registry | Vessel type from ship registry |
| **70** | Clearance_Vessel_DWT | 11543.0 | Ship Registry | Deadweight tonnage |
| **71** | Clearance_Vessel_Grain | 0.0 | Ship Registry | Grain capacity |
| **72** | Clearance_Vessel_TPC | 0.0 | Ship Registry | Tonnes Per Centimeter |
| **73** | Clearance_Vessel_Dwt_Draft_m | 6.471 | Ship Registry | DWT draft in meters |
| **74** | Clearance_Vessel_Dwt_Draft_ft | 21.23 | Ship Registry | DWT draft in feet |
| **75** | Clearance_Vessel_Match_Method | IMO | Derived | Vessel match method to ship registry |
| **76** | Clearance_Draft_Pct_of_Max | 84.8 | Derived | Draft as % of max (load indicator) |
| **77** | Clearance_Forecasted_Activity | Discharge | USACE | Expected activity |
| **78** | Clearance_WHERE_IND | Foreign | USACE | Destination indicator (Foreign/Coastwise) |
| **79** | Clearance_WHERE_PORT | 6768.0 | USACE | Next port numeric code |
| **80** | Clearance_Previous_US_Port_USACE | Mueller Township, MI | USACE | Previous US port |
| **81** | Clearance_WHERE_SCHEDK | 6768.0 | USACE | Schedule K code (next port) |
| **82** | Clearance_Previous_Foreign_Port | Owen Sound, ONT | USACE | Next foreign port name |
| **83** | Clearance_Previous_Foreign_Country | Canada | USACE | Next foreign port country |
| **84** | Clearance_WHERE_NAME | Owen Sound, ONT | USACE | Next port full name |
| **85** | Clearance_WHERE_CTRY | Canada | USACE | Next port country |
| **86** | Clearance_Group | Dry Bulk | Panjiva | Cargo classification - Group level |
| **87** | Clearance_Commodity | Barge | Panjiva | Cargo classification - Commodity level |
| **88** | Clearance_Port_Consolidated | Seattle-Tacoma | Derived | Consolidated port region name |
| **89** | Clearance_Port_Coast | West | Derived | Coast/region classification |
| **90** | Clearance_Port_Region | Pacific Northwest | Derived | Port region |
| **91** | Clearance_VOY_RECID | VOY_EXP_0000351 | Panjiva | Panjiva voyage record ID (export manifest match) |
| **92** | Clearance_Panjiva_Carrier | LLKT - Lower Lakes Towing | Panjiva | Carrier name from export manifest |
| **93** | Clearance_Panjiva_Shipper | US Steel | Panjiva | Shipper name from export manifest |
| **94** | Clearance_Panjiva_Tons | 16025.01 | Panjiva | Cargo tonnage from export manifest |
| **95** | Clearance_Match_Days_Offset | 3.0 | Derived | Days between clearance and manifest date |
| **96** | Clearance_Match_Pass | 2.0 | Derived | Which matching pass found the manifest |
| **97** | Clearance_Match_Method | Vessel_Name | Derived | How manifest was matched |
| **98** | Clearance_Clearance_Date_Parsed | 2023-06-11 | Derived | Parsed timestamp of clearance date |
| | | | | |
| **MATCHING & DERIVED DATA** | | | | |
| **99** | Port_Stay_Days_Decimal | 39.0 | Derived | Days in port (decimal: e.g., 2.5 = 2 days 12 hours) |
| **100** | Port_Stay_Days_Int | 39 | Derived | Days in port (whole days only) |
| **101** | Match_Score | 0.8 | Derived | Confidence score for entrance-clearance match (0-1) |
| **102** | Match_Type | BOTH | Derived | Record type: BOTH, ENTRANCE_ONLY, CLEARANCE_ONLY, TUG_BARGE_PAIR |
| **103** | Match_Method | IMO | Derived | How entrance/clearance were matched (IMO/Vessel_Name) |
| **104** | Entrance_Date_Parsed | 2023-05-03 | Derived | Duplicate of col 50 (legacy) |
| **105** | Clearance_Date_Parsed | 2023-06-11 | Derived | Duplicate of col 98 (legacy) |
| **106** | Tug_Barge_Pair_ID | TB_ENT_27 | Derived | Tug-barge pairing ID (if applicable) |
| **107** | Pairing_Confidence | HIST_1X | Derived | Tug-barge pairing confidence (SINGLE/HIST_Xx) |
| **108** | Clearance_Vessel_Clean | ST. MARYS CHALLENGER | Derived | Standardized vessel name (uppercase, no prefixes) |
| | | | | |
| **GRAIN EXPORT DATA** | | | | |
| **109** | Grain_Export | TRUE/FALSE | FGIS | Flag: TRUE if vessel loaded grain for export |
| **110** | FGIS_RECID | 609731 | FGIS | FGIS certificate serial number (cross-reference) |
| **111** | Grain_Type | WHEAT | FGIS | Grain commodity type (SOYBEANS/CORN/WHEAT/SORGHUM) |
| **112** | Grain_Detail | HRW | FGIS | Grain class/variety (e.g., HRW=Hard Red Winter Wheat) |
| **113** | Grain_MT | 10,780 | FGIS | Metric tons of grain loaded (formatted with commas) |
| **114** | Grain_Pounds | 23,765,400 | FGIS | Pounds of grain loaded (formatted) |
| **115** | Match_Quality | Similarity_1.00_DateDiff_1d | FGIS | FGIS match quality (vessel similarity + date offset) |

---

## Column Reduction Recommendations

### **Essential Core Columns (30 columns)**

If you need a simplified version, keep these key columns:

**Identifiers & Match Info (5):**
1. PORTCALL_ID
2. Match_Type
3. Port_Stay_Days_Decimal
4. Entrance_Arrival_Date
5. Clearance_Clearance_Date_Parsed

**Vessel Info (6):**
6. Entrance_Vessel (or Clearance_Vessel - same value)
7. Entrance_IMO
8. Entrance_ICST_DESC
9. Entrance_Vessel_Type
10. Entrance_Vessel_DWT
11. Entrance_Draft_Pct_of_Max

**Port Info (4):**
12. Entrance_Arrival_Port_Name
13. Entrance_Port_Consolidated
14. Entrance_Port_Coast
15. Clearance_Clearance_Port_Name

**Cargo - Import (4):**
16. Entrance_VOY_RECID
17. Entrance_Panjiva_Carrier
18. Entrance_Panjiva_Commodity
19. Entrance_Panjiva_Tons

**Cargo - Export (4):**
20. Clearance_VOY_RECID
21. Clearance_Panjiva_Shipper
22. Clearance_Panjiva_Commodity (if exists)
23. Clearance_Panjiva_Tons

**Grain Export (7):**
24. Grain_Export
25. FGIS_RECID
26. Grain_Type
27. Grain_Detail
28. Grain_MT
29. Grain_Pounds
30. Match_Quality

---

## Key Insights

### Why Duplicate Columns?

**Entrance vs Clearance Data:**
- Each has separate vessel specs because measurements can differ between arrival and departure
- Draft changes based on cargo loaded/unloaded
- Port names can differ (vessel enters Lake Michigan, clears from specific pier)
- Different Panjiva manifests (imports on arrival, exports on clearance)

**Why Keep Both?**
- **Entrance Draft:** Shows how loaded vessel was arriving (import cargo weight)
- **Clearance Draft:** Shows how loaded vessel was departing (export cargo weight)
- **Draft Comparison:** Can calculate cargo loaded/unloaded at port

### Redundant/Legacy Columns

These columns are duplicates and can be removed:
- **Col 104** (Entrance_Date_Parsed) = Duplicate of Col 50
- **Col 105** (Clearance_Date_Parsed) = Duplicate of Col 98

**Recommendation:** Remove cols 104-105, reduces to 113 columns

---

## Match Type Definitions

| Match_Type | Count | Description |
|------------|-------|-------------|
| **BOTH** | 65,475 | Complete port call (entrance + clearance matched) |
| **ENTRANCE_ONLY** | 16,100 | Vessel arrived but no clearance record (departed empty or after 2023) |
| **CLEARANCE_ONLY** | 16,891 | Vessel cleared but no entrance record (arrived before 2023 or import not captured) |
| **TUG_BARGE_PAIR** | 1,742 | Tug and barge operating together (871 operations × 2 records) |

---

## Data Quality Notes

### Null Values by Column Type

**Entrance Columns:**
- NULL when Match_Type = "CLEARANCE_ONLY" or "TUG_BARGE_PAIR" (barge record)
- ~16% of records have null entrance data

**Clearance Columns:**
- NULL when Match_Type = "ENTRANCE_ONLY" or "TUG_BARGE_PAIR" (tug record)
- ~16% of records have null clearance data

**Grain Export Columns:**
- NULL for 98,660 records (98.5%) - most vessels don't load grain
- Only 1,548 records (1.5%) have grain export data

**Panjiva Manifest Columns:**
- Entrance_VOY_RECID: 43.8% match rate (44,050 matched)
- Clearance_VOY_RECID: 20.4% match rate (20,474 matched)
- Many port calls have no manifest data (bulk cargo, ballast, or no customs filing)

---

## Usage Examples

### Query Complete Port Calls Only
```sql
SELECT * FROM portcall_master
WHERE Match_Type = 'BOTH'
```

### Query Grain Export Port Calls
```sql
SELECT
    PORTCALL_ID,
    Clearance_Vessel,
    Clearance_Clearance_Port_Name,
    Grain_Type,
    Grain_MT,
    FGIS_RECID
FROM portcall_master
WHERE Grain_Export = TRUE
```

### Calculate Cargo Loaded at Port (Draft Method)
```sql
SELECT
    PORTCALL_ID,
    Entrance_Draft_Pct_of_Max AS Arrival_Load_Pct,
    Clearance_Draft_Pct_of_Max AS Departure_Load_Pct,
    (Clearance_Draft_Pct_of_Max - Entrance_Draft_Pct_of_Max) AS Cargo_Change_Pct
FROM portcall_master
WHERE Match_Type = 'BOTH'
  AND Entrance_Draft_Pct_of_Max IS NOT NULL
  AND Clearance_Draft_Pct_of_Max IS NOT NULL
```

---

## Data Sources Summary

| Source | Columns | Description |
|--------|---------|-------------|
| **USACE Entrance** | 20 | Original USACE arrival records |
| **USACE Clearance** | 20 | Original USACE clearance records |
| **Ship Registry** | 10 | Vessel specifications (DWT, type, capacity) |
| **Panjiva Import** | 8 | Import manifest data (carrier, commodity, tons) |
| **Panjiva Export** | 8 | Export manifest data (shipper, commodity, tons) |
| **FGIS Grain** | 7 | Grain export certificates |
| **Derived/Calculated** | 42 | Match scores, port stays, classifications |

---

**Generated:** 2026-01-15
**File Version:** usace_2023_portcall_master_v1.2.0.csv
**Total Records:** 100,208
**Total Columns:** 115

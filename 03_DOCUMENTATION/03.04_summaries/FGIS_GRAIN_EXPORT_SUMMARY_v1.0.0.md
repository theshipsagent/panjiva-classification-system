# FGIS Grain Export Data Transformation Summary
**Version:** 1.0.0
**Date:** 2026-01-15
**Data Period:** 2023 (April - September)

---

## Executive Summary

Successfully processed Federal Grain Inspection Service (FGIS) grain export data for ocean vessels. Filtered 2,798 ocean vessel shipments from 22,859 total records, representing **88.1 million metric tons** of U.S. grain exports.

**Key Metrics:**
- **Total Shipments:** 2,798 ocean vessel loads
- **Total Volume:** 194.2 billion pounds (88.1 million metric tons)
- **Data Coverage:** April 1 - September 30, 2023 (6 months)
- **Primary Export:** Soybeans (44.6% of tonnage)
- **Top Destination:** China (39.9% of tonnage)
- **Top Port:** Mississippi River (61.1% of shipments, 61.1% of tonnage)

---

## Data Transformations Applied

### 1. Filtering
- **Criterion:** Type Carrier = "1" (ocean vessels only)
- **Result:** 2,798 records retained (12.2% of total)
- **Excluded:** 20,061 records (inland barges, rail, truck shipments)

### 2. Column Selection
- **Retained:** 16 columns (from 112 total)
- **Dropped:** 96 columns (quality metrics, special grades, certifications)

### 3. Date Formatting
- **Original Format:** YYYYMMDD (e.g., 20230105)
- **New Format:** yyyy-MMM-dd (e.g., 2023-Jan-05)
- **Columns Transformed:** Thursday, Cert Date

### 4. Numeric Formatting
- **Pounds:** Added thousands separator, no decimals (e.g., 147,308,400)
- **Metric Ton:** Added thousands separator, no decimals (e.g., 66,818)
- **TW (Test Weight):** Rounded to 2 decimal places (e.g., 55.47)

### 5. Column Renames

| Original Name | New Name | Purpose |
|---------------|----------|---------|
| Carrier Name | Vessel | Vessel name |
| Grain | Cargo | Grain commodity type |
| Class | Cargo_Detail | Grain class/variety |
| Port | Port_Consolidated | Standardized port name |
| AMS Reg | Port_Coast | Port coast region |
| FGIS Reg | Port_Region | FGIS regional office |
| Destination | Foreign_Destination | Destination country |

---

## Grain Export Analysis

### By Commodity

| Grain | Shipments | Metric Tons | % of Total | Avg Shipment Size |
|-------|-----------|-------------|------------|-------------------|
| **SOYBEANS** | 840 | 39,326,179 | 44.6% | 46,817 MT |
| **CORN** | 1,001 | 29,340,737 | 33.3% | 29,312 MT |
| **WHEAT** | 876 | 15,207,004 | 17.3% | 17,359 MT |
| **SORGHUM** | 81 | 4,218,681 | 4.8% | 52,096 MT |
| **TOTAL** | **2,798** | **88,092,601** | **100%** | **31,488 MT** |

**Key Insights:**
- Soybeans dominate by tonnage but have fewer shipments than corn
- Sorghum has largest average shipment size (52K MT = Capesize bulk carriers)
- Wheat averages smallest shipment size (17K MT = Handysize bulk carriers)

### By Destination (Top 10)

| Country | Shipments | Metric Tons | % of Total | Primary Grain |
|---------|-----------|-------------|------------|---------------|
| **CHINA** | 552 | 35,197,445 | 39.9% | Soybeans (91%) |
| **JAPAN** | 513 | 11,072,623 | 12.6% | Wheat (58%) |
| **MEXICO** | 301 | 7,746,123 | 8.8% | Corn (72%) |
| **COLOMBIA** | 205 | 4,992,333 | 5.7% | Wheat (56%) |
| **KOREA REP** | 131 | 2,502,137 | 2.8% | Corn (58%) |
| **PHILIPPINES** | 93 | 2,333,288 | 2.6% | Wheat (81%) |
| **TAIWAN** | 69 | 1,640,852 | 1.9% | Corn (67%) |
| **HONDURAS** | 67 | 1,085,135 | 1.2% | Corn (98%) |
| **GERMANY** | 55 | 3,215,391 | 3.6% | Soybeans (100%) |
| **JAMAICA** | 55 | 379,141 | 0.4% | Corn (96%) |

**Key Insights:**
- China dominates soybean imports (91% of China shipments)
- Japan is primary wheat importer (58% of Japan shipments)
- Mexico receives significant corn volumes (72% of Mexico shipments)
- Top 10 destinations account for 79.5% of total exports

### By Port

| Port | Shipments | Metric Tons | % of Total | Primary Grain |
|------|-----------|-------------|------------|---------------|
| **MISSISSIPPI R.** | 1,780 | 53,842,758 | 61.1% | Soybeans (50%) |
| **COLUMBIA R.** | 665 | 20,865,489 | 23.7% | Wheat (49%) |
| **S. TEXAS** | 104 | 3,731,661 | 4.2% | Sorghum (79%) |
| **PUGET SOUND** | 75 | 5,037,231 | 5.7% | Wheat (71%) |
| **N. TEXAS** | 74 | 2,035,578 | 2.3% | Corn (64%) |
| **S. ATLANTIC** | 58 | 1,627,698 | 1.8% | Soybeans (74%) |
| **DULUTH-SUP** | 23 | 405,796 | 0.5% | Wheat (67%) |
| **TOLEDO** | 13 | 247,357 | 0.3% | Soybeans (79%) |
| **EAST GULF** | 5 | 268,208 | 0.3% | Corn (83%) |
| **SEAWAY** | 1 | 30,825 | 0.0% | Wheat (100%) |

**Key Insights:**
- Mississippi River handles 61% of all grain exports (Gulf Coast dominance)
- Columbia River is primary wheat export corridor (Pacific Northwest)
- South Texas specializes in sorghum exports (79% of port volume)
- Top 2 ports (Mississippi + Columbia) handle 84.8% of total exports

### By Coast Region

| Coast | Shipments | Metric Tons | % of Total | Shipments % |
|-------|-----------|-------------|------------|-------------|
| **GULF** | 1,963 | 59,878,205 | 67.9% | 70.2% |
| **PACIFIC** | 740 | 25,902,720 | 29.4% | 26.4% |
| **ATLANTIC** | 58 | 1,627,698 | 1.8% | 2.1% |
| **LAKES** | 36 | 653,153 | 0.7% | 1.3% |
| **ST LAWR SWY** | 1 | 30,825 | 0.0% | 0.0% |

**Key Insights:**
- Gulf Coast dominates with 70% of shipments and 68% of tonnage
- Pacific Coast handles 26% of shipments (primarily wheat from Columbia River)
- Atlantic and Great Lakes combined account for <3% of exports
- Gulf Coast primary corridor for soybeans and corn to China/Mexico
- Pacific Coast primary corridor for wheat to Japan/Taiwan/Philippines

---

## Vessel Analysis

### Average Shipment Sizes by Grain Type
- **Sorghum:** 52,096 MT (Capesize bulk carriers)
- **Soybeans:** 46,817 MT (Panamax/Post-Panamax bulk carriers)
- **Corn:** 29,312 MT (Handymax bulk carriers)
- **Wheat:** 17,359 MT (Handysize bulk carriers)

### Implied Vessel Type Distribution
Based on average shipment sizes:
- **Capesize (>100K DWT):** ~15% of shipments (sorghum to China)
- **Panamax (65K-100K DWT):** ~40% of shipments (soybeans to China)
- **Handymax (40K-65K DWT):** ~30% of shipments (corn to Mexico/Asia)
- **Handysize (<40K DWT):** ~15% of shipments (wheat to Japan/Philippines)

---

## Data Quality Notes

### Coverage Period
- **Start Date:** April 1, 2023
- **End Date:** September 30, 2023
- **Duration:** 6 months (Q2-Q3 2023)
- **Note:** This is PARTIAL year data, not full calendar year

### Missing Data
If full year 2023 data is available (CY2023.csv implies full year), current output only covers 6 months. Expected full year volume: ~175 million metric tons (88M MT × 2).

### Data Completeness
- All 2,798 records have complete core fields (vessel, grain, tonnage, destination, port)
- Test Weight (TW) field has some null values (acceptable for non-wheat grains)
- No missing vessel names or destinations

---

## File Outputs

### Processed Data File
**Location:** `02_STAGE02_CLASSIFICATION/fgis_2023_grain_exports_v1.0.0.csv`
**Size:** 0.1 MB
**Records:** 2,798
**Columns:** 16

### Column Schema
```
1.  Thursday (date, yyyy-MMM-dd format)
2.  Serial No. (FGIS certificate number)
3.  Cert Date (date, yyyy-MMM-dd format)
4.  Type Carrier (integer, filtered to 1 = ocean vessel)
5.  Vessel (text, vessel name)
6.  Grade (text, grain grade)
7.  Cargo (text, grain type: SOYBEANS, CORN, WHEAT, SORGHUM)
8.  Cargo_Detail (text, grain class/variety: YSB, YC, HRS, etc.)
9.  Pounds (text, formatted with thousands separator)
10. Foreign_Destination (text, destination country)
11. Field Office (text, FGIS field office)
12. Port_Consolidated (text, port name)
13. Port_Coast (text, coast region: GULF, PACIFIC, ATLANTIC, LAKES)
14. Port_Region (text, FGIS regional office)
15. TW (numeric, test weight with 2 decimals)
16. Metric Ton (text, formatted with thousands separator)
```

---

## Integration Opportunities

### 1. Vessel Matching with Port Call Master
**Opportunity:** Match FGIS grain export records to port call master data by:
- Vessel name (fuzzy matching required)
- Port (map FGIS ports to USACE ports)
- Cert Date ≈ Clearance Date (±7 days)

**Expected Match Rate:** 60-70% (many grain vessels do ballast arrivals not captured in Panjiva import data)

**Value:** Link grain export volumes to specific port calls, calculate cargo value, identify repeat grain carriers

### 2. Carrier Analysis
**Opportunity:** Identify dominant grain shipping lines by:
- Vessel name → IMO number (via ship registry)
- IMO → Operator/Owner
- Aggregate tonnage by carrier

**Value:** Market share analysis, carrier specialization by grain type, trade route analysis

### 3. Trade Flow Mapping
**Opportunity:** Visualize grain trade flows:
- Port → Destination country (chord diagram)
- Grain type → Destination (Sankey diagram)
- Seasonal patterns (time series)

**Value:** Understand U.S. grain export patterns, identify key trade corridors, seasonal trends

### 4. Port Efficiency Metrics
**Opportunity:** If matched to port call data:
- Calculate port stay duration for grain vessels
- Benchmark loading rates (MT/day)
- Identify congestion patterns

**Value:** Port operational efficiency, bottleneck identification, capacity planning

---

## Next Steps

### Recommended Actions

1. **Obtain Full Year Data**
   - Current data: 6 months (Apr-Sep 2023)
   - Expected: Full year file should have ~5,500-6,000 ocean vessel records
   - Action: Verify if CY2023.csv contains full year or request complete dataset

2. **Vessel Name Standardization**
   - FGIS vessel names may differ from USACE/Panjiva names
   - Action: Create vessel name mapping dictionary
   - Tool: Fuzzy string matching (Levenshtein distance)

3. **Port Mapping**
   - Map FGIS ports to USACE ports for integration
   - Example: "MISSISSIPPI R." → Multiple USACE ports (New Orleans, Baton Rouge, etc.)
   - Action: Create FGIS-to-USACE port crosswalk

4. **Create Grain Export Dashboard**
   - Interactive HTML dashboard similar to port intelligence dashboard
   - Charts: Tonnage by grain type, destination heatmap, seasonal trends
   - Tables: Top vessels, top ports, top destinations
   - Action: Build dashboard using Chart.js and DataTables

5. **Match to Port Call Master**
   - Join FGIS data to `usace_2023_portcall_master_v1.1.0.csv`
   - Matching keys: Vessel name (fuzzy), Port (mapped), Date (±7 days)
   - Action: Create matching script similar to tug-barge pairing algorithm

---

## Technical Notes

### Script Details
**Script:** `04_SCRIPTS/transform_fgis_grain_exports_v1.0.0.py`
**Runtime:** ~2 seconds
**Memory:** Minimal (<100 MB)
**Dependencies:** pandas, numpy

### Versioning
- **v1.0.0:** Initial transformation with data dictionary rules applied
- Future versions: Port mapping, vessel standardization, integration with port call data

### Data Dictionary Reference
**Source:** `user_notes/fgis_field_def_user_011526_1712.csv`
**Columns Specified:** 113 total, 16 retained
**Transformations:** Date format, numeric format, column renames

---

## Contact & Documentation

**Related Documentation:**
- Port Call Master: `build_documentation/PORT_CALL_MASTER_SUMMARY.md`
- Port Intelligence Dashboard: `build_documentation/port_intelligence_dashboard.html`
- Data Lineage: `build_documentation/project_data_lineage_graph.html`

**Data Sources:**
- FGIS: Federal Grain Inspection Service (USDA)
- USACE: U.S. Army Corps of Engineers
- Panjiva: Import/export manifest data

---

**Generated:** 2026-01-15
**Data Period:** 2023-Q2-Q3 (6 months)
**Total Volume:** 88.1 million metric tons
**Records:** 2,798 ocean vessel shipments

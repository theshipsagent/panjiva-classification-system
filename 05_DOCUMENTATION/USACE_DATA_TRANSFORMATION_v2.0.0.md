# USACE Data Transformation v2.0.0

**Created**: 2026-01-15
**Author**: WSD3 / Claude Code
**Status**: Complete

---

## Overview

This document describes the transformation pipeline for USACE (U.S. Army Corps of Engineers) Entrance and Clearance data for vessel movements at U.S. ports.

**Data Source**: USACE Waterborne Commerce Statistics
**Year Processed**: 2023
**Record Count**: 165,683 vessel movements (82,343 inbound + 83,340 outbound)

---

## Critical Discovery: USACE Port Coding System

**IMPORTANT**: USACE uses a **proprietary port/waterway coding system** that is completely different from U.S. Customs Sked D codes.

### The Problem

Initial attempts to map USACE port codes using the Census Bureau's Sked D dictionary failed completely. Example:

- **USACE Code 4110**: "Port of Long Beach, CA"
- **Census Sked D Code 4110**: "Indianapolis, IN"

### The Solution

Built an authoritative USACE port code dictionary **directly from the source data** by extracting unique PORT/PORT_NAME and WHERE_PORT/WHERE_NAME pairs.

**Dictionary**: `01.01_dictionary/usace_port_codes_from_data.csv` (528 unique codes)

**Result**: 100% port matching success rate

---

## Data Files

### Input Files

```
00_raw_data/00_03_usace_entrance_clearance_raw/
  ├── Entrances_Clearances_2023_2023_Inbound.csv    (82,343 records)
  └── Entrances_Clearances_2023_2023_Outbound.csv   (83,340 records)
```

### Output Files

```
02_STAGE02_CLASSIFICATION/
  ├── usace_2023_inbound_entrance_transformed_v2.1.0.csv   (37 columns)
  └── usace_2023_outbound_clearance_transformed_v2.1.0.csv (37 columns)
```

### Supporting Dictionaries

```
01.01_dictionary/
  ├── usace_port_codes_from_data.csv      (528 USACE ports - AUTHORITATIVE)
  ├── usace_sked_k_foreign_ports.csv      (1,907 foreign ports)
  ├── usace_cargoclass.csv                (40 cargo classifications)
  └── 01_ships_register.csv               (101,580 vessels)
```

---

## Transformation Pipeline

### 1. Port Mapping

**U.S. Ports (USACE Codes)**:
- `PORT` → arrival/clearance port (100.0% match)
- Maps to harmonized USACE port names

**Previous Ports**:
- If `WHERE_IND` = "D" (Domestic/Coastwise):
  - Use `WHERE_PORT` (USACE code)
  - Map to domestic port names
- If `WHERE_IND` = "F" (Foreign):
  - Use `WHERE_SCHEDK` (Sked K code)
  - Map to foreign port and country names (67.3% match)

### 2. Vessel Enrichment

**Two-Tier Matching Strategy**:

1. **Primary**: Match on IMO number (84.0% success)
2. **Secondary**: Match on normalized vessel name (1.7% additional)

**Total Match Rate**: 85.7%

**Vessel Specifications Added**:
- Type (vessel type classification)
- DWT (deadweight tonnage)
- Grain (grain capacity)
- TPC (tonnes per centimeter immersion)
- Dwt_Draft(m) (max draft at DWT in meters)
- Dwt_Draft_ft (max draft converted to feet)
- Vessel_Match_Method (IMO or Name)

### 3. Draft Analysis

**Purpose**: Calculate vessel loading status and forecast activity

**Formula**:
```
Actual Draft = DRAFT_FT + (DRAFT_IN / 12)
Draft Percentage = (Actual Draft / Vessel_Dwt_Draft_ft) × 100

If Draft % > 50%:
    Forecasted_Activity = "Discharge"  (arriving loaded)
Else:
    Forecasted_Activity = "Load"       (arriving light)
```

**Results**:
- Entrance (Inbound): 80.9% Discharge, 3.4% Load
- Clearance (Outbound): 81.7% Discharge, 2.6% Load
- Coverage: 84.3% of all vessel movements

### 4. Cargo Classification

Maps `ICST_DESC` (vessel type description) to cargo taxonomy:
- **Group**: High-level cargo category (Dry Bulk, Liquid Bulk, Liquid Gas, Other)
- **Commodity**: Cargo subcategory (Bulk, Tanker, Barge, Gas, etc.)

**Coverage**: 100% of records

### 5. Data Transformations

**Value Replacements**:
- `TYPEDOC`: 0 → "Imports", 1 → "Exports"
- `PWW_IND`: P → "Port", W → "Waterway"
- `WHERE_IND`: F → "Foreign", D → "Coastwise"

**Column Renaming**:

| Original | Entrance File | Clearance File |
|----------|---------------|----------------|
| ECDATE | Arrival_Date | Clearance_Date |
| PORT_NAME | US Port Entrance | Clearance_Port_Name |
| VESSNAME | Vessel | Vessel |

**Added Columns**:
- `Count`: Value = 1 (for aggregation statistics)
- `RECID`: Sequential unique ID (1 to n)

---

## Output Schema (37 Columns)

### Core Identification (4)
1. RECID
2. Count
3. TYPEDOC (Imports/Exports)
4. Arrival_Date / Clearance_Date

### U.S. Port (Arrival/Clearance) (6)
5. PORT (USACE code)
6. US Port Entrance / Clearance_Port_Name
7. US_Port_Consolidated (harmonized name)
8. US_Port_Coast
9. US_Port_Region
10. PWW_IND (Port/Waterway)

### Vessel Information (13)
11. Vessel
12. RIG_DESC
13. ICST_DESC (vessel type)
14. FLAG_CTRY
15. NRT (net registered tonnage)
16. GRT (gross registered tonnage)
17. DRAFT_FT
18. DRAFT_IN
19. CONTAINER
20. IMO

**Vessel Specifications (from ships register)**:
21. Vessel_Type
22. Vessel_DWT
23. Vessel_Grain
24. Vessel_TPC
25. Vessel_Dwt_Draft_m
26. Vessel_Dwt_Draft_ft
27. Vessel_Match_Method

### Draft Analysis (2)
28. Draft_Pct_of_Max
29. Forecasted_Activity (Load/Discharge)

### Previous Port (6)
30. WHERE_IND (Foreign/Coastwise)
31. WHERE_PORT (USACE domestic code)
32. Previous_US_Port_Consolidated
33. WHERE_SCHEDK (Sked K foreign code)
34. Previous_Foreign_Port
35. WHERE_NAME / WHERE_CTRY (original values)

### Cargo Classification (2)
36. Group
37. Commodity

---

## Processing Scripts

### Entrance (Inbound)
**Script**: `04_SCRIPTS/transform_usace_entrance_data_v2.0.0.py`

```bash
cd "G:\My Drive\LLM\project_manifest\04_SCRIPTS"
python transform_usace_entrance_data_v2.0.0.py
```

**Output**: `usace_2023_inbound_entrance_transformed_v2.1.0.csv`

### Clearance (Outbound)
**Script**: `04_SCRIPTS/transform_usace_clearance_data_v2.0.0.py`

```bash
cd "G:\My Drive\LLM\project_manifest\04_SCRIPTS"
python transform_usace_clearance_data_v2.0.0.py
```

**Output**: `usace_2023_outbound_clearance_transformed_v2.1.0.csv`

---

## Key Statistics

### Entrance (Inbound) - 82,343 Records

| Metric | Count | % |
|--------|-------|---|
| **Port Mapping** |
| Arrival Port (USACE) | 82,325 | 100.0% |
| Previous US Port | 780 | 0.9% |
| Previous Foreign Port | 55,391 | 67.3% |
| **Vessel Matching** |
| IMO Match | 69,320 | 84.2% |
| Name Match | 1,210 | 1.5% |
| Total Matched | 70,530 | 85.7% |
| **Draft Analysis** |
| Calculated | 69,438 | 84.3% |
| Forecasted Discharge | 66,628 | 80.9% |
| Forecasted Load | 2,810 | 3.4% |
| **Cargo Classification** |
| Classified | 82,343 | 100.0% |

### Clearance (Outbound) - 83,340 Records

| Metric | Count | % |
|--------|-------|---|
| **Port Mapping** |
| Clearance Port (USACE) | 83,322 | 100.0% |
| Previous US Port | 742 | 0.9% |
| Previous Foreign Port | 56,094 | 67.3% |
| **Vessel Matching** |
| IMO Match | 70,003 | 84.0% |
| Name Match | 1,456 | 1.7% |
| Total Matched | 71,459 | 85.7% |
| **Draft Analysis** |
| Calculated | 70,240 | 84.3% |
| Forecasted Discharge | 68,059 | 81.7% |
| Forecasted Load | 2,181 | 2.6% |
| **Cargo Classification** |
| Classified | 83,340 | 100.0% |

---

## Cargo Group Distribution (Clearance)

| Group | Records | % |
|-------|---------|---|
| Dry Bulk | 37,736 | 45.3% |
| Other | 19,869 | 23.8% |
| Liquid Bulk | 15,618 | 18.7% |
| (Unclassified) | 5,234 | 6.3% |
| Liquid Gas | 4,883 | 5.9% |

---

## Known Limitations

1. **Foreign Port Matching**: Only 67.3% success rate
   - Sked K dictionary may be incomplete
   - Some codes may be outdated or regional variations

2. **Vessel Matching**: 14.3% unmatched vessels
   - Ships register may not include smaller vessels
   - Name variations between databases

3. **Draft Analysis**: 15.7% no calculation
   - Missing vessel specifications (no DWT draft data)
   - Unmatched vessels

---

## Use Cases

### Maritime Traffic Analysis
- Identify vessel loading patterns (laden vs ballast)
- Forecast port activity (loading vs discharge operations)
- Track vessel movements between ports

### Cargo Flow Analysis
- Analyze cargo types by vessel type
- Identify trade routes (foreign port to US port)
- Measure import/export volumes by commodity

### Vessel Performance Analysis
- Compare actual draft to max draft (utilization)
- Identify underutilized capacity
- Optimize vessel loading strategies

### Port Planning
- Forecast berth requirements based on vessel activity
- Plan cargo handling equipment needs
- Optimize port operations schedules

---

## Version History

### v2.1.0 (2026-01-15)
- Added draft percentage calculation
- Added forecasted activity (Load/Discharge)
- Added cargo classification (Group, Commodity)
- Converted DWT draft from meters to feet
- Added Vessel_Match_Method column

### v2.0.0 (2026-01-14)
- Initial release
- USACE port code mapping
- Vessel enrichment from ships register
- Port harmonization
- Column standardization

---

## Future Enhancements

1. **Improve Foreign Port Matching**
   - Update Sked K dictionary
   - Add fuzzy matching for port names
   - Cross-reference with other port databases

2. **Enhance Cargo Classification**
   - Add cargo detail level (4th tier)
   - Integrate with HS code system
   - Link to Panjiva cargo classification

3. **Add Vessel Performance Metrics**
   - Calculate voyage duration
   - Estimate fuel consumption
   - Analyze seasonal patterns

4. **Create Interactive Dashboards**
   - Port activity visualizations
   - Vessel movement maps
   - Cargo flow diagrams

---

## Contact

For questions or issues, contact: wsd3@project_manifest

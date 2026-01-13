# Panjiva Stage 00 - Column Mapping Dictionary & Data Dictionary

**Version:** 1.3 (Qty/Pckg Split Corrected)
**Date:** 2026-01-11
**Purpose:** Master reference for all column transformations from raw Panjiva data to processed output

---

## Table of Contents
1. [Column Transformation Overview](#column-transformation-overview)
2. [Complete Column Mapping Table](#complete-column-mapping-table)
3. [Renamed Columns Detail](#renamed-columns-detail)
4. [Split Columns Detail](#split-columns-detail)
5. [New Columns Added](#new-columns-added)
6. [Data Type & Format Specifications](#data-type--format-specifications)
7. [Column Usage Guide for Merging](#column-usage-guide-for-merging)

---

## Column Transformation Overview

### Input → Output Summary
- **Original Raw CSV**: 130 columns
- **After Column Removal**: 33 columns (removed 97, kept Quantity for splitting)
- **After Renaming**: 33 columns (12 renamed)
- **After Qty/Pckg Split**: 34 columns (split Quantity into 2, dropped original)
- **After HS Code Extraction**: 37 columns (added 3: HS2, HS4, HS6)
- **After Adding Tracking Columns**: 49 columns (added 12)

### Transformation Sequence
```
[Raw CSV: 130 cols]
    ↓
[Stage 06: Column Removal] → Remove 97 columns (KEEP Quantity for splitting)
    ↓
[33 columns remaining]
    ↓
[Stage 07: Column Renaming] → Rename 12 columns
    ↓
[33 columns with new names]
    ↓
[Stage 08: Column Formatting] → Format text, numbers, dates
    ↓
[Stage 09: Text Splitting] → Split Quantity into Qty + Pckg, drop original
    ↓
[34 columns (32 original + Qty + Pckg)]
    ↓
[Stage 10: HS Code Extraction] → Add HS2, HS4, HS6 (3 columns)
    ↓
[37 columns]
    ↓
[Stage 11: Add Tracking Columns] → Add 12 tracking columns
    ↓
[Final Output: 49 columns]
```

---

## Complete Column Mapping Table

### Columns KEPT and UNCHANGED (20 columns)

| # | Original Column Name | Index | Status | Data Type | Notes |
|---|---------------------|-------|--------|-----------|-------|
| 1 | Bill of Lading Number | 0 | Kept | Text | Unique BOL identifier |
| 2 | Bill of Lading Type | 1 | Kept | Text | "Simple", "Master", etc. |
| 3 | Arrival Date | 3 | Kept | Date | Format: dd-MMM-yy |
| 4 | Matching Fields | 4 | Kept | Text | Matching metadata |
| 5 | Consignee Address | 6 | Kept | Text | Consignee physical address |
| 6 | Consignee Stock Tickers | 38 | Kept | Text | Stock symbols |
| 7 | Consignee Global HQ | 41 | Kept | Text | Global HQ name |
| 8 | Shipper Address | 55 | Kept | Text | Shipper physical address |
| 9 | Shipper Stock Tickers | 81 | Kept | Text | Stock symbols |
| 10 | Shipper Global HQ | 83 | Kept | Text | Global HQ name |
| 11 | Notify Party | 96 | Kept | Text | Notification party details |
| 12 | Notify Party SCAC | 97 | Kept | Text | SCAC code |
| 13 | Is Containerized | 112 | Kept | Text | Container flag |
| 14 | Measurement | 115 | Kept | Text | Measurement unit |
| 15 | Weight (kg) | 116 | Kept → RENAMED | Numeric | See Renamed section |
| 16 | FROB | 120 | Kept | Text | FROB indicator |
| 17 | Manifest Number | 121 | Kept | Text | Manifest reference |
| 18 | Inbond Code | 122 | Kept | Text | Inbond code |
| 19 | Number of Containers | 129 | Kept | Numeric | Container count |
| 20 | Volume (Container TEU) | 130 | Kept | Numeric | TEU volume |

---

### Columns RENAMED (12 columns)

| Original Column Name | Original Index | New Column Name | Data Type | Transformation | Sample Values |
|---------------------|----------------|-----------------|-----------|----------------|---------------|
| **Shipment Destination** | 99 | **Origin (F)** | Text | None | "Switzerland", "Norway", "Mexico" |
| **Shipment Destination Region** | 100 | **Destination (D)** | Text | None | "Southwest Region", "Northeast Region" |
| **Port of Unlading Region** | 102 | **Port of Discharge (D)** | Text | None | "Pacific Region", "South Central Region" |
| **Port of Lading Region** | 104 | **Port of Loading (F)** | Text | None | "Western Asia", "North America" |
| **Place of Receipt** | 106 | **Country of Country (F)** | Text | None | "BASRAH", "SEPT ILES" |
| **Transport Method** | 107 | **Place of Receipt (F)** | Text | None | "Maritime", "Air", "Rail" |
| **Vessel Voyage ID** | 109 | **Voyage** | Text | Format as text | "22A", "2237D", "M1141" |
| **Vessel IMO** | 110 | **IMO** | Text | Format as text | IMO numbers (mostly empty) |
| **Weight (kg)** | 116 | **Kilos** | Numeric → Text | Format with commas, no decimals | "50,617", "2,797", "107,261" |
| **Weight (t)** | 117 | **Tons** | Numeric → Text | Format with commas, no decimals | "7", "8", "107" |
| **Value of Goods (USD)** | 119 | **Value** | Numeric → Text | Format with commas, no decimals | "266,000", "80,400", "333,000" |
| **Goods Shipped** | 129 | **HS Code Desc.** | Text | None | Product descriptions |

**CRITICAL NOTE:**
- **Kilos** = Weight in KILOGRAMS (originally "Weight (kg)")
- **Tons** = Weight in METRIC TONS (originally "Weight (t)")
- **Ratio Check**: Kilos ÷ Tons ≈ 1000 ✓

---

### Columns REMOVED (98 columns)

| Index Range | Column Names (Examples) | Reason for Removal |
|-------------|-------------------------|-------------------|
| 2 | Master Bill of Lading Number | Not needed for analysis |
| 5 | Consignee | Redundant with address |
| 7-31 | Consignee details (City, State, Postal Code, Phone, Fax, Email, Profile, SPCIQ ID, MI Key, DUNS, Industry, Revenue, Employees, Market Cap, etc.) | Detailed fields not needed |
| 33 | Consignee Revenue | Not needed |
| 35-47 | More consignee details (Incorporation Year, Trade Roles, Original Format, HQ Address, DUNS, Domestic HQ, etc.) | Detailed fields not needed |
| 49-73 | Shipper details (Similar to consignee: City, State, Phone, Email, Profile, IDs, Industry, Revenue, etc.) | Detailed fields not needed |
| 75 | Shipper Revenue | Not needed |
| 77-89 | More shipper details (Similar structure to consignee) | Detailed fields not needed |
| 92, 95, 97, 99 | Various intermediate fields | Not core to analysis |
| 102, 106 | Various location/method fields (kept others, removed duplicates) | Redundant |
| 116, 117 | Container-related | Not needed |
| 119, 120, 121 | Various codes/fields | Not core |
| 124-129 | HS Code, Container data, Dangerous Goods | Some kept, some removed |

**Note:** Column 107 (Quantity) was **KEPT** for text splitting in Stage 09, then dropped after creating Qty and Pckg columns.

---

## Split Columns Detail

### Stage 09: Quantity Text Splitting (Column 107 → Qty + Pckg)

**Original Column:** Index 107 = "Quantity" (e.g., "3903 PCS", "25 COL", "1 BLK")

**Split Into:**
| New Column | Data Type | Description | Sample Values | Format |
|------------|-----------|-------------|---------------|--------|
| **Qty** | Integer | Numeric portion of quantity | 3903, 25, 1, 2, 1540 | Integer, no decimals |
| **Pckg** | Text | Package type/unit (alpha portion) | "PCS", "COL", "BLK", "PKG", "UNT" | Text/String |

**Transformation Examples:**
```
Original (Quantity) → Qty (integer) + Pckg (text)
"3903 PCS"          → 3903 + "PCS"
"25 COL"            → 25 + "COL"
"1 BLK"             → 1 + "BLK"
"2 PKG"             → 2 + "PKG"
"1540 PCS"          → 1540 + "PCS"
```

**Top 10 Package Types (Pckg values):**
1. UNT - Units (29%)
2. PCS - Pieces (15%)
3. PKG - Packages (9%)
4. BDL - Bundles (7%)
5. CAS - Cases (6%)
6. VEH - Vehicles (5%)
7. REL - Reels (4%)
8. LBK - Loose Bulk (4%)
9. BLK - Bulk (4%)
10. BOX - Boxes (4%)

**Data Quality:**
- Qty range: 1 to 512,800
- Qty mean: ~553
- All rows have valid Qty values (100% populated)
- Pckg format: 2-4 letter abbreviations

**Processing Notes:**
- Regex pattern: `([0-9.,]+)\s*([A-Za-z]+.*)`
- Numeric portion converted to integer (no decimals)
- Commas removed from numbers before conversion
- Original Quantity column dropped after split

---

## New Columns Added

**Summary:**
- **Split Columns:** 2 (Qty, Pckg) - replaced original Quantity column
- **Extracted Columns:** 3 (HS2, HS4, HS6) - new columns extracted from HS Code Desc.
- **Tracking Columns:** 12 - new empty columns for future use
- **Total New/Modified:** 17 columns

### Stage 10: HS Code Extraction (3 columns)

| Column Name | Data Type | Source | Transformation | Sample Values |
|-------------|-----------|--------|----------------|---------------|
| **HS2** | Text | HS Code Desc. | Extract first 2 digits | "14", "99", "10", "81" |
| **HS4** | Text | HS Code Desc. | Extract first 4 digits | "1431", "9985", "1071", "8164" |
| **HS6** | Text | HS Code Desc. | Extract first 6 digits | "143149", "998599", "107136", "816442" |

**Extraction Logic:**
```
HS Code format: "1431.49 XXXX description"
→ HS2 = "14"
→ HS4 = "1431"
→ HS6 = "143149"
```

### Stage 11: Tracking & Reporting Columns (12 columns)

| Column Name | Data Type | Purpose | Format/Values | Population |
|-------------|-----------|---------|---------------|------------|
| **RAW_REC_ID** | Text | Unique record identifier for compliance | PANV-YYYYMMDD-XXXXXXXX | 100% (auto-generated) |
| **Count** | Integer | Aggregation counter | Always = 1 | 100% |
| **Group** | Text | User-defined grouping | Empty (for future use) | 0% |
| **Commodity** | Text | Commodity classification | Empty (for future use) | 0% |
| **Cargo** | Text | Cargo type | Empty (for future use) | 0% |
| **Cargo Detail** | Text | Detailed cargo description | Empty (for future use) | 0% |
| **Report_One** | Text | Report category 1 | Empty (for future use) | 0% |
| **Report_Two** | Text | Report category 2 | Empty (for future use) | 0% |
| **Report_Three** | Text | Report category 3 | Empty (for future use) | 0% |
| **Report_Four** | Text | Report category 4 | Empty (for future use) | 0% |
| **Filter** | Text | Filter flag | Empty (for future use) | 0% |
| **Note** | Text | Notes/comments | Empty (for future use) | 0% |

**RAW_REC_ID Format:**
- Prefix: `PANV` (Panjiva identifier)
- Date: `YYYYMMDD` (processing date)
- Sequence: `XXXXXXXX` (8-digit sequential number)
- Example: `PANV-20260110-00000001`

---

## Data Type & Format Specifications

### Text Columns (Preserved Exactly)
| Column | Format Rule | Example |
|--------|-------------|---------|
| Bill of Lading Number | String, preserve leading zeros | "EOFF95198122401" |
| Voyage | String, preserve format | "22A", "2237D" |
| IMO | String, preserve IMO number | "9630755", "9327803" |
| HS2, HS4, HS6 | String, preserve leading zeros | "14", "1431", "143149" |
| RAW_REC_ID | String, fixed format | "PANV-20260110-00015626" |

### Numeric Columns (Formatted with Commas)
| Column | Original Type | Output Format | Example Input | Example Output |
|--------|---------------|---------------|---------------|----------------|
| Kilos | Float (kg) | String with commas, no decimals | 50617000.0 | "50,617,000" |
| Tons | Float (metric tons) | String with commas, no decimals | 50617.0 | "50,617" |
| Value | Float (USD) | String with commas, no decimals | 26321000.0 | "26,321,000" |
| Count | Integer | Integer | 1 | 1 |

**Formatting Rule:**
```python
# Numeric → Round → Integer → Format with commas
pd.to_numeric(column).round(0).astype(int).apply(lambda x: f"{x:,}")
```

### Date Columns
| Column | Input Format | Output Format | Example |
|--------|-------------|---------------|---------|
| Arrival Date | Various (YYYY-MM-DD, MM/DD/YYYY, etc.) | dd-MMM-yy | "28-Feb-23", "31-Dec-24" |

**Date Formatting:**
```python
pd.to_datetime(column).dt.strftime('%d-%b-%y')
```

---

## Column Usage Guide for Merging

### Primary Keys for Joining
When merging Panjiva data with other datasets, use these columns:

| Join Type | Primary Column(s) | Secondary Column(s) | Notes |
|-----------|-------------------|---------------------|-------|
| **By Shipment** | Bill of Lading Number | Arrival Date | Most unique identifier |
| **By Vessel** | Voyage | IMO | Voyage + IMO combination |
| **By Product** | HS Code Desc. | HS2, HS4, HS6 | HS codes for product matching |
| **By Location** | Origin (F) | Destination (D) | Location-based analysis |
| **By Company** | Consignee Global HQ | Shipper Global HQ | Company-level matching |
| **By Internal ID** | RAW_REC_ID | - | Unique compliance identifier |

### Column Matching for Other Datasets

If you have **other shipping/trade datasets** that need to merge with this Panjiva data:

#### Required Column Mappings (MUST MATCH):
```
Other Dataset Column Name → Panjiva Column Name

"Origin Country" → "Origin (F)"
"Destination Country/Region" → "Destination (D)"
"Port of Arrival" → "Port of Discharge (D)"
"Port of Departure" → "Port of Loading (F)"
"Vessel Voyage Number" → "Voyage"
"IMO Number" → "IMO"
"Weight KG" → "Kilos"
"Weight MT" or "Weight Tons" → "Tons"
"Declared Value USD" → "Value"
"HS Code" or "HS Code 2/4/6" → "HS2", "HS4", "HS6"
"BOL" or "Bill of Lading" → "Bill of Lading Number"
```

#### Data Type Conversions for Merging:
```python
# When preparing other datasets to merge:

# Text columns - convert to string, strip whitespace
df['origin'] = df['origin'].astype(str).str.strip()

# Numeric columns - remove commas, convert to numeric
df['kilos'] = pd.to_numeric(df['kilos'].str.replace(',', ''), errors='coerce')

# Date columns - convert to dd-MMM-yy format
df['date'] = pd.to_datetime(df['date']).dt.strftime('%d-%b-%y')
```

---

## Validation Checks

### Data Integrity Checks (Use These for Quality Assurance):

```python
import pandas as pd

df = pd.read_csv('panjiva_imports_master_20260110.csv')

# 1. RAW_REC_ID uniqueness
assert df['RAW_REC_ID'].is_unique, "RAW_REC_IDs must be unique!"

# 2. Kilos/Tons ratio (should be ~1000)
kilos = pd.to_numeric(df['Kilos'].str.replace(',', ''), errors='coerce').sum()
tons = pd.to_numeric(df['Tons'].str.replace(',', ''), errors='coerce').sum()
ratio = kilos / tons
assert 900 < ratio < 1100, f"Kilos/Tons ratio is {ratio}, should be ~1000!"

# 3. Date format
assert df['Arrival Date'].str.match(r'\d{2}-[A-Z][a-z]{2}-\d{2}').all(), "Date format incorrect!"

# 4. Count column
assert (df['Count'] == 1).all(), "Count column should all be 1!"

# 5. Column count
assert len(df.columns) == 47, f"Should have 47 columns, found {len(df.columns)}!"

print("All validation checks passed!")
```

---

## Quick Reference: Final Column List (47 columns)

```
 1. Bill of Lading Number        [TEXT]
 2. Bill of Lading Type           [TEXT]
 3. Arrival Date                  [DATE: dd-MMM-yy]
 4. Matching Fields               [TEXT]
 5. Consignee Address             [TEXT]
 6. Consignee Stock Tickers       [TEXT]
 7. Consignee Global HQ           [TEXT]
 8. Shipper Address               [TEXT]
 9. Shipper Stock Tickers         [TEXT]
10. Shipper Global HQ             [TEXT]
11. Notify Party                  [TEXT]
12. Notify Party SCAC             [TEXT]
13. Origin (F)                    [TEXT] ★ RENAMED
14. Destination (D)               [TEXT] ★ RENAMED
15. Port of Discharge (D)         [TEXT] ★ RENAMED
16. Port of Loading (F)           [TEXT] ★ RENAMED
17. Country of Country (F)        [TEXT] ★ RENAMED
18. Place of Receipt (F)          [TEXT] ★ RENAMED
19. Voyage                        [TEXT] ★ RENAMED
20. IMO                           [TEXT] ★ RENAMED
21. Is Containerized              [TEXT]
22. Measurement                   [TEXT]
23. Weight (kg)                   [TEXT] (original, kept)
24. Kilos                         [TEXT: ###,###] ★ RENAMED & FORMATTED
25. Tons                          [TEXT: ###,###] ★ RENAMED & FORMATTED
26. Value                         [TEXT: ###,###] ★ RENAMED & FORMATTED
27. FROB                          [TEXT]
28. Manifest Number               [TEXT]
29. Inbond Code                   [TEXT]
30. Number of Containers          [NUMERIC]
31. HS Code Desc.                 [TEXT] ★ RENAMED
32. Volume (Container TEU)        [NUMERIC]
33. HS2                           [TEXT] ★ NEW
34. HS4                           [TEXT] ★ NEW
35. HS6                           [TEXT] ★ NEW
36. RAW_REC_ID                    [TEXT: PANV-YYYYMMDD-XXXXXXXX] ★ NEW
37. Count                         [INTEGER: 1] ★ NEW
38. Group                         [TEXT: empty] ★ NEW
39. Commodity                     [TEXT: empty] ★ NEW
40. Cargo                         [TEXT: empty] ★ NEW
41. Cargo Detail                  [TEXT: empty] ★ NEW
42. Report_One                    [TEXT: empty] ★ NEW
43. Report_Two                    [TEXT: empty] ★ NEW
44. Report_Three                  [TEXT: empty] ★ NEW
45. Report_Four                   [TEXT: empty] ★ NEW
46. Filter                        [TEXT: empty] ★ NEW
47. Note                          [TEXT: empty] ★ NEW
```

---

## Change Log

### Version 1.2 (2026-01-10 16:00) - CORRECTED
- ✅ **CRITICAL FIX**: Corrected Kilos/Tons mapping
  - "Weight (kg)" → "Kilos" (was incorrectly "Weight (t)" → "Kilos")
  - "Weight (t)" → "Tons" (was incorrectly "Weight (Original Format)" → "Tons")
- ✅ Verified ratio: Kilos ÷ Tons = 1000.00 (exactly correct)

### Version 1.1 (2026-01-10 12:20)
- Fixed column renaming from index-based to name-based
- Corrected Voyage, IMO, Value column mappings

### Version 1.0 (2026-01-10 11:27)
- Initial version with column transformations

---

**Document Location:** `G:\My Drive\LLM\project_manifest\build_documentation\COLUMN_MAPPING_DICTIONARY.md`
**Script Location:** `C:\Users\wsd3\panjiva_stage00_preprocessing.py`
**Last Updated:** 2026-01-10 16:05:00
**Status:** ✅ VERIFIED & CORRECTED

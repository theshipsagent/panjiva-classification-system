# Import Pipeline Data Type & Transformation Audit
**Generated:** 2026-01-21

**Purpose:** Document data types, formats, and transformations through RAW → PREPROCESSED → CLASSIFIED

---

## Pipeline Summary

- **RAW Columns:** 146
- **PREPROCESSED Columns:** 51
- **CLASSIFIED Columns:** 58

- **Columns Dropped:** 131
- **Columns Added (Preprocessing):** 7
- **Columns Added (Classification):** 7

---

## Core Fields: RAW → PREPROCESSED → CLASSIFIED

These fields exist across all pipeline stages (with possible renames):

### Bill of Lading Number

**RAW Stage:**
- Column Name: `Bill of Lading Number`
- Data Type: `object`
- Null %: 0.0%
- Unique Values: 1000
- Samples: `GLNLPORCHERAFT3`, `MLCWGEOH10000010`

**PREPROCESSED Stage:**
- Column Name: `Bill of Lading Number`
- Data Type: `object`
- Null %: 0.0%
- Unique Values: 1000
- Samples: `FSHP2307091063`, `ACLUSA00974315`

**CLASSIFIED Stage:**
- Column Name: `Bill of Lading Number`
- Data Type: `object`
- Null %: 0.0%
- Unique Values: 1000
- Samples: `MAETVNL72460901`, `LDCSOA2024070501`

**Transformation Summary:**
- Column name unchanged

---

### Arrival Date

**RAW Stage:**
- Column Name: `Arrival Date`
- Data Type: `object`
- Null %: 0.0%
- Unique Values: 11
- Samples: `2023-12-31`, `2023-12-31`
- Format: Date format: YYYY-MM-DD

**PREPROCESSED Stage:**
- Column Name: `Arrival Date`
- Data Type: `object`
- Null %: 0.0%
- Unique Values: 327
- Samples: `2023-08-11`, `2023-10-08`

**CLASSIFIED Stage:**
- Column Name: `Arrival Date`
- Data Type: `object`
- Null %: 0.0%
- Unique Values: 2
- Samples: `2024-09-01`, `2024-09-01`

**Transformation Summary:**
- Column name unchanged

---

### Consignee

**RAW Stage:**
- Column Name: `Consignee`
- Data Type: `object`
- Null %: 9.0%
- Unique Values: 262
- Samples: `Fire Protection Service`, `Halliburton Energy Services Inc.`

**PREPROCESSED Stage:**
- Column Name: `Consignee`
- Data Type: `object`
- Null %: 17.6%
- Unique Values: 485
- Samples: `Dr. Jane Reynolds Dba Paws Veterina`, `Marinemax East Inc.`

**CLASSIFIED Stage:**
- Column Name: `Consignee`
- Data Type: `object`
- Null %: 9.4%
- Unique Values: 334
- Samples: `Exxonmobil Production Co.`, `Hlj International Trading Co.`

**Transformation Summary:**
- Column name unchanged

---

### Shipper

**RAW Stage:**
- Column Name: `Shipper`
- Data Type: `object`
- Null %: 23.0%
- Unique Values: 249
- Samples: `Viking Life Saving Equipment`, `Halliburton Guyana Inc.`

**PREPROCESSED Stage:**
- Column Name: `Shipper`
- Data Type: `object`
- Null %: 20.6%
- Unique Values: 436
- Samples: `Pet Products Associates`, `Saxdor Yachts Oy`

**CLASSIFIED Stage:**
- Column Name: `Shipper`
- Data Type: `object`
- Null %: 12.7%
- Unique Values: 231
- Samples: `Sarnia Chemical Plant Imperial`, `Suncor Energy Marketing Inc.`

**Transformation Summary:**
- Column name unchanged

---

### Carrier

**RAW Stage:**
- Column Name: `Carrier`
- Data Type: `object`
- Null %: 0.0%
- Unique Values: 63
- Samples: `GLNL - Galene Logistics Inc`, `MLCW - Mclean Cargo Specialists (Division Of Crane Worldwide Logistics Llc)`

**PREPROCESSED Stage:**
- Column Name: `Carrier`
- Data Type: `object`
- Null %: 0.0%
- Unique Values: 160
- Samples: `FSHP - Formel, Stevenson Freight Services Llc`, `ACLU - Atlantic Container Line Ab`

**CLASSIFIED Stage:**
- Column Name: `Carrier`
- Data Type: `object`
- Null %: 0.0%
- Unique Values: 109
- Samples: `MAET - Maersk Tankers`, `LDCS - Louis Dreyfus Company Freight Asia Pte Ltd`

**Transformation Summary:**
- Column name unchanged

---

### Port of Unlading

**RAW Stage:**
- Column Name: `Port of Unlading`
- Data Type: `object`
- Null %: 0.0%
- Unique Values: 19
- Samples: `Houston, Houston, Texas`, `Houston, Houston, Texas`

**PREPROCESSED Stage:**
- Column Name: `Port of Discharge (D)` ⚠️ **RENAMED** from `Port of Unlading`
- Data Type: `object`
- Null %: 0.0%
- Unique Values: 70
- Samples: `Cyril E King Airport, Charlotte Amalie, Virgin Islands`, `Port of Virginia, Norfolk, Virginia`

**CLASSIFIED Stage:**
- Column Name: `Port of Discharge (D)`
- Data Type: `object`
- Null %: 0.0%
- Unique Values: 52
- Samples: `Baton Rouge (BTR) Airport, Baton Rouge, Louisiana`, `Port of Gramercy, Gramercy, Louisiana`

**Transformation Summary:**
- Column renamed: `Port of Unlading` → `Port of Discharge (D)`

---

### Port of Lading

**RAW Stage:**
- Column Name: `Port of Lading`
- Data Type: `object`
- Null %: 0.0%
- Unique Values: 127
- Samples: `Altamira, Mexico`, `Georgetown, Guyana`

**PREPROCESSED Stage:**
- Column Name: `Port of Loading (F)` ⚠️ **RENAMED** from `Port of Lading`
- Data Type: `object`
- Null %: 0.0%
- Unique Values: 196
- Samples: `Charlotte Amalie, St. Th, Virgin Islands (U.S.)`, `Hamburg, Germany`

**CLASSIFIED Stage:**
- Column Name: `Port of Loading (F)`
- Data Type: `object`
- Null %: 0.0%
- Unique Values: 109
- Samples: `Sarnia, Ont, Canada`, `Nha Trang, Vietnam`

**Transformation Summary:**
- Column renamed: `Port of Lading` → `Port of Loading (F)`

---

### Vessel

**RAW Stage:**
- Column Name: `Vessel`
- Data Type: `object`
- Null %: 0.0%
- Unique Values: 149
- Samples: `PORTO CHELI`, `INDUSTRIAL ACE`

**PREPROCESSED Stage:**
- Column Name: `Vessel`
- Data Type: `object`
- Null %: 0.0%
- Unique Values: 589
- Samples: `BONNIE G`, `ATLANTIC SUN`

**CLASSIFIED Stage:**
- Column Name: `Vessel`
- Data Type: `object`
- Null %: 0.0%
- Unique Values: 142
- Samples: `YM SATURN`, `OCEAN AZURE`

**Transformation Summary:**
- Column name unchanged

---

### Vessel IMO

**RAW Stage:**
- Column Name: `Vessel IMO`
- Data Type: `float64`
- Null %: 52.3%
- Unique Values: 63
- Samples: `9563706.0`, `9438573.0`

**PREPROCESSED Stage:**
- Column Name: `IMO` ⚠️ **RENAMED** from `Vessel IMO`
- Data Type: `float64`
- Null %: 31.8%
- Unique Values: 373
- Samples: `8023864.0`, `9670614.0`

**CLASSIFIED Stage:**
- Column Name: `IMO`
- Data Type: `float64`
- Null %: 50.7%
- Unique Values: 53
- Samples: `9362138.0`, `9960150.0`

**Transformation Summary:**
- Column renamed: `Vessel IMO` → `IMO`

---

### Goods Shipped

**RAW Stage:**
- Column Name: `Goods Shipped`
- Data Type: `object`
- Null %: 0.7%
- Unique Values: 559
- Samples: `LIFE RAFTS FOR EXCHANGE`, `OILS AND GAS EQUIPMENT`

**PREPROCESSED Stage:**
- Column Name: `Goods Shipped`
- Data Type: `object`
- Null %: 11.6%
- Unique Values: 787
- Samples: `SEALED PLTS DOG & CAT FOOD`, `1 X NEW MOTORBOAT SAXDOR 320 GTO, WITH HULL ID NUMBER SXF32351H324, 2 X MERCURY V8 AMS 300 ENGINES WITH NUMBERS 3B410242 AND 3B416090, SHRINKWRAPPED AND ON SHIPPING CRADLE. HS 890399`

**CLASSIFIED Stage:**
- Column Name: `Goods Shipped`
- Data Type: `object`
- Null %: 4.6%
- Unique Values: 811
- Samples: `BENZENE AND MIXTURES HAVING 10 BENZENE OR MOR MORE`, `PORTLAND CEMENT ASTM C 150/C150M-20 TYPE I/II IN BULK`

**Transformation Summary:**
- Column name unchanged

---

### HS Code

**RAW Stage:**
- Column Name: `HS Code`
- Data Type: `object`
- Null %: 0.4%
- Unique Values: 175
- Samples: `Classified: 8907.10`, `Classified: 8703.90`
- Format: Code/classification

**PREPROCESSED Stage:**
- Column Name: `HS Code Desc.` ⚠️ **RENAMED** from `HS Code`
- Data Type: `object`
- Null %: 0.9%
- Unique Values: 369
- Samples: `Classified: 2309.10`, `Parsed: 8903.99`

**CLASSIFIED Stage:**
- Column Name: `HS Code Desc.`
- Data Type: `object`
- Null %: 0.2%
- Unique Values: 280
- Samples: `Classified: 8703.90`, `Classified: 2523.21`

**Transformation Summary:**
- Column renamed: `HS Code` → `HS Code Desc.`

---

### Weight (kg)

**RAW Stage:**
- Column Name: `Weight (kg)`
- Data Type: `float64`
- Null %: 0.0%
- Unique Values: 909
- Samples: `750.0`, `1333.0`
- Format: Numeric: Weight/tonnage

**PREPROCESSED Stage:**
- Column Name: `Kilos` ⚠️ **RENAMED** from `Weight (kg)`
- Data Type: `float64`
- Null %: 0.0%
- Unique Values: 887
- Samples: `453.59238`, `4600.0`

**CLASSIFIED Stage:**
- Column Name: `Kilos`
- Data Type: `float64`
- Null %: 0.0%
- Unique Values: 806
- Samples: `8117803.0`, `51500000.0`

**Transformation Summary:**
- Column renamed: `Weight (kg)` → `Kilos`

---

### Weight (t)

**RAW Stage:**
- Column Name: `Weight (t)`
- Data Type: `float64`
- Null %: 0.0%
- Unique Values: 892
- Samples: `0.75`, `1.33`
- Format: Numeric: Weight/tonnage

**PREPROCESSED Stage:**
- Column Name: `Tons` ⚠️ **RENAMED** from `Weight (t)`
- Data Type: `float64`
- Null %: 0.0%
- Unique Values: 809
- Samples: `0.45`, `4.6`

**CLASSIFIED Stage:**
- Column Name: `Tons`
- Data Type: `float64`
- Null %: 0.0%
- Unique Values: 716
- Samples: `8117.8`, `51500.0`

**Transformation Summary:**
- Column renamed: `Weight (t)` → `Tons`

---

### Value of Goods (USD)

**RAW Stage:**
- Column Name: `Value of Goods (USD)`
- Data Type: `float64`
- Null %: 0.4%
- Unique Values: 823
- Samples: `12000.0`, `20000.0`
- Format: Numeric: Monetary value

**PREPROCESSED Stage:**
- Column Name: `Value` ⚠️ **RENAMED** from `Value of Goods (USD)`
- Data Type: `float64`
- Null %: 1.1%
- Unique Values: 794
- Samples: `2100.0`, `97000.0`

**CLASSIFIED Stage:**
- Column Name: `Value`
- Data Type: `float64`
- Null %: 1.7%
- Unique Values: 698
- Samples: `128724000.0`, `4069000.0`

**Transformation Summary:**
- Column renamed: `Value of Goods (USD)` → `Value`

---

### Measurement

**RAW Stage:**
- Column Name: `Measurement`
- Data Type: `object`
- Null %: 0.0%
- Unique Values: 108
- Samples: ` `, ` CM`

**PREPROCESSED Stage:**
- Column Name: `Measurement`
- Data Type: `object`
- Null %: 0.0%
- Unique Values: 319
- Samples: ` CF`, `105 X`

**CLASSIFIED Stage:**
- Column Name: `Measurement`
- Data Type: `object`
- Null %: 0.0%
- Unique Values: 183
- Samples: ` `, ` `

**Transformation Summary:**
- Column name unchanged

---

## Fields Added During Preprocessing

These fields are derived/engineered during preprocessing:

### Port_Consolidated

**Source:** Derived during preprocessing (not in RAW data)

**PREPROCESSED Stage:**
- Data Type: `object`
- Null %: 0.1%
- Unique Values: 28
- Samples: `Virgin Islands`, `Hampton Roads`

**Derivation Logic:** Standardized port name from `Port of Unlading`

---

### Port_Code

**Source:** Derived during preprocessing (not in RAW data)

**PREPROCESSED Stage:**
- Data Type: `float64`
- Null %: 0.1%
- Unique Values: 69
- Samples: `5101.0`, `1401.0`

**Derivation Logic:** Mapped port code from port name

---

### HS2

**Source:** Derived during preprocessing (not in RAW data)

**PREPROCESSED Stage:**
- Data Type: `float64`
- Null %: 0.9%
- Unique Values: 51
- Samples: `23.0`, `89.0`

**Derivation Logic:** Extracted from `HS Code` field (first 2 digits)

---

### HS4

**Source:** Derived during preprocessing (not in RAW data)

**PREPROCESSED Stage:**
- Data Type: `float64`
- Null %: 0.9%
- Unique Values: 200
- Samples: `2309.0`, `8903.0`

**Derivation Logic:** Extracted from `HS Code` field (first 4 digits)

---

### HS6

**Source:** Derived during preprocessing (not in RAW data)

**PREPROCESSED Stage:**
- Data Type: `float64`
- Null %: 0.9%
- Unique Values: 320
- Samples: `230910.0`, `890399.0`

**Derivation Logic:** Extracted from `HS Code` field (first 6 digits)

---

### Pckg

**Source:** Derived during preprocessing (not in RAW data)

**PREPROCESSED Stage:**
- Data Type: `object`
- Null %: 0.0%
- Unique Values: 32
- Samples: `PKG`, `PCS`

**Derivation Logic:** Package type code (extracted from description or mapping)

---

### RAW_REC_ID

**Source:** Derived during preprocessing (not in RAW data)

**PREPROCESSED Stage:**
- Data Type: `object`
- Null %: 0.0%
- Unique Values: 1000
- Samples: `PANV-20260112-00106392`, `PANV-20260112-00439514`

**Derivation Logic:** Unique record identifier (auto-generated)

---

## Fields Added During Classification

These fields are created during the classification phase:

### Vessel_Type_Simple

**Source:** Generated during classification

**CLASSIFIED Stage:**
- Data Type: `object`
- Null %: 46.9%
- Unique Values: 6
- Samples: `Tanker`, `Bulk Carrier`

**Purpose:** Simplified vessel type derived from ship registry lookup

---

### Group_Locked

**Source:** Generated during classification

**CLASSIFIED Stage:**
- Data Type: `bool`
- Null %: 0.0%
- Unique Values: 2
- Samples: `True`, `True`

**Purpose:** Boolean flag indicating if this taxonomy level is locked from further changes

---

### Commodity_Locked

**Source:** Generated during classification

**CLASSIFIED Stage:**
- Data Type: `bool`
- Null %: 0.0%
- Unique Values: 2
- Samples: `False`, `True`

**Purpose:** Boolean flag indicating if this taxonomy level is locked from further changes

---

### Cargo_Locked

**Source:** Generated during classification

**CLASSIFIED Stage:**
- Data Type: `bool`
- Null %: 0.0%
- Unique Values: 2
- Samples: `False`, `True`

**Purpose:** Boolean flag indicating if this taxonomy level is locked from further changes

---

### Cargo_Detail_Locked

**Source:** Generated during classification

**CLASSIFIED Stage:**
- Data Type: `bool`
- Null %: 0.0%
- Unique Values: 2
- Samples: `False`, `True`

**Purpose:** Boolean flag indicating if this taxonomy level is locked from further changes

---

### Classified_Phase

**Source:** Generated during classification

**CLASSIFIED Stage:**
- Data Type: `int64`
- Null %: 0.0%
- Unique Values: 4
- Samples: `1`, `3`

**Purpose:** Phase number (1-10) indicating which classification phase matched this record

---

### Last_Rule_ID

**Source:** Generated during classification

**CLASSIFIED Stage:**
- Data Type: `object`
- Null %: 0.0%
- Unique Values: 99
- Samples: `CARR-MAET`, `HS4-2523`

**Purpose:** Rule ID from dictionary that classified this record (for audit trail)

---

## Key Transformations Summary

### Column Renames (RAW → PREPROCESSED)

| RAW Column | PREPROCESSED Column | Reason |
|------------|---------------------|--------|
| `Weight (kg)` | `Kilos` | Shortened name |
| `Weight (t)` | `Tons` | Shortened name |
| `Value of Goods (USD)` | `Value` | Shortened name, USD implied |
| `Vessel IMO` | `IMO` | Shortened name |
| `Vessel Voyage ID` | `Voyage` | Shortened name |
| `HS Code` | `HS Code Desc.` | Clarified as description field |
| `Port of Unlading` | `Port of Discharge (D)` | Clarified as destination port |
| `Port of Lading` | `Port of Loading (F)` | Clarified as foreign/origin port |
| `Shipment Origin` | `Origin (F)` | Marked as foreign |
| `Shipment Destination` | `Destination (D)` | Marked as domestic |

### Data Type Changes

| Field | RAW Type | PREPROCESSED Type | Notes |
|-------|----------|-------------------|-------|

### Value Transformations

- **HS Codes:** Extracted into HS2 (2-digit), HS4 (4-digit), HS6 (6-digit) fields
- **Port Names:** Standardized and mapped to port codes
- **Carrier Names:** Extracted SCAC code from full carrier string
- **Weight:** Preserved in original format plus converted to Kilos/Tons
- **Classification:** Added Group/Commodity/Cargo/Cargo Detail taxonomy

---

## Data Integrity Checks

### Critical Fields - Non-Null Rates

- **Bill of Lading Number:** 100.0% populated ✓ GOOD
- **Arrival Date:** 100.0% populated ✓ GOOD
- **Tons:** 100.0% populated ✓ GOOD
- **Goods Shipped:** 88.4% populated ⚠ WARNING

---

*End of Data Type Audit*

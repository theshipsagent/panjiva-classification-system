# Party Harmonization Task

**Purpose**: Harmonize party names (Shipper, Consignee, Notify Party) to standardized entities for improved cargo classification and entity-based analysis.

**Status**: Recreated from documentation (2026-02-09)
**Original Work**: 2026-02-05 to 2026-02-06
**Latest Dictionary**: v1.3.0 (163 entities)

---

## Overview

Party harmonization standardizes messy party names from Panjiva data to canonical entity names with business profiles. This enables:

1. **Entity-based cargo classification** - Lock classifications when known single-product companies ship cargo
2. **Network analysis** - Track relationships between shippers, consignees, and intermediaries
3. **Company profiling** - Identify major players by commodity/trade lane
4. **Origin inference** - Use entity location to fill missing origin data

**Example**:
```
Raw Shipper Name: "NUH CIMENTO SANAYI VE TIC A.S."
Harmonized: "Nuh Cimento"
Entity_ID: "NUH-CIMENTO-001"
Entity_Type: "Cement"
Match_Type: "Exact"
```

---

## Dictionary

**Location**: `01_DICTIONARIES/01.06_parties/party_harmonization_master_v1.3.0.csv`

**Schema** (10 columns):
- `Entity_ID`: Unique identifier (e.g., "NUH-CIMENTO-001")
- `Canonical_Name`: Standardized company name (e.g., "Nuh Cimento")
- `Entity_Type`: Business sector (Oil/Gas, Cement, Steel, etc.)
- `Match_Keywords`: Keywords for matching (pipe-separated)
- `Match_Strategy`: "EXACT" or "CONTAINS" or "FUZZY"
- `Country`: Primary country of operations
- `Notes`: Additional context
- `Confidence`: Match confidence level (95-99%)
- `Date_Added`: When entity was added
- `Last_Modified`: Last update

**Current Coverage** (v1.3.0):
- **163 entities** across 11 sectors
- **Cement/Aggregates**: 19 entities (99% confidence)
- **Oil & Gas**: 23 entities (95-99% confidence)
- **Steel**: 11 entities (85-95% confidence)
- **Automotive**: 9 entities (90% confidence)
- **Mining**: 8 entities (95-99% confidence)
- **Chemicals**: 13 entities (75-95% confidence)
- **Others**: 80 entities (various)

**Projected Coverage**: 68-72% of consignee tonnage (414.7M tons in 2024)

---

## Scripts

### 1. `harmonize_party_names_v1.0.0.py` (MAIN SCRIPT)

**Purpose**: Match raw party names to harmonized entities and add standardized columns.

**Input**: `panjiva_imports_{year}_AUTHORITATIVE_v2.0.0.csv`
**Output**: `panjiva_imports_{year}_HARMONIZED_v1.0.0.csv`

**Process**:
1. Load preprocessed data
2. Load party harmonization dictionary
3. For each party role (Shipper, Consignee, Notify Party):
   - Match raw name against dictionary keywords
   - Apply match strategy (EXACT, CONTAINS, FUZZY)
   - Add harmonized columns: *_Harmonized, *_Entity_ID, *_Match_Type
4. Generate validation report with coverage statistics
5. Save harmonized CSV

**New Columns Added** (9 total):
- `Shipper_Harmonized`, `Shipper_Entity_ID`, `Shipper_Match_Type`
- `Consignee_Harmonized`, `Consignee_Entity_ID`, `Consignee_Match_Type`
- `Notify Party_Harmonized`, `Notify Party_Entity_ID`, `Notify Party_Match_Type`

**Runtime**: ~10 minutes for 450K records

---

### 2. `infer_parties_from_trade_lanes_v1.0.0.py` (INFERENCE)

**Purpose**: Use trade lane patterns to infer missing party information.

**Logic**:
- If Shipper is blank but origin port + HS4 code match known patterns → infer likely shipper
- Example: Origin=Brazil, Port=Tubarao, HS4=2601 (iron ore) → likely shipper=Vale

**Use Case**: Fill gaps in incomplete records using trade lane fingerprints

---

### 3. `refine_cement_with_entities_v1.0.0.py` (SECTOR-SPECIFIC)

**Purpose**: Use entity harmonization to refine cement classification.

**Logic**:
- If Shipper_Entity_ID matches known cement producer → lock cargo as Cement
- Example: Shipper_Entity_ID = "NUH-CIMENTO-001" → Cargo = Cement (99% confidence)

**Integration**: Creates entity-based classification rules for cargo dictionary

---

### 4. `validate_harmonization_v1.0.0.py` (VALIDATION)

**Purpose**: Generate validation reports and coverage statistics.

**Reports**:
- Match rate by party role (Shipper, Consignee, Notify)
- Tonnage coverage by entity
- Top unmatched party names
- Entity usage frequency

**Output**: `harmonization_validation_report_{timestamp}.txt`

---

## Workflow

### Initial Harmonization (Full Year)

```bash
cd "G:\My Drive\LLM\project_manifest\05_TASKS\05.01_party_harmonization"

# Step 1: Harmonize party names
python harmonize_party_names_v1.0.0.py --year 2024

# Step 2: Validate results
python validate_harmonization_v1.0.0.py --year 2024

# Step 3: Infer missing parties from trade lanes (optional)
python infer_parties_from_trade_lanes_v1.0.0.py --year 2024

# Step 4: Refine cement classification with entities (optional)
python refine_cement_with_entities_v1.0.0.py --year 2024
```

### Output Files

```
00_DATA/00.03_MATCHED/
├── panjiva_imports_2024_HARMONIZED_v1.0.0.csv (449K records, 68 columns)
└── harmonization_validation_report_20260206_150329.txt

03_DOCUMENTATION/03.04_summaries/
├── entity_summary_records_tonnage_20260206_0153.csv
└── unmatched_parties_v1.1.0_analysis_20260206_0119.csv
```

---

## Integration with Cargo Classification

**Not currently integrated** - Party harmonization creates a separate harmonized CSV file. The cargo classification pipeline (stages 1-7) does NOT use harmonized party columns.

**Future Integration**: Add entity-based rules to cargo classification dictionary:

**Example Entity Rule**:
```csv
Rule_ID: ENTITY-NUH-CEMENT-001
Phase: 1
Tier: 1
Required_Entity_ID: NUH-CIMENTO-001
HS4: 2523
Group: Dry Bulk
Commodity: Cement
Cargo: Cement
Cargo_Detail: Cement - Turkish Import
Lock_Group: TRUE
Lock_Commodity: TRUE
Lock_Cargo: TRUE
Lock_Cargo_Detail: TRUE
Note: Nuh Cimento only produces cement in Turkey - firm rule
Accuracy_Est: 99%
```

**Integration Plan**: See `03_DOCUMENTATION/03.04_summaries/PARTY_HARMONIZATION_TO_CARGO_CLASSIFICATION_INTEGRATION.md`

---

## Dictionary Maintenance

### Adding New Entities

1. Identify high-tonnage unmatched party names in validation reports
2. Research company (what do they make/ship?)
3. Add to dictionary with appropriate Match_Keywords
4. Test on small sample before full run
5. Increment version number

**Example**: Adding "Yamana Cement" (new Turkish cement producer)

```csv
Entity_ID: YAMANA-001
Canonical_Name: Yamana Cement
Entity_Type: Cement
Match_Keywords: YAMANA|YAMANA CIMENTO
Match_Strategy: CONTAINS
Country: Turkey
Notes: Turkish cement producer
Confidence: 99%
Date_Added: 2026-02-09
Last_Modified: 2026-02-09
```

### Version History

- **v1.0.0** (2026-02-05): Initial 36 entities (cement, oil, steel)
- **v1.1.0** (2026-02-05): Added 47 entities (mining, automotive, chemicals) → 83 total
- **v1.2.0** (2026-02-06): Added 43 entities (aggregates, logistics) → 126 total
- **v1.3.0** (2026-02-06): Added 37 entities (fertilizer, pulp, aluminum) → 163 total

**Projected v1.4.0**: Add 50-75 entities to reach 75% coverage target

---

## Performance Metrics

### v1.0.0 Results (2024 Data)

**Match Rates** (by records):
- Shipper: 24.3% matched (109,120 / 449,233)
- Consignee: 42.8% matched (192,271 / 449,233)
- Notify Party: 18.6% matched (83,557 / 449,233)

**Tonnage Coverage**:
- Consignee: 57.3% (414.7M / 723.9M tons)
- Shipper: 35.2% (254.8M tons)
- Notify Party: 22.1% (160.0M tons)

**Top Entities by Tonnage**:
1. EP Petroecuador: 42.3M tons (crude oil)
2. Vale: 38.7M tons (iron ore)
3. Valero: 35.2M tons (crude oil refiner)
4. Marathon Petroleum: 28.9M tons (crude oil refiner)
5. SOMO: 24.6M tons (Iraqi crude oil)

---

## Known Issues

1. **Multiple entity matches** - Some party names match multiple entities (e.g., "TOTAL" could be TotalEnergies or Total Specialties)
   - **Mitigation**: Use longest match first, add context from HS codes

2. **Subsidiary variations** - Parent companies have many subsidiaries with different names
   - **Example**: "Cemex USA", "Cemex Aggregates", "Cemex Trading" all = CEMEX-001
   - **Solution**: Add all variations to Match_Keywords

3. **Country-specific suffixes** - Same company, different countries
   - **Example**: "Lafarge Canada", "Lafarge Emirates", "Lafarge North America"
   - **Solution**: Create separate entity IDs per country/region

4. **Logistics intermediaries** - Freight forwarders/customs brokers are not actual shippers
   - **Examples**: "Coppersmith Global Logistics", "Blue Water Industries"
   - **Solution**: Flag as logistics entities, exclude from cargo classification

---

## Next Steps

### Phase 1: Restore Functionality (Complete)
- ✅ Recreate harmonization scripts from documentation
- ✅ Create task folder structure
- ✅ Document process and integration

### Phase 2: Test & Validate
- Run harmonization on 2024 data
- Compare results to original v1.0.0 harmonized CSV
- Validate match rates and tonnage coverage

### Phase 3: Expand Dictionary
- Add 50-75 new entities to reach v1.4.0
- Target unmatched high-tonnage parties
- Increase coverage from 68% → 75%

### Phase 4: Integration
- Add entity-based rules to cargo classification dictionary v3.7.0
- Modify classification scripts to check entity columns
- Test entity-locked rules on 15K sample

---

## File Paths

**Scripts**: `G:\My Drive\LLM\project_manifest\05_TASKS\05.01_party_harmonization\`

**Dictionary**: `G:\My Drive\LLM\project_manifest\01_DICTIONARIES\01.06_parties\party_harmonization_master_v1.3.0.csv`

**Input Data**: `G:\My Drive\LLM\project_manifest\00_DATA\00.02_PREPROCESSED\panjiva_imports_{year}_AUTHORITATIVE_v2.0.0.csv`

**Output Data**: `G:\My Drive\LLM\project_manifest\00_DATA\00.03_MATCHED\panjiva_imports_{year}_HARMONIZED_v1.0.0.csv`

**Documentation**: `G:\My Drive\LLM\project_manifest\03_DOCUMENTATION\03.04_summaries\PARTY_HARMONIZATION_*.md`

---

**Status**: Scripts recreated from documentation
**Ready for**: Testing and validation
**Author**: WSD3 / Claude Code
**Date**: 2026-02-09

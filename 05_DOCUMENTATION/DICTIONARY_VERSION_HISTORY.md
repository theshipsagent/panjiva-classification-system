# Dictionary Version History

## Version 3.6.0 - 2026-01-14 18:30

**Major Release: Refined Keywords & Comprehensive Commodity Coverage**

### Summary
- **668 total rules** (+95 from v3.4.0, +16.6%)
- **218 new user-edited rules** across 31 HS2 chapters
- **100% test classification rate** on 15K sample
- **Break-Bulk group eliminated** - replaced with reliable Dry Bulk/Liquid Bulk/Liquid Gas

### New Features

#### 1. Refined Keyword Strategy
- **Key_Phrases**: Multi-word phrases requiring exact matches (e.g., "CRUDE OIL", "PIG IRON")
- **Primary_Keywords**: Standalone product terms (e.g., "CEMENT", "STEEL")
- **Descriptor_Keywords**: Modifiers and qualifiers (e.g., "HOT", "ROLLED", "PRIME")
- **Match_Strategy**: PHRASE_REQUIRED vs PRIMARY_SUFFICIENT

#### 2. Comprehensive Coverage (218 New Rules)
- **HS27 Mineral Fuels** (13): Crude Oil, Petroleum Products, Coal, LNG
- **HS28 Inorganic Chemicals** (42): Caustic Soda, Ammonia, Fertilizers, Alumina
- **HS29 Organic Chemicals** (40): Alcohols, Ketones, Benzene, Acids
- **HS72-73 Iron & Steel** (40): Pig Iron, Flat Rolled, Long Products, Semi-Finished
- **HS76 Aluminum** (16): Unwrought, Plates, Bars, Wire, Foil
- **HS74 Copper** (2): Cathodes, Mattes
- **HS78-79 Lead & Zinc** (8): Unwrought, Concentrates
- **HS25 Stone/Earth** (9): Salt, Cement, Aggregates, Gypsum
- **HS31 Fertilizers** (3): Nitrogen, Potash, Compounds
- **HS26 Ores** (5): Bauxite, Iron Ore, Titanium Ore
- **Agricultural Products** (14): Grain, Oils, Coffee, Sugar, Rubber
- **Forestry** (6): Lumber, Paper, Wood Pulp
- **Construction** (17): Cement, Aggregates, Gypsum, Slag
- **General Cargo** (7): Vehicles, Machinery

### Test Results (15K Sample)

| Metric | v3.4.0 | v3.6.0 | Change |
|--------|--------|--------|--------|
| Total Rules | 573 | 668 | +95 (+16.6%) |
| Phase 3 Rules | 0 | 218 | +218 |
| Phase 3 Classifications | 0 | 1,443 | +1,443 (9.6%) |
| Dry Bulk % | 11.4% | 95.7% | +84.3 points |
| Break-Bulk % | 82.0% | 0.0% | -82.0 points |
| Classification Rate | 100% | 100% | Maintained |

### Breaking Changes
- **Break-Bulk group eliminated**: All records reclassified to Dry Bulk, Liquid Bulk, or Liquid Gas
- **Keyword columns changed**: Added Key_Phrases, Primary_Keywords, Descriptor_Keywords, Match_Strategy
- **Old Keywords column**: Still present but deprecated, will be removed in v4.0

### Files Changed
- `03_DICTIONARIES/03.01_cargo_classification/cargo_classification_dictionary_v3.6.0_20260114_1830.csv`
- `05_DOCUMENTATION/DICTIONARY_V3.6.0_SUMMARY.md`
- `05_DOCUMENTATION/DICTIONARY_V3.6.0_TEST_RESULTS.md`

### Classification Scripts
- Updated keyword matching logic in `classify_15k_sample_v3.6.0.py`
- Added `check_keyword_match()` function supporting refined strategy

### Contributors
- WSD3 (User) - Manual classification of 218 specialized rules
- Claude Code - Script development, testing, documentation

---



## Version 3.6.0 - 2026-01-14 18:30

**Major Release: Refined Keywords & Comprehensive Commodity Coverage**

### Summary
- **668 total rules** (+95 from v3.4.0, +16.6%)
- **218 new user-edited rules** across 31 HS2 chapters
- **100% test classification rate** on 15K sample
- **Break-Bulk group eliminated** - replaced with reliable Dry Bulk/Liquid Bulk/Liquid Gas

### New Features

#### 1. Refined Keyword Strategy
- **Key_Phrases**: Multi-word phrases requiring exact matches (e.g., "CRUDE OIL", "PIG IRON")
- **Primary_Keywords**: Standalone product terms (e.g., "CEMENT", "STEEL")
- **Descriptor_Keywords**: Modifiers and qualifiers (e.g., "HOT", "ROLLED", "PRIME")
- **Match_Strategy**: PHRASE_REQUIRED vs PRIMARY_SUFFICIENT

#### 2. Comprehensive Coverage (218 New Rules)
- **HS27 Mineral Fuels** (13): Crude Oil, Petroleum Products, Coal, LNG
- **HS28 Inorganic Chemicals** (42): Caustic Soda, Ammonia, Fertilizers, Alumina
- **HS29 Organic Chemicals** (40): Alcohols, Ketones, Benzene, Acids
- **HS72-73 Iron & Steel** (40): Pig Iron, Flat Rolled, Long Products, Semi-Finished
- **HS76 Aluminum** (16): Unwrought, Plates, Bars, Wire, Foil
- **HS74 Copper** (2): Cathodes, Mattes
- **HS78-79 Lead & Zinc** (8): Unwrought, Concentrates
- **HS25 Stone/Earth** (9): Salt, Cement, Aggregates, Gypsum
- **HS31 Fertilizers** (3): Nitrogen, Potash, Compounds
- **HS26 Ores** (5): Bauxite, Iron Ore, Titanium Ore
- **Agricultural Products** (14): Grain, Oils, Coffee, Sugar, Rubber
- **Forestry** (6): Lumber, Paper, Wood Pulp
- **Construction** (17): Cement, Aggregates, Gypsum, Slag
- **General Cargo** (7): Vehicles, Machinery

### Test Results (15K Sample)

| Metric | v3.4.0 | v3.6.0 | Change |
|--------|--------|--------|--------|
| Total Rules | 573 | 668 | +95 (+16.6%) |
| Phase 3 Rules | 0 | 218 | +218 |
| Phase 3 Classifications | 0 | 1,443 | +1,443 (9.6%) |
| Dry Bulk % | 11.4% | 95.7% | +84.3 points |
| Break-Bulk % | 82.0% | 0.0% | -82.0 points |
| Classification Rate | 100% | 100% | Maintained |

### Breaking Changes
- **Break-Bulk group eliminated**: All records reclassified to Dry Bulk, Liquid Bulk, or Liquid Gas
- **Keyword columns changed**: Added Key_Phrases, Primary_Keywords, Descriptor_Keywords, Match_Strategy
- **Old Keywords column**: Still present but deprecated, will be removed in v4.0

### Files Changed
- `03_DICTIONARIES/03.01_cargo_classification/cargo_classification_dictionary_v3.6.0_20260114_1830.csv`
- `05_DOCUMENTATION/DICTIONARY_V3.6.0_SUMMARY.md`
- `05_DOCUMENTATION/DICTIONARY_V3.6.0_TEST_RESULTS.md`

### Classification Scripts
- Updated keyword matching logic in `classify_15k_sample_v3.6.0.py`
- Added `check_keyword_match()` function supporting refined strategy

### Contributors
- WSD3 (User) - Manual classification of 218 specialized rules
- Claude Code - Script development, testing, documentation

---


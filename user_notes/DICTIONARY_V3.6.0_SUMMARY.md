# Cargo Classification Dictionary v3.6.0 DRAFT
## Created: 2026-01-14

---

## Summary

**Total Rules**: 668
**Original Rules (v3.5.0)**: 450
**New User-Edited Rules**: 218
**Overlapping HS4 Codes Replaced**: 123

---

## Breakdown by Classification Group

| Group | Rules | Percentage |
|-------|-------|------------|
| Dry Bulk | 554 | 83% |
| Liquid Bulk | 111 | 17% |
| Liquid Gas | 3 | <1% |

---

## Breakdown by Phase

| Phase | Rules | Description |
|-------|-------|-------------|
| Phase 1 | 65 | High confidence matches |
| Phase 2 | 51 | HS4 broad strokes |
| Phase 3 | 263 | User-edited specialized rules |
| Phase 5 | 1 | Override rules |
| Phase 6 | 288 | Fallback rules |

---

## New User-Edited Coverage (218 Rules across 31 HS2 Chapters)

### Energy & Fuels (13 rules)
- **HS27** (13): Crude Oil, Refined Petroleum, Coal, Petcoke, LNG, Bitumen

### Chemicals (86 rules)
- **HS28** (42): Inorganic Chemicals - Caustic Soda, Ammonia, Alumina, Phosphates, Titanium Oxides
- **HS29** (40): Organic Chemicals - Alcohols, Ketones, Benzene, Acids, Esters
- **HS38** (4): Misc Chemicals - Antifreeze, Additives, Fatty Acids

### Metals (64 rules)
- **HS72** (29): Iron & Steel - Pig Iron, Flat Rolled Products, Long Products, Semi-Finished
- **HS73** (11): Iron/Steel Articles - Pipe, Tube, Wire
- **HS74** (2): Copper - Cathodes, Mattes
- **HS76** (16): Aluminum - Unwrought, Plates, Bars, Wire, Foil
- **HS78** (3): Lead - Unwrought, Concentrates
- **HS79** (5): Zinc - Unwrought, Concentrates, Plates

### Construction Materials (23 rules)
- **HS25** (9): Stone/Earth - Salt, Portland Cement, Gypsum, Aggregates, Sand
- **HS68** (4): Stone/Ceramic - Worked Stone, Gypsum Articles, Slag Wool
- **HS69** (1): Ceramic Products - Building Bricks

### Fertilizers (3 rules)
- **HS31** (3): Nitrogen Fertilizers (Urea), Potash Fertilizers, Compound Fertilizers

### Raw Materials & Ores (8 rules)
- **HS26** (5): Ores - Bauxite, Iron Ore, Titanium Ore, Slag/Ash

### Agricultural Products (14 rules)
- **HS08** (1): Bananas
- **HS09** (1): Coffee
- **HS12** (1): Soybeans
- **HS15** (3): Vegetable Oils - Palm Oil, Coconut Oil, Tallow
- **HS17** (1): Sugar
- **HS20** (1): Orange Juice
- **HS23** (4): Animal Feed - Meal, Pellets, Oilcake
- **HS40** (2): Rubber - Natural, Synthetic

### Forestry Products (6 rules)
- **HS44** (3): Lumber, Fiberboard, Plywood
- **HS47** (1): Wood Pulp
- **HS48** (2): Paper & Paperboard

### General Cargo & Machinery (7 rules)
- **HS83** (1): Base Metal Fittings
- **HS84** (5): Machinery - Conveyors, Excavators, Parts
- **HS85** (1): Semiconductors
- **HS87** (2): Motor Vehicles, Auto Parts
- **HS95** (1): Toys

---

## Key Improvements in v3.6.0

### 1. Refined Keyword Strategy
- **Key_Phrases**: Multi-word phrases requiring exact matches (e.g., "CRUDE OIL", "PIG IRON")
- **Primary_Keywords**: Standalone product terms (e.g., "CEMENT", "STEEL")
- **Descriptor_Keywords**: Modifiers and qualifiers (e.g., "HOT", "ROLLED", "PRIME")
- **Match_Strategy**: PHRASE_REQUIRED vs PRIMARY_SUFFICIENT

### 2. Comprehensive Energy Coverage
- Complete HS27 mineral fuels classification
- Specific crude oil grades (MAYA, ARAB, ISTHMUS, BASRAH)
- Refined petroleum products (gasoline, diesel, jet fuel, VGO, ULSD, RBOB)
- Coal types (steam coal, metallurgical coal, anthracite, met coke)
- LNG and petroleum gases

### 3. Metals Classification Excellence
- All major steel products (72-73)
- Nonferrous metals (aluminum, copper, lead, zinc)
- Iron ore and pig iron
- Steel scrap types
- Ferroalloys and concentrates

### 4. Chemical Industry Coverage
- 82 pure chemical rules (HS28-29)
- Inorganic chemicals (caustic soda, ammonia, acids)
- Organic chemicals (alcohols, ketones, benzene, esters)
- Fertilizer chemicals

### 5. Construction Materials
- Portland cement and clinker
- Aggregates (sand, gravel, stone)
- Gypsum and gypsum products
- Slag and slag wool

### 6. Agricultural & Food Products
- Vegetable oils (palm, coconut, tallow)
- Grain and oilseeds
- Sugar, coffee, juice
- Rubber (natural and synthetic)

---

## Match Strategy Summary

### PHRASE_REQUIRED (High Specificity)
Used for ambiguous terms requiring context:
- Crude Oil (vs. crude rubber, crude barite)
- Steel Scrap (vs. copper scrap, aluminum scrap)
- Iron Ore (vs. other ores)
- Pig Iron (specific product)
- Portland Cement (vs. other cements)
- Palm Oil (vs. other oils)
- Caustic Soda (vs. other chemicals)

### PRIMARY_SUFFICIENT (Direct Match)
Used for unambiguous commodity terms:
- Generic chemicals without specific phrases
- General cargo items
- Machinery and equipment
- Products with clear single identifiers

---

## Tonnage Filters

### Liquid Bulk
- Chemicals: 250-12,000 tons
- Vegetable Oils: 250-18,000 tons
- Petroleum Products: 10,000-175,000 tons

### Dry Bulk
- Agricultural: 1.5-75,000 tons
- Construction Materials: 2,500-75,000 tons
- Metals (Finished): 1-9,500 tons
- Metals (Raw): 1,500-75,000 tons
- Fertilizers: 750-75,000 tons
- Forestry: 1.5-15,000 tons

### General Cargo
- Vehicles & Machinery: 1.5-250 tons

---

## Phase 3 User-Edited Rules Summary

All 218 new rules are assigned to **Phase 3** with:
- **Active**: TRUE
- **Lock_Group**: TRUE (prevents overwriting Group)
- **Lock_Commodity**: TRUE (prevents overwriting Commodity)
- **Lock_Cargo**: TRUE (prevents overwriting Cargo)
- **Lock_Cargo_Detail**: TRUE (prevents overwriting Cargo_Detail)
- **Source**: "User-edited specialized dictionary"
- **Priority**: 1

---

## Next Steps

1. **Review**: Check classification accuracy on test dataset
2. **Test**: Run classification on 15K sample
3. **Validate**: Compare results with previous version
4. **Deploy**: Move to authoritative dictionary when verified

---

## Files Created

- **cargo_classification_dictionary_v3.6.0_DRAFT_20260114.csv** (668 rules, 43 columns)
- **dictionary_rules_DRAFT_hs27_mineral_fuels.csv** (13 rules)
- **dictionary_rules_DRAFT_hs28-29_pure_chemicals.csv** (82 rules)
- **dictionary_rules_DRAFT_hs72-73_76-79_user_edits.csv** (64 rules)
- **dictionary_rules_DRAFT_2mil_tons_plus.csv** (59 rules)
- **dictionary_hs28-29_pure_chemicals_CORRECTED.csv** (typo-corrected source)
- **dictionary_all_hs4_2mil_tons_plus_CORRECTED.csv** (typo-corrected source)

---

## Typos Fixed

### HS28-29 Pure Chemicals
- Caustic Sodea → Caustic Soda
- liquid gas → Liquid Gas
- lpg → LPG (capitalization)
- Nitrogen Fertiliers → Nitrogen Fertilizers
- Tios → TiO2
- Mangeses → Manganese
- Zinc concventreatre → Zinc concentrate
- tbn bulkk → TBN

### 2M+ Tons Multi-Commodity
- chemicals → Chemicals (capitalization)
- copper csthodes → copper cathodes
- Phospourouse Fetilizers → Phosphorous Fertilizers
- phois rick, phospahte rockl → phos rock, phosphate rock
- flay ash → fly ash
- iron concetrates → iron concentrates
- Aggregatyes → Aggregates
- Removed incorrect keywords (COPPER in cement, CEMENT CLINKER in ceramic bricks)

---

**Dictionary v3.6.0 DRAFT is ready for testing and validation!**

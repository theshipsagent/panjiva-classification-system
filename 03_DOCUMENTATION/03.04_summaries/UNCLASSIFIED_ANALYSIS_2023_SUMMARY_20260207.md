# Unclassified Records Analysis - Panjiva 2023
**Analysis Date:** February 7, 2026
**File Analyzed:** `panjiva_2023_with_additional_refined_products_20260207_113532.csv`

---

## Executive Summary

**Total Dataset:**
- Records: 394,600
- Total Tonnage: 728,057,360.42 tons

**Unclassified Records:**
- Records: 110,838 (28.1% of total)
- Tonnage: 134,494,138.77 tons (18.5% of total tonnage)

**Coverage:** The top 15 HS2 codes account for **116.6 million tons (86.7%)** of all unclassified tonnage, suggesting focused dictionary expansion on these categories could dramatically improve classification rates.

---

## Top 15 Unclassified HS2 Codes by Tonnage

### 1. HS2 27 - Mineral Fuels, Oils (45.9M tons, 34.1%)
**Records:** 5,673
**Key Patterns:**
- **Refined petroleum products** dominating: heating oil, diesel, naphtha, alkylate, gasolina booster
- **Tank cleaning operations**: de-slopping operations, slops removal
- **Off-spec fuels**: waste/destruction shipments, off-spec VLSFO
- **Renewable diesel**: NESTE brand renewable diesel (multiple large shipments)

**Top Keywords:** BBLS (2,858), ULTRA (626), SULFUR (553), HEATING (515), DIESEL (463), NAPHTHA (461), SLOPS (420)

**Classification Opportunities:**
- Create Phase 4-5 rules for heating oil (HS27 + "HEATING OIL" or "ULTRA LOW SULFUR")
- Add naphtha classification (HS27 + "NAPHTHA")
- Add alkylate rules (HS27 + "ALKYLATE")
- Consider renewable diesel category (HS27 + "RENEWABLE DIESEL" or "NESTE")
- Add waste fuel/slops category (HS27 + "SLOPS" or "DESTRUCTION" or "OFF SPEC")

---

### 2. HS2 72 - Iron & Steel (21.4M tons, 15.9%)
**Records:** 5,957
**Key Patterns:**
- **Steel coils** (hot-rolled, cold-rolled, galvanized, prepainted)
- **Steel plate and billet**
- **Ferro-alloys** appearing in keywords
- **Zinc-coated products** (galvanized)

**Top Keywords:** COIL (4,064), STEEL (3,261), ALLOY (1,519), COATED (990), ZINC (936), PREPAINTED (918), FERRO (852), PRIME (772)

**Classification Opportunities:**
- Create HS72 + "COIL" rules for steel coils (may need tonnage ranges to distinguish from finished products)
- Add steel plate rules (HS72 + "PLATE")
- Add steel billet rules (HS72 + "BILLET")
- Add galvanized steel category (HS72 + "GALVANIZED" or "ZINC")
- Add ferro-alloy rules (HS72 + "FERRO")

---

### 3. HS2 29 - Organic Chemicals (15.5M tons, 11.5%)
**Records:** 2,164
**Key Patterns:**
- **Industrial solvents**: chlorobenzene, acetone, MTBE (methyl tertiary butyl ether)
- **Alcohols**: methyl alcohol, ethyl alcohol
- **Specialty chemicals**: TEOS (tetraethyl silicate), VEOVA monomers
- **Fatty acids**: stearic acid
- **Glycerine** (99.7% USP grade)

**Top Keywords:** BULK (991), ALCOHOL (385), METHYL (308), ETHYL (271), KETONE (210), CHLOROBENZENE (implied), MTBE (implied)

**Classification Opportunities:**
- Add industrial solvent category (HS29 + "CHLOROBENZENE" or "ACETONE" or "MTBE")
- Add alcohol rules (HS29 + "METHYL ALCOHOL" or "ETHYL ALCOHOL")
- Add glycerine rules (HS29 + "GLYCERIN" or "GLYCEROL")
- Add stearic acid (HS29 + "STEARIC ACID")

---

### 4. HS2 84 - Machinery & Mechanical Appliances (8.2M tons, 6.1%)
**Records:** 43,156 (largest record count)
**Key Patterns:**
- **Construction equipment**: excavators, loaders, material handlers (John Deere, Volvo brands)
- **Marine equipment**: cargo handling equipment, ship spare parts, turbochargers
- **Industrial machinery**: pumps, compressors, processing equipment
- **Repair/return shipments**: equipment returning for repair

**Top Keywords:** MACHINE (25,319), LOADER (20,588), EXCAVATOR (13,767), WHEEL (13,751), DEERE (11,646), FREIGHT (12,668)

**Classification Opportunities:**
- Add construction equipment rules (HS84 + "EXCAVATOR" or "LOADER" or "MATERIAL HANDLER")
- Add marine equipment category (HS84 + "CARGO HANDLING" or "SHIP EQUIPMENT" or "TURBOCHARGER")
- Consider brand-based rules (HS84 + "JOHN DEERE" or "CATERPILLAR")
- Add spare parts category (HS84 + "SPARE PARTS" or "SPARES")

---

### 5. HS2 26 - Ores, Slag & Ash (3.9M tons, 2.9%)
**Records:** 288
**Key Patterns:**
- **Blast furnace slag** (granulated)
- **Bauxite** (multiple large shipments)
- **Chloride slag** (titania chloride slag)
- **Chromite ore**

**Top Keywords:** SLAG (164), CHROMITE (63), BAUXITE (58), GRANULATED (55), BLAST (52)

**Classification Opportunities:**
- Add slag category (HS26 + "SLAG" + "BLAST FURNACE" or "GRANULATED")
- Add bauxite rules (HS26 + "BAUXITE")
- Add chromite rules (HS26 + "CHROMITE")
- Add chloride slag (HS26 + "CHLORIDE SLAG" or "TITANIA")

---

### 6. HS2 44 - Wood & Articles of Wood (2.7M tons, 2.0%)
**Records:** 733
**Key Patterns:**
- **Timber products**: European spruce, pine, eucalyptus
- **Fence pickets and boards** (kiln-dried)
- **Primary wood products**
- **Hardboard and panels**
- Note: Some misclassified steel structures appearing in samples

**Top Keywords:** WOOD (152), TIMBER (107), PANELS (89), PIECES (89)

**Classification Opportunities:**
- Add timber/lumber category (HS44 + "TIMBER" or "LUMBER" or "WOOD")
- Add fence pickets (HS44 + "FENCE PICKETS" or "PICKETS")
- Add hardboard (HS44 + "HARDBOARD")
- Add panel products (HS44 + "PANELS")

---

### 7. HS2 23 - Residues from Food Industries; Animal Feed (2.6M tons, 1.9%)
**Records:** 619
**Key Patterns:**
- **Organic soybean meal** (certified organic)
- **Organic sunflower meal**
- **DDGS** (distillers dried grains with solubles - animal feed)
- **Vegetable blend pellets** (feed grade)
- Note: Some misclassified chemicals (orthoxylene, slag)

**Top Keywords:** MEAL (1,695), ORGANIC (1,091), SOYBEAN (870), BULK (1,945), PREVENT (930), DURING (1,021), REGISTRATION (1,126)

**Classification Opportunities:**
- Add organic meal category (HS23 + "ORGANIC" + "SOYBEAN MEAL" or "SUNFLOWER MEAL")
- Add DDGS rules (HS23 + "DISTILLERS DRIED GRAINS" or "DDGS")
- Add animal feed category (HS23 + "ANIMAL FEED" or "FEED GRADE")

---

### 8. HS2 31 - Fertilizers (2.5M tons, 1.8%)
**Records:** 346
**Key Patterns:**
- **Potassium fertilizers**: KALISOP (potassium sulfate), 60ER KALI
- **Calcium nitrate** solutions (noxious liquids)
- **Triple superphosphate** (GTSP)
- **Liquid and granular forms**

**Top Keywords:** NITRATE (282), GRANULAR (182), CALCIUM (112), TRIPLE (105), POTASSIUM (90), LIQUID (100)

**Classification Opportunities:**
- Add potassium fertilizer rules (HS31 + "KALISOP" or "POTASSIUM" + "FERTILIZER")
- Add calcium nitrate (HS31 + "CALCIUM NITRATE")
- Add triple superphosphate (HS31 + "TRIPLE" + "SUPERPHOSPHATE" or "GTSP")
- Distinguish granular vs liquid forms

---

### 9. HS2 87 - Vehicles & Parts (2.3M tons, 1.7%)
**Records:** 17,319
**Key Patterns:**
- **Passenger vehicles**: Volvo (XC40, XC60, XC90), Land Rover (Defender, Range Rover), Mercedes-Benz
- **Heavy equipment**: Volvo articulated haulers (A30G, A45G)
- **Tractors**: RORO tractors, agricultural tractors
- **Spare parts and used equipment**

**Top Keywords:** VOLVO (92,847), ROVER (52,534), LAND (36,501), MERCEDES (32,097), BENZ (32,042), XC40 (40,616)

**Classification Opportunities:**
- Add passenger vehicle rules (HS87 + "VOLVO" or "LAND ROVER" or "MERCEDES")
- Add articulated hauler category (HS87 + "ARTICULATED HAULER")
- Add tractor rules (HS87 + "TRACTOR")
- Consider model-specific rules (HS87 + "XC40" or "XC60" or "DEFENDER")

---

### 10. HS2 38 - Miscellaneous Chemical Products (2.0M tons, 1.5%)
**Records:** 895
**Key Patterns:**
- **Fatty acids**: stearic acid (various grades 43%, 50%, 52%, 65%)
- **Hardened fatty acids**: coconut fatty acid, distilled fatty acid
- **Artificial graphite powder**
- Bulk liquid chemicals

**Top Keywords:** ACID (215), GRAPHITE (129), ARTIFICIAL (116), FATTY (102), STEARIC (70), BULK (218)

**Classification Opportunities:**
- Add fatty acid category (HS38 + "FATTY ACID" or "STEARIC ACID")
- Add graphite rules (HS38 + "GRAPHITE" + "ARTIFICIAL" or "POWDER")
- Distinguish by concentration/grade (43%, 50%, 65%)

---

### 11. HS2 28 - Inorganic Chemicals (2.0M tons, 1.5%)
**Records:** 793
**Key Patterns:**
- **Silicon carbide** (crude and refined)
- **Sulfates**: manganese sulfate, zinc sulfate, ferrous sulfate
- **Tabular alumina**
- **Sodium compounds**

**Top Keywords:** SILICON (182), CARBIDE (178), SODIUM (113), SULPHATE (104), ALUMINA (71), BAGS (180)

**Classification Opportunities:**
- Add silicon carbide rules (HS28 + "SILICON CARBIDE")
- Add sulfate category (HS28 + "SULFATE" or "SULPHATE" + metal name)
- Add alumina rules (HS28 + "TABULAR ALUMINA" or "ALUMINA")

---

### 12. HS2 12 - Oil Seeds & Oleaginous Fruits (1.9M tons, 1.4%)
**Records:** 338
**Key Patterns:**
- **Organic soybeans** (certified organic, NOP certified)
- **Organic flaxseed** (in bigbags)
- **Organic canola seed**
- **Mustard seed** (Canadian #1 oriental)
- **German rye**

**Top Keywords:** BULK (676), SOYBEANS (368), ORGANIC (315), CERTIFIED (92), SEED (70), FLAXSEED (implied), CANOLA (implied)

**Classification Opportunities:**
- Add organic seed category (HS12 + "ORGANIC" + "SOYBEANS" or "FLAXSEED" or "CANOLA")
- Add mustard seed (HS12 + "MUSTARD SEED")
- Add flaxseed rules (HS12 + "FLAXSEED")
- Add rye (HS12 + "RYE")

---

### 13. HS2 68 - Articles of Stone, Cement, Asbestos (1.9M tons, 1.4%)
**Records:** 259
**Key Patterns:**
- **Marble** products
- **Rock wool insulation**
- **Cement products**
- **Copper cathodes** (misclassified under HS68)
- **Granite components**

**Top Keywords:** WOOL (74), BULK (58), ROCK (32), SLAG (28), CEMENT (22), MARBLE (implied)

**Classification Opportunities:**
- Add marble category (HS68 + "MARBLE")
- Add rock wool/insulation (HS68 + "ROCK WOOL" or "INSULATION")
- Add cement products (HS68 + "CEMENT")
- Review copper entries (may need HS74 reclassification)

---

### 14. HS2 73 - Articles of Iron or Steel (1.9M tons, 1.4%)
**Records:** 4,555
**Key Patterns:**
- **Steel pipes and tubes** (seamless)
- **Structural steel**: I-beams, posts, galvanized structures
- **Fasteners**: nuts, bolts, screws, washers
- **Glass-lined steel**
- **Aluminum-steel composite products**

**Top Keywords:** STEEL (3,464), GLASS (1,384), ALUMINUM (1,174), NUTS (1,154), SHEETS (1,153), PIPES (1,041), SEAMLESS (877)

**Classification Opportunities:**
- Add steel pipe/tube category (HS73 + "PIPE" or "TUBE" + "SEAMLESS")
- Add structural steel (HS73 + "I-BEAM" or "BEAM" or "POST")
- Add fastener category (HS73 + "NUTS" or "BOLTS" or "SCREWS")
- Add glass-lined steel (HS73 + "GLASS")

---

### 15. HS2 25 - Salt; Sulfur; Earths & Stone (1.9M tons, 1.4%)
**Records:** 588
**Key Patterns:**
- **Granite blocks** (rough, various dimensions)
- **Cement** (Portland cement Type I/II)
- **Deadburned magnesite** (grade M-10, M-30B)
- **Carbon additive**

**Top Keywords:** BLOCKS (290), GRANITE (118), BULK (143), 60CM (117), 70CM (115), 75CM (115), WEIGHT (114), METRIC (109)

**Classification Opportunities:**
- Add granite blocks (HS25 + "GRANITE" + "BLOCKS")
- Add Portland cement (HS25 + "PORTLAND CEMENT" or "CEMENT")
- Add magnesite (HS25 + "MAGNESITE" or "DEADBURNED")
- Add carbon additive (HS25 + "CARBON ADDITIVE")

---

## Priority Recommendations

### High-Impact Quick Wins (>10M tons each)
1. **HS27 Refined Petroleum Products** (45.9M tons) - heating oil, diesel, naphtha, alkylate
2. **HS72 Steel Coils & Plate** (21.4M tons) - coils, plate, billet, galvanized
3. **HS29 Industrial Chemicals** (15.5M tons) - solvents, alcohols, fatty acids

### Medium-Impact Opportunities (2-4M tons each)
4. **HS26 Ores & Slag** (3.9M tons) - blast furnace slag, bauxite, chromite
5. **HS44 Wood Products** (2.7M tons) - timber, lumber, fence pickets
6. **HS23 Animal Feed** (2.6M tons) - organic meal, DDGS
7. **HS31 Fertilizers** (2.5M tons) - potassium, calcium nitrate, TSP
8. **HS87 Vehicles** (2.3M tons) - passenger vehicles, articulated haulers
9. **HS38 Specialty Chemicals** (2.0M tons) - fatty acids, graphite
10. **HS28 Inorganic Chemicals** (2.0M tons) - silicon carbide, sulfates

### Lower Priority but Still Significant (1-2M tons each)
11. **HS12 Oil Seeds** (1.9M tons) - organic soybeans, flaxseed, canola
12. **HS68 Stone Products** (1.9M tons) - marble, granite, cement
13. **HS73 Steel Articles** (1.9M tons) - pipes, tubes, structural steel
14. **HS25 Minerals** (1.9M tons) - granite blocks, cement, magnesite

---

## Strategic Notes

### HS84 Machinery Challenge
- **43,156 records** but only **8.2M tons** (6.1% of unclassified tonnage)
- Very low tonnage per record (average 191 kg/record)
- High variety: construction equipment, marine equipment, industrial machinery
- May require extensive keyword library due to equipment diversity
- Consider cost/benefit: many rules needed for moderate tonnage gain

### Misclassification Issues Detected
- Some **steel structures** appearing under HS44 (wood)
- Some **chemicals** (orthoxylene, slag) appearing under HS23 (animal feed)
- **Copper cathodes** appearing under HS68 (should be HS74)
- Suggests need for validation/correction rules in later phases

### Bulk vs. Packaged Products
- Many unclassified items explicitly marked as "IN BULK"
- Package type "LBK" (liquid bulk) rule already successful in current dictionary
- Consider adding "BULK" keyword rules for solid bulk commodities where appropriate

### Brand Name Patterns
Strong brand identification in vehicles and equipment:
- **Vehicles**: Volvo, Land Rover, Mercedes-Benz (HS87)
- **Equipment**: John Deere, Caterpillar, Volvo (HS84)
- Brand-based rules could provide high accuracy classification

---

## Implementation Roadmap

### Phase 1: High-Impact Petroleum & Steel (67.3M tons)
- HS27 refined products: 10-15 new rules
- HS72 steel coils/plate: 8-10 new rules
- **Estimated impact:** 67.3M tons (50% of unclassified)

### Phase 2: Industrial Chemicals (17.5M tons)
- HS29 organic chemicals: 8-12 new rules
- HS38 specialty chemicals: 5-8 new rules
- HS28 inorganic chemicals: 5-7 new rules
- **Estimated impact:** 17.5M tons (13% of unclassified)

### Phase 3: Bulk Commodities (12.7M tons)
- HS26 ores & slag: 4-5 new rules
- HS44 wood products: 4-6 new rules
- HS23 animal feed: 4-5 new rules
- HS31 fertilizers: 5-7 new rules
- HS12 oil seeds: 4-5 new rules
- **Estimated impact:** 12.7M tons (9% of unclassified)

### Phase 4: Manufactured Goods (12.1M tons)
- HS87 vehicles: 6-10 new rules
- HS73 steel articles: 5-7 new rules
- HS68 stone products: 3-5 new rules
- HS25 minerals: 3-5 new rules
- **Estimated impact:** 12.1M tons (9% of unclassified)

### Phase 5: Machinery (deferred)
- HS84 machinery: extensive rule library needed
- High record count but low tonnage
- Consider after other high-impact categories complete

---

## Total Potential Impact

**Current Status:**
- Classified: 71.7% of tonnage
- Unclassified: 18.5% of tonnage (134.5M tons)

**After Top 15 HS2 Implementation:**
- Additional coverage: 116.6M tons
- **New total classified: 87.4% of tonnage**
- Remaining unclassified: 17.9M tons (2.5% of total)

**Conclusion:** Focused dictionary expansion on these 15 HS2 codes could increase classification from 71.7% to 87.4%, a gain of 15.7 percentage points with targeted rule additions estimated at 100-150 new rules total.

---

## Files Generated

- **Analysis Script:** `G:\My Drive\LLM\project_manifest\02_SCRIPTS\02.04_analysis\analyze_unclassified_records_20260207.py`
- **Raw Report:** `G:\My Drive\LLM\project_manifest\02_SCRIPTS\02.04_analysis\unclassified_analysis_20260207.txt`
- **Summary (this file):** `G:\My Drive\LLM\project_manifest\03_DOCUMENTATION\03.04_summaries\UNCLASSIFIED_ANALYSIS_2023_SUMMARY_20260207.md`

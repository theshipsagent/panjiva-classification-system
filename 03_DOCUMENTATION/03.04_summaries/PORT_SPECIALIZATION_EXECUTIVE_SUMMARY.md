# PORT SPECIALIZATION ANALYSIS - EXECUTIVE SUMMARY

**Analysis Date:** February 5, 2026
**Data Source:** panjiva_imports_2024_classified_v2.0.0.csv
**Records Analyzed:** 419,255 shipments
**Total Tonnage:** 496.3 million tons

---

## KEY FINDINGS

### 1. PORT SPECIALIZATION DISTRIBUTION

Of the top 20 US ports:
- **19 ports** are moderately specialized (focused on 2-3 key commodities)
- **1 port** is diversified (Philadelphia - 11 commodity types)
- **0 ports** are highly specialized (single commodity)

This indicates that even "specialized" crude terminals handle some petroleum products, chemicals, or general cargo.

---

## 2. TOP 5 US PORTS BY TONNAGE

| Rank | Port | Total Tonnage | Coast | Specialization | Top Commodity (%) |
|------|------|--------------|-------|----------------|-------------------|
| 1 | Houston, TX | 56.7M tons | Gulf | Diversified Hub | General Cargo (37.8%) |
| 2 | New Orleans, LA | 30.7M tons | Gulf | Chemical/Petroleum | General Cargo (55.8%) |
| 3 | Port Arthur, TX | 26.0M tons | Gulf | Crude Terminal | Crude Oil (80.3%) |
| 4 | New York/Newark, NJ | 25.6M tons | East | Diversified | Chemicals (28.6%) |
| 5 | Long Beach, CA | 21.7M tons | West | Asian Imports | Pet Products (51.0%) |

---

## 3. CRUDE OIL TERMINAL RANKINGS

### Top 10 Crude Oil Import Ports (2024)

| Rank | Port | Crude Tonnage | % of Port Total | Top Sources |
|------|------|--------------|-----------------|-------------|
| 1 | Port Arthur, TX | 22.1M tons | 80.3% | Aruba, Mexico, Venezuela |
| 2 | Richmond, CA | 18.5M tons | 84.5% | Panama, Algeria, Argentina |
| 3 | Long Beach, CA | 15.0M tons | 20.6% | Iraq, Brazil, Panama |
| 4 | Houston, TX | 13.5M tons | 19.1% | Mexico, Colombia, Canada |
| 5 | Los Angeles, CA | 10.8M tons | 42.1% | Panama, Canada, Ecuador |
| 6 | New York/Newark, NJ | 6.5M tons | 25.5% | Canada, Libya, Neth. Antilles |
| 7 | Philadelphia, PA | 6.3M tons | 24.6% | Nigeria, Mexico, Canada |
| 8 | Corpus Christi, TX | 6.2M tons | 31.7% | Aruba, Colombia, Trinidad |
| 9 | Pascagoula, MS | 6.1M tons | 76.7% | Venezuela, Brazil, UK |
| 10 | New Orleans, LA | 5.5M tons | 16.4% | Venezuela, Mexico, Algeria |

**Key Insight:** Gulf Coast crude terminals (Port Arthur, Pascagoula) show highest specialization with 75-85% crude oil concentration. West Coast ports (Richmond, Long Beach, LA) import significant crude but maintain more diverse portfolios.

---

## 4. REGIONAL PATTERNS

### Gulf Coast (10 ports, 193.9M tons)
**Character:** Mix of crude terminals, chemical complexes, and diversified hubs

**Top Commodities:**
1. General Cargo - 76.6M tons (39.5%)
2. Crude Oil - 55.4M tons (28.6%)
3. Chemicals - 19.1M tons (9.9%)
4. Petroleum Products - 17.5M tons (9.0%)
5. Steel - 9.9M tons (5.1%)

**Specialization Types:**
- **Crude Terminals:** Port Arthur (80% crude), Pascagoula (77% crude)
- **Chemical Hubs:** Baton Rouge (57% chemicals), New Orleans
- **Diversified:** Houston (14 commodity types), Corpus Christi

### East Coast (6 ports, 87.4M tons)
**Character:** Diversified ports handling chemicals, petroleum products, Ro/Ro, steel, aggregates

**Top Commodities:**
1. General Cargo - 32.8M tons (37.6%)
2. Chemicals - 12.3M tons (14.0%)
3. Ro/Ro - 9.7M tons (11.1%)
4. Crude Oil - 9.6M tons (11.0%)
5. Petroleum Products - 9.5M tons (10.9%)

**Notable Ports:**
- **Philadelphia:** Most diversified (11 commodities, HHI=0.22)
- **Baltimore:** Strong Ro/Ro focus (27.5% of tonnage)
- **New York/Newark:** Chemical and petroleum products hub

### West Coast (3 ports, 58.0M tons)
**Character:** Pacific crude imports, petroleum products, Asian containerized trade

**Top Commodities:**
1. Crude Oil - 28.8M tons (49.6%)
2. Petroleum Products - 17.4M tons (30.0%)
3. General Cargo - 3.3M tons (5.7%)
4. Construction Materials - 3.3M tons (5.7%)
5. Ro/Ro - 2.7M tons (4.6%)

**Notable Ports:**
- **Richmond, CA:** Highly specialized crude terminal (84.5%)
- **Long Beach/LA:** Balanced petroleum products and crude
- **Pacific crude sources:** Iraq, Brazil, Panama, Ecuador

---

## 5. FOREIGN PORT PATTERNS

### Top 10 Foreign Loading Ports

| Rank | Port | Country | Tonnage | Specialization | Top Commodity (%) |
|------|------|---------|---------|----------------|-------------------|
| 1 | Rotterdam | Netherlands | 13.6M | Chemical Hub | Chemicals (88.3%) |
| 2 | Brazil Ports South | Brazil | 11.3M | Diversified | Gen Cargo (65.1%) |
| 3 | Sepetiba Bay | Brazil | 10.8M | Steel/Cargo | Steel (53.2%) |
| 4 | Armuelles | Panama | 9.8M | Petroleum | Crude (51.5%) |
| 5 | Jose | Venezuela | 9.8M | Crude Terminal | Crude (90.7%) |
| 6 | Vancouver | Canada | 9.5M | Diversified | Gen Cargo (38.5%) |
| 7 | Sao Paulo | Brazil | 9.2M | Diversified | Gen Cargo (54.7%) |
| 8 | UAE Ports | UAE | 9.2M | Mono-cargo | Gen Cargo (99.5%) |
| 9 | Freeport, Bahamas | Bahamas | 8.5M | Aggregates | Construction (42.1%) |
| 10 | Coatzacoalcos | Mexico | 8.0M | Chemical/Crude | Chemicals (73.5%) |

**Key Patterns:**
- **Venezuelan/Panamanian ports:** Crude oil specialists (85-90% crude)
- **Brazilian ports:** Steel, forestry, general cargo
- **European ports:** Chemical exports (Rotterdam 88% chemicals)
- **Mexican ports:** Crude oil and chemical exports
- **Canadian ports:** Aggregates, petroleum products, construction materials

---

## 6. PORT SPECIALIZATION INDEX METHODOLOGY

### Herfindahl-Hirschman Index (HHI)
- **Formula:** Sum of squared market shares
- **Scale:** 0 to 1 (or 0 to 10,000 if using percentages)
- **Interpretation:**
  - HHI > 0.50: Highly specialized (2-3 dominant commodities)
  - HHI 0.30-0.50: Moderately specialized
  - HHI < 0.30: Diversified (many commodities)

### Shannon Entropy
- **Formula:** -Σ(p_i × log(p_i))
- **Interpretation:**
  - Higher values = more diversity
  - Entropy > 2.0: High diversity (like Philadelphia's 1.80)
  - Entropy < 1.0: Low diversity (crude terminals ~0.6-0.8)

### Top 3 Concentration
- **Formula:** Sum of top 3 commodity shares
- **Interpretation:**
  - > 90%: Highly specialized (Port Arthur 92%, Richmond 95%)
  - 75-90%: Moderately specialized (most Gulf/East ports)
  - < 75%: Diversified (Houston 72%, Philadelphia 69%)

---

## 7. COMMODITY-SPECIFIC TERMINAL EXAMPLES

### Crude Oil Terminals
- **Port Arthur, TX:** 80.3% crude (Aruba, Mexico sources)
- **Richmond, CA:** 84.5% crude (Panama, Algeria sources)
- **Pascagoula, MS:** 76.7% crude (Venezuela primary source)

### Chemical Complexes
- **Rotterdam, Netherlands:** 88.3% chemicals
- **Baton Rouge, LA:** 57.2% chemicals
- **Coatzacoalcos, Mexico:** 73.5% chemicals

### Construction Material Ports
- **Auld's Cove, Nova Scotia:** 99.9% construction materials (aggregates to Tampa)
- **Freeport, Bahamas:** 42.1% construction materials
- **Tampa, FL:** 40.5% construction materials (receives NS aggregates)

### Steel Ports
- **Sepetiba Bay, Brazil:** 53.2% steel exports
- **Antwerp, Belgium:** 27.6% steel (second after chemicals)

### Diversified Hubs
- **Houston, TX:** 14 commodity types, no single commodity > 38%
- **Philadelphia, PA:** 11 commodity types, balanced portfolio
- **Vancouver, BC:** 7 commodities, strong general cargo and petroleum

---

## 8. KEY INSIGHTS AND PATTERNS

### Pattern 1: Gulf Coast Specialization
- **Eastern Gulf** (New Orleans, Mobile, Baton Rouge): Chemicals and petroleum products
- **Texas Gulf** (Port Arthur, Corpus Christi, Freeport): Crude oil focus
- **Houston:** Exception - truly diversified hub with 14 commodity types

### Pattern 2: Venezuelan/Mexican Crude Routes
- Venezuelan crude → Gulf ports (Pascagoula, New Orleans)
- Mexican crude → Texas ports (Houston, Port Arthur)
- Aruba (transshipment) → Port Arthur, Corpus Christi

### Pattern 3: Canadian Aggregates Trade
- Nova Scotia aggregates → East Coast (Tampa, Jacksonville)
- Vancouver → West Coast construction materials
- Canadian petroleum products → Northeast (Maine, New York)

### Pattern 4: Asian Import Concentrations
- Iraq crude → Long Beach
- Brazilian crude → Long Beach, Philadelphia
- Panama (transshipment) → Los Angeles, Richmond
- South Korean petroleum products → Long Beach

### Pattern 5: European Chemical Exports
- Rotterdam → New York/Newark (7.3M tons chemicals)
- Antwerp → East Coast steel and chemicals
- Belgium/Netherlands → diversified US chemical imports

### Pattern 6: Brazilian Commodity Mix
- **Steel:** Sepetiba Bay (5.8M tons)
- **Forestry:** Southern Brazil ports (2.1M tons)
- **General cargo:** Sao Paulo, Rio (5-6M tons each)
- Brazil is a major diversified exporter across multiple commodities

---

## 9. SURPRISING FINDINGS

1. **"General Cargo" Dominance:** General Cargo is the #1 commodity at 10 of 20 ports (likely containerized goods or miscellaneous bulk). This suggests classification may be lumping unclassified items.

2. **Philadelphia's Diversity:** Despite being an East Coast port, Philadelphia shows the lowest specialization (HHI=0.22) with 11 commodity types, making it more diversified than Houston.

3. **Richmond's Crude Focus:** Port of Richmond, CA (84.5% crude) is more specialized than Port Arthur, TX (80.3%), making it the most specialized major crude terminal.

4. **Gramercy's Cement Profile:** Port of Gramercy, LA shows 83.7% "General Cargo" - likely bulk cement from Vietnam/Asia based on partner data.

5. **Tampa's Aggregate Dependence:** Tampa receives 40.5% construction materials, primarily aggregates from Nova Scotia's Auld's Cove (99.9% pure aggregate exporter).

6. **San Juan's Petroleum Products:** Puerto Rico's San Juan receives 40.3% petroleum products (3.6M tons), second only to general cargo - critical energy security dependence.

---

## 10. RECOMMENDATIONS FOR FURTHER ANALYSIS

1. **Decompose "General Cargo":** Investigate what's being classified as General Cargo - likely containerized goods, cement, or unclassified bulk.

2. **Seasonal Patterns:** Analyze crude oil imports by quarter to identify seasonal refinery demand patterns.

3. **Trade Route Mapping:** Create origin-destination matrices for specific commodities (e.g., Venezuelan crude → which US ports).

4. **Port Pair Analysis:** Identify dominant port pairs (e.g., Auld's Cove ↔ Tampa for aggregates).

5. **Carrier-Port-Commodity Matching:** Cross-reference carrier specialization with port specialization (e.g., do chemical tanker operators concentrate at Baton Rouge?).

6. **Great Lakes Analysis:** Expand to include Great Lakes ports - likely to show Canadian aggregate/ore specialization.

7. **Refinery Capacity Correlation:** Compare crude import volumes to regional refinery capacity and utilization rates.

---

## FILES GENERATED

1. **port_specialization_profiles_v1.0.0_20260205_231654.csv**
   Top 20 US ports with HHI, entropy, top 3 commodities, regional patterns

2. **foreign_port_profiles_v1.0.0_20260205_231654.csv**
   Top 20 foreign loading ports with specialization metrics

3. **port_commodity_matrix_v1.0.0_20260205_231654.csv**
   Pivot table: 20 ports × 16 commodities with tonnage

4. **crude_terminal_sources_v1.0.0_20260205_231654.csv**
   Top 10 crude ports with source countries and tonnage

5. **regional_pattern_summary_v1.0.0_20260205_231654.csv**
   Regional aggregation (Gulf, East, West) with avg metrics

6. **port_specialization_analysis_v1.0.0_20260205_231654.txt**
   Full narrative report with detailed port profiles

---

## SCRIPT LOCATION

**Analysis Script:**
`G:\My Drive\LLM\project_manifest\02_SCRIPTS\02.04_analysis\analyze_port_specialization_v1.0.0.py`

**Outputs:**
`G:\My Drive\LLM\project_manifest\03_DOCUMENTATION\03.04_summaries\`

---

*End of Executive Summary*

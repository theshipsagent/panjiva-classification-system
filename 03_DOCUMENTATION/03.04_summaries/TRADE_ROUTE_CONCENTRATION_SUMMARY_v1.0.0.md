# Trade Route Concentration Analysis - Summary Report
## v1.0.0 | 2026-02-06

---

## Executive Summary

This analysis examines **supply chain resilience and concentration risk** for 18,965 harmonized consignees importing 174.9 million tons of cargo in 2024. The study reveals stark differences in diversification strategies, with major oil refiners maintaining well-diversified supply chains while specialized importers face significant single-source dependency risks.

**Key Findings:**
- **61.3%** of entities face HIGH concentration risk (11,627 entities)
- **24.8%** of tonnage (43.4M tons) concentrated in single-source dependencies
- **Top 3 most diversified**: Chevron (80 ports), Valero (69 ports), ExxonMobil (75 ports)
- **Most concentrated**: 1,234 entities rely 100% on single port (HHI = 10,000)

---

## Methodology

### Herfindahl-Hirschman Index (HHI)

The analysis uses HHI to measure concentration across three dimensions:
- **Port HHI**: Concentration of origin ports
- **Country HHI**: Geopolitical concentration
- **Shipper HHI**: Supplier concentration

**HHI Formula:** Sum of squared market shares (0-10,000 scale)

**Risk Categories:**
- **HHI < 1,500**: Low concentration (Diversified) - LOW RISK
- **1,500 ≤ HHI < 2,500**: Moderate concentration - MODERATE RISK
- **2,500 ≤ HHI < 5,000**: High concentration (Risky) - MODERATE-HIGH RISK
- **HHI ≥ 5,000**: Very high concentration (Single source risk) - HIGH RISK
- **HHI = 10,000**: Complete dependency on single source - CRITICAL RISK

### Resilience Score (0-100)

Multi-dimensional metric combining:
- **Port diversity** (25 points): Number of unique origin ports
- **Country diversity** (25 points): Geographic spread
- **Port HHI** (25 points): Inverse of port concentration
- **Country HHI** (25 points): Inverse of geopolitical concentration

**Score Interpretation:**
- **80-100**: Highly resilient (LOW RISK)
- **60-79**: Moderately resilient (MODERATE RISK)
- **30-59**: Vulnerable (HIGH RISK)
- **0-29**: Critically vulnerable (CRITICAL RISK)

---

## Overall Risk Distribution

### By Number of Entities

| Risk Level | Count | % of Entities | Avg HHI | Avg Ports |
|------------|-------|---------------|---------|-----------|
| **LOW** | 6,817 | 36.0% | 748 | 29 |
| **MODERATE** | 521 | 2.7% | 2,107 | 7 |
| **HIGH** | 11,627 | 61.3% | 8,254 | 2 |

### By Tonnage

| Risk Level | Tonnage | % of Total | Avg Entity Size |
|------------|---------|------------|-----------------|
| **LOW** | 113.5M tons | 64.9% | 16,649 tons |
| **MODERATE** | 18.1M tons | 10.3% | 34,682 tons |
| **HIGH** | 43.4M tons | 24.8% | 3,732 tons |

**Key Insight:** While 61% of entities face HIGH risk, they only represent 25% of tonnage. Large importers (oil refiners, traders) are well-diversified, while small specialized importers face concentration risk.

---

## Port Concentration Analysis

### Concentration Distribution

| Category | Entities | % | Total Tonnage | % of Tonnage |
|----------|----------|---|---------------|--------------|
| **Very High (>5000)** | 11,825 | 62.4% | 54.1M tons | 30.9% |
| **High (2500-5000)** | 759 | 4.0% | 14.3M tons | 8.2% |
| **Moderate (1500-2500)** | 628 | 3.3% | 12.2M tons | 7.0% |
| **Low (<1500)** | 5,753 | 30.3% | 94.2M tons | 53.9% |

### Single-Source Dependencies

**1,234 entities (6.5%)** rely 100% on a single port:
- Total tonnage at risk: **28.4 million tons** (16.2%)
- Examples:
  - **Saudi Refining Inc**: 15.0M tons, 100% from "High Seas, Gulf Of Mexico" (transshipment)
  - **Compass Minerals**: 3.3M tons, 100% from Goderich, Ont, Canada (salt mine)
  - **Eucatex**: 3.6M tons, 100% from Sao Paulo, Brazil (wood products)
  - **Blue Water Industries**: 1.8M tons, 100% from Newfoundland (aluminum)

---

## Geopolitical Risk Analysis

### Country Concentration

**High Geopolitical Risk** (>75% from single country):
- **4,387 entities** (23.1% of total)
- **64.2 million tons** at risk (36.7% of tonnage)

**Critical Examples:**

| Entity | Primary Country | % from Country | Tonnage | Risk Factor |
|--------|-----------------|----------------|---------|-------------|
| **Saudi Refining Inc** | Unknown (High Seas) | 100% | 15.0M tons | Crude oil transshipment dependency |
| **Irving Oil** | Canada | 99.6% | 18.3M tons | Single refinery supply chain |
| **Ternium** | Brazil | 80.1% | 8.4M tons | Steel slab concentration |
| **PMI Trading** | Mexico | 96.9% | 7.1M tons | Mexican crude dependency |
| **Monroe Energy** | Nigeria | 78.3% | 5.8M tons | West African crude risk |

### Geographic Diversification Leaders

| Entity | Countries | Top Country % | Resilience Score |
|--------|-----------|---------------|------------------|
| **Chevron** | 40 | 25.8% (Venezuela) | 94.5 |
| **ExxonMobil** | 33 | 29.0% (Netherlands) | 94.5 |
| **Valero** | 31 | 37.7% (Mexico) | 93.9 |
| **Vitol** | 31 | 15.2% (Neth. Antilles) | 97.2 |
| **BP** | 30 | 15.6% (Brazil) | 96.0 |

---

## Case Study: Top 20 Entities by Tonnage

### 1. Chevron - 58.7M tons (HIGHLY DIVERSIFIED)

**Port Concentration:**
- **80 unique ports** across 40 countries
- **Port HHI: 1,106** (Low concentration)
- Top 3 ports: 53.9% of total
  - High Seas, North Pacific: 21.4%
  - Armuelles, Panama: 16.4%
  - Jose, Venezuela: 16.0%

**Supply Chain Assessment:**
- **Resilience Score: 94.5** (LOW RISK)
- **Geographic spread**: Americas (70%), Middle East (15%), Europe/Asia (15%)
- **Backup routes**: Multiple crude sources with no single point >25%
- **Strategic advantage**: Can pivot between Venezuelan, Panamanian, Algerian, and Mexican crude

**Verdict:** GOLD STANDARD for supply chain resilience in crude oil sector

---

### 2. Valero - 43.5M tons (HIGHLY DIVERSIFIED)

**Port Concentration:**
- **69 unique ports** across 31 countries
- **Port HHI: 726** (Low concentration - BEST among top 20)
- Top 3 ports: 39.1% of total
  - Dos Bocas, Mexico: 15.1%
  - Orangestad, Aruba: 12.3%
  - High Seas, South Pacific: 11.7%

**Supply Chain Assessment:**
- **Resilience Score: 93.9** (LOW RISK)
- **Mexico concentration**: 37.7% (moderate geopolitical risk)
- **Alternative sources**: Iraq (6%), Canada (8%), Aruba (13%)
- **Strategic flexibility**: Can switch between Mexican, Middle Eastern, and Caribbean crude

**Verdict:** EXEMPLARY diversification - proves Mexican concentration answerable

---

### 3. Irving Oil - 18.3M tons (CRITICAL SINGLE-SOURCE RISK)

**Port Concentration:**
- **3 ports** (2 in Canada, 1 in Netherlands)
- **Port HHI: 9,898** (Very high concentration - CRITICAL)
- Saint John, NB, Canada: **99.5%** of total

**Supply Chain Assessment:**
- **Resilience Score: 18.0** (HIGH RISK - CRITICAL)
- **Single refinery dependency**: Almost all imports from own Saint John refinery
- **No geographic diversification**: 99.6% from Canada
- **Backup capacity**: Minimal (0.4% from Netherlands)

**Vulnerability Analysis:**
- **Disruption risk**: Single port closure = 99.5% supply loss
- **Geopolitical risk**: LOW (stable Canada)
- **Operational risk**: HIGH (single facility dependency)
- **Market position**: Vertically integrated refiner (explains concentration)

**Verdict:** HIGHEST CONCENTRATION among major importers - acceptable given vertical integration

---

### 4. Martin Marietta - 8.5M tons (MODERATE SINGLE-SOURCE RISK)

**Port Concentration:**
- **2 ports** (Canada 61.5%, Bahamas 38.5%)
- **Port HHI: 5,265** (Very high concentration)
- Auld's Cove, NS, Canada: 61.5%
- Freeport, Grand Bahama: 38.5%

**Supply Chain Assessment:**
- **Resilience Score: 38.7** (MODERATE RISK)
- **Product**: Aggregates/crushed stone (limited source options)
- **Geographic constraint**: Quarry locations dictate ports
- **Backup source**: Bahamas provides 38.5% redundancy

**Vulnerability Analysis:**
- **Primary dependency**: Canadian quarry for 61.5%
- **Secondary source**: Bahamas aggregates (38.5% is meaningful backup)
- **Industry context**: Aggregates naturally concentrated (quarry proximity)

**Verdict:** MODERATE RISK - acceptable for commodity aggregates sector

---

### 5. Saudi Refining Inc - 15.0M tons (CRITICAL OPACITY RISK)

**Port Concentration:**
- **1 port**: High Seas, Gulf of Mexico: **100%**
- **Port HHI: 10,000** (Maximum concentration - CRITICAL)

**Supply Chain Assessment:**
- **Resilience Score: 27.5** (HIGH RISK - CRITICAL)
- **Opacity issue**: "High Seas" = transshipment (true origin unknown)
- **Single shipper**: Bolanter Corporation (100%)
- **Geographic mystery**: Listed country = Mexico (0.3% of tonnage?!)

**Vulnerability Analysis:**
- **Data quality concern**: High Seas port suggests ship-to-ship transfers
- **True origin unknown**: Likely Saudi crude via transshipment
- **Operational complexity**: Transshipment adds supply chain nodes
- **Regulatory risk**: High Seas operations face oversight challenges

**Verdict:** CRITICAL RISK due to opacity - true diversification unknown

---

### 6-10: Additional High-Volume Importers

| Rank | Entity | Tonnage | Ports | Port HHI | Resilience | Risk |
|------|--------|---------|-------|----------|------------|------|
| 6 | **PBF Energy** | 18.3M | 33 | 1,539 | 95.2 | LOW |
| 7 | **Marathon** | 17.9M | 47 | 1,149 | 93.6 | LOW |
| 8 | **Emirates Aluminium** | 15.3M | 75 | 4,114 | 77.4 | LOW |
| 9 | **Ecopetrol** | 10.2M | 7 | 2,764 | 57.9 | MODERATE |
| 10 | **Ternium** | 8.4M | 26 | 5,549 | 69.8 | LOW |

**Pattern:** Oil refiners/traders = highly diversified (HHI <1,500). Specialized commodities (steel, aluminum) = moderate concentration.

---

## Most Diversified Entities (Top 10)

Ranked by **Resilience Score** (0-100):

| Rank | Entity | Score | Ports | Countries | Port HHI | Primary Source |
|------|--------|-------|-------|-----------|----------|----------------|
| 1 | **Vitol** | 97.2 | 54 | 31 | 547 | Sint Eustatius (14.5%) |
| 2 | **BP** | 96.0 | 39 | 22 | 632 | Angra Dos Reis (12.1%) |
| 3 | **Sunoco** | 96.3 | 21 | 19 | 721 | Freeport, Bahamas (9.7%) |
| 4 | **Puerto Rico Energy** | 95.6 | 32 | 16 | 553 | Mamonal, Colombia (9.9%) |
| 5 | **PBF Energy** | 95.2 | 33 | 12 | 1,539 | High Seas, GoM (33.1%) |
| 6 | **Chevron** | 94.5 | 80 | 40 | 1,106 | High Seas, NP (21.4%) |
| 7 | **ExxonMobil** | 94.5 | 75 | 33 | 932 | Rotterdam (25.2%) |
| 8 | **Gunvor USA** | 94.1 | 26 | 15 | 582 | Coatzacoalcos (10.1%) |
| 9 | **Diamond Green Diesel** | 93.9 | 32 | 16 | 721 | Rotterdam (17.1%) |
| 10 | **Valero** | 93.9 | 69 | 31 | 726 | Dos Bocas (15.1%) |

**Common Traits:**
- **Oil & gas traders/refiners** dominate top 10
- **No single source >35%** of total
- **Global reach**: Minimum 12 countries
- **Alternative routes**: Multiple backup suppliers

---

## Most Concentrated Entities (Top 10)

Ranked by **Port HHI** (highest = most risky):

| Rank | Entity | Port HHI | Primary Port | % | Tonnage | Risk |
|------|--------|----------|--------------|---|---------|------|
| 1 | **Saudi Refining** | 10,000 | High Seas, GoM | 100% | 15.0M | CRITICAL |
| 2 | **Atalco Gramercy** | 10,000 | Port Rhoades, Jamaica | 100% | 4.0M | CRITICAL |
| 3 | **Eucatex** | 10,000 | Sao Paulo, Brazil | 100% | 3.6M | CRITICAL |
| 4 | **Compass Minerals** | 10,000 | Goderich, Canada | 100% | 3.3M | CRITICAL |
| 5 | **Aes Puerto Rico** | 10,000 | Puerto Drummond, Colombia | 100% | 2.5M | CRITICAL |
| 6 | **Blue Water Industries** | 10,000 | Newfoundland, Canada | 100% | 1.8M | CRITICAL |
| 7 | **Wilmar Oleo** | 10,000 | Rotterdam, Netherlands | 100% | 1.8M | CRITICAL |
| 8 | **Dow Europe F412** | 10,000 | Coatzacoalcos, Mexico | 100% | 0.9M | CRITICAL |
| 9 | **McInnis USA** | 10,000 | Montreal, Canada | 100% | 0.9M | CRITICAL |
| 10 | **Totalenergies Petro** | 10,000 | Le Havre, France | 100% | 0.9M | CRITICAL |

**Common Traits:**
- **Specialized commodities**: Salt, bauxite, cement, wood products
- **Vertically integrated**: Often own the source facility
- **Geographic constraints**: Limited alternative sources
- **Acceptable risk**: Many have no viable alternatives

---

## Supply Chain Resilience Insights

### Primary vs Secondary Routes Analysis

**Entities with Strong Backup Capacity** (Secondary source >20%):

| Entity | Primary | Secondary | Backup % | Strategy |
|--------|---------|-----------|----------|----------|
| **Martin Marietta** | Canada 61.5% | Bahamas 38.5% | 38.5% | Dual-source aggregates |
| **Celanese** | Mexico 99.8% | - | 0.2% | No meaningful backup |
| **Mosaic** | Peru 87.1% | - | 12.9% | Weak backup for phosphate |
| **Emirates Aluminium** | UAE 53.3% | Multiple | 46.7% | Diversified sand sources |

### Single-Point Failure Risk

**Critical Dependencies** (>80% from single port):

| Entity | Port | % Dependency | Tonnage | Commodity |
|--------|------|--------------|---------|-----------|
| **Irving Oil** | Saint John, NB | 99.5% | 18.3M | Refined products |
| **North American Marine** | Bulgaria | 99.2% | 3.4M | Steel pipe |
| **Fibria Celulose** | Brazil South | 64.4% | 3.8M | Wood pulp |
| **Coppersmith Global** | Sepetiba Bay | 99.2% | 5.0M | Steel products |
| **Perin Trading** | Brazil South | 100% | 3.0M | Steel slabs |

---

## Geopolitical Concentration Risks

### Entities with >75% from Single Country

**High Geopolitical Exposure:**

| Entity | Country | % | Tonnage | Risk Assessment |
|--------|---------|---|---------|-----------------|
| **Irving Oil** | Canada | 99.6% | 18.3M | LOW (stable ally) |
| **Ternium** | Brazil | 80.1% | 8.4M | LOW (stable trade partner) |
| **PMI Trading** | Mexico | 96.9% | 7.1M | MODERATE (USMCA stability) |
| **Monroe Energy** | Nigeria | 78.3% | 5.8M | HIGH (political instability) |
| **Fibria Celulose** | Brazil | 100% | 3.8M | LOW (commodity source) |
| **Suncor Energy** | Canada | 75.7% | 3.4M | LOW (domestic integration) |
| **PAR Hawaii** | Libya | 44.4% | 3.4M | CRITICAL (sanctions risk) |

**Key Insight:** Country concentration != high risk. Canada/Mexico concentration is acceptable; Libya/Nigeria = concerning.

---

## Alternative Routes & Backup Analysis

### Entities with Effective Backup Strategies

**Top 5 Most Resilient Supply Chains:**

#### 1. **Vitol** - The Gold Standard
- **Primary**: Sint Eustatius (14.5%)
- **Backup routes**: 53 additional ports
- **No single country >16%**
- **Strategy**: Global trading network with redundant sourcing

#### 2. **Chevron** - Geographic Mastery
- **Primary hemisphere**: Americas (Venezuela, Panama, Mexico)
- **Backup hemisphere**: Middle East (Algeria, Kuwait)
- **Pivot capability**: Can switch regions within weeks
- **Strategy**: Multi-continental crude sourcing

#### 3. **BP** - Balanced Portfolio
- **Primary regions**: Brazil (15.6%), Argentina (11.4%), Bahamas (10.7%)
- **No single country >16%**
- **Strategy**: South American crude + Caribbean transshipment

#### 4. **Valero** - Flexible Refining
- **Primary**: Mexico (37.7%) - moderate concentration
- **Strong backups**: Iraq (6%), Canada (8%), Aruba (13%)
- **Strategy**: Refinery network allows source switching

#### 5. **Marathon** - Crude Diversification
- **Primary**: Iraq (27.9%)
- **Strong backups**: Mexico (13.5%), Brazil (11.5%), Canada (7.9%)
- **Strategy**: Middle East + Americas balance

---

## Industry-Specific Concentration Patterns

### Oil Refiners - HIGHLY DIVERSIFIED
- **Avg HHI**: 1,127 (LOW)
- **Avg Ports**: 52
- **Avg Countries**: 24
- **Risk Level**: LOW

**Representative entities**: Chevron, Valero, ExxonMobil, Marathon, BP

---

### Commodity Traders - HIGHLY DIVERSIFIED
- **Avg HHI**: 763 (LOW)
- **Avg Ports**: 38
- **Avg Countries**: 21
- **Risk Level**: LOW

**Representative entities**: Vitol, Trafigura, PMI Trading, Gunvor

---

### Specialized Importers - HIGH CONCENTRATION
- **Avg HHI**: 7,842 (VERY HIGH)
- **Avg Ports**: 2.3
- **Avg Countries**: 1.8
- **Risk Level**: HIGH (but often acceptable)

**Representative entities**: Compass Minerals (salt), Eucatex (wood), Atalco (bauxite)

---

### Steel Importers - MODERATE CONCENTRATION
- **Avg HHI**: 3,214 (HIGH)
- **Avg Ports**: 12
- **Avg Countries**: 8
- **Risk Level**: MODERATE

**Representative entities**: ArcelorMittal, Ternium, Nucor

---

### Auto Manufacturers - HIGH CONCENTRATION
- **Avg HHI**: 5,683 (VERY HIGH)
- **Avg Ports**: 6
- **Avg Countries**: 3
- **Risk Level**: MODERATE-HIGH

**Representative entities**: Toyota (79% from Gamagori, Japan), Hyundai (72% from Onsan, S. Korea)

**Context**: Assembly plant locations dictate port concentration - acceptable risk

---

## Recommendations by Risk Level

### HIGH RISK Entities (11,627 entities, 43.4M tons)

**Immediate Actions:**
1. **Identify critical single-source dependencies** (>80% from one port)
2. **Evaluate backup suppliers** for top 3 commodities
3. **Assess disruption scenarios**: What if primary port closes for 3 months?

**Strategic Recommendations:**
- **Dual-sourcing**: Target 60/40 split minimum for critical commodities
- **Geographic diversification**: Source from 2+ countries when possible
- **Inventory buffers**: Maintain 90-day reserves for single-source commodities

### MODERATE RISK Entities (521 entities, 18.1M tons)

**Monitoring Actions:**
1. **Track concentration trends** (is HHI increasing or decreasing?)
2. **Evaluate geopolitical risks** of primary source countries
3. **Assess port infrastructure** at primary loading ports

**Strategic Recommendations:**
- **Maintain current diversification**
- **Develop contingency plans** for primary source disruption
- **Monitor alternative sources** for market opportunities

### LOW RISK Entities (6,817 entities, 113.5M tons)

**Best Practices:**
1. **Document diversification strategy** for internal teams
2. **Share learnings** with industry peers
3. **Monitor for over-diversification** (diminishing returns >30 ports)

**Strategic Recommendations:**
- **Optimize current network** (reduce complexity where possible)
- **Focus on cost efficiency** rather than additional diversification
- **Benchmark against industry leaders**

---

## Data Quality Notes

### Limitations

1. **"High Seas" ports**: 47 entities use "High Seas" designation, obscuring true origin
2. **Harmonization coverage**: Analysis limited to 379,245 harmonized records (11.9% of total)
3. **Transshipment opacity**: Caribbean/Bahamas ports may mask ultimate origin
4. **Shipper reliability**: Shipper_Harmonized has gaps for some entities

### Recommendations for Future Analysis

1. **Resolve "High Seas" origins**: Cross-reference with vessel tracking data
2. **Expand harmonization**: Target coverage of 50%+ records
3. **Add temporal analysis**: Track HHI trends over 2023-2025
4. **Incorporate vessel data**: Use vessel names/IMO to infer true origin

---

## Conclusion

The analysis reveals a **bifurcated landscape** in supply chain resilience:

### Well-Diversified Sectors (64.9% of tonnage)
- **Oil refiners and commodity traders** demonstrate exemplary diversification
- **Average 40+ ports, 20+ countries, HHI <1,000**
- **Strategic advantage**: Can respond to geopolitical shifts within weeks
- **Examples**: Chevron (80 ports), Valero (69 ports), Vitol (54 ports)

### Concentrated Sectors (24.8% of tonnage)
- **Specialized commodities** face structural concentration constraints
- **Single-source dependencies often unavoidable** (quarries, mines, refineries)
- **Risk is often acceptable** given vertical integration or commodity nature
- **Examples**: Salt (single mine), Bauxite (single deposit), Automotive (assembly plants)

### Strategic Imperatives

**For HIGH RISK entities:**
- **Accept concentration where alternatives don't exist** (e.g., Compass Minerals salt)
- **Aggressively diversify where alternatives exist** (e.g., crude oil)
- **Build inventory buffers** for single-source critical commodities

**For LOW RISK entities:**
- **Maintain current diversification levels**
- **Avoid over-diversification** (diminishing returns beyond optimal portfolio)
- **Focus on operational efficiency** within existing network

**For policymakers:**
- **Monitor geopolitical concentration** (especially Middle East, Russia, China)
- **Support infrastructure development** for alternative routes
- **Encourage data transparency** (eliminate "High Seas" opacity)

---

## Files Generated

1. **trade_route_concentration_v1.0.0.csv** - Main analysis file
   - 18,965 entities with complete metrics
   - Columns: Entity, Tonnage, Ports, HHI, Resilience Score, Risk Level

2. **trade_route_concentration_detail_v1.0.0.csv** - Detailed route breakdown
   - 1,333 entity-port-country-shipper combinations
   - Top 50 entities by tonnage
   - Route ranking and percentage breakdowns

3. **entity_case_studies_v1.0.0.txt** - Deep dive analysis
   - 10 major entities (Chevron, Valero, Irving, etc.)
   - Complete port/country/shipper breakdowns
   - Strategic assessment for each

---

## Appendix: Technical Details

### Analysis Parameters
- **Dataset**: panjiva_imports_2024_HARMONIZED_v1.1.0.csv
- **Total records**: 3,184,323
- **Harmonized records**: 379,245 (11.9%)
- **Unique entities**: 18,965
- **Total tonnage**: 174,867,128 tons
- **Analysis date**: 2026-02-06
- **Runtime**: ~16 minutes

### HHI Calculation Example
Entity importing from 3 ports:
- Port A: 50% (2,500 squared)
- Port B: 30% (900 squared)
- Port C: 20% (400 squared)
- **HHI = 2,500 + 900 + 400 = 3,800** (High concentration)

### Resilience Score Calculation
Example (Chevron):
- Port diversity: (80/10) = 8.0 → capped at 1.0 → **25 points**
- Country diversity: (40/5) = 8.0 → capped at 1.0 → **25 points**
- Port HHI: (10,000 - 1,106) / 10,000 = 0.889 → **22.2 points**
- Country HHI: (10,000 - 1,104) / 10,000 = 0.890 → **22.2 points**
- **Total: 94.4 points** (LOW RISK)

---

**Report prepared by:** Trade Route Concentration Analysis v1.0.0
**Analysis date:** 2026-02-06
**Data source:** Panjiva Imports 2024 (Harmonized v1.1.0)
**Contact:** See project documentation for questions

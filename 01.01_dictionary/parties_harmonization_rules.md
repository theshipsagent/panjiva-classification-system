# Parties Harmonization Dictionary - Usage Guide

## Overview

This harmonization dictionary provides canonical entity matching for maritime cargo shipments. It resolves name variations, validates cargo context, and returns standardized party names with confidence scores.

## Dictionary Structure

Each entity in `parties_harmonization_master.json` contains:

- **canonical_name**: Official company name (standardized output)
- **entity_type**: Business category (Refiner, Trader, Manufacturer, Carrier, etc.)
- **name_patterns**: List of variations, abbreviations, subsidiaries, and common misspellings
- **cargo_context**: Expected cargo characteristics
  - **hs2_codes**: List of HS2 chapter codes typically handled
  - **keywords**: Cargo description keywords (positive indicators)
- **ports**: Known ports of operation
- **headquarters**: Company headquarters location
- **notes**: Additional context (subsidiaries, mergers, special cases)

## Matching Algorithm

### Phase 1: Name Normalization

The harmonization function performs these preprocessing steps:

1. **Convert to uppercase** for case-insensitive matching
2. **Remove legal suffixes**: INC, LLC, LTD, CORP, CORPORATION, LIMITED, SA, AG, PLC, NV
3. **Remove generic terms**: INTERNATIONAL, GLOBAL, TRADING, COMPANY, GROUP
4. **Remove punctuation**: Dots, commas, hyphens (except in compound names)
5. **Normalize whitespace**: Multiple spaces to single space, trim

Example transformations:
```
"Valero Marketing and Supply Company, LLC" → "VALERO MARKETING SUPPLY"
"Cemex Trading USA, Inc." → "CEMEX TRADING USA"
"BASF Corporation" → "BASF"
```

### Phase 2: Pattern Matching

The algorithm searches for matches using these strategies:

1. **Exact substring match**: Check if normalized input contains any pattern from `name_patterns`
2. **Pattern substring match**: Check if any pattern is contained in normalized input
3. **Word-level match**: Extract key entity identifier (first significant word)

Matching priority:
- Exact match on full pattern (highest confidence)
- Substring match on longer patterns (medium-high confidence)
- Core entity word match (medium confidence)
- Partial word match (lower confidence)

### Phase 3: Cargo Context Validation

Once a potential match is found, the algorithm validates using cargo context:

**HS2 Code Validation:**
- Extract HS2 (first 2 digits) from provided HS code
- Check if it matches any code in entity's `hs2_codes` list
- Special case: "ALL" matches any HS2 code (for ocean carriers)

**Keyword Validation:**
- Normalize cargo description (uppercase, remove punctuation)
- Check for presence of keywords from entity's keyword list
- Calculate keyword match score

**Validation Scoring:**
```
HS2 match: +40 points
Each keyword match: +10 points
Port match (if provided): +20 points
Base pattern match: +30 points
```

### Phase 4: Confidence Calculation

Final confidence score (0-100):

```python
confidence = min(100, base_score + context_score)

where:
base_score = 30 (exact pattern match) or 20 (partial match)
context_score = hs2_bonus + keyword_bonus + port_bonus
```

Confidence thresholds:
- **90-100**: Very high confidence (exact pattern + strong context)
- **70-89**: High confidence (good pattern + context match)
- **50-69**: Medium confidence (pattern match, weak context)
- **30-49**: Low confidence (weak pattern, no context)
- **<30**: No match (reject)

## Keyword Weighting System

### Positive Keywords (Relevant Indicators)

Each entity has a curated list of cargo keywords that indicate relevance. Examples:

**Petroleum Refiners:**
- Primary: CRUDE, PETROLEUM, GASOLINE, DIESEL, NAPHTHA
- Secondary: FUEL OIL, JET FUEL, AVIATION FUEL

**Cement Manufacturers:**
- Primary: CEMENT, CLINKER, CONCRETE
- Secondary: LIMESTONE, AGGREGATE, GYPSUM

**Steel Manufacturers:**
- Primary: STEEL, IRON, SLAB
- Secondary: COIL, SHEET, PLATE, REBAR, BEAM

### Negative Keywords (Irrelevant Indicators)

The algorithm also checks for incompatible cargo that would disqualify a match:

**Petroleum refiner receiving:**
- CEMENT, STEEL, GRAIN → Likely incorrect match

**Cement company receiving:**
- CRUDE OIL, GASOLINE → Likely incorrect match

Implementation:
```python
# Deduct points for incompatible cargo
if entity_type == "Petroleum Refiner" and "CEMENT" in cargo_desc:
    confidence -= 30
```

## Disambiguation Examples

### Example 1: Shell Oil vs Shell Chemical

**Input:** Party="SHELL TRADING", Cargo="ETHYLENE", HS2="29"

**Analysis:**
- Pattern matches: SHELL entity (petroleum refiner)
- HS2 "29" matches (organic chemicals - also in Shell's context)
- Keyword "ETHYLENE" matches (petrochemical product)
- **Result**: Shell Oil Company (confidence: 85)

**Note:** Shell operates both refining and petrochemical businesses. The HS2 code "29" and "ETHYLENE" indicate petrochemical division, but canonical name remains Shell Oil Company as parent entity.

### Example 2: Marathon Petroleum vs Marathon Oil

**Input:** Party="MARATHON", Cargo="CRUDE OIL", HS2="27"

**Analysis:**
- Pattern matches: MARATHON entity
- HS2 "27" matches (petroleum products)
- Keywords match: CRUDE, OIL
- **Result**: Marathon Petroleum Corporation (confidence: 95)

**Note:** Marathon Petroleum (refining) and Marathon Oil (exploration/production) split in 2011. The dictionary uses Marathon Petroleum as canonical name for refining operations.

### Example 3: Lafarge vs Holcim vs LafargeHolcim

**Input:** Party="LAFARGE CEMENT", Cargo="CLINKER", HS2="25"

**Analysis:**
- Pattern "LAFARGE" found in HOLCIM entity patterns
- HS2 "25" matches (mineral products)
- Keyword "CLINKER" matches
- **Result**: Holcim Ltd (confidence: 90)

**Note:** Lafarge and Holcim merged in 2015 to form LafargeHolcim (now Holcim). All variations map to canonical "Holcim Ltd".

### Example 4: Distinguishing Trafigura vs Vitol

**Input:** Party="TRAFIGURA BEHEER", Cargo="COPPER CONCENTRATE", HS2="26"

**Analysis:**
- Pattern "TRAFIGURA BEHEER" matches TRAFIGURA entity
- HS2 "26" matches (ores and minerals - Trafigura trades metals)
- Keyword "COPPER" matches
- **Result**: Trafigura Group Pte Ltd (confidence: 95)

**Contrast with Vitol:**
- Vitol focuses primarily on petroleum (HS2 "27")
- Vitol keywords: crude, naphtha, diesel, gasoline
- Trafigura trades both oil AND metals
- Cargo context (copper, HS2=26) points to Trafigura

### Example 5: Subsidiary Recognition

**Input:** Party="DIAMOND GREEN DIESEL LLC", Cargo="RENEWABLE DIESEL", HS2="27"

**Analysis:**
- Pattern "DIAMOND GREEN DIESEL" found in VALERO entity patterns
- HS2 "27" matches
- Keywords match: DIESEL, RENEWABLE
- **Result**: Valero Energy Corporation (confidence: 95)

**Note:** Dictionary explicitly lists subsidiaries under parent company patterns. DGD is a Valero subsidiary but maps to parent canonical name.

## Adding New Entities

To add a new entity to the dictionary:

### Step 1: Research Entity Profile

Gather information:
- Official legal name
- Common variations and abbreviations
- Known subsidiaries or trading names
- Primary business type
- Cargo types handled
- Ports of operation
- Parent company relationships

### Step 2: Define Cargo Context

Identify relevant HS2 codes:
- Use HS2 chapter code (first 2 digits)
- List all chapters the entity typically handles
- Examples:
  - Petroleum: "27"
  - Chemicals: "28", "29", "38"
  - Iron/Steel: "72", "73"
  - Grains: "10", "12"

Create keyword list:
- Include product names (CRUDE, GASOLINE, CEMENT, etc.)
- Include material types (PETROLEUM, STEEL, GRAIN, etc.)
- Include process terms (REFINED, CLINKER, SLAB, etc.)
- Use uppercase
- Focus on discriminating terms (avoid generic words like "CARGO")

### Step 3: Add JSON Entry

```json
"ENTITY_KEY": {
  "canonical_name": "Official Company Name Ltd.",
  "entity_type": "Manufacturer|Trader|Refiner|Carrier|etc",
  "name_patterns": [
    "PRIMARY NAME",
    "COMMON ABBREVIATION",
    "SUBSIDIARY NAME",
    "ALTERNATIVE SPELLING"
  ],
  "cargo_context": {
    "hs2_codes": ["27", "29"],
    "keywords": ["KEYWORD1", "KEYWORD2", "KEYWORD3"]
  },
  "ports": ["Port1", "Port2"],
  "headquarters": "City, Country",
  "notes": "Additional context about mergers, subsidiaries, etc."
}
```

### Step 4: Test the Entry

Use the test script to validate:
```python
# Test various name patterns
result = harmonize_party("SUBSIDIARY NAME LLC", "KEYWORD1 PRODUCT", "2701", "Port1")
assert result["canonical_name"] == "Official Company Name Ltd."
assert result["confidence"] >= 70

# Test cargo context validation
result = harmonize_party("PRIMARY NAME", "KEYWORD2", "2900", "")
assert result["confidence"] >= 60

# Test negative case (wrong cargo)
result = harmonize_party("PRIMARY NAME", "INCOMPATIBLE CARGO", "9999", "")
assert result["confidence"] < 50 or result["canonical_name"] is None
```

## Testing Methodology

### Unit Tests

Test individual components:

1. **Name normalization:**
   ```python
   assert normalize_name("Valero Marketing, LLC") == "VALERO MARKETING"
   ```

2. **Pattern matching:**
   ```python
   assert find_pattern_match("CEMEX USA INC", patterns) == "CEMEX"
   ```

3. **HS2 extraction:**
   ```python
   assert extract_hs2("270900") == "27"
   ```

4. **Keyword matching:**
   ```python
   assert count_keyword_matches("CRUDE PETROLEUM", ["CRUDE", "PETROLEUM"]) == 2
   ```

### Integration Tests

Test complete harmonization flow:

```python
# Test exact match with strong context
result = harmonize_party(
    party_name="VALERO MARKETING LLC",
    cargo_desc="CRUDE PETROLEUM",
    hs_code="2709",
    port="Houston"
)
assert result["canonical_name"] == "Valero Energy Corporation"
assert result["confidence"] >= 90

# Test partial match with weak context
result = harmonize_party(
    party_name="VALERO",
    cargo_desc="FUEL",
    hs_code="2710",
    port=""
)
assert result["canonical_name"] == "Valero Energy Corporation"
assert 60 <= result["confidence"] < 90

# Test no match (incompatible cargo)
result = harmonize_party(
    party_name="VALERO",
    cargo_desc="CEMENT CLINKER",
    hs_code="2523",
    port=""
)
assert result["canonical_name"] is None or result["confidence"] < 40
```

### Edge Cases

Test boundary conditions:

1. **Empty or null inputs:**
   ```python
   assert harmonize_party("", "", "", "") == {"canonical_name": None, "confidence": 0}
   ```

2. **Very short names:**
   ```python
   result = harmonize_party("BP", "CRUDE", "2709", "")
   assert result["canonical_name"] == "BP America Inc."
   ```

3. **Multiple potential matches:**
   ```python
   # When two entities could match, cargo context should disambiguate
   result = harmonize_party("INTERNATIONAL TRADING", "CRUDE", "27", "")
   # Should pick entity with best cargo context match
   ```

4. **Special characters:**
   ```python
   result = harmonize_party("CEMA-X, S.A. de C.V.", "CEMENT", "25", "")
   # Should still match CEMEX despite punctuation
   ```

### Performance Tests

For large datasets:

1. **Batch processing:**
   - Test 10,000 records in < 30 seconds
   - Verify memory usage stays reasonable

2. **Caching:**
   - Implement lookup cache for repeated party names
   - Verify cache hit rate > 80% on real data

## Common Pitfalls and Solutions

### Pitfall 1: Over-matching on Short Names

**Problem:** "BP OIL" matches both BP and other companies with "BP" in name

**Solution:** Require minimum pattern length (3+ characters) or use cargo context to disambiguate

### Pitfall 2: Legal Entity vs Trading Name

**Problem:** "SHELL TRADING" is trading division of Shell Oil Company

**Solution:** Map all divisions/trading names to parent company canonical name in `name_patterns`

### Pitfall 3: Merged Companies

**Problem:** Historical data has "LAFARGE" but current entity is "HOLCIM"

**Solution:** Include legacy names in `name_patterns` with note explaining merger

### Pitfall 4: Generic Terms

**Problem:** "INTERNATIONAL TRADING COMPANY" could match many entities

**Solution:** Require specific entity identifier beyond generic terms; use cargo context heavily

### Pitfall 5: Port Ambiguity

**Problem:** Many companies operate in Houston

**Solution:** Port matching provides bonus points but should not be primary discriminator

## Performance Optimization

### Indexing Strategy

For large-scale operations:

1. **Create inverted index:**
   ```python
   # Build pattern -> entity_key mapping
   pattern_index = {}
   for entity_key, entity_data in dictionary.items():
       for pattern in entity_data["name_patterns"]:
           pattern_index[pattern] = entity_key
   ```

2. **HS2 code index:**
   ```python
   # Build hs2 -> [entity_keys] mapping
   hs2_index = defaultdict(list)
   for entity_key, entity_data in dictionary.items():
       for hs2 in entity_data["cargo_context"]["hs2_codes"]:
           hs2_index[hs2].append(entity_key)
   ```

3. **Keyword index:**
   ```python
   # Build keyword -> [entity_keys] mapping
   keyword_index = defaultdict(list)
   for entity_key, entity_data in dictionary.items():
       for keyword in entity_data["cargo_context"]["keywords"]:
           keyword_index[keyword].append(entity_key)
   ```

### Caching Strategy

```python
from functools import lru_cache

@lru_cache(maxsize=10000)
def harmonize_party_cached(party_name, cargo_desc, hs_code, port):
    return harmonize_party(party_name, cargo_desc, hs_code, port)
```

### Batch Processing

For processing entire datasets:

```python
def harmonize_dataframe(df):
    """
    Harmonize parties in bulk with progress tracking
    """
    results = []
    for idx, row in df.iterrows():
        result = harmonize_party(
            row['party_name'],
            row['cargo_desc'],
            row['hs_code'],
            row['port']
        )
        results.append(result)
        if idx % 1000 == 0:
            print(f"Processed {idx} records...")

    df['canonical_name'] = [r['canonical_name'] for r in results]
    df['confidence'] = [r['confidence'] for r in results]
    return df
```

## Maintenance and Updates

### Monthly Review Tasks

1. **Check for company mergers/acquisitions:**
   - Update canonical names if needed
   - Add merged entity names to patterns
   - Update notes

2. **Review low-confidence matches:**
   - Analyze records with confidence < 50
   - Add missing patterns or improve cargo context

3. **Add new entities:**
   - Identify frequently appearing non-matched parties
   - Research and add to dictionary

### Quality Metrics

Track these metrics:

- **Match rate:** % of records with confidence >= 70
- **No-match rate:** % of records with no match
- **High-confidence rate:** % of records with confidence >= 90
- **Average confidence:** Mean confidence across all matches

Target benchmarks:
- Match rate: > 85%
- High-confidence rate: > 60%
- Average confidence: > 75

## API Usage Example

```python
import json

# Load dictionary
with open('parties_harmonization_master.json', 'r') as f:
    party_dictionary = json.load(f)

# Harmonize a single party
result = harmonize_party(
    party_name="VALERO MARKETING AND SUPPLY LLC",
    cargo_desc="CRUDE PETROLEUM OIL",
    hs_code="270900",
    port="Houston"
)

print(f"Canonical Name: {result['canonical_name']}")
print(f"Confidence: {result['confidence']}")
print(f"Entity Type: {result['entity_type']}")
print(f"Match Details: {result['match_details']}")

# Output:
# Canonical Name: Valero Energy Corporation
# Confidence: 95
# Entity Type: Petroleum Refiner
# Match Details: {'pattern_matched': 'VALERO MARKETING', 'hs2_match': True, 'keyword_matches': ['CRUDE', 'PETROLEUM'], 'port_match': True}
```

## Version History

**Version 1.0** (2026-01-12)
- Initial release
- 50+ major entities across 7 industry sectors
- Support for petroleum, cement, steel, metals, agricultural, forest products, and chemical industries
- Cargo context validation with HS2 codes and keywords
- Confidence scoring algorithm

## Future Enhancements

Planned improvements:

1. **Fuzzy matching:** Levenshtein distance for misspellings
2. **Machine learning:** Train model on labeled match data
3. **Multi-language support:** Handle non-English party names
4. **Temporal awareness:** Handle company names that changed over time
5. **Relationship mapping:** Track parent-subsidiary relationships explicitly
6. **API endpoint:** REST API for real-time harmonization requests

## Contact and Support

For questions, issues, or suggestions:
- Review this documentation
- Check test cases in `parties_harmonization_test.py`
- Examine dictionary entries in `parties_harmonization_master.json`

## License

This harmonization dictionary is provided for maritime trade data analysis and research purposes.

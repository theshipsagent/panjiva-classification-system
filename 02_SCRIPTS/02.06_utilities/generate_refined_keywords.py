"""
Generate refined keyword analysis with categorization
Filters out noise, identifies phrases, separates primary from descriptors

Author: WSD3 / Claude Code
Date: 2026-01-14
"""

import pandas as pd
from pathlib import Path
from datetime import datetime
from collections import Counter
import re

def stamp(msg):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

# Define keyword categories
NOISE_WORDS = {
    # Units of measure
    'PCS', 'BBLS', 'QTY', 'TONS', 'TON', 'BARRELS', 'BARREL', 'KGS', 'KGM', 'LBS',
    'METRIC', 'PIECES', 'PIECE', 'UNIT', 'UNITS', 'PACKAGES', 'PACKAGE', 'PKG',
    # Common connectors/descriptors
    'TOTAL', 'AND', 'FOR', 'THE', 'WITH', 'FROM', 'MADE', 'PER', 'NET', 'GROSS',
    'WEIGHT', 'VALUE', 'CODE', 'NUMBER', 'ONE', 'TWO', 'NEW', 'USED', 'USA',
    # Packing terms
    'PALLETS', 'PALLET', 'BOX', 'BOXES', 'CRATE', 'CRATES', 'ACCESSORIES',
    'MARKS', 'BOARD', 'FREIGHT', 'PAYABLE', 'SHIPPED', 'CLEAN', 'EMPTY',
    # Document terms
    'INVOICE', 'ORDER', 'FORM', 'CBP', 'CBPF', 'DOCUMENTS', 'DESCRIPTION',
    # Common numbers/codes
    'PIN', 'SERIAL', 'MODEL', 'TYPE', 'STANDARD', 'SPECIFICATION', 'SPEC',
    'CAB', 'DIM', 'DIMS', 'EXP', 'NCM', 'API', 'ASTM', 'KGS', 'MSO'
}

DESCRIPTOR_WORDS = {
    # Temperature/Process
    'HOT', 'COLD', 'ROLLED', 'GALVANIZED', 'COATED', 'PRIME', 'SEAMLESS',
    'WELDED', 'ERW', 'DIP', 'ZINC', 'STAINLESS', 'DEFORMED', 'REINFORCING',
    # Quality/Grade
    'PRIME', 'SCRAP', 'GRADE', 'QUALITY', 'STANDARD', 'PREMIUM',
    # Size/Shape descriptors
    'FLAT', 'WIDE', 'HEAVY', 'LIGHT', 'THICK', 'THIN', 'LONG', 'SHORT',
    # State
    'FRESH', 'DRIED', 'FROZEN', 'BULK', 'PACKED', 'LOOSE', 'BUNDLED'
}

# Key phrases to identify (these are STRONG matches)
KEY_PHRASES = [
    'CRUDE OIL', 'STEEL PIPE', 'STEEL PIPES', 'HOT ROLLED', 'COLD ROLLED',
    'LINE PIPE', 'STEEL COIL', 'STEEL COILS', 'STEEL SHEET', 'STEEL SHEETS',
    'PIG IRON', 'IRON ORE', 'CEMENT CLINKER', 'PORTLAND CEMENT',
    'TUBULAR GOODS', 'MOTOR VEHICLE', 'MOTOR VEHICLES',
    'PETROLEUM OIL', 'FUEL OIL', 'PALM OIL',
    'FLAT ROLLED', 'SEAMLESS PIPE', 'WELDED PIPE',
    'LUMBER', 'PAPER', 'PULP', 'ALUMINUM', 'COPPER',
    'WHEAT', 'CORN', 'BARLEY', 'SOYBEAN'
]

def extract_phrases(text):
    """Extract key phrases from text"""
    text_upper = text.upper()
    found_phrases = []
    for phrase in KEY_PHRASES:
        if phrase in text_upper:
            found_phrases.append(phrase)
    return found_phrases

def categorize_word(word):
    """Categorize a word as NOISE, DESCRIPTOR, or PRIMARY"""
    word = word.upper()
    if word in NOISE_WORDS:
        return 'NOISE'
    elif word in DESCRIPTOR_WORDS:
        return 'DESCRIPTOR'
    else:
        return 'PRIMARY'

# Paths
PANJIVA_DIR = Path(r"G:\My Drive\LLM\project_manifest\00_DATA/00.02_PREPROCESSED\01_01_panjiva_imports_step_one")
OUTPUT_FILE = Path(r"G:\My Drive\LLM\project_manifest\user_notes\hs_code_keywords_refined.csv")

stamp("=== Generate Refined Keywords Analysis ===")
stamp("")

# Load Panjiva data
stamp("Loading Panjiva data (all 3 years)...")
panjiva_files = list(PANJIVA_DIR.glob("*.csv"))

# Dictionary to accumulate data by HS4
hs4_keywords = {}

for file in panjiva_files:
    stamp(f"  Processing: {file.name}")
    df = pd.read_csv(file, dtype=str, low_memory=False)

    # Filter to records with HS4 codes
    df_with_hs4 = df[df['HS4'].notna()].copy()
    stamp(f"    Records with HS4: {len(df_with_hs4):,}")

    # Group by HS4
    for hs4, group in df_with_hs4.groupby('HS4'):
        if hs4 not in hs4_keywords:
            hs4_keywords[hs4] = {
                'goods_shipped_text': [],
                'record_count': 0
            }

        # Collect Goods Shipped text
        goods = group['Goods Shipped'].dropna()
        hs4_keywords[hs4]['goods_shipped_text'].extend(goods.tolist())
        hs4_keywords[hs4]['record_count'] += len(group)

stamp("")
stamp(f"Total unique HS4 codes: {len(hs4_keywords)}")

# Analyze keywords for each HS4
stamp("")
stamp("Analyzing keywords by category...")

results = []

for hs4 in sorted(hs4_keywords.keys()):
    data = hs4_keywords[hs4]

    # Sample goods shipped text (first 1000 records)
    sample_text = ' '.join(data['goods_shipped_text'][:1000])

    # Extract phrases first
    phrases = extract_phrases(sample_text)
    phrase_counts = Counter(phrases)
    top_phrases = [phrase for phrase, count in phrase_counts.most_common(10)]
    phrases_str = ', '.join(top_phrases)

    # Extract words
    words = re.findall(r'\b[A-Z]{3,}\b|\b[A-Z][a-z]{2,}\b', sample_text)

    # Categorize words
    primary_words = []
    descriptor_words = []
    noise_words = []

    for word in words:
        category = categorize_word(word)
        if category == 'PRIMARY':
            primary_words.append(word)
        elif category == 'DESCRIPTOR':
            descriptor_words.append(word)
        # Skip noise words

    # Get top words by category
    primary_counts = Counter(primary_words)
    top_primary = [word for word, count in primary_counts.most_common(10)]
    primary_str = ', '.join(top_primary)

    descriptor_counts = Counter(descriptor_words)
    top_descriptors = [word for word, count in descriptor_counts.most_common(8)]
    descriptors_str = ', '.join(top_descriptors)

    # Get HS2
    hs2 = hs4[:2] if len(hs4) >= 2 else ''

    results.append({
        'HS2': hs2,
        'HS4': hs4,
        'Key_Phrases': phrases_str,
        'Primary_Keywords': primary_str,
        'Descriptor_Keywords': descriptors_str,
        'Record_Count': data['record_count']
    })

# Create DataFrame
df_results = pd.DataFrame(results)

# Sort by record count
df_results = df_results.sort_values('Record_Count', ascending=False)

stamp(f"  Analyzed keywords for {len(df_results)} HS4 codes")

# Show examples
stamp("")
stamp("Examples of refined keywords:")
stamp("")

# Show steel example
steel_example = df_results[df_results['HS4'] == '7304'].iloc[0] if '7304' in df_results['HS4'].values else None
if steel_example is not None:
    stamp("HS4 7304 (Seamless Steel Tubes/Pipes):")
    stamp(f"  Key Phrases: {steel_example['Key_Phrases']}")
    stamp(f"  Primary Keywords: {steel_example['Primary_Keywords']}")
    stamp(f"  Descriptors: {steel_example['Descriptor_Keywords']}")
    stamp("")

# Show oil example
oil_example = df_results[df_results['HS4'] == '2709'].iloc[0] if '2709' in df_results['HS4'].values else None
if oil_example is not None:
    stamp("HS4 2709 (Crude Petroleum Oil):")
    stamp(f"  Key Phrases: {oil_example['Key_Phrases']}")
    stamp(f"  Primary Keywords: {oil_example['Primary_Keywords']}")
    stamp(f"  Descriptors: {oil_example['Descriptor_Keywords']}")
    stamp("")

# Show coil example
coil_example = df_results[df_results['HS4'] == '7210'].iloc[0] if '7210' in df_results['HS4'].values else None
if coil_example is not None:
    stamp("HS4 7210 (Flat-rolled Steel, Coated):")
    stamp(f"  Key Phrases: {coil_example['Key_Phrases']}")
    stamp(f"  Primary Keywords: {coil_example['Primary_Keywords']}")
    stamp(f"  Descriptors: {coil_example['Descriptor_Keywords']}")
    stamp("")

# Save
stamp("")
stamp(f"Saving to: {OUTPUT_FILE.name}")
df_results.to_csv(OUTPUT_FILE, index=False)

stamp("")
stamp("Complete!")
stamp("")
stamp("Keyword categories:")
stamp(f"  - Key Phrases: Strong multi-word identifiers (e.g. 'CRUDE OIL')")
stamp(f"  - Primary Keywords: Standalone product terms (e.g. 'STEEL', 'PIPE')")
stamp(f"  - Descriptors: Modifiers/qualifiers (e.g. 'HOT', 'SEAMLESS', 'PRIME')")
stamp(f"  - Noise words filtered: Units, measures, common words")

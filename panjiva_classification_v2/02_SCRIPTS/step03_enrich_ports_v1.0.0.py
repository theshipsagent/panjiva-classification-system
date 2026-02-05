"""
Port Enrichment v1.0.0
======================

Purpose: Add port classification data to classified files

Enriches:
- Port_Consolidated (e.g., "New York", "Houston", "Delaware River")
- Port_Coast (e.g., "East", "West", "Gulf")
- Port_Region (e.g., "North Atlantic", "Gulf Coast", "Pacific")
- Port_Code (e.g., 1001, 4601)

Matching Logic:
1. Extract Census code from "Port of Discharge (D)" field
   Example: "New York, New York" → Try to find code 1001
2. Match against us_port_dictionary.csv
3. Fill in consolidated name, coast, region, code

Input:  Classified CSV (60 columns, port columns empty)
Output: Enriched CSV (60 columns, port columns filled)

Usage:
    python step03_enrich_ports_v1.0.0.py 2024
    python step03_enrich_ports_v1.0.0.py 2023
    python step03_enrich_ports_v1.0.0.py 2025

Author: WSD3 / Claude Code
Date: 2026-01-28
Version: 1.0.0
"""

import pandas as pd
import numpy as np
import sys
import logging
import re
from pathlib import Path
from datetime import datetime

# ============================================================================
# CONFIGURATION
# ============================================================================

PROJECT_ROOT = Path(__file__).parent.parent
PORT_DICT = Path(r"G:\My Drive\LLM\project_manifest\01_DICTIONARIES\01.02_ports\us_port_dictionary.csv")
INPUT_DIR = PROJECT_ROOT / "03_DATA" / "02_classified"
OUTPUT_DIR = PROJECT_ROOT / "03_DATA" / "03_enriched"
LOG_DIR = PROJECT_ROOT / "05_LOGS"

# Create directories
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Logging setup
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
log_file = LOG_DIR / f"step03_enrich_ports_{timestamp}.log"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

# ============================================================================
# PORT MATCHING LOGIC
# ============================================================================

def load_port_dictionary():
    """Load port dictionary and create lookup structures"""
    logging.info("Loading port dictionary...")

    if not PORT_DICT.exists():
        logging.error(f"Port dictionary not found: {PORT_DICT}")
        return None, None

    df_ports = pd.read_csv(PORT_DICT, dtype=str, encoding='utf-8')

    # Create lookup by Code
    port_lookup_code = {}
    for _, row in df_ports.iterrows():
        code = str(row['Code']).strip()
        port_lookup_code[code] = {
            'Port_Consolidated': str(row.get('Port_Consolidated', '')).strip(),
            'Port_Coast': str(row.get('Port_Coast', '')).strip(),
            'Port_Region': str(row.get('Port_Region', '')).strip(),
            'Port_Code': code
        }

    # Create lookup by Sked_D (port name)
    port_lookup_name = {}
    for _, row in df_ports.iterrows():
        sked_d = str(row.get('Sked_D_E', '')).strip().upper()
        if sked_d and sked_d != 'nan':
            port_lookup_name[sked_d] = {
                'Port_Consolidated': str(row.get('Port_Consolidated', '')).strip(),
                'Port_Coast': str(row.get('Port_Coast', '')).strip(),
                'Port_Region': str(row.get('Port_Region', '')).strip(),
                'Port_Code': str(row['Code']).strip()
            }

    logging.info(f"  Loaded {len(df_ports)} port records")
    logging.info(f"  Code lookup: {len(port_lookup_code)} entries")
    logging.info(f"  Name lookup: {len(port_lookup_name)} entries")

    return port_lookup_code, port_lookup_name

def extract_port_code(port_str):
    """
    Try to extract Census port code from port string
    Examples:
      "New York, New York" → Try to infer code 1001
      "Houston, Houston, Texas" → Try to infer code 2601
    """
    if pd.isna(port_str) or port_str == '':
        return None

    port_str = str(port_str).strip()

    # Look for 4-digit codes in parentheses or at end
    # Example: "New York (1001)" or "New York - 1001"
    match = re.search(r'[\(\-\s](\d{4})[\)\s]*$', port_str)
    if match:
        return match.group(1)

    return None

def normalize_port_name(port_str):
    """
    Normalize port name for matching
    "Houston, Houston, Texas" → "HOUSTON, TX"
    "New York, New York" → "NEW YORK, NY"
    "Port of Brunswick, Brunswick, Georgia" → "BRUNSWICK, GA"
    """
    if pd.isna(port_str) or port_str == '':
        return ''

    port_str = str(port_str).strip().upper()

    # Remove common prefixes
    port_str = re.sub(r'^(PORT OF|THE PORT OF|PORT AUTHORITY OF|REGIONAL PORT AUTHORITY)\s+', '', port_str)
    port_str = re.sub(r'\s+(PORT AUTHORITY|REGIONAL PORT AUTHORITY|STATE PORT AUTHORITY|PORTS AUTHORITY)$', '', port_str)

    # Split by commas
    parts = [p.strip() for p in port_str.split(',')]

    # Remove duplicates: "HOUSTON, HOUSTON, TEXAS" → "HOUSTON, TEXAS"
    if len(parts) >= 3 and parts[0] == parts[1]:
        parts = [parts[0], parts[2]]

    # Extract city and state
    if len(parts) >= 2:
        city = parts[-2]  # Second to last is usually city
        state = parts[-1]  # Last is usually state
    elif len(parts) == 1:
        # Just city name
        city = parts[0]
        state = ''
    else:
        return port_str

    # State abbreviations
    state_abbrev = {
        'TEXAS': 'TX', 'CALIFORNIA': 'CA', 'NEW YORK': 'NY',
        'FLORIDA': 'FL', 'LOUISIANA': 'LA', 'ALABAMA': 'AL',
        'MISSISSIPPI': 'MS', 'GEORGIA': 'GA', 'VIRGINIA': 'VA',
        'MARYLAND': 'MD', 'DELAWARE': 'DE', 'NEW JERSEY': 'NJ',
        'PENNSYLVANIA': 'PA', 'MASSACHUSETTS': 'MA', 'MAINE': 'ME',
        'WASHINGTON': 'WA', 'OREGON': 'OR', 'HAWAII': 'HI',
        'ALASKA': 'AK', 'PUERTO RICO': 'PR', 'SOUTH CAROLINA': 'SC',
        'NORTH CAROLINA': 'NC', 'CONNECTICUT': 'CT', 'RHODE ISLAND': 'RI'
    }

    state = state_abbrev.get(state, state)

    if state:
        return f"{city}, {state}"
    else:
        return city

def match_port(port_str, port_lookup_code, port_lookup_name):
    """
    Match port string against dictionary
    Returns dict with Port_Consolidated, Port_Coast, Port_Region, Port_Code
    """
    default = {
        'Port_Consolidated': '',
        'Port_Coast': '',
        'Port_Region': '',
        'Port_Code': ''
    }

    if pd.isna(port_str) or str(port_str).strip() == '':
        return default

    # Try 1: Extract and match by code
    code = extract_port_code(port_str)
    if code and code in port_lookup_code:
        return port_lookup_code[code]

    # Try 2: Normalize and match by name
    normalized = normalize_port_name(port_str)
    if normalized in port_lookup_name:
        return port_lookup_name[normalized]

    # Try 3: Partial match on city name
    city = normalized.split(',')[0].strip() if ',' in normalized else normalized
    for key, value in port_lookup_name.items():
        if key.startswith(city):
            return value

    return default

# ============================================================================
# ENRICHMENT FUNCTION
# ============================================================================

def enrich_ports(df, port_lookup_code, port_lookup_name):
    """Add port classification to dataframe"""
    logging.info("Enriching port data...")

    # Apply matching to each row
    port_data = df['Port of Discharge (D)'].apply(
        lambda x: match_port(x, port_lookup_code, port_lookup_name)
    )

    # Extract individual fields
    df['Port_Consolidated'] = port_data.apply(lambda x: x['Port_Consolidated'])
    df['Port_Coast'] = port_data.apply(lambda x: x['Port_Coast'])
    df['Port_Region'] = port_data.apply(lambda x: x['Port_Region'])
    df['Port_Code'] = port_data.apply(lambda x: x['Port_Code'])

    # Stats
    enriched = (df['Port_Code'] != '').sum()
    pct = enriched / len(df) * 100

    logging.info(f"  Ports enriched: {enriched:,} / {len(df):,} ({pct:.1f}%)")

    # Show top ports
    if enriched > 0:
        logging.info(f"\nTop 10 ports:")
        top_ports = df[df['Port_Code'] != '']['Port_Consolidated'].value_counts().head(10)
        for port, count in top_ports.items():
            pct = count / len(df) * 100
            logging.info(f"  {port}: {count:,} ({pct:.1f}%)")

    return df

# ============================================================================
# MAIN PROCESSING
# ============================================================================

def process_year(year):
    """Process a single year's classified file"""

    # Find latest classified file for this year
    pattern = f"panjiva_imports_{year}_classified*.csv"
    files = sorted(INPUT_DIR.glob(pattern), key=lambda x: x.stat().st_mtime, reverse=True)

    if not files:
        logging.error(f"No classified file found for {year} in {INPUT_DIR}")
        return False

    input_file = files[0]
    output_file = OUTPUT_DIR / f"panjiva_imports_{year}_enriched_v1.0.0_{timestamp}.csv"

    logging.info("="*70)
    logging.info(f"PROCESSING YEAR {year}")
    logging.info("="*70)
    logging.info(f"Input: {input_file.name}")
    logging.info(f"Output: {output_file.name}")

    try:
        # Load port dictionary
        port_lookup_code, port_lookup_name = load_port_dictionary()
        if not port_lookup_code:
            return False

        # Load classified data
        logging.info(f"\nLoading classified data...")
        df = pd.read_csv(input_file, dtype=str, low_memory=False)
        logging.info(f"  Loaded: {len(df):,} rows, {len(df.columns)} columns")

        # Enrich ports
        df = enrich_ports(df, port_lookup_code, port_lookup_name)

        # Save output
        logging.info(f"\nSaving enriched file...")
        df.to_csv(output_file, index=False)

        size_mb = output_file.stat().st_size / (1024*1024)
        logging.info(f"  Saved: {output_file.name}")
        logging.info(f"  Size: {size_mb:.1f} MB")
        logging.info(f"  Rows: {len(df):,}")
        logging.info(f"  Columns: {len(df.columns)}")

        # Verify output
        logging.info(f"\nVerifying output...")
        port_cols = ['Port_Consolidated', 'Port_Coast', 'Port_Region', 'Port_Code']
        for col in port_cols:
            filled = (df[col] != '').sum()
            pct = filled / len(df) * 100
            logging.info(f"  {col}: {filled:,} ({pct:.1f}%) filled")

        logging.info(f"\nCOMPLETED SUCCESSFULLY")
        return True

    except Exception as e:
        logging.error(f"Error processing {year}: {e}")
        import traceback
        logging.error(traceback.format_exc())
        return False

# ============================================================================
# MAIN
# ============================================================================

def main():
    if len(sys.argv) < 2:
        print("Usage: python step03_enrich_ports_v1.0.0.py <year>")
        print("Example: python step03_enrich_ports_v1.0.0.py 2024")
        sys.exit(1)

    year = sys.argv[1]

    logging.info("="*70)
    logging.info("PORT ENRICHMENT v1.0.0")
    logging.info("="*70)
    logging.info(f"Year: {year}")
    logging.info(f"Timestamp: {timestamp}")
    logging.info(f"Log: {log_file}")

    success = process_year(year)

    if success:
        logging.info("\n" + "="*70)
        logging.info("STATUS: SUCCESS")
        logging.info("="*70)
        logging.info(f"\nEnriched file ready for analysis/export")
    else:
        logging.error("\n" + "="*70)
        logging.error("STATUS: FAILED")
        logging.error("="*70)
        sys.exit(1)

if __name__ == "__main__":
    main()

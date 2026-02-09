"""
Stage 6: Final Catchall (Rule 133)
===================================
Mark all remaining as General Cargo for 100% coverage.

Input:  panjiva_ALL_YEARS_stage5.csv
Output: panjiva_ALL_YEARS_stage6.csv
"""
import pandas as pd
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(r"G:\My Drive\LLM\project_manifest")
INPUT_FILE = BASE_DIR / "00_DATA" / "00.03_MATCHED" / "panjiva_ALL_YEARS_stage5.csv"
OUTPUT_FILE = BASE_DIR / "00_DATA" / "00.03_MATCHED" / "panjiva_ALL_YEARS_stage6.csv"

def stamp(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

def apply_final_catchall():
    stamp("="*80)
    stamp("STAGE 6: FINAL CATCHALL (Rule 133)")
    stamp("="*80)
    start = datetime.now()
    
    stamp("\n1. Loading data...")
    df = pd.read_csv(INPUT_FILE, dtype=str, low_memory=False)
    stamp(f"   Total records: {len(df):,}")
    
    df['Tons_Numeric'] = pd.to_numeric(df['Tons'], errors='coerce').fillna(0)
    unclassified_before = df['Group'].isna().sum()
    tons_before = df.loc[df['Group'].isna(), 'Tons_Numeric'].sum()
    stamp(f"   Unclassified: {unclassified_before:,} records, {tons_before:,.0f} tons")
    
    stamp("\n2. Applying Rule 133 catchall...")
    unclassified_mask = df['Group'].isna()
    
    df.loc[unclassified_mask, 'Group'] = 'Break Bulk'
    df.loc[unclassified_mask, 'Commodity'] = 'General Cargo'
    df.loc[unclassified_mask, 'Cargo'] = 'General Cargo'
    df.loc[unclassified_mask, 'Cargo_Detail'] = 'General Cargo'
    df.loc[unclassified_mask, 'Classified_By_Rule'] = 'Rule_133_Final_Catchall'
    
    stamp(f"   Classified {unclassified_before:,} records as General Cargo")
    
    stamp("\n" + "="*80)
    stamp("3. FINAL RESULTS")
    stamp("="*80)
    
    unclassified_after = df['Group'].isna().sum()
    tons_after = df.loc[df['Group'].isna(), 'Tons_Numeric'].sum()
    
    stamp(f"\nBEFORE: {unclassified_before:,} records, {tons_before:,.0f} tons")
    stamp(f"CAPTURED: {unclassified_before:,} records, {tons_before:,.0f} tons")
    stamp(f"AFTER: {unclassified_after:,} records, {tons_after:,.0f} tons")
    
    classified_total = ((df['Group'].notna()) & (df['Group'] != 'EXCLUDED')).sum()
    excluded_total = (df['Group'] == 'EXCLUDED').sum()
    classified_pct = (classified_total / len(df) * 100)
    excluded_pct = (excluded_total / len(df) * 100)
    
    tons_classified = df.loc[(df['Group'].notna()) & (df['Group'] != 'EXCLUDED'), 'Tons_Numeric'].sum()
    tons_excluded = df.loc[df['Group'] == 'EXCLUDED', 'Tons_Numeric'].sum()
    total_tons = df['Tons_Numeric'].sum()
    tons_classified_pct = (tons_classified / total_tons * 100) if total_tons > 0 else 0
    tons_excluded_pct = (tons_excluded / total_tons * 100) if total_tons > 0 else 0
    
    stamp(f"\nOVERALL:")
    stamp(f"  Classified:   {classified_total:,} records ({classified_pct:.1f}%), {tons_classified:,.0f} tons ({tons_classified_pct:.1f}%)")
    stamp(f"  Excluded:     {excluded_total:,} records ({excluded_pct:.1f}%), {tons_excluded:,.0f} tons ({tons_excluded_pct:.1f}%)")
    stamp(f"  Unclassified: {unclassified_after:,} records ({100-classified_pct-excluded_pct:.1f}%), {tons_after:,.0f} tons ({100-tons_classified_pct-tons_excluded_pct:.1f}%)")
    
    if unclassified_after == 0:
        stamp("\n*** 100% CLASSIFICATION ACHIEVED! ***")
    
    stamp("\n4. SAVING OUTPUT...")
    df.drop(columns=['Tons_Numeric'], inplace=True)
    df.to_csv(OUTPUT_FILE, index=False)
    stamp(f"   Saved: {OUTPUT_FILE.name}")
    
    duration = (datetime.now() - start).total_seconds() / 60
    stamp(f"\nSTAGE 6 COMPLETE - Duration: {duration:.1f} minutes")

if __name__ == "__main__":
    apply_final_catchall()

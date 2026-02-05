"""
Split Excel file with multiple worksheets into separate CSV files

Author: WSD3 / Claude Code
Date: 2026-01-14
"""

import pandas as pd
from pathlib import Path

def split_excel_to_csv(excel_file):
    """Split Excel file into separate CSV files, one per worksheet"""

    excel_path = Path(excel_file)
    output_dir = excel_path.parent
    base_name = excel_path.stem

    print(f"Reading: {excel_path.name}")
    print()

    # Read all sheets
    excel_data = pd.read_excel(excel_file, sheet_name=None, engine='openpyxl')

    print(f"Found {len(excel_data)} worksheets:")
    print()

    # Save each sheet as CSV
    for sheet_name, df in excel_data.items():
        # Create clean filename from sheet name
        clean_sheet_name = sheet_name.replace(' ', '_').replace('/', '_')
        csv_filename = f"{base_name}_{clean_sheet_name}.csv"
        csv_path = output_dir / csv_filename

        # Save to CSV
        df.to_csv(csv_path, index=False)

        print(f"[OK] {sheet_name}")
        print(f"  -> {csv_filename}")
        print(f"  Rows: {len(df):,} | Columns: {len(df.columns)}")
        print()

    print("Done!")
    print(f"Files saved to: {output_dir}")

if __name__ == "__main__":
    excel_file = r"G:\My Drive\LLM\project_manifest\00_raw_data\00_03_usace_entrance_clearance_raw\Entrances_Clearances_2023.xlsx"
    split_excel_to_csv(excel_file)

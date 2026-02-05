"""
Check Full Pipeline Progress

Monitors output directory and shows current status

Author: WSD3 / Claude Code
Date: 2026-01-14
"""

import os
from pathlib import Path
from datetime import datetime

def check_progress():
    output_dir = Path(r"G:\My Drive\LLM\project_manifest\00_DATA/00.03_MATCHED\classification_full_2024_v3.6.0")
    output_file = output_dir / "panjiva_imports_2024_classified_v3.6.0.csv"
    stats_file = output_dir / "classification_stats_v3.6.0_2024.csv"

    print("=" * 60)
    print("Pipeline Progress Check")
    print("=" * 60)
    print()

    if not output_dir.exists():
        print("Status: Pipeline starting (output directory not created yet)")
        print("This is normal for the first few minutes.")
        return

    print(f"Output directory: {output_dir}")
    print()

    if output_file.exists():
        file_size = output_file.stat().st_size / (1024 * 1024)  # MB
        mod_time = datetime.fromtimestamp(output_file.stat().st_mtime)
        print(f"✓ Results file exists: {output_file.name}")
        print(f"  Size: {file_size:.1f} MB")
        print(f"  Last modified: {mod_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print()

        if stats_file.exists():
            print(f"✓ Stats file exists: {stats_file.name}")
            print()
            print("STATUS: Pipeline COMPLETE!")
        else:
            print("STATUS: Classification complete, generating statistics...")
    else:
        print("STATUS: Classification in progress...")
        print("(Results file not created yet)")

    print()
    print("Check again in 30-60 minutes for updates")
    print("=" * 60)

if __name__ == "__main__":
    check_progress()

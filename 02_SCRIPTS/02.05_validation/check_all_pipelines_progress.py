"""
Check All Pipeline Progress (2023, 2024, 2025)

Monitors all three years simultaneously

Author: WSD3 / Claude Code
Date: 2026-01-14
"""

import os
from pathlib import Path
from datetime import datetime

def check_year_progress(year):
    """Check progress for a specific year"""
    output_dir = Path(rf"G:\My Drive\LLM\project_manifest\00_DATA/00.03_MATCHED\classification_full_{year}_v3.6.0")
    output_file = output_dir / f"panjiva_imports_{year}_classified_v3.6.0.csv"
    stats_file = output_dir / f"classification_stats_v3.6.0_{year}.csv"

    print(f"{'='*60}")
    print(f"Year {year}")
    print(f"{'='*60}")

    if not output_dir.exists():
        print("Status: Starting (output directory not created yet)")
        print()
        return "starting"

    if output_file.exists():
        file_size = output_file.stat().st_size / (1024 * 1024)  # MB
        mod_time = datetime.fromtimestamp(output_file.stat().st_mtime)
        print(f"[OK] Results file: {output_file.name}")
        print(f"     Size: {file_size:.1f} MB")
        print(f"     Last modified: {mod_time.strftime('%H:%M:%S')}")

        if stats_file.exists():
            print(f"[OK] Stats file: {stats_file.name}")
            print()
            print("STATUS: COMPLETE!")
            print()
            return "complete"
        else:
            print()
            print("STATUS: Classification complete, generating statistics...")
            print()
            return "finishing"
    else:
        print("STATUS: Classification in progress...")
        print("(Results file not created yet)")
        print()
        return "running"

def main():
    print()
    print("="*60)
    print("FULL PIPELINE PROGRESS - ALL YEARS")
    print(f"Checked at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    print()

    status_2023 = check_year_progress("2023")
    status_2024 = check_year_progress("2024")
    status_2025 = check_year_progress("2025")

    # Summary
    print("="*60)
    print("SUMMARY")
    print("="*60)

    statuses = {
        "2023": status_2023,
        "2024": status_2024,
        "2025": status_2025
    }

    for year, status in statuses.items():
        status_icon = {
            "starting": "[STARTING]",
            "running": "[RUNNING]",
            "finishing": "[FINISHING]",
            "complete": "[COMPLETE]"
        }.get(status, "[UNKNOWN]")

        print(f"{year}: {status_icon}")

    complete_count = sum(1 for s in statuses.values() if s == "complete")
    running_count = sum(1 for s in statuses.values() if s in ["starting", "running", "finishing"])

    print()
    print(f"Complete: {complete_count}/3")
    print(f"Running: {running_count}/3")

    if complete_count == 3:
        print()
        print("ALL PIPELINES COMPLETE!")
    else:
        print()
        print("Check again in 30-60 minutes for updates")

    print("="*60)

if __name__ == "__main__":
    main()

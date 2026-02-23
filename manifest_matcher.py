"""
Import Manifest ↔ MRTIS Vessel Matching

Enriches MRTIS voyage segment data with Panjiva import manifest cargo details
by matching vessel visits to discharge terminals on the Lower Mississippi River.
The manifest Arrival Date is matched to the vessel's FirstTerminalArrivalTime
within a ±5 calendar day window (Arrival Date is date-only).

Standalone post-pipeline script — does NOT modify voyage_analyzer.py or the
manifest pipeline.

Usage:
    python manifest_matcher.py ^
        --segments "G:/My Drive/LLM/project_mrtis/results_2025_review/voyage_segments.csv" ^
        --manifest "G:/My Drive/LLM/project_manifest/PIPELINE/phase_07_enrichment/phase_07_output.csv" ^
        --zones "G:/My Drive/LLM/project_mrtis/terminal_zone_dictionary.csv" ^
        --output "G:/My Drive/LLM/project_mrtis/results_2025_review/"
"""

import sys
import csv
import logging
import argparse
from pathlib import Path
from datetime import datetime, date, timedelta
from collections import defaultdict

import pandas as pd

# Add project_mrtis to path for shared utilities
PROJECT_MRTIS = Path(__file__).parent.parent / "project_mrtis"
sys.path.insert(0, str(PROJECT_MRTIS))

from src.data.vessel_name_normalizer import normalize_vessel_name, build_name_key

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Columns to load from the manifest CSV (13 of 68)
MANIFEST_COLUMNS = [
    'Arrival Date', 'Vessel', 'IMO', 'Tons',
    'Group', 'Commodity', 'Cargo', 'Cargo_Detail',
    'Country of Origin (F)', 'Shipper', 'Consignee',
    'Bill of Lading Number', 'Port_Consolidated',
]


class ManifestIndex:
    """Loads New Orleans manifest data and builds vessel lookup indices.

    Dual-key index: IMO (primary, exact) + vessel name key (fallback).
    """

    def __init__(self, manifest_path: Path):
        self.manifest_path = manifest_path
        self.imo_index: dict[str, list[dict]] = defaultdict(list)
        self.name_index: dict[str, list[dict]] = defaultdict(list)
        self.total_loaded = 0
        self._load()

    def _load(self):
        """Read manifest CSV, filter to New Orleans, build dual index."""
        if not self.manifest_path.exists():
            raise FileNotFoundError(f"Manifest file not found: {self.manifest_path}")

        logger.info(f"Loading manifest data from {self.manifest_path}")
        df = pd.read_csv(
            self.manifest_path,
            usecols=MANIFEST_COLUMNS,
            dtype={'IMO': str, 'Bill of Lading Number': str},
            low_memory=False,
        )
        logger.info(f"  Total manifest records: {len(df):,}")

        # Filter to New Orleans corridor
        df = df[df['Port_Consolidated'] == 'New Orleans'].copy()
        logger.info(f"  New Orleans records: {len(df):,}")

        # Parse arrival date
        df['arrival_date'] = pd.to_datetime(df['Arrival Date'], errors='coerce').dt.date

        # Clean IMO — strip whitespace, drop non-numeric
        df['imo_clean'] = df['IMO'].fillna('').astype(str).str.strip()
        df.loc[~df['imo_clean'].str.match(r'^\d+$'), 'imo_clean'] = ''

        # Build name key for fallback matching
        df['name_key'] = df['Vessel'].apply(
            lambda v: build_name_key(v) if pd.notna(v) else ''
        )

        # Convert to list of dicts for indexing
        records = df.to_dict('records')
        self.total_loaded = len(records)

        for rec in records:
            ad = rec.get('arrival_date')
            if ad is None or pd.isna(ad):
                continue

            # IMO index
            imo = rec.get('imo_clean', '')
            if imo:
                self.imo_index[imo].append(rec)

            # Name index
            nk = rec.get('name_key', '')
            if nk:
                self.name_index[nk].append(rec)

        # Sort each vessel's records by arrival date
        for key in self.imo_index:
            self.imo_index[key].sort(
                key=lambda r: r['arrival_date'] if r['arrival_date'] else date.min
            )
        for key in self.name_index:
            self.name_index[key].sort(
                key=lambda r: r['arrival_date'] if r['arrival_date'] else date.min
            )

        logger.info(
            f"  Indexed {self.total_loaded:,} records — "
            f"{len(self.imo_index):,} distinct IMOs, "
            f"{len(self.name_index):,} distinct vessel names"
        )

    def find_matches(self, imo: str, vessel_name: str, reference_date: date,
                     window_days: int = 5) -> tuple[list[dict], str]:
        """Find manifest records matching a vessel within ±window_days.

        Tries IMO match first, falls back to vessel name.

        Args:
            imo: IMO number (string)
            vessel_name: Vessel name (any case/format)
            reference_date: Date to match against (FirstTerminalArrivalTime)
            window_days: Calendar days for match window (default ±5)

        Returns:
            Tuple of (matching records, match_key) where match_key is
            'IMO' or 'NAME' or '' if no match.
        """
        window_start = reference_date - timedelta(days=window_days)
        window_end = reference_date + timedelta(days=window_days)

        def _filter_window(records):
            return [
                r for r in records
                if r.get('arrival_date') and window_start <= r['arrival_date'] <= window_end
            ]

        # Try IMO first
        imo_clean = str(imo).strip() if imo else ''
        if imo_clean and imo_clean in self.imo_index:
            matches = _filter_window(self.imo_index[imo_clean])
            if matches:
                return matches, 'IMO'

        # Fallback to vessel name
        name_key = build_name_key(vessel_name)
        if name_key and name_key in self.name_index:
            matches = _filter_window(self.name_index[name_key])
            if matches:
                return matches, 'NAME'

        return [], ''


def _load_discharge_zones(csv_path: Path) -> set[str]:
    """Load discharge-capable zone names from terminal_zone_dictionary.csv.

    Returns set of Zone names where Activity is 'Discharge - Only' or
    'Load or Discharge' (133 zones).
    """
    zones = set()
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            activity = row.get('Activity', '').strip()
            if activity in ('Discharge - Only', 'Load or Discharge'):
                zones.add(row['Zone'])
    return zones


def _parse_arrival_date(arrival_str: str) -> date | None:
    """Parse FirstTerminalArrivalTime string to date.

    Expected format: '2025-01-15 22:50:00'
    """
    if not arrival_str or not arrival_str.strip():
        return None
    try:
        return datetime.strptime(arrival_str.strip(), '%Y-%m-%d %H:%M:%S').date()
    except ValueError:
        return None


def _aggregate_matches(matches: list[dict]) -> dict:
    """Aggregate multiple manifest BOL matches into summary columns."""
    if not matches:
        return {}

    bols = set()
    total_tons = 0.0
    groups = []
    commodities = []
    cargos = []
    cargo_details = []
    origins = []
    shippers = []
    arrival_dates = []

    for m in matches:
        bol = m.get('Bill of Lading Number', '')
        if bol:
            bols.add(bol)

        tons = m.get('Tons')
        if pd.notna(tons):
            try:
                total_tons += float(tons)
            except (ValueError, TypeError):
                pass

        for val, lst in [
            (m.get('Group', ''), groups),
            (m.get('Commodity', ''), commodities),
            (m.get('Cargo', ''), cargos),
            (m.get('Cargo_Detail', ''), cargo_details),
            (m.get('Country of Origin (F)', ''), origins),
            (m.get('Shipper', ''), shippers),
        ]:
            if pd.notna(val) and val and val not in lst:
                lst.append(str(val))

        ad = m.get('arrival_date')
        if ad:
            arrival_dates.append(ad)

    # Limit shippers to top 3 to avoid overly long fields
    shippers_display = shippers[:3]
    if len(shippers) > 3:
        shippers_display.append(f'(+{len(shippers) - 3} more)')

    return {
        'ManifestBOLCount': len(bols),
        'ManifestTotalTons': round(total_tons, 2) if total_tons > 0 else '',
        'ManifestGroup': ', '.join(groups),
        'ManifestCommodity': ', '.join(commodities),
        'ManifestCargo': ', '.join(cargos),
        'ManifestCargoDetail': ', '.join(cargo_details),
        'ManifestOrigins': ', '.join(origins),
        'ManifestShippers': ', '.join(shippers_display),
        'ManifestArrivalDate': min(arrival_dates).isoformat() if arrival_dates else '',
    }


class ManifestMatcher:
    """Orchestrates matching MRTIS voyage segments against import manifest data."""

    MANIFEST_COLUMNS = [
        'ManifestMatchStatus', 'ManifestMatchKey', 'ManifestBOLCount',
        'ManifestTotalTons', 'ManifestGroup', 'ManifestCommodity',
        'ManifestCargo', 'ManifestCargoDetail', 'ManifestOrigins',
        'ManifestShippers', 'ManifestArrivalDate', 'ManifestTimeDeltaDays',
    ]

    def __init__(self, manifest_index: ManifestIndex, discharge_zones: set[str],
                 window_days: int = 5):
        self.manifest_index = manifest_index
        self.discharge_zones = discharge_zones
        self.window_days = window_days

        # Stats
        self.total_segments = 0
        self.discharge_visits = 0
        self.matched = 0
        self.matched_by_imo = 0
        self.matched_by_name = 0
        self.unmatched = 0
        self.no_arrival = 0
        self.not_discharge_zone = 0
        self.unmatched_vessels: dict[str, int] = defaultdict(int)
        self.time_deltas: list[float] = []
        self.tonnage_by_group: dict[str, float] = defaultdict(float)
        self.tonnage_by_commodity: dict[str, float] = defaultdict(float)
        self.detail_rows: list[dict] = []

    def match_segments(self, segments_path: Path) -> tuple[list[dict], list[str]]:
        """Read voyage_segments.csv and match each segment.

        Returns (enriched segment dicts, original column names).
        """
        logger.info(f"Reading segments from {segments_path}")
        with open(segments_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            original_columns = list(reader.fieldnames)
            segments = list(reader)

        self.total_segments = len(segments)
        logger.info(f"  Total segments: {self.total_segments:,}")

        enriched = []
        for seg in segments:
            row = dict(seg)
            zone = seg.get('DischargeTerminalZone', '')

            if not zone or zone not in self.discharge_zones:
                row.update(self._empty_manifest('NOT_DISCHARGE_ZONE'))
                self.not_discharge_zone += 1
                enriched.append(row)
                continue

            self.discharge_visits += 1
            arrival_str = seg.get('FirstTerminalArrivalTime', '')
            arrival_date = _parse_arrival_date(arrival_str)

            if not arrival_date:
                row.update(self._empty_manifest('NO_ARRIVAL'))
                self.no_arrival += 1
                enriched.append(row)
                continue

            imo = seg.get('IMO', '')
            vessel_name = seg.get('VesselName', '')
            matches, match_key = self.manifest_index.find_matches(
                imo, vessel_name, arrival_date, self.window_days
            )

            if matches:
                agg = _aggregate_matches(matches)

                # Time delta to nearest manifest arrival date
                nearest = min(
                    matches,
                    key=lambda m: abs((m['arrival_date'] - arrival_date).days)
                    if m.get('arrival_date') else 999
                )
                delta_days = (nearest['arrival_date'] - arrival_date).days if nearest.get('arrival_date') else ''

                row['ManifestMatchStatus'] = 'MATCHED'
                row['ManifestMatchKey'] = match_key
                row['ManifestBOLCount'] = agg['ManifestBOLCount']
                row['ManifestTotalTons'] = agg['ManifestTotalTons']
                row['ManifestGroup'] = agg['ManifestGroup']
                row['ManifestCommodity'] = agg['ManifestCommodity']
                row['ManifestCargo'] = agg['ManifestCargo']
                row['ManifestCargoDetail'] = agg['ManifestCargoDetail']
                row['ManifestOrigins'] = agg['ManifestOrigins']
                row['ManifestShippers'] = agg['ManifestShippers']
                row['ManifestArrivalDate'] = agg['ManifestArrivalDate']
                row['ManifestTimeDeltaDays'] = delta_days

                self.matched += 1
                if match_key == 'IMO':
                    self.matched_by_imo += 1
                else:
                    self.matched_by_name += 1

                if isinstance(delta_days, (int, float)):
                    self.time_deltas.append(delta_days)

                # Track tonnage by group and commodity
                for m in matches:
                    tons = 0.0
                    try:
                        tons = float(m.get('Tons', 0)) if pd.notna(m.get('Tons')) else 0.0
                    except (ValueError, TypeError):
                        pass
                    group = str(m.get('Group', 'UNKNOWN')) if pd.notna(m.get('Group')) else 'UNKNOWN'
                    commodity = str(m.get('Commodity', 'UNKNOWN')) if pd.notna(m.get('Commodity')) else 'UNKNOWN'
                    self.tonnage_by_group[group] += tons
                    self.tonnage_by_commodity[commodity] += tons

                # Build detail rows — one per matched BOL
                for m in matches:
                    tons_val = ''
                    try:
                        tons_val = float(m.get('Tons', '')) if pd.notna(m.get('Tons')) else ''
                    except (ValueError, TypeError):
                        pass

                    self.detail_rows.append({
                        'VoyageID': seg.get('VoyageID', ''),
                        'VesselName': vessel_name,
                        'IMO': imo,
                        'DischargeTerminalZone': zone,
                        'FirstTerminalArrivalTime': arrival_str,
                        'MatchKey': match_key,
                        'BillOfLading': m.get('Bill of Lading Number', ''),
                        'ArrivalDate': m['arrival_date'].isoformat() if m.get('arrival_date') else '',
                        'Group': m.get('Group', '') if pd.notna(m.get('Group')) else '',
                        'Commodity': m.get('Commodity', '') if pd.notna(m.get('Commodity')) else '',
                        'Cargo': m.get('Cargo', '') if pd.notna(m.get('Cargo')) else '',
                        'Cargo_Detail': m.get('Cargo_Detail', '') if pd.notna(m.get('Cargo_Detail')) else '',
                        'Tons': tons_val,
                        'Origin': m.get('Country of Origin (F)', '') if pd.notna(m.get('Country of Origin (F)')) else '',
                        'Shipper': m.get('Shipper', '') if pd.notna(m.get('Shipper')) else '',
                        'Consignee': m.get('Consignee', '') if pd.notna(m.get('Consignee')) else '',
                        'time_delta_days': (m['arrival_date'] - arrival_date).days if m.get('arrival_date') else '',
                    })
            else:
                row.update(self._empty_manifest('UNMATCHED'))
                self.unmatched += 1
                self.unmatched_vessels[vessel_name] += 1

            enriched.append(row)

        logger.info(f"  Discharge zone visits: {self.discharge_visits:,}")
        logger.info(f"  Matched: {self.matched:,} (IMO: {self.matched_by_imo}, NAME: {self.matched_by_name})")
        logger.info(f"  Unmatched: {self.unmatched:,}")
        logger.info(f"  No arrival time: {self.no_arrival:,}")

        return enriched, original_columns

    def _empty_manifest(self, status: str) -> dict:
        """Return empty manifest columns with given status."""
        return {
            'ManifestMatchStatus': status,
            'ManifestMatchKey': '',
            'ManifestBOLCount': '',
            'ManifestTotalTons': '',
            'ManifestGroup': '',
            'ManifestCommodity': '',
            'ManifestCargo': '',
            'ManifestCargoDetail': '',
            'ManifestOrigins': '',
            'ManifestShippers': '',
            'ManifestArrivalDate': '',
            'ManifestTimeDeltaDays': '',
        }

    def write_enriched_csv(self, enriched: list[dict], original_columns: list[str],
                           output_path: Path):
        """Write voyage_segments_manifest_enriched.csv."""
        all_columns = list(original_columns) + self.MANIFEST_COLUMNS
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=all_columns, extrasaction='ignore')
            writer.writeheader()
            writer.writerows(enriched)

        logger.info(f"Wrote enriched segments: {output_path} ({len(enriched):,} rows)")

    def write_detail_csv(self, output_path: Path):
        """Write manifest_match_detail.csv — one row per matched BOL."""
        detail_columns = [
            'VoyageID', 'VesselName', 'IMO', 'DischargeTerminalZone',
            'FirstTerminalArrivalTime', 'MatchKey', 'BillOfLading',
            'ArrivalDate', 'Group', 'Commodity', 'Cargo', 'Cargo_Detail',
            'Tons', 'Origin', 'Shipper', 'Consignee', 'time_delta_days',
        ]
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=detail_columns)
            writer.writeheader()
            writer.writerows(self.detail_rows)

        logger.info(f"Wrote match detail: {output_path} ({len(self.detail_rows):,} rows)")

    def write_report(self, output_path: Path):
        """Write manifest_match_report.txt with summary statistics."""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        lines = []

        lines.append("=" * 70)
        lines.append("Import Manifest ↔ MRTIS Vessel Matching Report")
        lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("=" * 70)

        # Overview
        lines.append("")
        lines.append("SEGMENT OVERVIEW")
        lines.append("-" * 40)
        lines.append(f"  Total segments:           {self.total_segments:>8,}")
        lines.append(f"  Not discharge zone:       {self.not_discharge_zone:>8,}")
        lines.append(f"  Discharge zone visits:    {self.discharge_visits:>8,}")
        lines.append(f"    Matched:                {self.matched:>8,}")
        lines.append(f"      by IMO:               {self.matched_by_imo:>8,}")
        lines.append(f"      by vessel name:       {self.matched_by_name:>8,}")
        lines.append(f"    Unmatched:              {self.unmatched:>8,}")
        lines.append(f"    No arrival time:        {self.no_arrival:>8,}")

        if self.discharge_visits > 0:
            match_rate = self.matched / self.discharge_visits * 100
            lines.append(f"  Match rate:               {match_rate:>7.1f}%")

        # Time delta distribution
        if self.time_deltas:
            lines.append("")
            lines.append("TIME DELTA DISTRIBUTION (days, MRTIS arrival → manifest arrival)")
            lines.append("-" * 40)
            buckets = defaultdict(int)
            for d in self.time_deltas:
                buckets[int(d)] += 1
            for delta in sorted(buckets.keys()):
                bar = '#' * buckets[delta]
                lines.append(f"  {delta:>+3d} days: {buckets[delta]:>4d}  {bar}")
            avg_delta = sum(self.time_deltas) / len(self.time_deltas)
            abs_deltas = [abs(d) for d in self.time_deltas]
            lines.append(f"  Mean delta:    {avg_delta:>+.1f} days")
            lines.append(f"  Mean |delta|:  {sum(abs_deltas)/len(abs_deltas):.1f} days")
            lines.append(f"  Same day (0):  {buckets.get(0, 0):>4d}")

        # Tonnage by Group
        if self.tonnage_by_group:
            lines.append("")
            lines.append("TONNAGE BY GROUP")
            lines.append("-" * 40)
            total_tons = sum(self.tonnage_by_group.values())
            for group, tons in sorted(self.tonnage_by_group.items(),
                                      key=lambda x: -x[1]):
                pct = tons / total_tons * 100 if total_tons > 0 else 0
                lines.append(f"  {group:<30s}: {tons:>12,.0f} tons ({pct:>5.1f}%)")
            lines.append(f"  {'TOTAL':<30s}: {total_tons:>12,.0f} tons")

        # Tonnage by Commodity
        if self.tonnage_by_commodity:
            lines.append("")
            lines.append("TONNAGE BY COMMODITY")
            lines.append("-" * 40)
            total_tons = sum(self.tonnage_by_commodity.values())
            for commodity, tons in sorted(self.tonnage_by_commodity.items(),
                                          key=lambda x: -x[1]):
                pct = tons / total_tons * 100 if total_tons > 0 else 0
                lines.append(f"  {commodity:<30s}: {tons:>12,.0f} tons ({pct:>5.1f}%)")

        # Unmatched vessels
        if self.unmatched_vessels:
            lines.append("")
            lines.append("UNMATCHED VESSEL NAMES (MRTIS name → count)")
            lines.append("-" * 40)
            for name, count in sorted(self.unmatched_vessels.items(),
                                      key=lambda x: -x[1]):
                key = build_name_key(name)
                lines.append(f"  {name:<35s} (key: {key}) × {count}")

        lines.append("")

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))

        logger.info(f"Wrote match report: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Match MRTIS voyage segments to import manifest data")
    parser.add_argument('--segments', type=str, required=True,
                        help='Path to voyage_segments.csv')
    parser.add_argument('--manifest', type=str, required=True,
                        help='Path to phase_07_output.csv (manifest data)')
    parser.add_argument('--zones', type=str, required=True,
                        help='Path to terminal_zone_dictionary.csv')
    parser.add_argument('--output', type=str, required=True,
                        help='Output directory for results')
    parser.add_argument('--window-days', type=int, default=5,
                        help='Match window in calendar days (default: 5)')
    args = parser.parse_args()

    logger.info("=" * 60)
    logger.info("Import Manifest ↔ MRTIS Vessel Matching")
    logger.info("=" * 60)

    # Load manifest index
    manifest_index = ManifestIndex(Path(args.manifest))

    # Load discharge zones
    discharge_zones = _load_discharge_zones(Path(args.zones))
    logger.info(f"Discharge zones: {len(discharge_zones)}")

    # Run matching
    matcher = ManifestMatcher(manifest_index, discharge_zones, args.window_days)
    enriched, original_columns = matcher.match_segments(Path(args.segments))

    # Write outputs
    output_dir = Path(args.output)
    matcher.write_enriched_csv(
        enriched, original_columns,
        output_dir / "voyage_segments_manifest_enriched.csv"
    )
    matcher.write_detail_csv(output_dir / "manifest_match_detail.csv")
    matcher.write_report(output_dir / "manifest_match_report.txt")

    logger.info("=" * 60)
    logger.info("Done.")


if __name__ == "__main__":
    main()

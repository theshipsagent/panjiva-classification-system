"""
Lower Mississippi River Cargo Demographics Report
Generates an HTML report with Chart.js visualizations.

IMPORTS: phase_07_output.csv  -> filtered to Port_Consolidated = "New Orleans"
         (covers New Orleans, Baton Rouge, Gramercy — the LMR port cluster)
EXPORTS: 12 ZIP files (2023)  -> filtered to Port of Lading containing "New Orleans"
"""

import sys
import io
# Force UTF-8 output on Windows to avoid cp1252 encoding errors
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

import pandas as pd
import numpy as np
import zipfile
import os
import json
from pathlib import Path
from datetime import datetime

BASE = Path("G:/My Drive/LLM/project_manifest")
MANIFEST = BASE / "PIPELINE/phase_07_enrichment/phase_07_output.csv"
EXPORTS_DIR = BASE / "RAW_DATA/00_02_panjiva_exports_raw"
OUT_HTML = BASE / "DOCUMENTATION/dashboards/lmr_cargo_report.html"

# ── HS-code to cargo group mapping for exports ─────────────────────────────
HS2_MAP = {
    "01": "Dry Bulk – Agricultural",
    "02": "Dry Bulk – Agricultural",
    "03": "Dry Bulk – Agricultural",
    "04": "Dry Bulk – Agricultural",
    "05": "Dry Bulk – Agricultural",
    "07": "Dry Bulk – Agricultural",
    "08": "Dry Bulk – Agricultural",
    "10": "Dry Bulk – Grain",
    "11": "Dry Bulk – Agricultural",
    "12": "Dry Bulk – Grain",
    "15": "Liquid Bulk – Vegetable Oils",
    "17": "Dry Bulk – Sugar",
    "18": "Dry Bulk – Agricultural",
    "23": "Dry Bulk – Animal Feed",
    "25": "Dry Bulk – Minerals & Ores",
    "26": "Dry Bulk – Minerals & Ores",
    "27": "Liquid Bulk – Petroleum",
    "28": "Liquid Bulk – Chemicals",
    "29": "Liquid Bulk – Chemicals",
    "31": "Dry Bulk – Fertilizer",
    "32": "Liquid Bulk – Chemicals",
    "38": "Liquid Bulk – Chemicals",
    "39": "Liquid Bulk – Plastics",
    "44": "Break Bulk – Forest Products",
    "47": "Break Bulk – Pulp & Paper",
    "48": "Break Bulk – Pulp & Paper",
    "68": "Dry Bulk – Minerals & Ores",
    "72": "Break Bulk – Steel",
    "73": "Break Bulk – Steel",
    "76": "Break Bulk – Metals",
    "84": "Break Bulk – Machinery",
    "85": "Break Bulk – Machinery",
    "87": "Break Bulk – Vehicles",
}

HS4_GRAIN = {"1001", "1002", "1003", "1004", "1005", "1006", "1007", "1008",
             "1201", "1202", "1204", "1205", "1206", "1207", "1208", "1209"}


def hs2_classify(hs_raw):
    try:
        h = str(hs_raw).strip().replace(".", "")[:4]
        hs2 = h[:2]
        hs4 = h[:4]
        if hs4 in HS4_GRAIN:
            return "Dry Bulk – Grain"
        if hs2 == "27":
            # distinguish crude/refined/LPG from coal
            hs4i = int(h) if h.isdigit() else 0
            if hs4i in range(2701, 2703):
                return "Dry Bulk – Coal"
            elif hs4i == 2711:
                return "Liquid Gas – LPG/LNG"
            return "Liquid Bulk – Petroleum"
        return HS2_MAP.get(hs2, "Other")
    except Exception:
        return "Other"


def group_simple(cargo_group_str):
    s = str(cargo_group_str).strip()
    if s in ("Dry Bulk",):
        return "Dry Bulk"
    if s in ("Liquid Bulk",):
        return "Liquid Bulk"
    if s in ("Liquid Gas",):
        return "Liquid Gas"
    if s in ("Break Bulk",):
        return "Break Bulk"
    if s == "Container":
        return "Container"
    return "Other"


# ════════════════════════════════════════════════════════
# 1. LOAD IMPORTS
# ════════════════════════════════════════════════════════
print("Loading imports …")
USE_COLS = [
    "Arrival Date", "Tons", "Group", "Commodity", "Cargo", "Cargo_Detail",
    "Port_Consolidated", "Country of Origin (F)", "Shipper", "Consignee",
    "Filter", "Vessel_Type_Simple", "Port_Code"
]
df_raw = pd.read_csv(MANIFEST, usecols=USE_COLS, dtype=str, low_memory=False)
print(f"  Raw rows: {len(df_raw):,}")

# Filter to Lower Miss River cluster
# In phase_07_output, Port_Consolidated = "New Orleans" covers:
#   New Orleans (2002), Morgan City (2001), Gramercy (2010), Baton Rouge (2004)
imp = df_raw[df_raw["Port_Consolidated"].str.strip() == "New Orleans"].copy()
print(f"  LMR rows (all): {len(imp):,}")

# Remove excluded records
imp = imp[imp["Filter"].str.strip().str.upper() != "EXCLUDED"].copy()
print(f"  LMR rows (classified): {len(imp):,}")

imp["Tons"] = pd.to_numeric(imp["Tons"], errors="coerce").fillna(0)
imp["Year"] = pd.to_datetime(imp["Arrival Date"], errors="coerce").dt.year
imp = imp[imp["Year"].between(2023, 2025)]
print(f"  LMR rows 2023-2025: {len(imp):,}")

# ════════════════════════════════════════════════════════
# 2. LOAD EXPORTS
# ════════════════════════════════════════════════════════
print("Loading exports …")
exp_frames = []
for zf in sorted(EXPORTS_DIR.glob("*.zip")):
    with zipfile.ZipFile(zf) as z:
        with z.open(z.namelist()[0]) as csf:
            chunk = pd.read_csv(csf, usecols=[
                "Shipment Date", "Shipper", "Port of Lading", "Port of Unlading",
                "Port of Unlading Region", "Port of Unlading Country",
                "Goods Shipped", "HS Code", "Weight (t)", "Is Containerized"
            ], dtype=str, low_memory=False)
            lmr = chunk[chunk["Port of Lading"].str.contains("New Orleans", na=False)]
            exp_frames.append(lmr)

exp = pd.concat(exp_frames, ignore_index=True)
print(f"  LMR export rows: {len(exp):,}")

# Dedup by (Shipment Date, HS Code, Weight, Shipper, Port of Unlading)
exp = exp.drop_duplicates(
    subset=["Shipment Date", "HS Code", "Weight (t)", "Shipper", "Port of Unlading"]
)
print(f"  After dedup: {len(exp):,}")

exp["Tons"] = pd.to_numeric(exp["Weight (t)"], errors="coerce").fillna(0)
exp["Year"] = pd.to_datetime(exp["Shipment Date"], errors="coerce").dt.year
exp["CargoGroup"] = exp["HS Code"].apply(hs2_classify)
exp["Month"] = pd.to_datetime(exp["Shipment Date"], errors="coerce").dt.to_period("M")

# ════════════════════════════════════════════════════════
# 3. IMPORT STATISTICS
# ════════════════════════════════════════════════════════
print("Computing import statistics …")

# Overall summary
imp_total_tons = imp["Tons"].sum()
imp_total_recs = len(imp)

# Group breakdown
imp_group = (
    imp.groupby(["Year", "Group"])["Tons"]
    .sum().reset_index()
    .sort_values(["Year", "Tons"], ascending=[True, False])
)

# Top commodity by tons (all years combined)
imp_commodity = (
    imp.groupby(["Group", "Commodity"])["Tons"]
    .sum().reset_index()
    .sort_values("Tons", ascending=False)
)

# Dry Bulk detail
dry = imp[imp["Group"] == "Dry Bulk"].copy()
dry_commodity = (
    dry.groupby("Commodity")["Tons"]
    .sum().reset_index()
    .sort_values("Tons", ascending=False)
)

dry_cargo = (
    dry.groupby(["Commodity", "Cargo"])["Tons"]
    .sum().reset_index()
    .sort_values("Tons", ascending=False)
)

# Monthly imports by group (2023-2025)
imp["Month"] = pd.to_datetime(imp["Arrival Date"], errors="coerce").dt.to_period("M")
imp_monthly = (
    imp.groupby(["Month", "Group"])["Tons"]
    .sum().reset_index()
    .sort_values("Month")
)
imp_monthly["Month"] = imp_monthly["Month"].astype(str)

# Top countries of origin for dry bulk
dry_origin = (
    dry.groupby("Country of Origin (F)")["Tons"]
    .sum().reset_index()
    .sort_values("Tons", ascending=False)
    .head(15)
)

# Top consignees (dry bulk)
dry_consignees = (
    dry.groupby("Consignee")["Tons"]
    .sum().reset_index()
    .sort_values("Tons", ascending=False)
    .head(10)
)

# Liquid Bulk detail
liq = imp[imp["Group"] == "Liquid Bulk"].copy()
liq_commodity = (
    liq.groupby("Commodity")["Tons"]
    .sum().reset_index()
    .sort_values("Tons", ascending=False)
)

# Liquid Gas detail
gas = imp[imp["Group"] == "Liquid Gas"].copy()
gas_commodity = (
    gas.groupby("Commodity")["Tons"]
    .sum().reset_index()
    .sort_values("Tons", ascending=False)
)

# Year-over-year group comparison
imp_yoy = (
    imp.groupby(["Year", "Group"])["Tons"]
    .sum().unstack(fill_value=0)
)

# ════════════════════════════════════════════════════════
# 4. EXPORT STATISTICS
# ════════════════════════════════════════════════════════
print("Computing export statistics …")

exp_total_tons = exp["Tons"].sum()
exp_total_recs = len(exp)

exp_group = (
    exp.groupby("CargoGroup")["Tons"]
    .sum().reset_index()
    .sort_values("Tons", ascending=False)
)

exp_monthly = (
    exp.groupby("Month")["Tons"]
    .sum().reset_index()
    .sort_values("Month")
)
exp_monthly["Month"] = exp_monthly["Month"].astype(str)

exp_dest = (
    exp.groupby("Port of Unlading Region")["Tons"]
    .sum().reset_index()
    .sort_values("Tons", ascending=False)
    .head(10)
)

exp_country = (
    exp.groupby("Port of Unlading Country")["Tons"]
    .sum().reset_index()
    .sort_values("Tons", ascending=False)
    .head(15)
)

exp_top_shippers = (
    exp.groupby("Shipper")["Tons"]
    .sum().reset_index()
    .sort_values("Tons", ascending=False)
    .head(10)
)

# ════════════════════════════════════════════════════════
# 5. LOAD FACILITY DATA (MRTIS cargo matching results)
# ════════════════════════════════════════════════════════
FACILITY_CSV = Path("G:/My Drive/LLM/project_mrtis/results_phase2_full/cargo_match/facility_cargo_summary.csv")

fac_df = None
fac_top = None
fac_comm = None
mrtis_note = ""

if FACILITY_CSV.exists():
    print("Loading facility data …")
    fac_df = pd.read_csv(FACILITY_CSV, dtype=str)
    fac_df["ImportTons"] = pd.to_numeric(fac_df["ImportTons"], errors="coerce").fillna(0)
    fac_df["ExportTons"] = pd.to_numeric(fac_df["ExportTons"], errors="coerce").fillna(0)
    fac_df["TotalTons"]  = pd.to_numeric(fac_df["TotalTons"],  errors="coerce").fillna(0)

    # Top 20 facilities by import tonnage
    fac_by_facility = (
        fac_df.groupby("Facility")[["ImportTons", "ExportTons"]]
        .sum().reset_index()
        .sort_values("ImportTons", ascending=False)
        .head(20)
    )

    # Top commodity mix per top-10 facility (stacked bar data)
    top10_fac = fac_by_facility.head(10)["Facility"].tolist()
    fac_comm_data = fac_df[fac_df["Facility"].isin(top10_fac)].copy()
    comm_totals = fac_comm_data.groupby("Commodity")["ImportTons"].sum().sort_values(ascending=False)
    top_comms = comm_totals.head(8).index.tolist()

    fac_stacked = {}
    for comm in top_comms:
        row = fac_comm_data[fac_comm_data["Commodity"] == comm].groupby("Facility")["ImportTons"].sum()
        fac_stacked[comm] = [float(round(row.get(f, 0), 0)) for f in top10_fac]

    mrtis_note = f"Matched {len(fac_df):,} facility-commodity pairs via MRTIS vessel tracking (multi-year 2018–2025). 2023 terminal data available Jan only; 2024–2025 complete."
    print(f"  Facility records: {len(fac_df):,}  |  Facilities: {fac_df['Facility'].nunique():,}")
else:
    print("  Facility CSV not found — skipping facility section")
    fac_by_facility = pd.DataFrame(columns=["Facility","ImportTons","ExportTons"])
    top10_fac = []
    fac_stacked = {}

# ════════════════════════════════════════════════════════
# 6. SERIALIZE TO JSON FOR CHART.JS
# ════════════════════════════════════════════════════════
def safe_list(series):
    return [None if (isinstance(x, float) and np.isnan(x)) else
            (int(x) if isinstance(x, (np.integer,)) else
             float(round(x, 1)) if isinstance(x, (float, np.floating)) else x)
            for x in series]


# Import monthly time-series per group
groups_in_data = imp_monthly["Group"].unique().tolist()
months_all = sorted(imp_monthly["Month"].unique().tolist())

imp_ts_data = {}
for g in groups_in_data:
    subset = imp_monthly[imp_monthly["Group"] == g].set_index("Month")["Tons"]
    imp_ts_data[g] = safe_list([subset.get(m, 0) for m in months_all])

# Dry bulk commodity chart
db_labels = safe_list(dry_commodity["Commodity"].tolist())
db_tons = safe_list(dry_commodity["Tons"].tolist())

# Dry bulk cargo detail (top 20)
dry_cargo_top = dry_cargo.head(20)
dc_labels = safe_list((dry_cargo_top["Commodity"] + " / " + dry_cargo_top["Cargo"]).tolist())
dc_tons = safe_list(dry_cargo_top["Tons"].tolist())

# Liquid bulk commodity chart
lb_labels = safe_list(liq_commodity["Commodity"].tolist())
lb_tons = safe_list(liq_commodity["Tons"].tolist())

# Liquid gas commodity chart
lg_labels = safe_list(gas_commodity["Commodity"].tolist()) if len(gas_commodity) > 0 else []
lg_tons = safe_list(gas_commodity["Tons"].tolist()) if len(gas_commodity) > 0 else []

# Import group pie
imp_group_agg = imp.groupby("Group")["Tons"].sum().reset_index().sort_values("Tons", ascending=False)
imp_pie_labels = safe_list(imp_group_agg["Group"].tolist())
imp_pie_tons = safe_list(imp_group_agg["Tons"].tolist())

# Import dry bulk origin
dry_orig_labels = safe_list(dry_origin["Country of Origin (F)"].tolist())
dry_orig_tons = safe_list(dry_origin["Tons"].tolist())

# Import dry bulk top consignees
dry_cons_labels = safe_list(dry_consignees["Consignee"].str[:35].tolist())
dry_cons_tons = safe_list(dry_consignees["Tons"].tolist())

# Export group
exp_pie_labels = safe_list(exp_group["CargoGroup"].tolist())
exp_pie_tons = safe_list(exp_group["Tons"].tolist())

# Export monthly
exp_months = safe_list(exp_monthly["Month"].tolist())
exp_monthly_tons = safe_list(exp_monthly["Tons"].tolist())

# Export destinations
exp_dest_labels = safe_list(exp_dest["Port of Unlading Region"].tolist())
exp_dest_tons = safe_list(exp_dest["Tons"].tolist())

# Export countries
exp_ctry_labels = safe_list(exp_country["Port of Unlading Country"].tolist())
exp_ctry_tons = safe_list(exp_country["Tons"].tolist())

# Export top shippers
exp_ship_labels = safe_list(exp_top_shippers["Shipper"].str[:35].tolist())
exp_ship_tons = safe_list(exp_top_shippers["Tons"].tolist())

# Facility top-20 bar chart
fac_labels   = safe_list(fac_by_facility["Facility"].str[:40].tolist())
fac_imp_tons = safe_list(fac_by_facility["ImportTons"].tolist())
fac_exp_tons = safe_list(fac_by_facility["ExportTons"].tolist())

# Facility commodity stacked bar
fac_stacked_comms  = list(fac_stacked.keys())
fac_stacked_facs   = [f[:30] for f in top10_fac]
fac_stacked_vals   = [safe_list(fac_stacked[c]) for c in fac_stacked_comms]

# Year comparison (imports)
yoy_years = [int(y) for y in imp_yoy.index.tolist()]
yoy_groups = [str(c) for c in imp_yoy.columns.tolist()]
yoy_data = {}
for g in yoy_groups:
    yoy_data[g] = safe_list(imp_yoy[g].tolist())

# Summary KPIs
imp_by_year = imp.groupby("Year")["Tons"].sum()
imp_by_group_pct = (imp_group_agg.set_index("Group")["Tons"] / imp_total_tons * 100).round(1)

dry_pct = float(imp_by_group_pct.get("Dry Bulk", 0))
liq_pct = float(imp_by_group_pct.get("Liquid Bulk", 0))
gas_pct = float(imp_by_group_pct.get("Liquid Gas", 0))
bb_pct = float(imp_by_group_pct.get("Break Bulk", 0))

exp_grain_tons = float(exp[exp["CargoGroup"] == "Dry Bulk – Grain"]["Tons"].sum())
exp_grain_pct = round(exp_grain_tons / exp_total_tons * 100, 1) if exp_total_tons > 0 else 0

print("\n== KEY METRICS ==================================")
print(f"Imports  LMR 2023-2025: {imp_total_recs:,} records | {imp_total_tons/1e6:.2f}M tons")
print(f"  Dry Bulk: {dry_pct:.1f}%  Liquid Bulk: {liq_pct:.1f}%  Liquid Gas: {gas_pct:.1f}%  Break Bulk: {bb_pct:.1f}%")
print(f"Exports  LMR 2023:      {exp_total_recs:,} records | {exp_total_tons/1e6:.2f}M tons")
print(f"  Grain: {exp_grain_pct:.1f}% of export tonnage")
print("=================================================\n")

# ════════════════════════════════════════════════════════
# 6. BUILD HTML REPORT
# ════════════════════════════════════════════════════════
PALETTE = [
    "#2563EB", "#16A34A", "#DC2626", "#D97706", "#7C3AED",
    "#0891B2", "#DB2777", "#059669", "#EA580C", "#6366F1",
    "#84CC16", "#F59E0B", "#06B6D4", "#8B5CF6", "#EC4899"
]

def jd(obj):
    return json.dumps(obj)

def fmt_m(val):
    if val >= 1e9: return f"{val/1e9:.2f}B"
    if val >= 1e6: return f"{val/1e6:.2f}M"
    if val >= 1e3: return f"{val/1e3:.1f}K"
    return str(int(val))

report_date = datetime.now().strftime("%B %d, %Y")

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Lower Mississippi River — Cargo Demographics Report</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>
  :root {{
    --navy: #0f172a; --blue: #2563EB; --green: #16A34A; --amber: #D97706;
    --red: #DC2626; --text: #1e293b; --muted: #64748b; --bg: #f8fafc;
    --card: #ffffff; --border: #e2e8f0;
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: 'Segoe UI', system-ui, sans-serif; background: var(--bg); color: var(--text); font-size: 14px; }}
  header {{ background: var(--navy); color: #fff; padding: 2rem 2.5rem 1.5rem; }}
  header h1 {{ font-size: 1.7rem; font-weight: 700; letter-spacing: -0.3px; }}
  header p {{ color: #94a3b8; margin-top: .3rem; font-size: .88rem; }}
  .badge {{ display: inline-block; background: rgba(255,255,255,.12); border-radius: 4px;
            padding: 2px 8px; font-size: .78rem; margin-top: .5rem; margin-right: .4rem; }}
  main {{ max-width: 1380px; margin: 0 auto; padding: 2rem 1.5rem 4rem; }}
  h2 {{ font-size: 1.2rem; font-weight: 700; color: var(--navy); margin: 2.2rem 0 1rem;
        border-left: 4px solid var(--blue); padding-left: .7rem; }}
  h3 {{ font-size: 1rem; font-weight: 600; color: var(--navy); margin-bottom: .5rem; }}
  .section-note {{ font-size: .82rem; color: var(--muted); margin: -.5rem 0 1rem; padding-left: 1.1rem; }}
  .kpi-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 1rem; margin-bottom: 1.5rem; }}
  .kpi {{ background: var(--card); border: 1px solid var(--border); border-radius: 8px;
           padding: 1rem 1.2rem; position: relative; overflow: hidden; }}
  .kpi::before {{ content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px; background: var(--kpi-color, var(--blue)); }}
  .kpi .val {{ font-size: 1.65rem; font-weight: 700; color: var(--navy); }}
  .kpi .label {{ font-size: .75rem; color: var(--muted); margin-top: .2rem; }}
  .kpi .sub {{ font-size: .8rem; color: var(--muted); margin-top: .4rem; }}
  .chart-grid {{ display: grid; gap: 1.2rem; }}
  .chart-grid-2 {{ grid-template-columns: repeat(auto-fit, minmax(480px, 1fr)); }}
  .chart-grid-3 {{ grid-template-columns: repeat(auto-fit, minmax(340px, 1fr)); }}
  .chart-card {{ background: var(--card); border: 1px solid var(--border); border-radius: 8px; padding: 1.2rem; }}
  .chart-card canvas {{ max-height: 320px; }}
  .chart-card.tall canvas {{ max-height: 420px; }}
  .chart-card.xlarge canvas {{ max-height: 500px; }}
  .note-box {{ background: #fffbeb; border: 1px solid #fde68a; border-radius: 8px;
               padding: .9rem 1.1rem; font-size: .82rem; color: #92400e; margin: 1rem 0; }}
  .note-box b {{ color: #78350f; }}
  .divider {{ border: none; border-top: 2px solid var(--border); margin: 2.5rem 0 1.5rem; }}
  footer {{ text-align: center; font-size: .78rem; color: var(--muted); padding: 1rem; }}
</style>
</head>
<body>
<header>
  <h1>Lower Mississippi River — Cargo Demographics Report</h1>
  <p>Port Complex: New Orleans LA · Baton Rouge LA · Gramercy LA &nbsp;|&nbsp; Generated {report_date}</p>
  <span class="badge">IMPORTS 2023–2025 (complete)</span>
  <span class="badge">EXPORTS 2023 (latest complete year)</span>
  <span class="badge">Source: Panjiva U.S. Customs Data</span>
</header>

<main>

<!-- ═══════ TOP KPIs ═══════ -->
<h2>Executive Summary</h2>
<div class="kpi-grid">
  <div class="kpi" style="--kpi-color:#2563EB">
    <div class="val">{fmt_m(imp_total_tons)}</div>
    <div class="label">Total Import Tons (2023–2025)</div>
    <div class="sub">{imp_total_recs:,} classified shipment records</div>
  </div>
  <div class="kpi" style="--kpi-color:#DC2626">
    <div class="val">{dry_pct:.0f}%</div>
    <div class="label">Dry Bulk Share of Imports</div>
    <div class="sub">{fmt_m(float(dry["Tons"].sum()))} tons</div>
  </div>
  <div class="kpi" style="--kpi-color:#0891B2">
    <div class="val">{liq_pct:.0f}%</div>
    <div class="label">Liquid Bulk Share of Imports</div>
    <div class="sub">{fmt_m(float(liq["Tons"].sum()))} tons</div>
  </div>
  <div class="kpi" style="--kpi-color:#7C3AED">
    <div class="val">{gas_pct:.0f}%</div>
    <div class="label">Liquid Gas Share of Imports</div>
    <div class="sub">{fmt_m(float(gas["Tons"].sum()))} tons if any</div>
  </div>
  <div class="kpi" style="--kpi-color:#D97706">
    <div class="val">{bb_pct:.0f}%</div>
    <div class="label">Break Bulk Share of Imports</div>
    <div class="sub">{fmt_m(float(imp[imp["Group"]=="Break Bulk"]["Tons"].sum()))} tons</div>
  </div>
  <div class="kpi" style="--kpi-color:#16A34A">
    <div class="val">{fmt_m(exp_total_tons)}</div>
    <div class="label">Total Export Tons (2023)</div>
    <div class="sub">{exp_total_recs:,} shipment records (2023 only)</div>
  </div>
  <div class="kpi" style="--kpi-color:#059669">
    <div class="val">{exp_grain_pct:.0f}%</div>
    <div class="label">Grain Share of Exports</div>
    <div class="sub">{fmt_m(exp_grain_tons)} tons</div>
  </div>
</div>

<!-- ═══════ IMPORTS SECTION ═══════ -->
<h2>Imports — Cargo Demographics (2023–2025)</h2>
<p class="section-note">Classified records arriving at New Orleans, Baton Rouge, and Gramercy — excludes white noise and carrier-excluded shipments.</p>

<div class="chart-grid chart-grid-2">

  <div class="chart-card">
    <h3>Import Cargo Group Share (all years, by tonnage)</h3>
    <canvas id="impPie"></canvas>
  </div>

  <div class="chart-card tall">
    <h3>Monthly Import Tonnage by Group (2023–2025)</h3>
    <canvas id="impMonthly"></canvas>
  </div>

</div>

<div class="chart-grid chart-grid-2" style="margin-top:1.2rem">
  <div class="chart-card">
    <h3>Year-over-Year Comparison — Import Tons by Group</h3>
    <canvas id="impYOY"></canvas>
  </div>
  <div class="chart-card">
    <h3>Imports by Year — Total Tonnage</h3>
    <canvas id="impYearBar"></canvas>
  </div>
</div>

<!-- ═══════ DRY BULK ═══════ -->
<hr class="divider">
<h2>Dry Bulk — Detailed Breakdown</h2>
<p class="section-note">Dry Bulk covers Ferrous Raw Materials, Fertilizers, Agricultural commodities, Minerals & Ores, Construction Materials, Carbon Products, and Non-Ferrous Raw Materials.</p>

<div class="kpi-grid">
  <div class="kpi" style="--kpi-color:#DC2626">
    <div class="val">{fmt_m(float(dry["Tons"].sum()))}</div>
    <div class="label">Total Dry Bulk Tons</div>
    <div class="sub">2023–2025</div>
  </div>
  <div class="kpi" style="--kpi-color:#DC2626">
    <div class="val">{len(dry):,}</div>
    <div class="label">Shipment Records</div>
    <div class="sub">Dry Bulk classified</div>
  </div>
  <div class="kpi" style="--kpi-color:#DC2626">
    <div class="val">{len(dry_commodity):}</div>
    <div class="label">Distinct Commodities</div>
    <div class="sub">Within Dry Bulk group</div>
  </div>
  <div class="kpi" style="--kpi-color:#DC2626">
    <div class="val">{dry_pct:.1f}%</div>
    <div class="label">Share of All Imports</div>
    <div class="sub">By tonnage</div>
  </div>
</div>

<div class="chart-grid chart-grid-2">
  <div class="chart-card tall">
    <h3>Dry Bulk — Tonnage by Commodity</h3>
    <canvas id="dbCommodity"></canvas>
  </div>
  <div class="chart-card tall">
    <h3>Dry Bulk — Top Cargo Categories (Commodity / Cargo)</h3>
    <canvas id="dbCargo"></canvas>
  </div>
</div>

<div class="chart-grid chart-grid-2" style="margin-top:1.2rem">
  <div class="chart-card tall">
    <h3>Dry Bulk — Top Origins (Country of Origin)</h3>
    <canvas id="dbOrigin"></canvas>
  </div>
  <div class="chart-card tall">
    <h3>Dry Bulk — Top Consignees by Tonnage</h3>
    <canvas id="dbConsignees"></canvas>
  </div>
</div>

<!-- ═══════ LIQUID BULK ═══════ -->
<hr class="divider">
<h2>Liquid Bulk — Summary</h2>
<p class="section-note">Includes Petroleum (crude, refined products, fuel oil), Chemicals, Agricultural (vegetable oils), and Fertilizer liquids.</p>

<div class="kpi-grid">
  <div class="kpi" style="--kpi-color:#0891B2">
    <div class="val">{fmt_m(float(liq["Tons"].sum()))}</div>
    <div class="label">Total Liquid Bulk Tons</div>
    <div class="sub">2023–2025</div>
  </div>
  <div class="kpi" style="--kpi-color:#0891B2">
    <div class="val">{liq_pct:.1f}%</div>
    <div class="label">Share of All Imports</div>
    <div class="sub">By tonnage</div>
  </div>
</div>

<div class="chart-grid chart-grid-2">
  <div class="chart-card">
    <h3>Liquid Bulk — Tonnage by Commodity</h3>
    <canvas id="lbCommodity"></canvas>
  </div>
  <div class="chart-card">
    <h3>Liquid Gas — Tonnage by Commodity</h3>
    <canvas id="lgCommodity"></canvas>
  </div>
</div>

<!-- ═══════ FACILITY SECTION ═══════ -->
<hr class="divider">
<h2>Terminal Facility Analysis — Import Cargo (MRTIS Vessel Tracking)</h2>
<p class="section-note">Vessel movements from MRTIS matched to Panjiva import manifests using IMO number (primary) and vessel name (fallback) within a ±3 day date window. Cargo type assigned from the matched manifest record.</p>

<div class="note-box">
  <b>Methodology:</b> MRTIS records vessel crossings of the Southwest Pass Bar and terminal visits on the Lower Mississippi River.
  Inbound laden vessels (high arrival draft) are matched to import BOLs arriving ±3 days of the terminal arrival date.
  {mrtis_note}
</div>

<div class="kpi-grid">
  <div class="kpi" style="--kpi-color:#2563EB">
    <div class="val">{len(fac_by_facility):,}</div>
    <div class="label">Facilities Identified</div>
    <div class="sub">With matched import cargo</div>
  </div>
  <div class="kpi" style="--kpi-color:#2563EB">
    <div class="val">{fmt_m(float(fac_by_facility["ImportTons"].sum()))}</div>
    <div class="label">Total Import Tons (MRTIS)</div>
    <div class="sub">Multi-year 2018–2025</div>
  </div>
  <div class="kpi" style="--kpi-color:#16A34A">
    <div class="val">{fac_df["Commodity"].nunique() if fac_df is not None else 0}</div>
    <div class="label">Commodity Types</div>
    <div class="sub">Across all facilities</div>
  </div>
  <div class="kpi" style="--kpi-color:#D97706">
    <div class="val">{fac_by_facility.head(1)["Facility"].values[0] if len(fac_by_facility) > 0 else "N/A"}</div>
    <div class="label">#1 Facility by Tonnage</div>
    <div class="sub">{fmt_m(float(fac_by_facility.head(1)["ImportTons"].values[0])) if len(fac_by_facility) > 0 else "—"} import tons</div>
  </div>
</div>

<div class="chart-grid chart-grid-2">
  <div class="chart-card xlarge">
    <h3>Top 20 Facilities — Import Tonnage</h3>
    <canvas id="facilityBar"></canvas>
  </div>
  <div class="chart-card xlarge">
    <h3>Top 10 Facilities — Commodity Mix (Imports)</h3>
    <canvas id="facilityStacked"></canvas>
  </div>
</div>

<!-- ═══════ EXPORTS SECTION ═══════ -->
<hr class="divider">
<h2>Exports — Cargo Demographics (2023)</h2>

<div class="note-box">
  <b>Data Completeness Note:</b> Export manifests have an 18–24 month reporting lag compared to imports.
  The 12 Panjiva export files available are all 2023 vintage — <b>2023 is the most recent complete export year.</b>
  2024 and 2025 export data is not yet available in this dataset.
  Import data runs through 2025 and is updated monthly.
</div>

<div class="kpi-grid">
  <div class="kpi" style="--kpi-color:#16A34A">
    <div class="val">{fmt_m(exp_total_tons)}</div>
    <div class="label">Total Export Tons (2023)</div>
    <div class="sub">{exp_total_recs:,} shipment records</div>
  </div>
  <div class="kpi" style="--kpi-color:#16A34A">
    <div class="val">{exp_grain_pct:.0f}%</div>
    <div class="label">Grain Exports</div>
    <div class="sub">{fmt_m(exp_grain_tons)} tons</div>
  </div>
  <div class="kpi" style="--kpi-color:#16A34A">
    <div class="val">{len(exp_top_shippers)}</div>
    <div class="label">Top Exporters Tracked</div>
    <div class="sub">By tonnage</div>
  </div>
</div>

<div class="chart-grid chart-grid-2">
  <div class="chart-card">
    <h3>Export Cargo Group Share (2023, by tonnage)</h3>
    <canvas id="expPie"></canvas>
  </div>
  <div class="chart-card">
    <h3>Monthly Export Tonnage (2023)</h3>
    <canvas id="expMonthly"></canvas>
  </div>
</div>

<div class="chart-grid chart-grid-2" style="margin-top:1.2rem">
  <div class="chart-card tall">
    <h3>Exports — Destination Regions</h3>
    <canvas id="expDest"></canvas>
  </div>
  <div class="chart-card tall">
    <h3>Exports — Top Destination Countries</h3>
    <canvas id="expCountry"></canvas>
  </div>
</div>

<div class="chart-grid" style="margin-top:1.2rem">
  <div class="chart-card tall">
    <h3>Exports — Top Shippers by Tonnage (2023)</h3>
    <canvas id="expShippers"></canvas>
  </div>
</div>

</main>
<footer>Lower Mississippi River Cargo Report &nbsp;|&nbsp; Generated {report_date} &nbsp;|&nbsp; Source: Panjiva U.S. Customs Manifests</footer>

<script>
const P = {jd(PALETTE)};
const P12 = [...P, ...P.slice(0,3)];

// ─── helpers ──────────────────────────────────────────────
function barH(id, labels, data, label, color) {{
  new Chart(document.getElementById(id), {{
    type: 'bar',
    data: {{ labels, datasets: [{{ label, data, backgroundColor: color || P[0], borderRadius: 3 }}] }},
    options: {{ indexAxis: 'y', responsive: true, maintainAspectRatio: true,
      scales: {{ x: {{ ticks: {{ callback: v => v>=1e6 ? (v/1e6).toFixed(1)+'M' : v>=1e3 ? (v/1e3).toFixed(0)+'K' : v }} }} }},
      plugins: {{ legend: {{ display: false }},
        tooltip: {{ callbacks: {{ label: c => (c.raw/1e3).toFixed(1)+' K tons' }} }} }} }} }});
}}
function barV(id, labels, data, label, color) {{
  new Chart(document.getElementById(id), {{
    type: 'bar',
    data: {{ labels, datasets: [{{ label, data, backgroundColor: color || P[0], borderRadius: 3 }}] }},
    options: {{ responsive: true, maintainAspectRatio: true,
      scales: {{ y: {{ ticks: {{ callback: v => v>=1e6 ? (v/1e6).toFixed(1)+'M' : v>=1e3 ? (v/1e3).toFixed(0)+'K' : v }} }} }},
      plugins: {{ legend: {{ display: false }},
        tooltip: {{ callbacks: {{ label: c => (c.raw/1e3).toFixed(1)+' K tons' }} }} }} }} }});
}}
function pie(id, labels, data) {{
  new Chart(document.getElementById(id), {{
    type: 'doughnut',
    data: {{ labels, datasets: [{{ data, backgroundColor: P12 }}] }},
    options: {{ responsive: true, maintainAspectRatio: true,
      plugins: {{ legend: {{ position: 'right', labels: {{ boxWidth: 12, font: {{size:11}} }} }},
        tooltip: {{ callbacks: {{ label: c => c.label + ': ' + (c.raw/1e6).toFixed(2)+'M tons (' +
          (c.raw/c.dataset.data.reduce((a,b)=>a+b,0)*100).toFixed(1)+'%)' }} }} }} }} }});
}}
function lineMulti(id, labels, datasets) {{
  new Chart(document.getElementById(id), {{
    type: 'line',
    data: {{ labels, datasets }},
    options: {{ responsive: true, maintainAspectRatio: true,
      scales: {{ y: {{ ticks: {{ callback: v => v>=1e6 ? (v/1e6).toFixed(1)+'M' : v>=1e3 ? (v/1e3).toFixed(0)+'K' : v }} }} }},
      plugins: {{ legend: {{ position: 'top', labels: {{ boxWidth: 12, font: {{size:11}} }} }},
        tooltip: {{ callbacks: {{ label: c => c.dataset.label + ': ' + (c.raw/1e3).toFixed(1)+' K tons' }} }} }} }} }});
}}
function barGrouped(id, labels, datasets) {{
  new Chart(document.getElementById(id), {{
    type: 'bar',
    data: {{ labels, datasets }},
    options: {{ responsive: true, maintainAspectRatio: true,
      scales: {{ y: {{ ticks: {{ callback: v => v>=1e6 ? (v/1e6).toFixed(1)+'M' : v>=1e3 ? (v/1e3).toFixed(0)+'K' : v }} }} }},
      plugins: {{ legend: {{ position: 'top', labels: {{ boxWidth: 12, font: {{size:11}} }} }},
        tooltip: {{ callbacks: {{ label: c => c.dataset.label + ': ' + (c.raw/1e3).toFixed(1)+' K tons' }} }} }} }} }});
}}

// ─── IMPORT PIE ──────────────────────────────────────────
pie('impPie', {jd(imp_pie_labels)}, {jd(imp_pie_tons)});

// ─── IMPORT MONTHLY TIME SERIES ──────────────────────────
const impTsGroups = {jd(list(imp_ts_data.keys()))};
const impTsColors = {jd(PALETTE[:len(imp_ts_data)])};
const impTsDatasets = impTsGroups.map((g, i) => ({{
  label: g,
  data: {jd(list(imp_ts_data.values()))}[i],
  borderColor: impTsColors[i],
  backgroundColor: impTsColors[i] + '22',
  fill: false, tension: 0.3, borderWidth: 2, pointRadius: 2
}}));
lineMulti('impMonthly', {jd(months_all)}, impTsDatasets);

// ─── YEAR COMPARISON ─────────────────────────────────────
const yoyYears = {jd(yoy_years)}.map(String);
const yoyGroups = {jd(yoy_groups)};
const yoyColors = {jd(PALETTE[:len(yoy_groups)])};
const yoyDatasets = yoyGroups.map((g, i) => ({{
  label: g,
  data: {jd(list(yoy_data.values()))}[i],
  backgroundColor: yoyColors[i], borderRadius: 3
}}));
barGrouped('impYOY', yoyYears, yoyDatasets);

// ─── YEAR TOTAL BAR ──────────────────────────────────────
const yearTotals = {jd([float(round(imp[imp["Year"]==y]["Tons"].sum(),0)) for y in sorted(imp["Year"].dropna().unique().tolist())])};
barV('impYearBar', {jd([str(int(y)) for y in sorted(imp["Year"].dropna().unique().tolist())])}, yearTotals, 'Tons', P[0]);

// ─── DRY BULK ────────────────────────────────────────────
barH('dbCommodity', {jd(db_labels)}, {jd(db_tons)}, 'Tons', P[2]);
barH('dbCargo', {jd(dc_labels)}, {jd(dc_tons)}, 'Tons', '#B45309');
barH('dbOrigin', {jd(dry_orig_labels)}, {jd(dry_orig_tons)}, 'Tons', P[3]);
barH('dbConsignees', {jd(dry_cons_labels)}, {jd(dry_cons_tons)}, 'Tons', P[4]);

// ─── LIQUID BULK ─────────────────────────────────────────
barH('lbCommodity', {jd(lb_labels)}, {jd(lb_tons)}, 'Tons', P[1]);

// ─── LIQUID GAS ──────────────────────────────────────────
{('barH(\'lgCommodity\', ' + jd(lg_labels) + ', ' + jd(lg_tons) + ', \'Tons\', P[5]);') if lg_labels else
 'document.getElementById(\'lgCommodity\').closest(\'.chart-card\').innerHTML += \'<p style="color:#94a3b8;text-align:center;padding:2rem">No Liquid Gas records in LMR imports dataset</p>\';'}



// ─── FACILITY ─────────────────────────────────────────
(function() {{
  const ctx = document.getElementById('facilityBar');
  if (!ctx) return;
  new Chart(ctx, {{
    type: 'bar',
    data: {{
      labels: {jd(fac_labels)},
      datasets: [
        {{label:'Import Tons', data:{jd(fac_imp_tons)}, backgroundColor:'rgba(37,99,235,0.85)', borderRadius:3}},
        {{label:'Export Tons', data:{jd(fac_exp_tons)}, backgroundColor:'rgba(22,163,74,0.85)', borderRadius:3}}
      ]
    }},
    options: {{
      indexAxis:'y', responsive:true, maintainAspectRatio:false,
      plugins:{{legend:{{position:'top'}},tooltip:{{callbacks:{{label:c=>c.dataset.label+': '+fmtN(c.raw)}}}}}},
      scales:{{x:{{ticks:{{callback:v=>fmtN(v)}}}},y:{{ticks:{{font:{{size:11}}}}}}}}
    }}
  }});
}})();

(function() {{
  const ctx2 = document.getElementById('facilityStacked');
  if (!ctx2) return;
  const facComms = {jd(fac_stacked_comms)};
  const facFacs  = {jd(fac_stacked_facs)};
  const facVals  = {jd(fac_stacked_vals)};
  const ds = facComms.map((c,i)=>({{
    label:c, data:facVals[i], backgroundColor:P[i%P.length], borderRadius:2
  }}));
  new Chart(ctx2, {{
    type:'bar',
    data:{{labels:facFacs, datasets:ds}},
    options:{{
      indexAxis:'y', responsive:true, maintainAspectRatio:false,
      plugins:{{legend:{{position:'top',labels:{{boxWidth:12,font:{{size:10}}}}}},
               tooltip:{{callbacks:{{label:c=>c.dataset.label+': '+fmtN(c.raw)}}}}}},
      scales:{{x:{{stacked:true,ticks:{{callback:v=>fmtN(v)}}}},y:{{stacked:true,ticks:{{font:{{size:11}}}}}}}}
    }}
  }});
}})();


// ─── EXPORTS ─────────────────────────────────────────────
pie('expPie', {jd(exp_pie_labels)}, {jd(exp_pie_tons)});
barV('expMonthly', {jd(exp_months)}, {jd(exp_monthly_tons)}, 'Tons', P[4]);
barH('expDest', {jd(exp_dest_labels)}, {jd(exp_dest_tons)}, 'Tons', P[1]);
barH('expCountry', {jd(exp_ctry_labels)}, {jd(exp_ctry_tons)}, 'Tons', P[3]);
barH('expShippers', {jd(exp_ship_labels)}, {jd(exp_ship_tons)}, 'Tons', P[2]);
</script>
</body>
</html>
"""

OUT_HTML.parent.mkdir(parents=True, exist_ok=True)
OUT_HTML.write_text(html, encoding="utf-8")
print(f"Report written → {OUT_HTML}")
print("Open in a browser to view the charts.")

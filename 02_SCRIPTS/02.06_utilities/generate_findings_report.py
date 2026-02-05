"""
Generate Key Findings Report from Port Intelligence Dashboard Data
Version: 1.0.0
"""

import json
from pathlib import Path

# Paths
BASE_DIR = Path(r"G:\My Drive\LLM\project_manifest")
DATA_FILE = BASE_DIR / "03_DOCUMENTATION/03.04_summaries" / "port_intelligence_data.json"
OUTPUT_FILE = BASE_DIR / "03_DOCUMENTATION/03.04_summaries" / "PORT_INTELLIGENCE_KEY_FINDINGS.md"

# Load dashboard data
with open(DATA_FILE, 'r') as f:
    data = json.load(f)

# Generate report
report_lines = []

report_lines.append("# Port Intelligence Dashboard - Key Findings Report")
report_lines.append("")
report_lines.append("**Generated**: " + data['metadata']['generated'])
report_lines.append("**Data Source**: " + data['metadata']['data_source'])
report_lines.append("")
report_lines.append("---")
report_lines.append("")

# Executive Summary
exec_stats = data['executive_summary']
report_lines.append("## Executive Summary")
report_lines.append("")
report_lines.append(f"- **Total Port Calls**: {exec_stats['total_portcalls']:,}")
report_lines.append(f"- **Complete Port Calls**: {exec_stats['complete_portcalls']:,} ({exec_stats['complete_portcalls']/exec_stats['total_portcalls']*100:.1f}%)")
report_lines.append(f"- **Import Entrances**: {exec_stats['total_imports']:,}")
report_lines.append(f"- **Export Clearances**: {exec_stats['total_exports']:,}")
report_lines.append(f"- **Tug-Barge Pairs**: {exec_stats['tug_barge_pairs']:,}")
report_lines.append(f"- **Active Ports**: {exec_stats['unique_ports']}")
report_lines.append("")
report_lines.append(f"- **Average Port Stay**: {exec_stats['avg_port_stay']:.1f} days")
report_lines.append(f"- **Median Port Stay**: {exec_stats['median_port_stay']:.0f} days")
report_lines.append(f"- **Average Import Vessel Size**: {exec_stats['avg_import_dwt']:,.0f} DWT")
report_lines.append(f"- **Average Export Vessel Size**: {exec_stats['avg_export_dwt']:,.0f} DWT")
report_lines.append("")

# Regional Analysis
report_lines.append("## Regional Performance")
report_lines.append("")
regional = sorted(data['regional_analysis'], key=lambda x: x['total_calls'], reverse=True)
report_lines.append("| Coast | Total Calls | Imports | Exports | Avg DWT | Avg Stay (days) |")
report_lines.append("|-------|-------------|---------|---------|---------|-----------------|")
for region in regional:
    avg_dwt = region.get('avg_dwt', 0) or 0
    avg_stay = region.get('avg_stay', 0) or 0
    report_lines.append(f"| {region['coast']} | {region['total_calls']:,} | {region['imports']:,} | {region['exports']:,} | {avg_dwt:,.0f} | {avg_stay:.1f} |")
report_lines.append("")

# Top Ports
report_lines.append("## Top 15 Ports by Total Activity")
report_lines.append("")
ports = data['port_profiles'][:15]
report_lines.append("| Port | Total Calls | Imports | Exports | Avg Import DWT | Avg Stay (days) |")
report_lines.append("|------|-------------|---------|---------|----------------|-----------------|")
for port in ports:
    avg_dwt = port.get('avg_import_dwt', 0) or 0
    avg_stay = port.get('avg_port_stay', 0) or 0
    report_lines.append(f"| {port['port']} | {port['total_calls']:,} | {port['imports']:,} | {port['exports']:,} | {avg_dwt:,.0f} | {avg_stay:.1f} |")
report_lines.append("")

# Ship Size Analysis
report_lines.append("## Ship Size Distribution (Imports)")
report_lines.append("")
import_sizes = sorted(data['ship_size_analysis']['import_sizes'].items(), key=lambda x: x[1], reverse=True)[:15]
total_imports = sum(data['ship_size_analysis']['import_sizes'].values())
report_lines.append("| Ship Size Class | Vessel Count | Percentage |")
report_lines.append("|-----------------|--------------|------------|")
for size_class, count in import_sizes:
    pct = (count / total_imports) * 100
    report_lines.append(f"| {size_class} | {count:,} | {pct:.1f}% |")
report_lines.append("")

# Ship size insights
report_lines.append("### Key Ship Size Insights")
report_lines.append("")
top_3_sizes = import_sizes[:3]
report_lines.append(f"1. **{top_3_sizes[0][0]}** vessels dominate imports with {top_3_sizes[0][1]:,} arrivals ({(top_3_sizes[0][1]/total_imports)*100:.1f}%)")
report_lines.append(f"2. **{top_3_sizes[1][0]}** vessels account for {top_3_sizes[1][1]:,} arrivals ({(top_3_sizes[1][1]/total_imports)*100:.1f}%)")
report_lines.append(f"3. **{top_3_sizes[2][0]}** vessels represent {top_3_sizes[2][1]:,} arrivals ({(top_3_sizes[2][1]/total_imports)*100:.1f}%)")
report_lines.append("")

# Port Efficiency
report_lines.append("## Port Efficiency Analysis")
report_lines.append("")
turnaround = sorted(data['operational_metrics']['turnaround_by_port'], key=lambda x: x['median_days'])
fastest = turnaround[:5]
slowest = turnaround[-5:]

report_lines.append("### Fastest Turnaround (Top 5)")
report_lines.append("")
report_lines.append("| Port | Port Calls | Avg Days | Median Days |")
report_lines.append("|------|------------|----------|-------------|")
for port in fastest:
    report_lines.append(f"| {port['port']} | {port['count']:,} | {port['avg_days']:.1f} | {port['median_days']:.1f} |")
report_lines.append("")

report_lines.append("### Slowest Turnaround (Bottom 5)")
report_lines.append("")
report_lines.append("| Port | Port Calls | Avg Days | Median Days |")
report_lines.append("|------|------------|----------|-------------|")
for port in slowest:
    report_lines.append(f"| {port['port']} | {port['count']:,} | {port['avg_days']:.1f} | {port['median_days']:.1f} |")
report_lines.append("")

# Ship Size vs Turnaround
report_lines.append("## Turnaround Time by Ship Size")
report_lines.append("")
report_lines.append("*Analysis limited to ship size classes with >100 complete port calls*")
report_lines.append("")
size_turnaround = [(k, v) for k, v in data['ship_size_analysis']['complete_by_size'].items()
                   if v['count'] > 100 and k != 'Unknown']
size_turnaround = sorted(size_turnaround, key=lambda x: x[1]['median_stay'])
report_lines.append("| Ship Size Class | Port Calls | Avg Days | Median Days |")
report_lines.append("|-----------------|------------|----------|-------------|")
for size_class, stats in size_turnaround:
    report_lines.append(f"| {size_class} | {stats['count']:,} | {stats['avg_stay']:.1f} | {stats['median_stay']:.1f} |")
report_lines.append("")

# Insights
report_lines.append("### Turnaround Insights")
report_lines.append("")
if len(size_turnaround) > 0:
    fastest_size = size_turnaround[0]
    slowest_size = size_turnaround[-1]
    report_lines.append(f"- **Fastest ship size**: {fastest_size[0]} with median {fastest_size[1]['median_stay']:.1f} days")
    report_lines.append(f"- **Slowest ship size**: {slowest_size[0]} with median {slowest_size[1]['median_stay']:.1f} days")
    report_lines.append(f"- **Range**: {slowest_size[1]['median_stay'] - fastest_size[1]['median_stay']:.1f} days difference")
report_lines.append("")

# Top Cargo Flows
report_lines.append("## Top Import Cargo Flows (Port-Commodity)")
report_lines.append("")
report_lines.append("*Top 20 port-commodity pairs by shipment count*")
report_lines.append("")
import_flows = [f for f in data['cargo_flow']['import_flow'] if f.get('Entrance_HS2') and f['Entrance_HS2'] != 'null'][:20]
report_lines.append("| Port | HS2 Code | Shipments |")
report_lines.append("|------|----------|-----------|")
for flow in import_flows:
    report_lines.append(f"| {flow['Entrance_Port_Consolidated']} | {flow['Entrance_HS2']} | {flow['count']:,} |")
report_lines.append("")

report_lines.append("## Top Export Cargo Flows (Port-Commodity)")
report_lines.append("")
report_lines.append("*Top 20 port-commodity pairs by shipment count*")
report_lines.append("")
export_flows = [f for f in data['cargo_flow']['export_flow'] if f.get('Clearance_HS2') and f['Clearance_HS2'] != 'null'][:20]
report_lines.append("| Port | HS2 Code | Shipments |")
report_lines.append("|------|----------|-----------|")
for flow in export_flows:
    report_lines.append(f"| {flow['Clearance_Port_Consolidated']} | {flow['Clearance_HS2']} | {flow['count']:,} |")
report_lines.append("")

# Strategic Insights
report_lines.append("## Strategic Insights")
report_lines.append("")
report_lines.append("### Port Infrastructure Capacity")
report_lines.append("")
# Find ports with highest avg DWT
ports_by_dwt = sorted([(p['port'], p.get('avg_import_dwt', 0) or 0) for p in data['port_profiles'][:15]],
                      key=lambda x: x[1], reverse=True)[:5]
report_lines.append("**Ports handling largest vessels (by avg import DWT):**")
for port, dwt in ports_by_dwt:
    report_lines.append(f"- {port}: {dwt:,.0f} DWT")
report_lines.append("")

report_lines.append("### Import/Export Balance")
report_lines.append("")
# Calculate import/export ratios
port_ratios = []
for port in data['port_profiles'][:15]:
    if port['exports'] > 0:
        ratio = port['imports'] / port['exports']
        port_ratios.append((port['port'], ratio, port['imports'], port['exports']))

import_heavy = sorted(port_ratios, key=lambda x: x[1], reverse=True)[:5]
export_heavy = sorted(port_ratios, key=lambda x: x[1])[:5]

report_lines.append("**Most Import-Heavy Ports:**")
for port, ratio, imports, exports in import_heavy:
    report_lines.append(f"- {port}: {ratio:.2f}:1 ratio ({imports:,} imports / {exports:,} exports)")
report_lines.append("")

report_lines.append("**Most Export-Heavy Ports:**")
for port, ratio, imports, exports in export_heavy:
    report_lines.append(f"- {port}: {ratio:.2f}:1 ratio ({imports:,} imports / {exports:,} exports)")
report_lines.append("")

# Recommendations
report_lines.append("## Recommendations")
report_lines.append("")
report_lines.append("### For Port Authorities")
report_lines.append("1. **Benchmark turnaround times** against fastest ports in similar size categories")
report_lines.append("2. **Invest in infrastructure** to accommodate larger vessel sizes (dredging, cranes)")
report_lines.append("3. **Analyze cargo specialization** to attract complementary industries")
report_lines.append("4. **Study complete port call patterns** to optimize berth allocation")
report_lines.append("")

report_lines.append("### For Shipping Companies")
report_lines.append("1. **Select ports based on vessel size** - match ship DWT to port capabilities")
report_lines.append("2. **Plan for port stay duration** - median values better than averages for planning")
report_lines.append("3. **Consider cargo specialization** - some ports excel at specific HS2 codes")
report_lines.append("4. **Monitor regional patterns** - Gulf vs Pacific vs Atlantic have different profiles")
report_lines.append("")

report_lines.append("### For Trade Analysts")
report_lines.append("1. **Track HS2 concentration** at major ports for commodity flow analysis")
report_lines.append("2. **Monitor ship size trends** as indicator of trade volume and infrastructure")
report_lines.append("3. **Analyze import/export imbalances** for economic insights")
report_lines.append("4. **Use complete port calls** as proxy for actual trade completion")
report_lines.append("")

# Conclusion
report_lines.append("---")
report_lines.append("")
report_lines.append("## Dashboard Access")
report_lines.append("")
report_lines.append("**Interactive Dashboard**: `port_intelligence_dashboard.html`")
report_lines.append("**Full Documentation**: `PORT_INTELLIGENCE_DASHBOARD_README.md`")
report_lines.append("**Raw Data**: `port_intelligence_data.json`")
report_lines.append("")
report_lines.append("For detailed analysis, charts, and interactive filtering, open the HTML dashboard in a web browser.")

# Write report
with open(OUTPUT_FILE, 'w') as f:
    f.write('\n'.join(report_lines))

print(f"Key findings report generated: {OUTPUT_FILE}")
print(f"Report contains {len(report_lines)} lines")

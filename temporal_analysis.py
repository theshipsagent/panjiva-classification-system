"""
Temporal Analysis: Cargo Flow Trends & Seasonal Patterns
Lower Mississippi River Maritime Commerce

Analyzes:
- Monthly cargo flow trends by commodity
- Seasonal patterns (harvest vs off-season)
- Year-over-year comparisons (2023 vs 2024 vs 2025)
- Terminal visit frequency patterns
- Import/export balance over time
- Growth rates and forecasting

Data Sources:
- phase_07_output.csv: Classified import manifest (854,870 records)
- mrtis_terminal_visits_2024_WITH_RULES.csv: Terminal visits with predictions

Output:
- Monthly trend analysis by commodity
- Seasonal pattern identification
- Year-over-year growth metrics
- Forecast estimates for 2025
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
from collections import defaultdict

class TemporalAnalyzer:
    """Analyze temporal patterns in Lower Mississippi River cargo flows"""

    def __init__(self):
        self.base_dir = Path(__file__).resolve().parent
        self.manifest_path = self.base_dir / "PIPELINE" / "phase_07_enrichment" / "phase_07_output.csv"
        self.terminal_visits_path = self.base_dir / "user_notes" / "mrtis_terminal_visits_2024_WITH_RULES.csv"
        self.output_dir = self.base_dir / "user_notes" / "temporal_analysis"
        self.output_dir.mkdir(exist_ok=True)

        # Lower Mississippi ports
        self.lower_miss_ports = [
            'New Orleans', 'Baton Rouge', 'Gramercy', 'Garyville',
            'Chalmette', 'Venice', 'Morgan City', 'Lake Charles'
        ]

        print("Temporal Analyzer initialized")
        print(f"Output directory: {self.output_dir}")

    def load_manifest_data(self):
        """Load classified import manifest data"""
        print("\nLoading import manifest data...")
        print(f"Source: {self.manifest_path}")

        # Load data
        df = pd.read_csv(
            self.manifest_path,
            low_memory=False
        )

        # Parse date column
        df['Arrival Date'] = pd.to_datetime(df['Arrival Date'], errors='coerce')

        # Filter to Lower Mississippi ports
        df_lower_miss = df[df['Port_Consolidated'].isin(self.lower_miss_ports)].copy()

        # Convert numeric columns
        df_lower_miss['Tons'] = pd.to_numeric(df_lower_miss['Tons'], errors='coerce').fillna(0)

        # Extract year, month, quarter
        df_lower_miss['Year'] = df_lower_miss['Arrival Date'].dt.year
        df_lower_miss['Month'] = df_lower_miss['Arrival Date'].dt.month
        df_lower_miss['Quarter'] = df_lower_miss['Arrival Date'].dt.quarter
        df_lower_miss['YearMonth'] = df_lower_miss['Arrival Date'].dt.to_period('M')
        df_lower_miss['MonthName'] = df_lower_miss['Arrival Date'].dt.strftime('%B')

        print(f"Loaded: {len(df_lower_miss):,} import records")
        print(f"Date range: {df_lower_miss['Arrival Date'].min()} to {df_lower_miss['Arrival Date'].max()}")
        print(f"Years covered: {sorted(df_lower_miss['Year'].dropna().unique())}")

        return df_lower_miss

    def load_terminal_visits(self):
        """Load terminal visit data with Phase 3 predictions"""
        print("\nLoading terminal visit data...")
        print(f"Source: {self.terminal_visits_path}")

        df = pd.read_csv(self.terminal_visits_path, low_memory=False)

        # Parse date (use ArrivalTime_dt if available, otherwise ArrivalTime)
        if 'ArrivalTime_dt' in df.columns:
            df['Visit_Date'] = pd.to_datetime(df['ArrivalTime_dt'], errors='coerce')
        else:
            df['Visit_Date'] = pd.to_datetime(df['ArrivalTime'], errors='coerce')

        df['Year'] = df['Visit_Date'].dt.year
        df['Month'] = df['Visit_Date'].dt.month
        df['Quarter'] = df['Visit_Date'].dt.quarter
        df['YearMonth'] = df['Visit_Date'].dt.to_period('M')
        df['MonthName'] = df['Visit_Date'].dt.strftime('%B')

        print(f"Loaded: {len(df):,} terminal visits")
        print(f"Date range: {df['Visit_Date'].min()} to {df['Visit_Date'].max()}")

        return df

    def analyze_monthly_trends(self, df):
        """Analyze monthly cargo trends by commodity"""
        print("\n" + "="*80)
        print("MONTHLY CARGO TRENDS ANALYSIS")
        print("="*80)

        # Monthly totals by commodity
        monthly_commodity = df.groupby(['YearMonth', 'Commodity']).agg({
            'Tons': 'sum',
            'Bill of Lading Number': 'count'
        }).reset_index()

        monthly_commodity.columns = ['YearMonth', 'Commodity', 'Tons', 'Shipments']
        monthly_commodity['Tons'] = monthly_commodity['Tons'].astype(float)

        # Sort by month and tonnage
        monthly_commodity = monthly_commodity.sort_values(['YearMonth', 'Tons'], ascending=[True, False])

        # Get top 10 commodities by total tonnage
        top_commodities = df.groupby('Commodity')['Tons'].sum().nlargest(10).index.tolist()

        print(f"\nTop 10 Commodities by Total Tonnage:")
        for i, commodity in enumerate(top_commodities, 1):
            total_tons = df[df['Commodity'] == commodity]['Tons'].sum()
            print(f"  {i:2d}. {commodity}: {total_tons:,.0f} tons")

        # Filter to top commodities
        monthly_top = monthly_commodity[monthly_commodity['Commodity'].isin(top_commodities)]

        # Save detailed monthly data
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = self.output_dir / f"monthly_commodity_trends_{timestamp}.csv"
        monthly_top.to_csv(output_file, index=False)
        print(f"\nSaved: {output_file}")

        return monthly_commodity, top_commodities

    def analyze_seasonal_patterns(self, df):
        """Identify seasonal patterns by commodity"""
        print("\n" + "="*80)
        print("SEASONAL PATTERN ANALYSIS")
        print("="*80)

        # Group by month (across all years) and commodity
        seasonal = df.groupby(['Month', 'MonthName', 'Commodity']).agg({
            'Tons': 'sum',
            'Bill of Lading Number': 'count'
        }).reset_index()

        seasonal.columns = ['Month', 'MonthName', 'Commodity', 'Tons', 'Shipments']
        seasonal = seasonal.sort_values(['Commodity', 'Month'])

        # Calculate average monthly tonnage by commodity
        commodity_monthly_avg = seasonal.groupby('Commodity')['Tons'].mean()

        # Identify peak months for top commodities
        print("\nSeasonal Patterns - Peak Months:")
        print("-" * 80)

        top_commodities = df.groupby('Commodity')['Tons'].sum().nlargest(15).index.tolist()

        seasonal_summary = []

        for commodity in top_commodities:
            commodity_data = seasonal[seasonal['Commodity'] == commodity].copy()
            if len(commodity_data) == 0:
                continue

            # Find peak month
            peak_row = commodity_data.loc[commodity_data['Tons'].idxmax()]
            low_row = commodity_data.loc[commodity_data['Tons'].idxmin()]

            avg_tons = commodity_data['Tons'].mean()
            peak_tons = peak_row['Tons']
            low_tons = low_row['Tons']

            seasonality_ratio = peak_tons / low_tons if low_tons > 0 else 0

            print(f"\n{commodity}:")
            print(f"  Peak: {peak_row['MonthName']} ({peak_tons:,.0f} tons)")
            print(f"  Low: {low_row['MonthName']} ({low_tons:,.0f} tons)")
            print(f"  Seasonality Ratio: {seasonality_ratio:.2f}x")

            seasonal_summary.append({
                'Commodity': commodity,
                'Peak_Month': peak_row['MonthName'],
                'Peak_Tons': peak_tons,
                'Low_Month': low_row['MonthName'],
                'Low_Tons': low_tons,
                'Average_Monthly_Tons': avg_tons,
                'Seasonality_Ratio': seasonality_ratio
            })

        # Save seasonal patterns
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = self.output_dir / f"seasonal_patterns_{timestamp}.csv"
        seasonal.to_csv(output_file, index=False)
        print(f"\nSaved detailed seasonal data: {output_file}")

        # Save seasonal summary
        summary_file = self.output_dir / f"seasonal_summary_{timestamp}.csv"
        pd.DataFrame(seasonal_summary).to_csv(summary_file, index=False)
        print(f"Saved seasonal summary: {summary_file}")

        return seasonal, seasonal_summary

    def analyze_year_over_year(self, df):
        """Compare year-over-year changes"""
        print("\n" + "="*80)
        print("YEAR-OVER-YEAR COMPARISON")
        print("="*80)

        # Annual totals by commodity
        annual = df.groupby(['Year', 'Commodity']).agg({
            'Tons': 'sum',
            'Bill of Lading Number': 'count'
        }).reset_index()

        annual.columns = ['Year', 'Commodity', 'Tons', 'Shipments']
        annual = annual.sort_values(['Commodity', 'Year'])

        # Get top commodities
        top_commodities = df.groupby('Commodity')['Tons'].sum().nlargest(15).index.tolist()

        print("\nYear-over-Year Growth Analysis:")
        print("-" * 80)

        yoy_summary = []

        for commodity in top_commodities:
            commodity_data = annual[annual['Commodity'] == commodity].copy()

            if len(commodity_data) < 2:
                continue

            print(f"\n{commodity}:")

            # Calculate YoY growth
            commodity_data = commodity_data.sort_values('Year')
            years = commodity_data['Year'].tolist()
            tons = commodity_data['Tons'].tolist()

            for i in range(len(years)):
                print(f"  {int(years[i])}: {tons[i]:,.0f} tons", end="")

                if i > 0:
                    growth = tons[i] - tons[i-1]
                    growth_pct = (growth / tons[i-1] * 100) if tons[i-1] > 0 else 0
                    print(f" (YoY: {growth:+,.0f} tons, {growth_pct:+.1f}%)", end="")

                print()

                if i > 0:
                    yoy_summary.append({
                        'Commodity': commodity,
                        'Year': int(years[i]),
                        'Prior_Year': int(years[i-1]),
                        'Current_Tons': tons[i],
                        'Prior_Tons': tons[i-1],
                        'Change_Tons': growth,
                        'Change_Percent': growth_pct
                    })

        # Overall annual summary
        print("\n" + "-" * 80)
        print("Overall Annual Totals:")
        print("-" * 80)

        annual_total = df.groupby('Year').agg({
            'Tons': 'sum',
            'Bill of Lading Number': 'count',
            'Country of Origin (F)': 'nunique',
            'Commodity': 'nunique'
        }).reset_index()

        annual_total.columns = ['Year', 'Total_Tons', 'Total_Shipments', 'Countries', 'Commodities']

        for _, row in annual_total.iterrows():
            print(f"\n{int(row['Year'])}:")
            print(f"  Total Tonnage: {row['Total_Tons']:,.0f} tons")
            print(f"  Total Shipments: {row['Total_Shipments']:,.0f}")
            print(f"  Origin Countries: {int(row['Countries'])}")
            print(f"  Commodities: {int(row['Commodities'])}")

        # Save YoY analysis
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        output_file = self.output_dir / f"annual_totals_{timestamp}.csv"
        annual.to_csv(output_file, index=False)
        print(f"\nSaved annual data: {output_file}")

        yoy_file = self.output_dir / f"year_over_year_growth_{timestamp}.csv"
        pd.DataFrame(yoy_summary).to_csv(yoy_file, index=False)
        print(f"Saved YoY growth data: {yoy_file}")

        overall_file = self.output_dir / f"annual_summary_{timestamp}.csv"
        annual_total.to_csv(overall_file, index=False)
        print(f"Saved annual summary: {overall_file}")

        return annual, yoy_summary, annual_total

    def analyze_terminal_visit_patterns(self, df_visits):
        """Analyze temporal patterns in terminal visits"""
        print("\n" + "="*80)
        print("TERMINAL VISIT TEMPORAL PATTERNS")
        print("="*80)

        # Monthly visit counts by cargo prediction
        monthly_visits = df_visits.groupby(['YearMonth', 'PredictedCargo']).size().reset_index()
        monthly_visits.columns = ['YearMonth', 'PredictedCargo', 'Visits']
        monthly_visits = monthly_visits.sort_values(['YearMonth', 'Visits'], ascending=[True, False])

        # Top predicted cargo types
        top_cargo_types = df_visits['PredictedCargo'].value_counts().head(10).index.tolist()

        print("\nTop 10 Predicted Cargo Types (2024 Terminal Visits):")
        for i, cargo in enumerate(top_cargo_types, 1):
            count = (df_visits['PredictedCargo'] == cargo).sum()
            print(f"  {i:2d}. {cargo}: {count:,} visits")

        # Monthly totals
        print("\nMonthly Visit Totals (2024):")
        print("-" * 60)

        monthly_total = df_visits.groupby('YearMonth').size().reset_index()
        monthly_total.columns = ['YearMonth', 'Total_Visits']

        for _, row in monthly_total.iterrows():
            print(f"  {row['YearMonth']}: {row['Total_Visits']:,} visits")

        # Save terminal visit patterns
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        output_file = self.output_dir / f"monthly_terminal_visits_{timestamp}.csv"
        monthly_visits.to_csv(output_file, index=False)
        print(f"\nSaved: {output_file}")

        return monthly_visits

    def analyze_import_export_balance(self, df_manifest, df_visits):
        """Analyze import vs export balance over time"""
        print("\n" + "="*80)
        print("IMPORT/EXPORT BALANCE ANALYSIS")
        print("="*80)

        # Import volumes by month (from manifest)
        monthly_imports = df_manifest.groupby('YearMonth').agg({
            'Tons': 'sum',
            'Bill of Lading Number': 'count'
        }).reset_index()
        monthly_imports.columns = ['YearMonth', 'Import_Tons', 'Import_Shipments']

        # Export estimates by month (from LOADING operations in terminal visits)
        df_export = df_visits[df_visits['OperationType'] == 'LOADING'].copy()
        monthly_exports = df_export.groupby('YearMonth').size().reset_index()
        monthly_exports.columns = ['YearMonth', 'Export_Loadings']

        # Merge
        balance = pd.merge(monthly_imports, monthly_exports, on='YearMonth', how='outer').fillna(0)
        balance = balance.sort_values('YearMonth')

        print("\nMonthly Import/Export Balance:")
        print("-" * 80)
        print(f"{'Month':<15} {'Import Tons':>15} {'Import Count':>15} {'Export Loadings':>15}")
        print("-" * 80)

        for _, row in balance.iterrows():
            print(f"{str(row['YearMonth']):<15} {row['Import_Tons']:>15,.0f} {row['Import_Shipments']:>15,.0f} {row['Export_Loadings']:>15,.0f}")

        # Save balance data
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = self.output_dir / f"import_export_balance_{timestamp}.csv"
        balance.to_csv(output_file, index=False)
        print(f"\nSaved: {output_file}")

        return balance

    def generate_forecast_estimates(self, annual_total):
        """Generate simple forecast for 2025 based on growth trends"""
        print("\n" + "="*80)
        print("2025 FORECAST ESTIMATES")
        print("="*80)

        # Calculate average growth rate from available years
        if len(annual_total) < 2:
            print("Insufficient data for forecasting (need at least 2 years)")
            return None

        annual_total = annual_total.sort_values('Year')
        years = annual_total['Year'].tolist()
        tons = annual_total['Total_Tons'].tolist()

        # Calculate YoY growth rates
        growth_rates = []
        for i in range(1, len(years)):
            growth_pct = (tons[i] - tons[i-1]) / tons[i-1] * 100
            growth_rates.append(growth_pct)

        avg_growth_rate = np.mean(growth_rates)

        # Simple forecast: apply average growth rate to most recent year
        latest_year = years[-1]
        latest_tons = tons[-1]

        if latest_year < 2025:
            years_ahead = 2025 - latest_year
            forecast_2025 = latest_tons * ((1 + avg_growth_rate/100) ** years_ahead)

            print(f"\nHistorical Growth Rate: {avg_growth_rate:+.2f}% per year")
            print(f"Most Recent Year ({int(latest_year)}): {latest_tons:,.0f} tons")
            print(f"\n2025 Forecast: {forecast_2025:,.0f} tons")
            print(f"  (assuming {avg_growth_rate:+.2f}% annual growth)")

            return {
                'Forecast_Year': 2025,
                'Base_Year': int(latest_year),
                'Base_Tonnage': latest_tons,
                'Average_Growth_Rate': avg_growth_rate,
                'Forecast_Tonnage': forecast_2025
            }
        else:
            print(f"Most recent data is from {int(latest_year)}, cannot forecast 2025")
            return None

    def generate_comprehensive_report(self):
        """Generate comprehensive temporal analysis report"""
        print("\n" + "="*80)
        print("COMPREHENSIVE TEMPORAL ANALYSIS")
        print("Lower Mississippi River Cargo Flows")
        print("="*80)

        # Load data
        df_manifest = self.load_manifest_data()
        df_visits = self.load_terminal_visits()

        # Run analyses
        monthly_trends, top_commodities = self.analyze_monthly_trends(df_manifest)
        seasonal_patterns, seasonal_summary = self.analyze_seasonal_patterns(df_manifest)
        annual_data, yoy_growth, annual_total = self.analyze_year_over_year(df_manifest)
        terminal_patterns = self.analyze_terminal_visit_patterns(df_visits)
        balance_data = self.analyze_import_export_balance(df_manifest, df_visits)
        forecast = self.generate_forecast_estimates(annual_total)

        # Generate summary report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = self.output_dir / f"temporal_analysis_report_{timestamp}.txt"

        with open(report_file, 'w') as f:
            f.write("="*80 + "\n")
            f.write("TEMPORAL ANALYSIS REPORT\n")
            f.write("Lower Mississippi River Cargo Flows\n")
            f.write("="*80 + "\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Analysis Period: {df_manifest['Arrival Date'].min()} to {df_manifest['Arrival Date'].max()}\n\n")

            f.write("KEY FINDINGS:\n\n")

            # Annual summary
            f.write("1. ANNUAL IMPORT TOTALS:\n")
            for _, row in annual_total.iterrows():
                f.write(f"   {int(row['Year'])}: {row['Total_Tons']:,.0f} tons ({row['Total_Shipments']:,.0f} shipments)\n")
            f.write("\n")

            # Top commodities
            f.write("2. TOP COMMODITIES (All Years Combined):\n")
            for i, commodity in enumerate(top_commodities[:10], 1):
                total_tons = df_manifest[df_manifest['Commodity'] == commodity]['Tons'].sum()
                f.write(f"   {i:2d}. {commodity}: {total_tons:,.0f} tons\n")
            f.write("\n")

            # Seasonal patterns
            f.write("3. SEASONAL PATTERNS:\n")
            for item in seasonal_summary[:5]:
                f.write(f"   {item['Commodity']}:\n")
                f.write(f"      Peak: {item['Peak_Month']} ({item['Peak_Tons']:,.0f} tons)\n")
                f.write(f"      Low: {item['Low_Month']} ({item['Low_Tons']:,.0f} tons)\n")
                f.write(f"      Seasonality Ratio: {item['Seasonality_Ratio']:.2f}x\n\n")

            # Terminal visits
            f.write("4. TERMINAL VISIT PATTERNS (2024):\n")
            f.write(f"   Total Visits: {len(df_visits):,}\n")
            f.write(f"   Export Loadings: {(df_visits['OperationType'] == 'LOADING').sum():,}\n")
            f.write(f"   Discharge OperationTypes: {(df_visits['OperationType'] == 'DISCHARGE').sum():,}\n\n")

            # Forecast
            if forecast:
                f.write("5. 2025 FORECAST:\n")
                f.write(f"   Estimated Tonnage: {forecast['Forecast_Tonnage']:,.0f} tons\n")
                f.write(f"   Based on {forecast['Average_Growth_Rate']:+.2f}% annual growth rate\n\n")

            f.write("\n" + "="*80 + "\n")
            f.write("All detailed outputs saved to: user_notes/temporal_analysis/\n")
            f.write("="*80 + "\n")

        print(f"\n{'='*80}")
        print(f"TEMPORAL ANALYSIS COMPLETE")
        print(f"{'='*80}")
        print(f"\nReport saved: {report_file}")
        print(f"All outputs saved to: {self.output_dir}")

        return report_file


if __name__ == "__main__":
    analyzer = TemporalAnalyzer()
    analyzer.generate_comprehensive_report()

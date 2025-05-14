# src/main.py
import sys
import argparse
from api.ichooserx_api import IChooseRxAPI
from sheets.google_sheets import GoogleSheetsExporter
from utils.formatters import format_export_data, calculate_clean_score, count_manufacturers

def main():
    parser = argparse.ArgumentParser(description="Fetch filtered drug data and export to Google Sheets.")
    parser.add_argument(
        "--drug-names",
        nargs="+",
        required=True,
        help="One or more generic drug names or active ingredients/substance names (e.g. --drug-names Dextroamphetamine Ibuprofen Metformin Melatonin)"
    )
    parser.add_argument(
        "--filters",
        nargs="*",
        default=[],
        help="Optional filters (e.g. --filters artificial_colors artificial_sweeteners artificial_flavors preservatives added_sugar sugar_alcohols gluten possible_endocrine_disruptors vegan potentially_harmful_additives)",
    )
    args = parser.parse_args()

    api = IChooseRxAPI()
    raw_data = api.get_export_summaries(args.drug_names, args.filters)

    if not raw_data:
        print("❌ No data received from API.")
        sys.exit(1)

    formatted_data = format_export_data(raw_data)
    exporter = GoogleSheetsExporter()
    exporter.export_data(formatted_data)

    print("✅ Export complete.")

if __name__ == "__main__":
    main()

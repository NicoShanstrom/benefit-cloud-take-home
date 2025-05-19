import pandas as pd
from utils.alignment_score import calculate_alignment_score
from utils.manufacturer_utils import count_manufacturers
from utils.timestamp import current_timestamp

def format_export_data(raw_data):
    timestamp = current_timestamp()
    filters_used = raw_data.get("filters_applied", [])
    filters_str = ", ".join([f["label"] for f in filters_used])

    rows = []

    rows.append(["Created At:", f"{timestamp}"])
    rows.append(["Filters Used:", filters_str])
    rows.append([])

    summary_header = ["Drug Name", "Total Results", "Filtered Results", "Alignment Score (0-10)"]
    rows.append(summary_header)
    rows.append(["", "", "", "Based on % of drug variants matching your selected filters"])

    summary_data = []
    all_manufacturer_sections = []

    for summary in raw_data.get("summary", []):
        drug_name = summary["drug_name"]
        total = summary.get("total_results", 0)
        filtered = summary.get("filtered_results", 0)
        alignment_score = calculate_alignment_score(filtered, total)

        summary_data.append([drug_name, total, filtered, alignment_score])

        mfr_counts = count_manufacturers(summary.get("data", []))
        manufacturer_section = [[]]  
        manufacturer_section.append([f"Top Manufacturers for {drug_name}", "Count"])

        mfr_df = pd.DataFrame({
            "Manufacturer": list(mfr_counts.keys()),
            "Count": list(mfr_counts.values())
        }).sort_values(by="Count", ascending=False)

        for _, row in mfr_df.iterrows():
            manufacturer_section.append([row["Manufacturer"], row["Count"]])

        all_manufacturer_sections.extend(manufacturer_section)

    summary_df = pd.DataFrame(summary_data, columns=summary_header)
    summary_df.sort_values(by="Filtered Results", ascending=False, inplace=True)
    rows.extend(summary_df.values.tolist())

    rows.extend(all_manufacturer_sections)

    return rows
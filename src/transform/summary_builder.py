import pandas as pd
from utils.alignment_score import calculate_alignment_score
from utils.manufacturer_utils import count_manufacturers
from utils.timestamp import current_timestamp

def format_export_data(raw_data):
    timestamp = current_timestamp()
    filters_used = raw_data.get("filters_applied", [])
    filters_str = ", ".join([f["label"] for f in filters_used])

    summary_rows = []
    manufacturer_sections = []

    drug_summaries = raw_data.get("summary", [])
    for summary in drug_summaries:
        drug_name = summary["drug_name"]
        total = summary.get("total_results", 0)
        filtered = summary.get("filtered_results", 0)
        alignment_score = calculate_alignment_score(filtered, total)
        summary_rows.append([drug_name, total, filtered, alignment_score])

        mfr_counts = count_manufacturers(summary.get("data", []))
        mfr_df = pd.DataFrame({
            f"Top Manufacturers for {drug_name}": list(mfr_counts.keys()),
            "Count": list(mfr_counts.values())
        })
        manufacturer_sections.append(mfr_df)

    summary_df = pd.DataFrame(
        summary_rows,
        columns=["Drug Name", "Total Results", "Filtered Results", "Alignment Score (0-10)*"]
    )

    metadata = pd.DataFrame([
        ["Created At:", timestamp],
        ["Filters Used:", filters_str],
        ["", ""],
        ["", "*Based on % of drug variants matching your selected filters"],
        ["", ""]
    ])

    full_df = pd.concat([metadata, summary_df], ignore_index=True)
    for mfr_df in manufacturer_sections:
        full_df = pd.concat([full_df, pd.DataFrame([["", ""]]), mfr_df], ignore_index=True)

    return full_df
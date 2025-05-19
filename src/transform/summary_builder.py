# from utils.alignment_score import calculate_alignment_score
# from utils.manufacturer_utils import count_manufacturers
# from utils.timestamp import current_timestamp

# def format_export_data(raw_data):
#     timestamp = current_timestamp()
#     filters_used = raw_data.get("filters_applied", [])
#     filters_str = ", ".join([f["label"] for f in filters_used])
#     rows = []

#     rows.append(["Created At:", timestamp])
#     rows.append(["Filters Used:", filters_str])
#     rows.append([])

#     rows.append([
#         "Drug Name",
#         "Total Results",
#         "Filtered Results",
#         "Alignment Score (1-10)",
#     ])

#     rows.append(["", "", "", "Based on % of drug variants matching your selected filters"])

#     drug_summaries = raw_data.get("summary", [])
#     manufacturer_sections = []

#     for summary in drug_summaries:
#         drug_name = summary["drug_name"]
#         total = summary.get("total_results", 0)
#         filtered = summary.get("filtered_results", 0)
#         alignment_score = calculate_alignment_score(filtered, total)
#         manufacturer_counts = count_manufacturers(summary.get("data", []))

#         rows.append([drug_name, total, filtered, alignment_score])

#         manufacturer_sections.append([])
#         manufacturer_sections.append([f"Top Manufacturers for {drug_name}", "Count"])
#         for name, count in manufacturer_counts.items():
#             manufacturer_sections.append([name, count])

#     rows.append([])

#     rows.extend(manufacturer_sections)

#     return rows

import pandas as pd
from utils.alignment_score import calculate_alignment_score
from utils.manufacturer_utils import count_manufacturers
from utils.timestamp import current_timestamp

def format_export_data(raw_data):
    timestamp = current_timestamp()
    filters_used = raw_data.get("filters_applied", [])
    filters_str = ", ".join([f["label"] for f in filters_used])

    rows = []

    # --- Metadata ---
    rows.append(["Created At:", timestamp])
    rows.append(["Filters Used:", filters_str])
    rows.append([])

    # --- Summary Header + Footnote ---
    summary_header = ["Drug Name", "Total Results", "Filtered Results", "Alignment Score (0-10)"]
    rows.append(summary_header)
    rows.append(["", "", "", "Based on % of drug variants matching your selected filters"])

    # --- Summary DataFrame ---
    summary_data = []
    all_manufacturer_sections = []

    for summary in raw_data.get("summary", []):
        drug_name = summary["drug_name"]
        total = summary.get("total_results", 0)
        filtered = summary.get("filtered_results", 0)
        alignment_score = calculate_alignment_score(filtered, total)

        summary_data.append([drug_name, total, filtered, alignment_score])

        # Create DataFrame for manufacturers
        mfr_counts = count_manufacturers(summary.get("data", []))
        manufacturer_section = [[]]  
        manufacturer_section.append([f"Top Manufacturers for {drug_name}", "Count"])
        for name, count in mfr_counts.items():
            manufacturer_section.append([name, count])

        all_manufacturer_sections.extend(manufacturer_section)

    # Convert summary DataFrame to list-of-lists
    summary_df = pd.DataFrame(summary_data, columns=summary_header)
    rows.extend(summary_df.values.tolist())

    # Combine everything
    rows.extend(all_manufacturer_sections)

    return rows
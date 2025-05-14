from utils.alignment_score import calculate_alignment_score
from utils.manufacturer_utils import count_manufacturers
from utils.timestamp import current_timestamp

def format_export_data(raw_data):
    timestamp = current_timestamp()
    filters_used = raw_data.get("filters_applied", [])
    filters_str = ", ".join([f["label"] for f in filters_used])
    rows = []

    # Header rows
    rows.append(["Export Timestamp:", timestamp])
    rows.append(["Filters Used:", filters_str])
    rows.append([])  # Spacer row

    # Column headers
    rows.append([
        "Drug Name",
        "Total Results",
        "Filtered Results",
        "Alignment Score (1-10)",
        "Top Manufacturers"
    ])

    drug_summaries = raw_data.get("summary", [])

    for summary in drug_summaries:
        drug_name = summary["drug_name"]
        total = summary.get("total_results", 0)
        filtered = summary.get("filtered_results", 0)
        alignment_score = calculate_alignment_score(filtered, total)
        manufacturer_counts = count_manufacturers(summary.get("data", []))
        top_mfrs = ", ".join([f"{k} ({v})" for k, v in manufacturer_counts.items()])

        rows.append([drug_name, total, filtered, alignment_score, top_mfrs])

    return rows


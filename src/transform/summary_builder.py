from utils.clean_score import calculate_clean_score
from utils.manufacturer_utils import count_manufacturers
from utils.timestamp import current_timestamp

def format_export_data(raw_data):
    timestamp = current_timestamp()
    filters_used = raw_data.get("filters_applied", [])
    filters_str = ", ".join([f["label"] for f in filters_used])

    rows = []

    # header row showing what filters were used
    rows.append(["Created At:", timestamp])
    rows.append(["Filters Used:", filters_str])
    rows.append([])  # Blank row for spacing

    # Column headers
    rows.append([
        "Drug Name",
        "Total Results",
        "Filtered Results",
        "Clean Score (1-10)",
        "Top Manufacturers"
    ])

    if isinstance(raw_data, dict):
        drug_summaries = [raw_data]
    else:
        drug_summaries = raw_data
    for summary in drug_summaries:
      drug_name = summary["drug_name"]
      total = summary["total_results"]
      filtered = summary["filtered_results"]
      clean_score = calculate_clean_score(total, filtered)
      manufacturer_counts = count_manufacturers(summary.get("data", []))
      top_mfrs = ", ".join([f"{k} ({v})" for k, v in manufacturer_counts.items()])
    
      rows.append([drug_name, total, filtered, clean_score, top_mfrs])

    return rows

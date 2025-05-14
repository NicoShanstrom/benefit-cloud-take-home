from collections import Counter

def count_manufacturers(drug_data: list) -> dict:
    manufacturers = [entry["manufacturer_name"] for entry in drug_data if "manufacturer_name" in entry]
    return dict(Counter(manufacturers))

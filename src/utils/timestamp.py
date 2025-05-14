from datetime import datetime, timezone

def current_timestamp():
    """Returns the current UTC timestamp as a human-readable string."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S %Z")

def safe_sheet_timestamp():
    """Returns a UTC timestamp string safe for use in Google Sheet titles (no colons)."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H-%M-%S UTC")

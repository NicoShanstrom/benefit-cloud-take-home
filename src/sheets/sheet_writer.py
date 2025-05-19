import os
import gspread
from dotenv import load_dotenv
from oauth2client.service_account import ServiceAccountCredentials
from utils.timestamp import current_timestamp

load_dotenv()

class GoogleSheetsExporter:
    def __init__(self, sheet_name="Drug Export Summary"):
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive"
        ]
        service_account_path = os.environ.get("GOOGLE_CREDENTIALS_PATH")
        if not service_account_path or not os.path.exists(service_account_path):
            raise FileNotFoundError("Missing or invalid GOOGLE_CREDENTIALS_PATH in environment")
        creds = ServiceAccountCredentials.from_json_keyfile_name(service_account_path, scope)
        client = gspread.authorize(creds)

        self.sheet = client.open(sheet_name).sheet1

    def export_data(self, rows):
        timestamp = current_timestamp()
        new_sheet_title = f"Export {timestamp}"

        try:
            new_sheet = self.sheet.spreadsheet.add_worksheet(title=new_sheet_title, rows=str(len(rows)+10), cols="10")
        except Exception as e:
            print(f"[ERROR] Failed to create new worksheet: {e}")
            return

        for i, row in enumerate(rows):
            try:
                new_sheet.insert_row(row, index=i+1)
            except Exception as e:
                print(f"[ERROR] Failed to write row {i+1}: {e}")

        print(f"✅ Data written to new worksheet: '{new_sheet_title}'")

import os
import gspread
import pandas as pd
from dotenv import load_dotenv
from oauth2client.service_account import ServiceAccountCredentials
from gspread_dataframe import set_with_dataframe
from utils.timestamp import safe_sheet_timestamp

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

        # self.sheet = client.open(sheet_name).sheet1
        self.spreadsheet = client.open(sheet_name)

    def export_data(self, df: pd.DataFrame):
        timestamp = safe_sheet_timestamp()
        sheet_title = f"Export {timestamp}"

        try:
            worksheet = self.spreadsheet.add_worksheet(title=sheet_title, rows="1", cols="1")

            set_with_dataframe(worksheet, df)
            print(f"Data written to new worksheet: '{sheet_title}'")
        except Exception as e:
            print(f"[ERROR] Failed to create or write to worksheet: {e}")
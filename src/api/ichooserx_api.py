import os
from dotenv import load_dotenv
from api.base_api import BaseAPIClient

load_dotenv()

class IChooseRxAPI(BaseAPIClient):
    def __init__(self):
        base_url = os.getenv("ICHOOSERX_API_BASE_URL")
        if not base_url:
            raise ValueError("Missing ICHOOSERX_API_BASE_URL in environment variables")
        super().__init__(base_url)

    def get_export_summaries(self, drug_names, filters):
        params = {
            "drug_names[]": drug_names,
            "filters[]": filters
        }
        return self.get("export_summaries", params=params)

from api.base_api import BaseAPIClient

class IChooseRxAPI(BaseAPIClient):
    def __init__(self):
        super().__init__("https://ichooserx-api-387898904134.us-central1.run.app/api/v1")

    def get_export_summaries(self, drug_names, filters):
        params = {
            "drug_names[]": drug_names,
            "filters[]": filters
        }
        return self.get("export_summaries", params=params)

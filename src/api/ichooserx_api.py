from .base_api import BaseAPIClient

class IChooseRxAPIClient(BaseAPIClient):
    def get_export_summary(self, drug_names, filters):
        if isinstance(drug_names, str):
            drug_names = [drug_names]
        
        params = {
            "drug_names[]": drug_names,
            "filters[]": filters
        }

        return self.get("export_summaries", params=params)

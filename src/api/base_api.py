import httpx

class BaseAPIClient:
    def __init__(self, base_url: str, timeout: int = 30):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.client = httpx.Client(timeout=self.timeout)

    def get(self, endpoint: str, params: dict = None):
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        try:
            response = self.client.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"[ERROR] API returned error: {e.response.status_code} - {e.response.text}")
        except httpx.RequestError as e:
            print(f"[ERROR] Request failed: {str(e)}")
        return None

    def close(self):
        self.client.close()

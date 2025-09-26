import hashlib, html, json, re, time, urllib.parse

class JobAPI:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.firecrawl.com/v1/jobs"

    def search_jobs(self, query: str, location: str = "", page: int = 1, per_page: int = 10) -> dict:
        """Search for jobs using the Firecrawl API."""
        params = {
            "query": query,
            "location": location,
            "page": page,
            "per_page": per_page,
            "api_key": self.api_key
        }
        url = f"{self.base_url}/search?{urllib.parse.urlencode(params)}"
        
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()
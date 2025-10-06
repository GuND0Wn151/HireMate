from requests import get, post
from typing import Optional


class APIClient:
      @staticmethod
      def get(url: str, headers: Optional[dict] = None, params: Optional[dict] = None) -> dict:
            response = get(url, headers=headers, params=params)
            response.raise_for_status()
            return response.json()
      
      @staticmethod
      def post(url: str, headers: Optional[dict] = None, data: Optional[dict] = None, json: Optional[dict] = None) -> dict:
            response = post(url, headers=headers, data=data, json=json)
            response.raise_for_status()
            return response.json()
      
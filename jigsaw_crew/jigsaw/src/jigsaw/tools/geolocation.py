import requests
import json
from crewai_tools import BaseTool
from pydantic import BaseModel, Field

class Geolocation(BaseTool):
    name: str
    description: str
    api_key: str

    def _run(self, argument: str) -> str:
        url = f"https://api.jigsawstack.com/v1/geo/search?search_value={argument}"
        headers = {
            'x-api-key': self.api_key
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise an exception for bad status codes
            data = response.json()

            if data.get('success') and data.get('data'):
                # Return the full address of the first result
                return data['data'][0].get('full_address', 'Full address not available')
            else:
                return "No results found for the given location."

        except requests.RequestException as e:
            return f"Error calling the Jigsaw Stack API: {str(e)}"
        except json.JSONDecodeError:
            return "Error decoding the API response"

    def _arun(self, argument: str) -> str:
        # Asynchronous implementation if needed
        raise NotImplementedError("Asynchronous execution not implemented for this tool.")

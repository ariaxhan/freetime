import requests
from crewai_tools import BaseTool
from pydantic import BaseModel, Field
import json

class SummaryTool(BaseTool):
    name: str
    description: str
    api_key: str
    output_file: str = "summary_output.md"  # Default output file

    def _run(self, text: str) -> str:
        url = "https://api.jigsawstack.com/v1/ai/summary"
        headers = {
            'Content-Type': 'application/json',
            'x-api-key': self.api_key
        }

        payload = {
            "text": text
        }

        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()  # Raise an exception for bad status codes
            data = response.json()

            if 'summary' in data:
                summary = data['summary']

                # Write the summary to a markdown file
                with open(self.output_file, 'w') as f:
                    f.write(f"# Summary\n\n{summary}")

                return summary
            else:
                return "No summary found in the response."

        except requests.RequestException as e:
            return f"Error calling the Jigsaw Stack API: {str(e)}"
        except json.JSONDecodeError:
            return "Error decoding the API response"

    def _arun(self, text: str) -> str:
        # Asynchronous implementation if needed
        raise NotImplementedError("Asynchronous execution not implemented for this tool.")

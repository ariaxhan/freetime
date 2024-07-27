import requests
from crewai_tools import BaseTool
from pydantic import BaseModel, Field
import time
import json

class WebSearchSummaryTool(BaseTool):
    name: str
    description: str
    api_key: str
    web_search_output_file: str = "web_search_results.txt"  # Default output file for web search results
    summary_output_file: str = "summary_output.md"  # Default output file for summary

    def _run(self, query: str) -> str:
        # Perform web search
        web_search_results = self.perform_web_search(query)

        # Perform summary on the search results
        summary_result = self.perform_summary(web_search_results)

        return summary_result

    def perform_web_search(self, query: str) -> str:
        url = f"https://api.jigsawstack.com/v1/web/search?query={query}"
        headers = {
            'x-api-key': self.api_key
        }

        max_retries = 2
        attempts = 0

        while attempts < max_retries:
            try:
                response = requests.get(url, headers=headers)
                response.raise_for_status()  # Raise an exception for bad status codes
                data = response.json()

                if 'results' in data and data['results']:
                    # Process the search results
                    results = data['results']
                    formatted_results = "\n".join([result['title'] + ": " + result['url'] for result in results])

                    # Write the results to a file
                    with open(self.web_search_output_file, 'w') as f:
                        f.write(formatted_results)

                    return formatted_results
                else:
                    return "No results found for the given query."

            except requests.RequestException as e:
                attempts += 1
                if attempts < max_retries:
                    time.sleep(1)  # Wait before retrying
                else:
                    return f"Error calling the Jigsaw Stack API after {max_retries} attempts: {str(e)}"
            except json.JSONDecodeError:
                return "Error decoding the API response"

    def perform_summary(self, text: str) -> str:
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
                with open(self.summary_output_file, 'w') as f:
                    f.write(f"# Summary\n\n{summary}")

                return summary
            else:
                return "No summary found in the response."

        except requests.RequestException as e:
            return f"Error calling the Jigsaw Stack API: {str(e)}"
        except json.JSONDecodeError:
            return "Error decoding the API response"

    def _arun(self, query: str) -> str:
        # Asynchronous implementation if needed
        raise NotImplementedError("Asynchronous execution not implemented for this tool.")

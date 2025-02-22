from langchain.tools import BaseTool
import os
from supabase import create_client, Client
from datetime import datetime
import json
from pydantic import Field
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file located one level higher
env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

class DataFetchTool(BaseTool):
    name = "Data Fetch Tool"
    description = "Fetches and preprocesses user data from Supabase"

    url: str = Field(..., description="Supabase URL")
    key: str = Field(..., description="Supabase API key")
    supabase: Client = Field(default=None)


    def __init__(self, **data):
        super().__init__(**data)
        url = os.environ.get("SUPABASE_URL")
        key = os.environ.get("SUPABASE_KEY")
        self.supabase = create_client(url, key)

    def _run(self, table: str = 'users') -> dict:
        try:
            response = self.supabase.table(table).select('*').execute()
            users_data = response.data
            availability_data = {"users": []}
            interests_data = {"users": []}
            usernames = {"users": []}

            for user_info in users_data:
                if user_info.get("username") != "FreeTime":  # Skip the FreeTime user
                    # Process availability
                    availability_user = {
                        "name": user_info.get("name", ""),
                        "username": user_info.get("username", ""),
                        "city": user_info.get("city", ""),
                        "availability": []
                    }
                    for date in user_info.get("availableDates", []):
                        start_dt = datetime.fromisoformat(date["start"].replace("Z", "+00:00"))
                        end_dt = datetime.fromisoformat(date["end"].replace("Z", "+00:00"))
                        availability_user["availability"].append({
                            "day": start_dt.strftime("%A"),
                            "date": start_dt.strftime("%Y-%m-%d"),
                            "start": start_dt.strftime("%H:%M"),
                            "end": end_dt.strftime("%H:%M")
                        })
                    availability_data["users"].append(availability_user)

                    # Process interests
                    interests_user = {
                        "name": user_info.get("name", ""),
                        "city": user_info.get("city", ""),
                        "age": user_info.get("age", ""),
                        "interests": user_info.get("interests", [])
                    }
                    interests_data["users"].append(interests_user)

                    # Process usernames
                    username_user = {
                        "name": user_info.get("name", ""),
                        "username": user_info.get("username", "")
                    }
                    usernames["users"].append(username_user)

            return {
                "availability_data": json.dumps(availability_data),
                "interests_data": json.dumps(interests_data),
                "username_data": json.dumps(usernames)
            }
        except Exception as e:
            return f"An error occurred while fetching and processing data: {e}"

# Example usage
# if __name__ == "__main__":
#     tool = DataFetchTool.from_env()
#     result = tool._run()
#     print("Availability Data:")
#     print(json.dumps(json.loads(result["availability_data"]), indent=2))
#     print("\nInterests Data:")
#     print(json.dumps(json.loads(result["interests_data"]), indent=2))
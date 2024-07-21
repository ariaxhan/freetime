from langchain.tools import BaseTool
from firebase_admin import credentials, db, initialize_app
import firebase_admin
from datetime import datetime
import json
from pydantic import Field

class DataFetchTool(BaseTool):
    name = "Data Fetch Tool"
    description = "Fetches and preprocesses user data from Firebase"
    ref: db.Reference = Field(default=None, exclude=True)

    def __init__(self):
        super().__init__()
        if not firebase_admin._apps:
            cred = credentials.Certificate("tools/cred/serviceAccountKey.json")
            initialize_app(cred, {
                'databaseURL': 'https://freetime-9428d-default-rtdb.firebaseio.com/'
            })
        self.ref = db.reference('/')

    def _run(self, path: str = 'users') -> dict:
        try:
            users_data = self.ref.child(path).get()
            
            availability_data = {"users": []}
            interests_data = {"users": []}

            for username, user_info in users_data.items():
                if username != "FreeTime":  # Skip the FreeTime user
                    # Process availability
                    availability_user = {
                        "name": user_info.get("name", ""),
                        "username": username,
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
                        "username": username,
                        "city": user_info.get("city", ""),
                        "interests": user_info.get("interests", [])
                    }
                    interests_data["users"].append(interests_user)

            return {
                "availability_data": json.dumps(availability_data),
                "interests_data": json.dumps(interests_data)
            }
        except Exception as e:
            return f"An error occurred while fetching and processing data: {e}"

# Example usage
# if __name__ == "__main__":
#     tool = DataFetchTool()
#     result = tool._run()
#     print("Availability Data:")
#     print(json.dumps(json.loads(result["availability_data"]), indent=2))
#     print("\nInterests Data:")
#     print(json.dumps(json.loads(result["interests_data"]), indent=2))
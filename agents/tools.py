import firebase_admin
from firebase_admin import credentials, initialize_app, db
from crewai_tools import BaseTool

class DataUploader(BaseTool):
    name: str = "Firebase JSON Uploader"
    description: str = "Uploads JSON data to Firebase Realtime Database."

    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://freetime-9428d-default-rtdb.firebaseio.com/'
    })

    def _run(self, json_data: dict) -> str:
        try:
            ref = db.reference('/')
            ref.set(json_data)
            return "Data uploaded successfully."
        except Exception as e:
            return f"An error occurred: {e}"

# Example usage
if __name__ == "__main__":
    tool = DataUploader()
    json_data = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "age": 30
    }
    result = tool._run(json_data)
    print(result)

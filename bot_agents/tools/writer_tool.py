from langchain.tools import BaseTool
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import json
from pydantic import Field

class FirebaseWriterTool(BaseTool):
    name = "Firebase Data Writer"
    description = "Writes JSON data to Firebase Realtime Database."
    ref: db.Reference = Field(default=None, exclude=True)


    def __init__(self):
        super().__init__()
        if not firebase_admin._apps:
            cred = credentials.Certificate("agents/serviceAccountKey.json")
            firebase_admin.initialize_app(cred, {
                'databaseURL': 'https://freetime-9428d-default-rtdb.firebaseio.com/'
            })
        self.ref = db.reference('/')

    def _run(self, path: str, data: str) -> str:
        try:
            parsed_data = json.loads(data)
            self.ref.child(path).set(parsed_data)
            return f"Data written successfully to {path}"
        except json.JSONDecodeError:
            return "Error: Invalid JSON data provided"
        except Exception as e:
            return f"An error occurred while writing data: {e}"

    def write_data(self, path: str, data: dict) -> str:
        self.ref.child(path).set(data)
        return f"Data written successfully to {path}"
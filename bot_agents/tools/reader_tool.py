from langchain.tools import BaseTool
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import json
from pydantic import Field

class FirebaseReaderTool(BaseTool):
    name = "Firebase Data Reader"
    description = "Reads JSON data from Firebase Realtime Database."
    ref: db.Reference = Field(default=None, exclude=True)


    def __init__(self):
        super().__init__()
        if not firebase_admin._apps:
            cred = credentials.Certificate("tools/cred/serviceAccountKey.json")
            firebase_admin.initialize_app(cred, {
                'databaseURL': 'https://freetime-9428d-default-rtdb.firebaseio.com/'
            })
        self.ref = db.reference('/')

    def _run(self, path: str = '/') -> str:
        try:
            data = self.ref.child(path).get()
            return json.dumps(data) if data is not None else json.dumps({})
        except Exception as e:
            return f"An error occurred while reading data: {e}"

    def read_data(self, path: str = '/') -> dict:
        data = self.ref.child(path).get()
        return data if data is not None else {}
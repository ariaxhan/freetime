from langchain.tools import BaseTool
from datetime import datetime
import json
from pydantic import BaseModel, Field
import requests
from typing import Type

class DiscordArgsSchema(BaseModel):
    channel_name: str = Field(description="Name of the channel to be created as a group chat")
    usernames: str = Field(description="List of the usernames separated by commas of discord usernames to invite to the channel/group chat")
    message: str = Field(description="Message to send to users inviting them to the event")

class DiscordMessageTool(BaseTool):
    name = "Discord Message Tool"
    description = "Calls the discord bot to send a message to available users suggesting an event"
    guild_id: int = 1264631960282857554
    url: str = 'http://127.0.0.1:5000/create_group_chat'
    args_schema: Type[BaseModel] = DiscordArgsSchema
    
    def __init__(self):
        super().__init__()

    def _run(self, usernames: list, channel_name: str, message: str) -> str:
        try:
            # Prepare the payload
            payload = {
                "guild_id": self.guild_id,
                "channel_name": channel_name,
                "usernames": usernames,
                "message": message
            }
            headers = {
                'Content-Type': 'application/json'
            }
            # call discord bot
            print('Calling discord bot with the following args:')
            print(json.dumps(payload, indent=2))
            response = requests.post(self.url, headers=headers, json=payload)
            
            return response.status_code
        
        except Exception as e:
            return f"An error occurred while calling the discord bot: {e}"

# Example usage
# if __name__ == "__main__":
#     tool = DataFetchTool()
#     result = tool._run()
#     print("Availability Data:")
#     print(json.dumps(json.loads(result["availability_data"]), indent=2))
#     print("\nInterests Data:")
#     print(json.dumps(json.loads(result["interests_data"]), indent=2))
from tools.discord_message_tool import DiscordMessageTool

# Create an instance of the DiscordMessageTool
discord_message_tool = DiscordMessageTool()

# Define test data
test_channel_name = "test-channel"
test_usernames = "user1,user2,user3"
test_message = "Hello! This is a test message."

# Call the _run method with the test data
response = discord_message_tool._run(usernames=test_usernames, channel_name=test_channel_name, message=test_message)

# Print the response to check if the call was successful
print(f"Response status code: {response}")
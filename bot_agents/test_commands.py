import requests

url = 'http://localhost:5000/create_group_chat'
data = {
    'guild_id': '1264631960282857554',
    'channel_name': 'dinner-plans',
    'usernames': ['Max', 'Ally', 'Aria'],
    'message': "Let's go to dinner at Alfredo's at 6pm"
}

response = requests.post(url, json=data)
print(response)
print(response.json())
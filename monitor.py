from slack_sdk import WebClient
import requests
import time

from lstm import get_submit

SLACK_BOT_TOKEN = 'xoxb-8020284472341-8063046305312-VrJHOqy8CBM6Tue7KM6Oo3Tw'
client = WebClient(token=SLACK_BOT_TOKEN)
CHANNEL_ID = "C080P6M4DKL"  # Replace with the ID of the channel you want to monitor
TARGET_USER_ID = "U080GCRATP1"  # Replace with Joe Arrowsmith's user ID
TARGET_MESSAGE = "Data has just been released"  # Replace with the target message content
def get_channel_messages(channel_id, latest_ts=None):
    """Fetch messages from a Slack channel."""
    url = "https://slack.com/api/conversations.history"
    headers = {"Authorization": f"Bearer {SLACK_BOT_TOKEN}"}
    params = {
        "channel": channel_id,
        "limit": 2,  # Fetch the last 10 messages
    }
    if latest_ts:
        params["oldest"] = latest_ts  # Only fetch messages after the last checked timestamp
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        if data["ok"]:
            return data["messages"]
        else:
            print(f"Error: {data['error']}")
    else:
        print(f"HTTP Error: {response.status_code}")
    return []
def monitor_channel():
    """Continuously poll the channel for new messages."""
    latest_ts = None  # Tracks the last processed message timestamp
    while True:
        messages = get_channel_messages(CHANNEL_ID, latest_ts)
        for message in reversed(messages):  # Process messages in chronological order
            user_id = message.get("user")
            text = message.get("text")
            ts = message.get("ts")
            # Check if the message matches the target conditions
            if user_id == TARGET_USER_ID and TARGET_MESSAGE.lower() in str(text).lower():
                print("Target message detected!")
                execute_custom_code(text, ts)
            # Update the latest timestamp
            latest_ts = ts
        time.sleep(5)  # Poll every 5 seconds
def execute_custom_code(message, ts):
    """Custom logic triggered by a specific message."""
    # print(f'Custom code executed for message: "{message}" - {ts}')
    # Add your logic here: API calls, database updates, etc.
    def extract_code(msg):
        extracted = []
        recording = False
        current = []

        for char in msg:
            if char == "'":
                if recording:
                    extracted.append("".join(current))
                    current = []
                    recording = False
                else:
                    recording = True
            elif recording:
                current.append(char)
        
        return extracted[0], extracted[1]
    
    cryptname, cryptcode = extract_code(message)
    print(cryptname, cryptcode)
    pos_dict = get_submit(cryptname, cryptcode)
    print(pos_dict)

    def post_to_google_form(pos_dict):
        FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSeUYMkI5ce18RL2aF5C8I7mPxF7haH23VEVz7PQrvz0Do0NrQ/formResponse"
        
        # Prepare form data
        form_data = {
            "emailAddress": "dswdavid1@gmail.com",
            "entry.1985358237": str(pos_dict)
        }
        
        try:
            response = requests.post(FORM_URL, data=form_data)
            if response.status_code == 200:
                print("Form submitted successfully!")
            else:
                print(f"Failed to submit form. Status code: {response.status_code}")
        except Exception as e:
            print(f"Error submitting form: {str(e)}")

    # post_to_google_form(pos_dict)

if __name__ == "__main__":
    monitor_channel()
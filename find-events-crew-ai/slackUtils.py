# Import WebClient from Python SDK (github.com/slackapi/python-slack-sdk)
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import os
import dotenv

dotenv.load_dotenv()


class SlackClient:
    def __init__(self):
        self._token = os.environ['SLACK_BOT_TOKEN']

    def post_message(self, channel_id, message):
        client = WebClient(token=self._token)

        try:
            # Call the conversations.list method using the WebClient
            result = client.chat_postMessage(
                channel=channel_id,
                text=message,
                # You could also use a blocks[] array to send richer content
            )
            # Print result, which includes information about the message (like TS)
            print("Message posted to slack")
            print(result)

        except SlackApiError as e:
            print(f"Error: {e}")

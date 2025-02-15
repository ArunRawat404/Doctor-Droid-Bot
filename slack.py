import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv
from database import save_message
from gemini_api import generate_response

# Load environment variables
load_dotenv()

# Initialize Slack client
slack_client = WebClient(token=os.getenv("SLACK_BOT_TOKEN"))

def handle_slack_event(event_data):
    """Handles Slack events and responds to user messages."""
    event = event_data.get("event", {})

    # Ignore messages from bots
    if event.get("bot_id"):
        return  

    user_id = event.get("user")
    user_message = event.get("text")
    channel_id = event.get("channel")

    if not user_id or not user_message or not channel_id:
        return  

    # Store user message
    save_message(user_id, user_message)

    # Generate AI response
    ai_response = generate_response(user_message)

    # Store bot response
    save_message("Bot", ai_response)

    # Send response to Slack
    try:
        slack_client.chat_postMessage(channel=channel_id, text=f"Arun's Droid: {ai_response}")
    except SlackApiError as e:
        print(f"Slack API Error: {e.response['error']}")

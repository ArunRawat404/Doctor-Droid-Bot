from fastapi import FastAPI, Request
import os
import json
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from database import save_message
from gemini_api import generate_response

# Load environment variables
load_dotenv()

app = FastAPI()
slack_client = WebClient(token=os.getenv("SLACK_BOT_TOKEN"))

# Track processed event IDs to prevent duplicate handling
processed_events = set()

@app.post("/slack/events")
async def slack_events(request: Request):
    """Handles incoming Slack events."""
    data = await request.json()
    event = data.get("event", {})

    # Handle Slack challenge for verification
    if "challenge" in data:
        return {"challenge": data["challenge"]}

    # Ignore bot messages
    if event.get("bot_id"):
        return {"status": "ignored"}

    event_id = data.get("event_id")
    if event_id in processed_events:
        return {"status": "duplicate"}
    
    processed_events.add(event_id)

    if event.get("type") == "app_mention":
        user_message = event.get("text", "").strip()
        channel_id = event.get("channel", "")

        bot_user_id = next(
            (auth["user_id"] for auth in data.get("authorizations", []) if "user_id" in auth),
            None
        )

        if bot_user_id:
            user_message = user_message.replace(f"<@{bot_user_id}>", "").strip()

            # Generate AI response
            ai_response = generate_response(user_message)

            # Store messages
            save_message("User", user_message)
            save_message("Bot", ai_response)

            # Send response to Slack
            try:
                slack_client.chat_postMessage(channel=channel_id, text=f"Arun's Bot: {ai_response}")
            except SlackApiError as e:
                print(f"Slack API Error: {e.response['error']}")

    return {"status": "ok"}

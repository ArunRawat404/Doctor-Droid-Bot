from fastapi import FastAPI, Request
import os
import json
import requests
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from database import save_message
from gemini_api import generate_response

# Load environment variables
load_dotenv()

app = FastAPI()

SLACK_CLIENT_ID = os.getenv("SLACK_CLIENT_ID")
SLACK_CLIENT_SECRET = os.getenv("SLACK_CLIENT_SECRET")

slack_client = WebClient(token=os.getenv("SLACK_BOT_TOKEN"))

# Track processed event IDs to prevent duplicate handling
processed_events = set()

import requests
from fastapi import Request

SLACK_CLIENT_ID = os.getenv("SLACK_CLIENT_ID")
SLACK_CLIENT_SECRET = os.getenv("SLACK_CLIENT_SECRET")

@app.get("/slack/oauth")
async def slack_oauth(request: Request):
    """Handles Slack OAuth redirection."""
    code = request.query_params.get("code")
    
    if not code:
        return {"error": "Missing authorization code"}

    # Exchange code for a token
    response = requests.post("https://slack.com/api/oauth.v2.access", data={
        "client_id": SLACK_CLIENT_ID,
        "client_secret": SLACK_CLIENT_SECRET,
        "code": code,
        "redirect_uri": "https://doctor-droid-bot.onrender.com/slack/oauth"
    })

    slack_response = response.json()

    if not slack_response.get("ok"):
        return {"error": slack_response.get("error")}

    return {"message": "Slack app installed successfully!", "data": slack_response}


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

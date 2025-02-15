# Slack Bot with Gemini AI Integration

This is a Slack bot that integrates with Google Gemini AI to provide automated responses to user queries. The bot listens for messages in Slack channels and generates AI-powered replies.

## Features

- Listens for messages in Slack channels
- Uses Google Gemini AI to generate responses
- Prevents duplicate responses
- Stores conversation history in an SQLite database

## Installation and Setup

### Prerequisites

- Python 3.8+
- A Slack App with necessary permissions
- Google Gemini AI API Key
- `ngrok` (for local testing)
- A `.env` file with the following environment variables:
  ```env
  SLACK_BOT_TOKEN=your_slack_bot_token
  GEMINI_API_KEY=your_gemini_api_key
  SLACK_SIGNING_SECRET=your_slack_signing_secret
  ```

## Running Locally

1. Clone the repository:

```bash
  git clone https://github.com/your-repo/slack-gemini-bot.git
  cd slack-gemini-bot
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set up ngrok by going to official site (for Slack to access your local server)

4. Run ngrok

```bash
  ngrok http 8000
```

5. Start the FastAPI server

```bash
uvicorn bot:app --reload --host 0.0.0.0 --port 8000
```

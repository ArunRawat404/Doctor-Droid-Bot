import os
from dotenv import load_dotenv
import google.generativeai as genai
from database import get_last_messages

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate_response(user_message):
    chat_history = get_last_messages(5)  # Retrieve last 5 messages
    context = "\n".join([f"{user}: {msg}" for user, msg in chat_history])

    prompt = f"Here is the conversation so far:\n{context}\nUser: {user_message}\nAI:"

    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)

    return response.text if response else "Sorry, I couldn't process that."

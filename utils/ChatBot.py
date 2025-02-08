import google.generativeai as genai
import google.api_core.exceptions
import os
from typing import List, Dict

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def ask_chatbot(chat_messages: List[Dict[str, str]], user_message: str) -> str:
    """
    Processes the last 5 messages from WhatsApp chat and sends them to Gemini 2.0 for response.
    Also calculates and prints token count.
    """
    if not isinstance(chat_messages, list):
        return "Error: Chat history is not a valid list format."

    # # Extract only the last 5 messages
    # last_five_messages: List[Dict[str, str]] = chat_messages[-5:] if len(chat_messages) > 5 else chat_messages

    # # Format the last 5 messages in WhatsApp style
    # formatted_chat: str = "\n".join([
    #     f"{msg['timestamp']} {msg['sender']}: {msg['message']}" for msg in last_five_messages
    # ])

    prompt: str = f"--- WhatsApp Chat ---\n{chat_messages}\n\nUser: {user_message}\nBot:"

    print(f"Chat messages: {chat_messages}")

    #  Use Gemini's count_tokens() to check token usage before sending
    model = genai.GenerativeModel("gemini-2.0-flash")
    token_usage = model.count_tokens(prompt)
    
    print(f"Token Count: {token_usage.total_tokens}")

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except google.api_core.exceptions.ResourceExhausted:
        return "Error: Exceeded API quota or rate limits. Try again later."

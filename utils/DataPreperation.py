import re
from typing import List, Dict

MAX_TOKENS = 1_000_000  # Keep only the last 1 million tokens
TOKEN_ESTIMATE_RATIO = 1  # 1 token ≈ 4 characters

def estimate_token_count(text: str) -> int:
    """Estimates token count (1 token ≈ 4 characters)."""
    return len(text) // TOKEN_ESTIMATE_RATIO


def get_last_1m_tokens(chat_messages: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """
    Trims the chat messages to ensure the total token count does not exceed 1 million.
    Keeps only the most recent messages that fit within the token limit.
    """
    total_tokens = 0
    trimmed_chat = []

    # Process messages from newest to oldest
    for message in reversed(chat_messages):
        message_text = f"{message['sender']}: {message['message']}"  # Simpler format for estimating
        message_tokens = estimate_token_count(message_text)

        if total_tokens + message_tokens > MAX_TOKENS:
            print(f"Stopping. Adding this message would exceed the limit: {message_text}")
            break  # Stop before exceeding the limit

        trimmed_chat.append(message)
        total_tokens += message_tokens
        print(f"Added message. Current total tokens: {total_tokens}")

    # Reverse back to maintain correct order
    trimmed_chat.reverse()
    print(f"Final number of messages: {len(trimmed_chat)}")
    return trimmed_chat

def parse_whatsapp_data(file_path: str) -> List[Dict[str, str]]:
    """
    Parses WhatsApp chat export file, extracts timestamp, sender, and message content.
    Filters out messages that are empty or contain only 'null'.
    """
    messages = []
    pattern = re.compile(r"(\d{1,2}/\d{1,2}/\d{2,4}),?\s+(\d{1,2}:\d{2}\s?[apAP][mM])\s-\s([^:]+):\s(.+)")
    
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            match = pattern.match(line.strip())
            if match:
                date, time, sender, message = match.groups()
                message = message.strip()
                if message and message.lower() != "null":
                    messages.append({
                        "sender": sender.strip(),
                        "message": message
                    })

    return get_last_1m_tokens(messages)


# def parse_whatsapp_data(file_path: str) -> List[Dict[str, str]]:
#     """
#     Parses WhatsApp chat export file and extracts timestamp, sender, and message content.
#     Removes entries where the message is empty or contains 'null'.
#     """
#     messages: List[Dict[str, str]] = []

#     # Improved Regular Expression Pattern to Extract WhatsApp Chat Messages
#     pattern: str = r"(\d{1,2}/\d{1,2}/\d{2,4}),?\s+(\d{1,2}:\d{2}\s?[apAP][mM])\s-\s([^:]+):\s(.+)"

#     with open(file_path, "r", encoding="utf-8") as file:
#         for line in file:
#             match = re.match(pattern, line.strip())
#             if match:
#                 date, time, sender, message = match.groups()
#                 message = message.strip()  # Remove unnecessary whitespace
                
#                 if message and message.lower() != "null":  # ✅ Exclude 'null' messages
#                     #timestamp: str = f"{date}, {time}"
#                     messages.append({
#                         #"timestamp": timestamp,
#                         "sender": sender.strip(),
#                         "message": message
#                     })
    
#     return messages



def format_chat_for_llm(chat_data: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """
    Ensures chat history is formatted properly before sending to LLM.
    """
    if not isinstance(chat_data, list):
        print(f"ERROR: Expected a list of dictionaries, but got {type(chat_data)}")
        return []  # Return an empty list instead of a string  

    return chat_data  # Return as a structured list, not a string

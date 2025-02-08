from email import message
import re

def parse_whatsapp_data(file_path):
    messages = []

    # Improved Regular Expression Pattern to Extract WhatsApp Chat Messages
    pattern = r"(\d{1,2}/\d{1,2}/\d{2,4}),?\s+(\d{1,2}:\d{2}\s?[apAP][mM])\s-\s([^:]+):\s(.+)"

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            match = re.match(pattern, line.strip())
            #print(f"Line: {line.strip()} | Match: {match}")  # Debugging Output
            if match:
                date, time, sender, message = match.groups()
                timestamp = f"{date}, {time}"
                messages.append({
                    "timestamp": timestamp,
                    "sender": sender.strip(),
                    "message": message.strip()
                })
    return messages

 

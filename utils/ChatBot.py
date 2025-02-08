import os
import ai21
import faiss
import numpy as np
from ai21 import AI21Client
from ai21.models.chat import UserMessage
from sentence_transformers import SentenceTransformer
import torch

client = AI21Client(api_key=os.getenv("AI21_API_KEY"))

# Load model with GPU support
device = "cuda" if torch.cuda.is_available() else "cpu"
embedding_model = SentenceTransformer("all-MiniLM-L6-v2", device=device) 

vector_dimension = 384  # MiniLM embedding size
index = faiss.IndexFlatL2(vector_dimension)
message_store = [] 

def store_chat_embeddings(chat_messages):
    global index, message_store
    message_store = chat_messages  # Keep original messages
    
    print(f"Device selected: {device}")

    # Convert messages to embeddings
    chat_texts = [msg["message"] for msg in chat_messages]
    embeddings = embedding_model.encode(chat_texts)

    # Store in FAISS
    index.add(np.array(embeddings).astype("float32"))
    print(f"Stored {len(chat_messages)} messages in FAISS with GPU acceleration.")


def retrieve_relevant_messages(query, top_k=5):
    global index, message_store

    # Convert query to embedding
    query_embedding = embedding_model.encode([query])
    
    # Find top_k similar messages
    _, indices = index.search(np.array(query_embedding).astype("float32"), top_k)
    
    # Return retrieved messages
    retrieved_messages = [message_store[i] for i in indices[0] if i < len(message_store)]
    
    return retrieved_messages


def format_chat_for_llm(chat_data):
    if not isinstance(chat_data, list):
        print(f"ERROR: Expected a list of dictionaries, but got {type(chat_data)}")
        return ""  # Return empty string to prevent errors

    return "\n".join([f"{msg['timestamp']} {msg['sender']}: {msg['message']}" for msg in chat_data])


# Function to send the chat data to Gemini and get a response
def ask_chatbot(chat_messages, user_message):
   
    retrieved_messages = retrieve_relevant_messages(user_message, top_k=5)
    print(f"message retrieved: {retrieved_messages}")

    # Format retrieved messages
    formatted_history = "\n".join(
        [f"{msg['timestamp']} {msg['sender']}: {msg['message']}" for msg in retrieved_messages]
    )

    # Construct message for Jamba
    messages = [
        UserMessage(content=f"Chat History:\n{formatted_history}\n\nUser: {user_message}\nBot:")
    ]

    # Create AI21 Labs message list
    messages = [
        UserMessage(
            content=f"Chat History:\n{formatted_history}\n\nUser: {user_message}\nBot:"
        )
    ]

    try:
        response = client.chat.completions.create(
            model="jamba-1.5-large",  # Using Jamba model
            messages=messages,
            top_p=1.0,  # Enables diverse responses
            max_tokens=500
        )

        return response.to_json()["choices"][0]["message"]["content"].strip()

    except Exception as e:
        return f"Error calling Jamba API: {str(e)}"

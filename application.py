from fastapi import FastAPI, File, UploadFile, Request
from utils.ChatBot import ask_chatbot, store_chat_embeddings
from utils.DataPreperation import parse_whatsapp_data
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import os
import json
import shutil

# Set up Jinja2Templates for rendering HTML
templates = Jinja2Templates(directory="templates")


application = FastAPI()

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Global variable to store chat data
chat_data_store = {"chat_history": None}


# ---> home route (public, no API key required)
@application.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# API Endpoint to Upload a WhatsApp Chat File (Stores Parsed Data Globally)
@application.post("/upload_chat/")
async def upload_chat_file(file: UploadFile = File(...)):
    file_location = f"{UPLOAD_FOLDER}/{file.filename}"

    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Parse and format the chat data once, then store in global variable
    unformatted_chat_history = parse_whatsapp_data(file_location)

    store_chat_embeddings(unformatted_chat_history) 
    

    # Ensure chat data is stored as a valid list of dictionaries
    chat_data_store["chat_history"] = json.dumps(unformatted_chat_history)  # Store as JSON string

    print(f"✅ Stored chat history type: {type(chat_data_store['chat_history'])}")  

    return {"filename": file.filename, "message": "File uploaded and parsed successfully"}

# Define Pydantic Model for User Query (No Filename Needed)
class UserQuery(BaseModel):
    user_message: str  # Only the user query, chat data is retrieved from global variable


@application.post("/chat/")
async def chat_with_ai(query: UserQuery):
    chat_history = chat_data_store.get("chat_history")

    if not chat_history:
        return {"error": "No chat file found. Please upload a file first."}

    # Convert JSON string back to a list
    if isinstance(chat_history, str):
        try:
            chat_history = json.loads(chat_history)  # Convert back to list
        except json.JSONDecodeError:
            return {"error": "Stored chat history is not a valid JSON format"}

    print(f"chat_history type after conversion: {type(chat_history)}")  # Debugging output

    response = ask_chatbot(chat_history, query.user_message)

    return {"user_message": query.user_message, "bot_response": response}

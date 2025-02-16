# ChatVibes
An application that analyses your chats and offer meaningful insights

# AI-Powered WhatsApp Chatbot

## About the Project
This project is an AI-powered chatbot designed to process WhatsApp chat files and provide responses based on chat history. It uses **FastAPI** for backend API development and **Google Gemini 2.0** for AI-generated responses. Additionally, the project includes a **front-end GUI** accessible from the home route (`/`), built using **HTML and CSS**, allowing users to test the chatbot from a web interface.

⚠️ **Safety Note**: This chatbot uses AI, which means responses may sometimes be vague, inaccurate, or misleading. Always verify critical information before taking action based on AI-generated responses.

## Features
- Upload a WhatsApp chat file.
- Automatically parse and format chat data for AI processing.
- Ask AI questions based on WhatsApp chat history.
- Uses **Google Gemini 2.0** for generating responses.
- Built with **FastAPI** for high-performance API functionality.
- Includes a **web-based GUI** where users can test the chatbot.

## Pre-requisites
Before running this project, ensure you have the following installed:
- **Python 3.8+**
- **FastAPI** (`pip install fastapi`)
- **Uvicorn** (`pip install uvicorn`)
- **Google Generative AI SDK** (`pip install google-generativeai`)
- **Starlette** (`pip install starlette`)
- **Pydantic** (`pip install pydantic`)

You also need a **Google Gemini API key**, which should be stored in your environment variables as `GEMINI_API_KEY`.


## How to Run
### 1. Clone the Repository
```sh
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

### 2. Install Dependencies
```sh
pip install -r requirements.txt
```
(Ensure that `requirements.txt` contains all necessary dependencies.)

### 3. Set Up Environment Variables
Create a `.env` file and add your **Google Gemini API key**:
```
GEMINI_API_KEY=your_api_key_here
```

Alternatively, you can set it in your terminal (Linux/macOS):
```sh
export GEMINI_API_KEY=your_api_key_here
```
For Windows (PowerShell):
```sh
$env:GEMINI_API_KEY="your_api_key_here"
```

### 4. Run the FastAPI Server
```sh
uvicorn main:application --host 0.0.0.0 --port 8000 --reload
```

This will start the server on **http://127.0.0.1:8000**.


## API Endpoints
### **1. Home Page**
`GET /`
- Returns the home page (renders `index.html`).
- Provides a web-based interface to test the chatbot using HTML & CSS.

### **2. Upload WhatsApp Chat File**
`POST /upload_chat/`
- Uploads a WhatsApp chat file (`.txt`).
- Stores parsed chat data globally.

#### Example Request (cURL)
```sh
curl -X POST -F "file=@chat.txt" http://127.0.0.1:8000/upload_chat/
```

### **3. Chat with AI**
`POST /chat/`
- Sends a user query based on uploaded chat history.

#### Example Request (JSON)
```sh
curl -X POST "http://127.0.0.1:8000/chat/" \
     -H "Content-Type: application/json" \
     -d '{"user_message": "Hello!"}'
```

#### Example Response
```json
{
  "user_message": "Hello!",
  "bot_response": "Hi there! How can I assist you today?"
}
```


## Known Issues & Limitations
- AI-generated responses can be **vague or misleading**.
- High API usage can **exceed token limits**, leading to quota errors.
- Uploaded chat files are **not permanently stored** and are lost when the server restarts.


## License
This project is open-source.

**Happy Coding! 🚀**


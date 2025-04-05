from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from main import JARVIS

# Load environment variables from .env file
load_dotenv()

# Check if OpenAI API key is set
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY environment variable is not set")

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

jarvis = JARVIS()

class TextInput(BaseModel):
    text: str

@app.post("/process-text")
def process_text(input_data: TextInput):
    output = jarvis._handle_user_input(input_data.text)
    # processed_text = input_data.text.upper()  # Example: Convert to uppercase
    return {"output": output}
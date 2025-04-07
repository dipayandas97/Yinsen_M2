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
    output = jarvis._handle_user_input(input_data.text, response_format='HTML')
    # Get the current agent name
    #agent_name = jarvis.current_agent.name if hasattr(jarvis, 'current_agent') and jarvis.current_agent else "Mia"
    # Return just the output
    return {"output": output}



# Helper function to read file and return list of strings
def read_file_lines(filepath: str) -> list:
    if not os.path.exists(filepath):
        return ["Error: File not found."]
    with open(filepath, "r", encoding="utf-8") as f:
        return [line.strip() for line in f.readlines() if line.strip()]


@app.get("/read_logs")
def get_file_1():
    filepath = os.getenv("LOGS_FILE_PATH", "file1.txt")
    lines = read_file_lines(filepath)
    return {"data": lines}


@app.get("/read_calendar")
def get_file_2():
    filepath = os.getenv("CALENDAR_FILE_PATH", "file2.txt")
    lines = read_file_lines(filepath)
    return {"data": lines}
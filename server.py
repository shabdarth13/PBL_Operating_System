from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from vocalshell.nlp_parser import NLPCommandParser
from vocalshell.command_executor import CommandExecutor
from vocalshell.utils import load_config
from vocalshell.speech_engine import SpeechRecognizer

import tempfile
import os

# ------------------------------------------
# FastAPI Setup
# ------------------------------------------
app = FastAPI(title="VocalShell API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------------
# Load Components
# ------------------------------------------
config = load_config("config/system_config.json")
parser = NLPCommandParser(config["system"]["commands_config"])
executor = CommandExecutor(config.get("executor", {}))

speech = SpeechRecognizer(
    model_path=config["system"]["model_path"],
    use_online=not config["speech"].get("prefer_offline", True),
    config=config.get("speech", {})
)

# ------------------------------------------
# Text Request Model
# ------------------------------------------
class TextRequest(BaseModel):
    text: str

# ------------------------------------------
# Routes
# ------------------------------------------

@app.get("/")
def home():
    return {"status": "VocalShell API running"}


# -----------------------------------------------------------
# PROCESS TEXT COMMAND
# -----------------------------------------------------------
@app.post("/process-text")
def process_text(request: TextRequest):
    text = request.text.strip()

    command, params, description, metadata = parser.parse_command(text)

    if command is None:
        return {
            "success": False,
            "output": "Could not understand command"
        }

    success, output = executor.execute_command(command, metadata)

    return {
        "success": success,
        "command": command,
        "output": output
    }


# -----------------------------------------------------------
# PROCESS VOICE COMMAND (MIC AUDIO FROM FRONTEND)
# -----------------------------------------------------------
@app.post("/process-voice")
async def process_voice(file: UploadFile = File(...)):

    # Save temp file for speech engine
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(await file.read())
        audio_path = tmp.name

    # Run speech-to-text
    text = speech.transcribe_audio(audio_path)

    # Delete temp file
    os.remove(audio_path)

    if not text:
        return {
            "success": False,
            "output": "Speech not recognized"
        }

    # Parse + Execute the command
    command, params, description, metadata = parser.parse_command(text)

    if command is None:
        return {
            "success": False,
            "text": text,
            "output": "Could not understand spoken command"
        }

    success, output = executor.execute_command(command, metadata)

    return {
        "success": success,
        "text": text,
        "command": command,
        "output": output
    }

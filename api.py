import logging
import shutil
import tempfile
import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from dotenv import load_dotenv
from openai import OpenAI
from utils import convert_to_mp3, needs_conversion, remove_file

# Load environment variables from .env
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize OpenAI client
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    logger.error("OPENAI_API_KEY is missing. Please check your .env file.")
    raise RuntimeError("OPENAI_API_KEY not found")

# Get model configuration
model_name = os.getenv("OPENAI_TRANSCRIPTION_MODEL", "gpt-4o-transcribe")
client = OpenAI(api_key=api_key)

# Create FastAPI app
app = FastAPI()

@app.get("/health-check")
def status():
    """
    Health check endpoint.
    """
    logging.info("Heath check requested.")
    return {"status": "ok"}

@app.head("/status")
def status():
    """
    Status endpoint.
    """
    logging.info("Status check requested.")
    return {"status": "ok"}


@app.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided.")

    extension = file.filename.rsplit(".", 1)[-1].lower()

    with tempfile.TemporaryDirectory() as tmpdir:
        original_path = os.path.join(tmpdir, file.filename)

        # Save uploaded file to disk
        with open(original_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        # Convert only if necessary
        if needs_conversion(extension):
            logger.info(f"Converting '{file.filename}' to .mp3...")
            file_to_send = convert_to_mp3(original_path)
        else:
            file_to_send = original_path

        # Call OpenAI API
        with open(file_to_send, "rb") as audio:
            try:
                response = client.audio.transcriptions.create(
                    model=model_name,
                    file=audio
                )
                transcription_text = response.text
                logger.info(f"Transcription: {transcription_text}")

                # Eliminate the file after transcribing using the new utility function
                remove_file(file_to_send)

                # Return transcription result
                return {"transcription": transcription_text}
            except Exception as e:
                logger.error(f"OpenAI transcription failed: {e}")
                raise HTTPException(status_code=400, detail="Transcription failed.")
import logging
import tempfile
import os
from typing import Optional
from fastapi import FastAPI, Query, UploadFile, File, HTTPException
from dotenv import load_dotenv
from openai import OpenAI
from .audio_processor import AudioProcessor
from app.utils import remove_file
# Importar excepciones comunes de decodificación
try:
    from pydub.exceptions import CouldntDecodeError
except ImportError:
    CouldntDecodeError = Exception  # fallback si no está pydub

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
app = FastAPI(
    title="My Audio Transcription API",
    description="This API allows you to upload audio files and get transcriptions.",
    version="1.0.0"
)

audio_processor = AudioProcessor(client, model_name)

@app.get("/health-check")
def health_check():
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
async def transcribe_audio(
    file: UploadFile = File(...),
    max_duration: Optional[int] = Query(
        None,
        description="Maximum allowed duration in seconds (optional)"
    )
):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided.")

    extension = file.filename.rsplit(".", 1)[-1].lower()

    with tempfile.TemporaryDirectory() as tmpdir:
        original_path = os.path.join(tmpdir, file.filename)

        try:
            # Save file
            audio_processor.save_uploaded_file(file, original_path)

            # Check duration if applicable
            duration = audio_processor.get_audio_duration_seconds(original_path)
            audio_processor.validate_duration(duration, max_duration)

            # Prepare audio file
            file_to_send = audio_processor.prepare_audio_file(original_path, extension)

            # Transcribe
            transcription_text = audio_processor.transcribe(file_to_send)

            # Clean up converted file if different
            if file_to_send != original_path:
                remove_file(file_to_send)

            return {
                "transcription": transcription_text,
                "duration_seconds": duration
            }

        except CouldntDecodeError as e:
            logger.error(f"Audio decode error: {e}")
            raise HTTPException(status_code=400, detail="Invalid audio file or corrupted file.")
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise HTTPException(status_code=500, detail="Transcription failed.")
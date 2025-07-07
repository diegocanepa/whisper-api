import os
import logging
from typing import Optional
from fastapi import UploadFile, HTTPException
from pydub import AudioSegment

logger = logging.getLogger(__name__)


class AudioProcessor:
    """
    A class responsible for validating, converting, and transcribing audio files.
    """

    def __init__(self, transcription_client, model_name: str):
        """
        Args:
            transcription_client: An instance of the OpenAI client or any other service client.
            model_name: The transcription model name.
        """
        self.transcription_client = transcription_client
        self.model_name = model_name

    def save_uploaded_file(self, upload_file: UploadFile, destination_path: str):
        """Save the uploaded file to disk."""
        with open(destination_path, "wb") as f:
            upload_file.file.seek(0)
            f.write(upload_file.file.read())
        logger.info(f"File saved to {destination_path}")

    def get_audio_duration_seconds(self, file_path: str) -> float:
        """Compute the duration of the audio file in seconds."""
        audio_segment = AudioSegment.from_file(file_path)
        duration = len(audio_segment) / 1000
        logger.info(f"Audio duration: {duration:.2f}s")
        return duration

    def validate_duration(self, duration: float, max_duration: Optional[int]):
        """Raise an error if the duration exceeds the allowed limit."""
        if max_duration is not None and duration > max_duration:
            raise HTTPException(
                status_code=400,
                detail=f"Audio is too long ({duration:.2f}s). Maximum allowed is {max_duration}s."
            )

    def prepare_audio_file(self, original_path: str, extension: str) -> str:
        """Convert the file to mp3 if needed."""
        from app.utils import needs_conversion, convert_to_mp3  # Keep dependencies minimal
        if needs_conversion(extension):
            logger.info(f"Converting '{original_path}' to mp3...")
            return convert_to_mp3(original_path)
        return original_path

    def transcribe(self, file_path: str) -> str:
        """Call the transcription service."""
        with open(file_path, "rb") as audio_file:
            response = self.transcription_client.audio.transcriptions.create(
                model=self.model_name,
                file=audio_file
            )
            logger.info("Transcription completed.")
            return response.text

import subprocess
import os
import logging
from fastapi import HTTPException

logger = logging.getLogger(__name__)

ALLOWED_DIRECT_FORMATS = {"mp3", "wav", "m4a"}

def needs_conversion(extension: str) -> bool:
    """Check if the file needs to be converted to mp3."""
    return extension.lower() not in ALLOWED_DIRECT_FORMATS

def convert_to_mp3(input_path: str) -> str:
    """Convert any audio file to .mp3."""
    output_path = os.path.splitext(input_path)[0] + ".mp3"
    try:
        subprocess.run(
            ["ffmpeg", "-y", "-i", input_path, "-acodec", "libmp3lame", output_path],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return output_path
    except subprocess.CalledProcessError as e:
        logger.error(f"ffmpeg conversion failed: {e}")
        raise HTTPException(status_code=500, detail="Audio conversion failed.")

def remove_file(file_path: str):
    """Delete the file from the filesystem if it exists."""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"File '{file_path}' has been deleted.")
        else:
            logger.warning(f"File '{file_path}' does not exist, skipping deletion.")
    except Exception as e:
        logger.error(f"Failed to delete file '{file_path}': {e}")
